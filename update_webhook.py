#!/usr/bin/env python3
"""
更新飞书 Webhook URL
"""

import requests
import json

# 配置
SERVER_URL = "http://localhost:3000"
USERNAME = "root"
PASSWORD = "123456"
NEW_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/5f57f0a2814076ad7e269d09f56e0ad2"

def login():
    """登录获取 session"""
    session = requests.Session()
    session.get(f"{SERVER_URL}/")

    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    response = session.post(f"{SERVER_URL}/api/user/login", json=login_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 登录成功")
        return session
    else:
        print("ERROR: 登录失败 -", result.get('message'))
        return None

def get_feishu_channel(session):
    """获取飞书通道信息"""
    response = session.get(f"{SERVER_URL}/api/channel/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            channels = result.get('data', [])
            for ch in channels:
                if ch.get('type') == 'lark':
                    return ch
    return None

def update_webhook_url(session, channel_id, new_url):
    """更新 Webhook URL"""
    update_data = {
        "name": "feishu",
        "type": "lark",
        "description": "飞书群机器人",
        "url": new_url,
        "status": 1
    }

    response = session.put(f"{SERVER_URL}/api/channel/{channel_id}", json=update_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: Webhook URL 更新成功")
        print(f"新 URL: {new_url}")
        return True
    else:
        print("ERROR: Webhook URL 更新失败 -", result.get('message'))
        return False

def test_feishu_push():
    """测试飞书推送"""
    test_data = {
        "title": "🎉 飞书推送测试成功",
        "description": "Webhook URL 已更新",
        "content": "恭喜！您的飞书推送配置已完全生效！现在可以接收任务完成提醒了。",
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 🎉 飞书推送测试成功！请检查您的飞书群消息")
        return True
    else:
        print("ERROR: 飞书推送测试失败 -", result.get('message'))
        return False

def main():
    print("=== 更新飞书 Webhook URL ===")
    print(f"新 URL: {NEW_WEBHOOK_URL}")
    print()

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 获取飞书通道
    print("\n2. 获取飞书通道信息...")
    feishu_channel = get_feishu_channel(session)
    if not feishu_channel:
        print("ERROR: 未找到飞书通道")
        return

    channel_id = feishu_channel.get('id')
    print(f"找到飞书通道 ID: {channel_id}")

    # 3. 更新 Webhook URL
    print("\n3. 更新 Webhook URL...")
    if not update_webhook_url(session, channel_id, NEW_WEBHOOK_URL):
        return

    # 4. 测试推送
    print("\n4. 测试飞书推送...")
    test_feishu_push()

    print("\n=== 配置完成 ===")
    print("🎉 飞书推送系统已完全配置完成！")
    print("现在您可以使用以下命令发送通知：")
    print("python claude_notify.py \"任务名称\" \"完成\" \"详细信息\"")

if __name__ == "__main__":
    main()