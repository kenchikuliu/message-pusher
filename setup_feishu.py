#!/usr/bin/env python3
"""
飞书通道快速配置脚本
"""

import requests
import json

# 配置
SERVER_URL = "http://localhost:3000"
USERNAME = "root"
PASSWORD = "123456"

def login():
    """登录获取 session"""
    session = requests.Session()

    # 先获取登录页面
    session.get(f"{SERVER_URL}/")

    # 登录
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

def check_channels(session):
    """检查现有通道"""
    response = session.get(f"{SERVER_URL}/api/channel/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            channels = result.get('data', [])
            print(f"现有通道数量: {len(channels)}")
            for ch in channels:
                print(f"- {ch.get('name')}: {ch.get('type')} (状态: {'启用' if ch.get('status') else '禁用'})")
            return channels
        else:
            print("ERROR: 获取通道失败 -", result.get('message'))
    else:
        print("ERROR: API调用失败")
    return []

def setup_feishu_channel(session, webhook_url):
    """设置飞书推送通道"""

    # 创建飞书通道
    channel_data = {
        "name": "feishu",
        "type": "lark",
        "description": "飞书群机器人",
        "url": webhook_url,
        "status": 1  # 启用
    }

    response = session.post(f"{SERVER_URL}/api/channel/", json=channel_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 飞书通道设置成功")
        return True
    else:
        print("ERROR: 飞书通道设置失败 -", result.get('message'))
        return False

def set_default_channel(session, channel_name="feishu"):
    """设置默认推送通道"""

    # 设置默认通道
    option_data = {
        "PushDefaultChannel": channel_name
    }

    response = session.put(f"{SERVER_URL}/api/option/", json=option_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 默认通道设置成功")
        return True
    else:
        print("ERROR: 默认通道设置失败 -", result.get('message'))
        return False

def test_notification(session):
    """测试通知"""
    test_data = {
        "title": "[TEST] 飞书推送测试",
        "description": "飞书群机器人配置成功",
        "content": "恭喜！您的飞书推送配置已经生效！🎉",
        "token": "claude_task_2025"
    }

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 测试通知发送成功！请检查飞书群消息")
        return True
    else:
        print("ERROR: 测试通知失败 -", result.get('message'))
        return False

def main():
    print("=== 飞书通道快速配置 ===")
    print()

    # 1. 登录
    print("1. 正在登录...")
    session = login()
    if not session:
        return

    # 2. 检查现有通道
    print("\n2. 检查现有通道...")
    channels = check_channels(session)

    # 检查是否已有飞书通道
    feishu_exists = any(ch.get('type') == 'lark' for ch in channels)
    if feishu_exists:
        print("发现已存在飞书通道，跳过创建步骤")
    else:
        # 3. 询问 Webhook URL
        print("\n3. 配置飞书 Webhook")
        webhook_url = input("请输入飞书机器人的 Webhook URL: ").strip()

        if not webhook_url:
            print("ERROR: 需要提供 Webhook URL")
            return

        if not webhook_url.startswith('https://open.feishu.cn/open-apis/bot/v2/hook/'):
            print("WARNING: URL 格式可能不正确，请确认是飞书机器人 Webhook URL")

        # 4. 创建飞书通道
        print("\n4. 正在创建飞书通道...")
        if not setup_feishu_channel(session, webhook_url):
            return

    # 5. 设置为默认通道
    print("\n5. 正在设置为默认通道...")
    set_default_channel(session, "feishu")

    # 6. 测试通知
    print("\n6. 正在测试通知...")
    test_notification(session)

    print("\n=== 配置完成 ===")
    print("现在您可以使用以下命令发送飞书通知：")
    print("python claude_notify.py \"任务名称\" \"完成\" \"详细信息\"")

if __name__ == "__main__":
    main()