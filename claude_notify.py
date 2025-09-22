#!/usr/bin/env python3
"""
Claude Code 任务完成提醒脚本
用法: python claude_notify.py [任务名称] [状态] [详细信息]
"""

import requests
import sys
import json
from datetime import datetime

# 配置
SERVER_URL = "http://localhost:3000/push/root"
TOKEN = "claude_task_2025"

def send_notification(title, description, content="", token=TOKEN, channel="feishu"):
    """发送通知到消息推送服务"""
    data = {
        "title": title,
        "description": description,
        "content": content,
        "token": token,
        "channel": channel  # 明确指定使用飞书通道
    }

    try:
        response = requests.post(SERVER_URL, json=data, timeout=10)
        result = response.json()

        if result.get('success'):
            print("SUCCESS: 提醒发送成功 -", title)
            return True
        else:
            print("ERROR: 发送失败 -", result.get('message', '未知错误'))
            return False

    except requests.exceptions.RequestException as e:
        print("ERROR: 网络错误 -", str(e))
        return False
    except json.JSONDecodeError:
        print("ERROR: 服务器响应格式错误")
        return False
    except Exception as e:
        print("ERROR: 发送失败 -", str(e))
        return False

def notify_claude_completion(task_name="Claude Code 任务", status="完成", details="", duration=""):
    """Claude Code 任务完成专用通知"""

    # 构建内容
    content_parts = [
        f"**🤖 Claude Code 执行报告**\n",
        f"- **任务**: {task_name}",
        f"- **状态**: {status}",
        f"- **完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]

    if duration:
        content_parts.append(f"- **耗时**: {duration}")

    if details:
        content_parts.append(f"- **详情**: {details}")

    content_parts.append("\n---\n_🔔 来自 Claude Code 自动提醒_")

    content = "\n".join(content_parts)

    # 确定标题图标
    if "失败" in status or "错误" in status:
        icon = "[FAIL]"
    elif "完成" in status or "成功" in status:
        icon = "[OK]"
    elif "进行" in status:
        icon = "[RUNNING]"
    else:
        icon = "[CLAUDE]"

    title = f"{icon} {task_name}"
    description = f"状态: {status}"

    return send_notification(title, description, content)

def notify_simple(title, message):
    """简单通知"""
    return send_notification(title, message)

def notify_script_completion(script_name, success=True, details=""):
    """脚本执行完成通知"""
    status = "成功完成" if success else "执行失败"
    icon = "✅" if success else "❌"

    content = f"""**📝 脚本执行报告**

- **脚本**: {script_name}
- **状态**: {status}
- **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **详情**: {details or '无额外信息'}

---
_🔔 自动执行提醒_"""

    title = f"{icon} {script_name}"
    description = f"脚本{status}"

    return send_notification(title, description, content)

def main():
    """命令行入口"""
    if len(sys.argv) == 1:
        # 默认测试通知
        notify_claude_completion()
    elif len(sys.argv) == 2:
        # 简单通知
        notify_simple("🔔 提醒", sys.argv[1])
    elif len(sys.argv) == 3:
        # 任务状态通知
        task_name = sys.argv[1]
        status = sys.argv[2]
        notify_claude_completion(task_name, status)
    elif len(sys.argv) >= 4:
        # 完整通知
        task_name = sys.argv[1]
        status = sys.argv[2]
        details = sys.argv[3]
        duration = sys.argv[4] if len(sys.argv) > 4 else ""
        notify_claude_completion(task_name, status, details, duration)

if __name__ == "__main__":
    main()