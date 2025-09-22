#!/usr/bin/env python3
"""
Claude Code 自动输出捕获和通知系统
可以捕获任何Claude Code的输出并自动发送通知
"""

import sys
import subprocess
import time
import json
import re
from datetime import datetime
import threading
import queue

class ClaudeOutputCapture:
    def __init__(self):
        self.MESSAGE_PUSHER_API = "http://localhost:3000/push/root"
        self.CLAUDE_TASK_TOKEN = "claude_task_2025"
        self.FEISHU_CHANNEL = "feishu"
        self.output_queue = queue.Queue()

    def extract_task_info(self, output_text):
        """从Claude Code输出中提取任务信息"""
        lines = output_text.strip().split('\n')

        # 查找任务描述
        task_name = "Claude Code 任务"
        status = "完成"
        details = []

        # 简单的模式匹配来提取信息
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 查找任务完成指示
            if any(keyword in line.lower() for keyword in ['完成', 'success', 'done', 'finished']):
                status = "成功完成"
                if len(line) < 100:  # 如果行不太长，作为任务名
                    task_name = line

            # 查找错误指示
            elif any(keyword in line.lower() for keyword in ['error', 'failed', '错误', '失败']):
                status = "失败"
                if len(line) < 100:
                    task_name = line

            # 收集详细信息
            if len(line) > 10 and len(line) < 200:
                details.append(line)

        # 如果没找到合适的任务名，用第一行非空行
        if task_name == "Claude Code 任务" and details:
            task_name = details[0]
            details = details[1:]

        return task_name, status, details[:3]  # 最多3行详情

    def send_notification(self, task_name, status, details, execution_time=""):
        """发送通知到飞书"""
        import requests

        # 构建消息
        title = f"[AUTO] Claude Code - {task_name}"
        description = f"自动捕获 | {status}"

        content_lines = [
            f"任务: {task_name}",
            f"状态: {status}",
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]

        if execution_time:
            content_lines.append(f"耗时: {execution_time}")

        if details:
            content_lines.append("详情:")
            for detail in details:
                content_lines.append(f"  {detail}")

        content_lines.append("--- 来自 Claude Code 自动捕获")
        content = "\n".join(content_lines)

        # API请求
        api_data = {
            "title": title,
            "description": description,
            "content": content,
            "token": self.CLAUDE_TASK_TOKEN,
            "channel": self.FEISHU_CHANNEL
        }

        try:
            response = requests.post(self.MESSAGE_PUSHER_API, json=api_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"[AUTO-NOTIFY] 通知发送成功: {task_name}")
                    return True
            print(f"[AUTO-NOTIFY] 发送失败: {response.status_code}")
        except Exception as e:
            print(f"[AUTO-NOTIFY] 异常: {e}")

        return False

    def capture_command_output(self, command_args):
        """捕获命令输出并发送通知"""
        start_time = time.time()

        try:
            # 执行命令并捕获输出
            result = subprocess.run(
                command_args,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )

            end_time = time.time()
            execution_time = f"{end_time - start_time:.1f}秒"

            # 合并stdout和stderr
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += "\n" + result.stderr

            # 显示原始输出
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            # 提取任务信息
            task_name, status, details = self.extract_task_info(output)

            # 如果命令失败，更新状态
            if result.returncode != 0:
                status = "执行失败"
                details.insert(0, f"退出码: {result.returncode}")

            # 发送通知
            self.send_notification(task_name, status, details, execution_time)

            return result.returncode

        except subprocess.TimeoutExpired:
            print("命令执行超时")
            self.send_notification("Claude Code 任务", "执行超时", ["命令执行超过5分钟"], "超时")
            return 1
        except Exception as e:
            print(f"执行异常: {e}")
            self.send_notification("Claude Code 任务", "执行异常", [str(e)], "异常")
            return 1

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Claude Code 自动输出捕获和通知系统")
        print()
        print("用法:")
        print("  python claude_auto_notify.py <命令> [参数...]")
        print()
        print("示例:")
        print("  python claude_auto_notify.py python my_script.py")
        print("  python claude_auto_notify.py npm run build")
        print("  python claude_auto_notify.py git status")
        print()
        print("功能:")
        print("  - 执行指定命令")
        print("  - 捕获所有输出")
        print("  - 自动分析任务信息")
        print("  - 发送通知到飞书")
        return

    # 获取要执行的命令
    command_args = sys.argv[1:]

    print(f"[AUTO-CAPTURE] 执行命令: {' '.join(command_args)}")
    print("=" * 50)

    # 创建捕获器并执行
    captor = ClaudeOutputCapture()
    exit_code = captor.capture_command_output(command_args)

    print("=" * 50)
    print(f"[AUTO-CAPTURE] 命令完成，退出码: {exit_code}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()