#!/usr/bin/env python3
"""
修复默认通道配置
"""

import requests
import json

def login():
    """登录获取session"""
    session = requests.Session()
    session.get("http://localhost:3000/")

    login_data = {
        "username": "root",
        "password": "123456"
    }

    response = session.post("http://localhost:3000/api/user/login", json=login_data)
    result = response.json()

    if result.get('success'):
        print("LOGIN SUCCESS")
        return session
    else:
        print("LOGIN FAILED:", result.get('message'))
        return None

def get_options(session):
    """获取系统选项"""
    response = session.get("http://localhost:3000/api/option/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            options = result.get('data', {})
            print("当前系统选项:")
            if isinstance(options, dict):
                for key, value in options.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  选项数据: {options}")
            return options
        else:
            print("ERROR: 获取选项失败 -", result.get('message'))
    else:
        print("ERROR: API调用失败")
    return {}

def set_default_channel(session, channel_name="feishu"):
    """设置默认推送通道"""
    option_data = {
        "PushDefaultChannel": channel_name
    }

    response = session.put("http://localhost:3000/api/option/", json=option_data)
    result = response.json()

    if result.get('success'):
        print(f"SUCCESS: 默认通道设置为 {channel_name}")
        return True
    else:
        print("ERROR: 默认通道设置失败 -", result.get('message'))
        return False

def check_channels(session):
    """检查通道配置"""
    response = session.get("http://localhost:3000/api/channel/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            channels = result.get('data', [])
            print(f"现有通道: {len(channels)}")
            for ch in channels:
                print(f"- {ch.get('name')}: {ch.get('type')} (状态: {'启用' if ch.get('status') else '禁用'})")
                if ch.get('type') == 'lark':
                    print(f"  URL: {ch.get('url')}")
            return channels
        else:
            print("ERROR: 获取通道失败 -", result.get('message'))
    else:
        print("ERROR: API调用失败")
    return []

def test_push_with_channel(channel_name="feishu"):
    """测试指定通道的推送"""
    data = {
        "title": "[TEST] 飞书推送测试",
        "description": "测试飞书机器人推送功能",
        "content": "恭喜！飞书推送配置成功 🎉",
        "token": "claude_task_2025",
        "channel": channel_name
    }

    response = requests.post("http://localhost:3000/push/root", json=data)
    result = response.json()

    if result.get('success'):
        print(f"SUCCESS: {channel_name} 通道推送测试成功！请检查飞书群消息")
        return True
    else:
        print(f"ERROR: {channel_name} 通道推送失败 -", result.get('message'))
        return False

def main():
    print("=== 修复默认通道配置 ===")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 检查当前选项
    print("\n1. 检查当前系统选项:")
    get_options(session)

    # 3. 检查通道配置
    print("\n2. 检查通道配置:")
    channels = check_channels(session)

    # 4. 设置默认通道为feishu
    print("\n3. 设置默认通道:")
    set_default_channel(session, "feishu")

    # 5. 再次检查选项确认
    print("\n4. 确认配置:")
    get_options(session)

    # 6. 测试推送
    print("\n5. 测试推送:")
    test_push_with_channel("feishu")

if __name__ == "__main__":
    main()