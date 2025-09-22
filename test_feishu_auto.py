#!/usr/bin/env python3
"""
飞书通道自动配置脚本（测试版）
"""

import requests
import json

# 配置
SERVER_URL = "http://localhost:3000"
USERNAME = "root"
PASSWORD = "123456"

# 示例 Webhook URL（需要用户替换为真实的）
EXAMPLE_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

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

def setup_test_feishu_channel(session):
    """设置测试飞书推送通道"""

    # 创建飞书通道（测试用）
    channel_data = {
        "name": "feishu",
        "type": "lark",
        "description": "飞书群机器人（测试配置）",
        "url": EXAMPLE_WEBHOOK_URL,
        "status": 1  # 启用
    }

    response = session.post(f"{SERVER_URL}/api/channel/", json=channel_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 飞书通道（测试）设置成功")
        print(f"注意: 当前使用的是示例 URL: {EXAMPLE_WEBHOOK_URL}")
        print("请在 Web 界面中将 URL 更新为您的真实 Webhook URL")
        return True
    else:
        print("ERROR: 飞书通道设置失败 -", result.get('message'))
        return False

def set_default_channel(session, channel_name="feishu"):
    """设置默认推送通道"""

    # 设置默认通道
    option_data = {
        "DefaultChannel": channel_name
    }

    response = session.put(f"{SERVER_URL}/api/option/", json=option_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 默认通道设置成功")
        return True
    else:
        print("ERROR: 默认通道设置失败 -", result.get('message'))
        return False

def main():
    print("=== 飞书通道自动配置（测试） ===")
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
        print("发现已存在飞书通道")
    else:
        # 3. 创建测试飞书通道
        print("\n3. 正在创建测试飞书通道...")
        if not setup_test_feishu_channel(session):
            return

    # 4. 设置为默认通道
    print("\n4. 正在设置为默认通道...")
    set_default_channel(session, "feishu")

    print("\n=== 测试配置完成 ===")
    print("接下来请：")
    print("1. 访问 http://localhost:3000")
    print("2. 登录后进入 '推送设置'")
    print("3. 找到飞书通道，将 URL 更新为您的真实 Webhook URL")
    print("4. 点击 '测试' 按钮验证配置")
    print("5. 使用 python claude_notify.py 进行测试")

if __name__ == "__main__":
    main()