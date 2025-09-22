#!/usr/bin/env python3
"""
修复默认推送通道配置
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

def get_channels(session):
    """获取所有通道"""
    response = session.get(f"{SERVER_URL}/api/channel/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            channels = result.get('data', [])
            print(f"找到 {len(channels)} 个通道:")
            for ch in channels:
                print(f"- ID: {ch.get('id')}, 名称: {ch.get('name')}, 类型: {ch.get('type')}, 状态: {'启用' if ch.get('status') else '禁用'}")
            return channels
    return []

def get_current_options(session):
    """获取当前系统选项"""
    response = session.get(f"{SERVER_URL}/api/option/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            options = result.get('data', {})
            print("当前系统选项:")
            if isinstance(options, dict):
                for key, value in options.items():
                    print(f"- {key}: {value}")
            else:
                print(f"- 选项数据格式: {type(options)}")
                print(f"- 选项内容: {options}")
            return options
    return {}

def update_user_default_channel(session, channel_name):
    """更新用户默认通道"""
    # 尝试不同的配置选项名称
    option_names = [
        "DefaultChannel",
        "PushDefaultChannel",
        "default_channel",
        "push_default_channel"
    ]

    success = False
    for option_name in option_names:
        option_data = {option_name: channel_name}

        response = session.put(f"{SERVER_URL}/api/option/", json=option_data)
        result = response.json()

        if result.get('success'):
            print(f"SUCCESS: 默认通道设置成功 ({option_name})")
            success = True
            break
        else:
            print(f"尝试 {option_name}: {result.get('message', '失败')}")

    return success

def test_direct_channel_push(session, channel_name):
    """直接测试指定通道推送"""
    # 使用指定通道名称进行推送
    test_data = {
        "title": f"[TEST] 通道测试 - {channel_name}",
        "description": f"使用 {channel_name} 通道推送",
        "content": "这是一条测试消息",
        "token": "claude_task_2025",
        "channel": channel_name  # 明确指定通道
    }

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)
    result = response.json()

    if result.get('success'):
        print(f"SUCCESS: {channel_name} 通道推送成功")
        return True
    else:
        print(f"ERROR: {channel_name} 通道推送失败 - {result.get('message')}")
        return False

def main():
    print("=== 修复默认通道配置 ===")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 获取通道列表
    print("\n2. 获取通道列表...")
    channels = get_channels(session)

    # 3. 获取当前配置
    print("\n3. 获取当前系统选项...")
    get_current_options(session)

    # 4. 查找飞书通道
    feishu_channel = None
    for ch in channels:
        if ch.get('type') == 'lark':
            feishu_channel = ch
            break

    if not feishu_channel:
        print("ERROR: 没有找到飞书通道")
        return

    channel_name = feishu_channel.get('name')
    print(f"\n4. 找到飞书通道: {channel_name}")

    # 5. 设置默认通道
    print(f"\n5. 设置 {channel_name} 为默认通道...")
    update_user_default_channel(session, channel_name)

    # 6. 测试推送
    print(f"\n6. 测试 {channel_name} 通道推送...")
    test_direct_channel_push(session, channel_name)

    print("\n=== 修复完成 ===")
    print("请现在使用 python claude_notify.py 进行测试")

if __name__ == "__main__":
    main()