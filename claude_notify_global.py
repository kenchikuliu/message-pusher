#!/usr/bin/env python3
"""
Claude Code 全局通知系统 - 简化版本
解决emoji编码问题，直接使用Message Pusher API
"""

import requests
import sys
import os
import time
from datetime import datetime

# 配置
MESSAGE_PUSHER_API = "http://localhost:3000/push/root"
CLAUDE_TASK_TOKEN = "claude_task_2025"
FEISHU_CHANNEL = "feishu"

def get_status_prefix(status):
    """获取状态前缀（无emoji）"""
    status_lower = status.lower()
    if "完成" in status or "成功" in status or "success" in status_lower:
        return "[OK]"
    elif "失败" in status or "错误" in status or "error" in status_lower or "fail" in status_lower:
        return "[FAIL]"
    elif "警告" in status or "warning" in status_lower:
        return "[WARN]"
    else:
        return "[INFO]"

def detect_task_type(description):
    """简单的任务类型检测"""
    description_lower = description.lower()

    if any(word in description_lower for word in ["分析", "检查", "扫描", "review", "analyze"]):
        return "代码分析"
    elif any(word in description_lower for word in ["生成", "创建", "generate", "create", "build"]):
        return "代码生成"
    elif any(word in description_lower for word in ["重构", "优化", "refactor", "optimize"]):
        return "代码重构"
    elif any(word in description_lower for word in ["修复", "fix", "bug", "错误"]):
        return "bug修复"
    elif any(word in description_lower for word in ["测试", "test", "验证"]):
        return "测试"
    elif any(word in description_lower for word in ["部署", "deploy", "发布"]):
        return "部署"
    else:
        return "其他任务"

def send_claude_notification(task_name, status="完成", details="", duration=""):
    """发送Claude Code通知"""

    # 自动检测任务类型
    task_type = detect_task_type(task_name)
    status_prefix = get_status_prefix(status)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构建消息
    title = f"{status_prefix} Claude Code - {task_name}"
    description = f"{task_type} | {status}"

    # 构建详细内容
    content_lines = [
        f"任务: {task_name}",
        f"类型: {task_type}",
        f"状态: {status}",
        f"时间: {current_time}"
    ]

    if duration:
        content_lines.append(f"耗时: {duration}")

    if details:
        content_lines.append(f"详情: {details}")

    # 添加项目信息
    try:
        current_dir = os.path.basename(os.getcwd())
        content_lines.append(f"项目: {current_dir}")
    except:
        pass

    content_lines.append("--- 来自 Claude Code 全局通知")
    content = "\n".join(content_lines)

    # 构建API请求
    api_data = {
        "title": title,
        "description": description,
        "content": content,
        "token": CLAUDE_TASK_TOKEN,
        "channel": FEISHU_CHANNEL
    }

    try:
        response = requests.post(MESSAGE_PUSHER_API, json=api_data, timeout=15)

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"SUCCESS: 通知发送成功 - {title}")
                return True
            else:
                print(f"ERROR: {result.get('message', '未知错误')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

    return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python claude_notify_global.py <任务名> [状态] [详情] [耗时]")
        print("示例: python claude_notify_global.py '代码分析' '完成' '发现3个问题' '2分钟'")
        return

    task_name = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else "完成"
    details = sys.argv[3] if len(sys.argv) > 3 else ""
    duration = sys.argv[4] if len(sys.argv) > 4 else ""

    send_claude_notification(task_name, status, details, duration)

if __name__ == "__main__":
    main()