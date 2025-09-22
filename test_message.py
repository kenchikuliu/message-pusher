#!/usr/bin/env python3
"""
测试消息推送
"""

import requests
import json

def login():
    """登录获取session"""
    session = requests.Session()

    # 先获取登录页面
    session.get("http://localhost:3000/")

    # 登录
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

def get_user_info(session):
    """获取用户信息"""
    response = session.get("http://localhost:3000/api/user/self")
    if response.ok:
        result = response.json()
        if result.get('success'):
            user = result.get('data', {})
            print(f"用户信息: {user.get('username')} (token: {user.get('token')})")
            return user
    return None

def set_user_token(session, token="claude_task_2025"):
    """设置用户推送token"""
    data = {
        "token": token
    }

    response = session.put("http://localhost:3000/api/user/self", json=data)
    result = response.json()

    if result.get('success'):
        print(f"SUCCESS: 用户token设置成功: {token}")
        return True
    else:
        print("ERROR: token设置失败 -", result.get('message'))
        return False

def test_push_direct():
    """直接测试推送API"""
    data = {
        "title": "[TEST] 飞书推送测试",
        "description": "测试消息推送功能",
        "content": "这是一条测试消息 🎉",
        "token": "claude_task_2025"
    }

    response = requests.post("http://localhost:3000/push/root", json=data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 直接推送测试成功！")
        return True
    else:
        print("ERROR: 直接推送失败 -", result.get('message'))
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
        else:
            print("ERROR: 获取通道失败 -", result.get('message'))
    else:
        print("ERROR: API调用失败")

def main():
    print("=== 消息推送测试 ===")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 检查用户信息
    user = get_user_info(session)

    # 3. 设置token
    set_user_token(session)

    # 4. 检查通道
    check_channels(session)

    # 5. 测试推送
    print("\n测试直接推送...")
    test_push_direct()

if __name__ == "__main__":
    main()