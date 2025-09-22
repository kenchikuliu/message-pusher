#!/usr/bin/env python3
"""
Claude Code 监控和通知系统
监控Claude Code的所有输出并自动发送通知
"""

import sys
import time
import json
import re
import requests
from datetime import datetime
from io import StringIO

class ClaudeMonitor:
    def __init__(self):
        self.MESSAGE_PUSHER_API = "http://localhost:3000/push/root"
        self.CLAUDE_TASK_TOKEN = "claude_task_2025"
        self.FEISHU_CHANNEL = "feishu"
        self.captured_output = []
        self.start_time = None

    def start_monitoring(self):
        """开始监控"""
        self.start_time = time.time()
        self.captured_output = []
        print("[CLAUDE-MONITOR] 开始监控Claude Code输出...")

    def capture_output(self, text):
        """捕获输出文本"""
        self.captured_output.append({
            'text': text,
            'timestamp': time.time()
        })

    def analyze_output(self):
        """分析捕获的输出"""
        if not self.captured_output:
            return "Claude Code 任务", "执行完成", []

        # 合并所有输出
        full_text = "\n".join([item['text'] for item in self.captured_output])
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]

        # 智能分析
        task_name = "Claude Code 任务"
        status = "完成"
        key_points = []

        # 查找任务描述模式
        for line in lines:
            # 查找成功/完成模式
            if any(keyword in line.lower() for keyword in ['success', '成功', '完成', 'done', 'finished', 'completed']):
                status = "成功完成"
                if len(line) < 80 and '成功' in line:
                    task_name = line
                    break

            # 查找错误模式
            elif any(keyword in line.lower() for keyword in ['error', 'failed', '错误', '失败', 'exception']):
                status = "执行失败"
                if len(line) < 80:
                    task_name = line

        # 提取关键信息点
        for line in lines[-10:]:  # 关注最后10行
            if len(line) > 5 and len(line) < 150:
                # 过滤无用信息
                if not any(skip in line.lower() for skip in ['timestamp', 'debug', 'info', '===', '---']):
                    key_points.append(line)

        return task_name, status, key_points[:3]

    def send_notification(self, custom_message=None):
        """发送通知"""
        if custom_message:
            task_name, status, details = custom_message['task'], custom_message['status'], custom_message.get('details', [])
        else:
            task_name, status, details = self.analyze_output()

        # 计算执行时间
        execution_time = ""
        if self.start_time:
            duration = time.time() - self.start_time
            if duration < 60:
                execution_time = f"{duration:.1f}秒"
            else:
                execution_time = f"{duration/60:.1f}分钟"

        # 构建通知
        title = f"[MONITOR] Claude Code - {task_name}"
        description = f"自动监控 | {status}"

        content_lines = [
            f"任务: {task_name}",
            f"状态: {status}",
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]

        if execution_time:
            content_lines.append(f"耗时: {execution_time}")

        if details:
            content_lines.append("关键信息:")
            for detail in details:
                content_lines.append(f"  {detail}")

        content_lines.append("--- Claude Code 自动监控")
        content = "\n".join(content_lines)

        # 发送API请求
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
                    print(f"[MONITOR] ✅ 通知发送成功: {task_name}")
                    return True
            print(f"[MONITOR] ❌ 发送失败: {response.status_code}")
        except Exception as e:
            print(f"[MONITOR] ❌ 异常: {e}")

        return False

# 全局监控实例
_monitor = ClaudeMonitor()

def start_claude_monitoring():
    """开始Claude Code监控"""
    global _monitor
    _monitor.start_monitoring()

def notify_claude_task(task_name, status="完成", details=None):
    """手动发送Claude任务通知"""
    global _monitor
    message = {
        'task': task_name,
        'status': status,
        'details': details or []
    }
    return _monitor.send_notification(message)

def notify_claude_completion(task_name, status="成功完成", details="", duration=""):
    """Claude任务完成通知（简化接口）"""
    details_list = [details] if details else []
    return notify_claude_task(task_name, status, details_list)

def auto_notify_on_exit():
    """程序退出时自动发送通知"""
    global _monitor
    if _monitor.captured_output:
        _monitor.send_notification()

# 自动启动监控
start_claude_monitoring()

# 注册退出时自动通知
import atexit
atexit.register(auto_notify_on_exit)

def main():
    """命令行使用"""
    if len(sys.argv) < 2:
        print("Claude Code 监控系统")
        print()
        print("用法1 - 手动发送通知:")
        print("  python claude_monitor.py notify <任务名> [状态] [详情]")
        print()
        print("用法2 - 在Python中导入使用:")
        print("  from claude_monitor import notify_claude_completion")
        print("  notify_claude_completion('任务完成', '成功', '详细信息')")
        print()
        print("示例:")
        print("  python claude_monitor.py notify '代码分析' '完成' '分析了50个文件'")
        return

    if sys.argv[1] == "notify":
        task = sys.argv[2] if len(sys.argv) > 2 else "Claude Code 任务"
        status = sys.argv[3] if len(sys.argv) > 3 else "完成"
        details = sys.argv[4] if len(sys.argv) > 4 else ""

        notify_claude_completion(task, status, details)

if __name__ == "__main__":
    main()