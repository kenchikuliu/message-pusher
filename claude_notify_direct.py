#!/usr/bin/env python3
"""
Claude Code 任务完成提醒脚本 - 直接飞书版本
用法: python claude_notify_direct.py [任务名称] [状态] [详细信息]
"""

import requests
import sys
import json
from datetime import datetime

# 配置 - 您的飞书 Webhook URL
FEISHU_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/5f57f0a2814076ad7e269d09f56e0ad2"

def send_feishu_notification(title, description, content=""):
    """直接发送飞书通知"""

    # 构建飞书消息内容
    message_text = f"🤖 Claude Code 执行报告\n\n"
    message_text += f"任务: {title}\n"
    message_text += f"状态: {description}\n"
    message_text += f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    if content:
        message_text += f"详情: {content}\n"

    message_text += "\n---\n来自 Claude Code 自动提醒"

    # 飞书消息格式
    feishu_data = {
        "msg_type": "text",
        "content": {
            "text": message_text
        }
    }

    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=feishu_data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"SUCCESS: 飞书提醒发送成功 - {title}")
                return True
            else:
                print(f"ERROR: 飞书API错误 - {result.get('msg', '未知错误')}")
                return False
        else:
            print(f"ERROR: HTTP错误 - {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR: 网络错误 - {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: 发送失败 - {str(e)}")
        return False

def send_feishu_card_notification(title, description, content=""):
    """发送飞书富文本卡片通知"""

    # 确定状态图标
    if "失败" in description or "错误" in description:
        icon = "❌"
        color = "red"
    elif "完成" in description or "成功" in description:
        icon = "✅"
        color = "green"
    elif "进行" in description:
        icon = "🔄"
        color = "blue"
    else:
        icon = "🤖"
        color = "blue"

    # 构建卡片内容
    card_content = f"**{icon} 任务**: {title}\n"
    card_content += f"**📊 状态**: {description}\n"
    card_content += f"**⏰ 时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    if content:
        card_content += f"**📝 详情**: {content}\n"

    card_content += "\n---\n_来自 Claude Code 自动提醒_"

    # 飞书卡片消息格式
    card_data = {
        "msg_type": "interactive",
        "card": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": card_content,
                        "tag": "lark_md"
                    }
                }
            ],
            "header": {
                "title": {
                    "content": f"{icon} Claude Code 任务完成",
                    "tag": "plain_text"
                },
                "template": color
            }
        }
    }

    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=card_data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"SUCCESS: 飞书卡片提醒发送成功 - {title}")
                return True
            else:
                print(f"ERROR: 飞书API错误 - {result.get('msg', '未知错误')}")
                return False
        else:
            print(f"ERROR: HTTP错误 - {response.status_code}")
            return False

    except Exception as e:
        print(f"ERROR: 卡片发送失败 - {str(e)}")
        # 如果卡片失败，尝试普通文本
        return send_feishu_notification(title, description, content)

def notify_claude_completion(task_name="Claude Code 任务", status="完成", details="", use_card=True):
    """Claude Code 任务完成专用通知"""

    if use_card:
        return send_feishu_card_notification(task_name, status, details)
    else:
        return send_feishu_notification(task_name, status, details)

def main():
    """命令行入口"""
    if len(sys.argv) == 1:
        # 默认测试通知
        notify_claude_completion()
    elif len(sys.argv) == 2:
        # 简单通知
        notify_claude_completion("提醒", sys.argv[1])
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
        notify_claude_completion(task_name, status, details)

if __name__ == "__main__":
    main()