#!/usr/bin/env python3
"""
直接测试飞书 Webhook
"""

import requests
import json

# 您提供的飞书 Webhook URL
WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/5f57f0a2814076ad7e269d09f56e0ad2"

def test_direct_webhook():
    """直接测试飞书 Webhook"""

    # 飞书机器人消息格式
    message_data = {
        "msg_type": "text",
        "content": {
            "text": "🎉 飞书推送测试成功！\n\n任务: Claude Code 配置测试\n状态: 完成\n时间: 2025-09-20 19:10:00\n\n来自 Claude Code 任务完成提醒"
        }
    }

    print("测试飞书 Webhook 直接推送...")
    print(f"URL: {WEBHOOK_URL}")
    print("消息内容:")
    print(json.dumps(message_data, indent=2, ensure_ascii=False))

    try:
        response = requests.post(WEBHOOK_URL, json=message_data, timeout=10)

        print(f"\n响应状态码: {response.status_code}")
        print("响应内容:")
        print(response.text)

        if response.status_code == 200:
            print("\n✅ SUCCESS: 飞书 Webhook 测试成功！")
            print("请检查您的飞书群是否收到了消息")
            return True
        else:
            print(f"\n❌ ERROR: HTTP {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: 网络错误 - {e}")
        return False

def test_rich_card_message():
    """测试富文本卡片消息"""

    card_message = {
        "msg_type": "interactive",
        "card": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": "🤖 **Claude Code 任务完成**\n\n✅ **任务**: 飞书推送配置\n📊 **状态**: 完成\n⏰ **时间**: 2025-09-20 19:10:00\n📝 **详情**: 成功配置飞书推送功能\n\n---\n_来自 Claude Code 自动提醒_",
                        "tag": "lark_md"
                    }
                }
            ],
            "header": {
                "title": {
                    "content": "🎉 任务完成通知",
                    "tag": "plain_text"
                },
                "template": "green"
            }
        }
    }

    print("\n" + "="*50)
    print("测试飞书富文本卡片消息...")

    try:
        response = requests.post(WEBHOOK_URL, json=card_message, timeout=10)

        print(f"响应状态码: {response.status_code}")
        print("响应内容:")
        print(response.text)

        if response.status_code == 200:
            print("\n✅ SUCCESS: 飞书富文本卡片测试成功！")
            return True
        else:
            print(f"\n❌ ERROR: HTTP {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: 网络错误 - {e}")
        return False

def main():
    print("=== 飞书 Webhook 直接测试 ===")

    # 测试简单文本消息
    success1 = test_direct_webhook()

    # 测试富文本卡片
    success2 = test_rich_card_message()

    print("\n" + "="*50)
    if success1 or success2:
        print("🎉 飞书 Webhook 工作正常！")
        print("您现在可以在飞书群中看到测试消息")
    else:
        print("❌ 飞书 Webhook 测试失败")
        print("请检查：")
        print("1. URL 是否正确")
        print("2. 机器人是否已添加到群中")
        print("3. 机器人权限设置是否正确")

if __name__ == "__main__":
    main()