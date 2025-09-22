#!/usr/bin/env python3
"""
Claude Code 最终通知脚本
使用经过curl验证的成功格式
"""

import requests
import sys
import json
from datetime import datetime

WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

def send_claude_notification(task_name, status="success", result="", task_type="Custom", duration_sec=0):
    """
    发送Claude Code通知，使用curl验证过的成功格式
    """

    # 构建JSON payload - 与curl测试完全一致的格式
    payload = {
        "msg_type": "text",
        "content": {
            "task_name": task_name,
            "status": status,
            "result": result,
            "task_type": task_type,
            "duration_sec": duration_sec
        }
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                print(f"SUCCESS: {task_name}")
                return True
            else:
                print(f"ERROR: {data.get('msg')}")
        else:
            print(f"HTTP ERROR: {response.status_code}")

    except Exception as e:
        print(f"EXCEPTION: {e}")

    return False

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("Claude Code 通知脚本")
        print("用法: python claude_notify_final.py <任务名> [状态] [结果] [类型] [时长]")
        print("示例: python claude_notify_final.py '代码分析' 'success' '发现3个问题' 'Custom' 30")
        return

    task_name = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else "success"
    result = sys.argv[3] if len(sys.argv) > 3 else ""
    task_type = sys.argv[4] if len(sys.argv) > 4 else "Custom"
    duration_sec = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5].isdigit() else 0

    send_claude_notification(task_name, status, result, task_type, duration_sec)

if __name__ == "__main__":
    main()