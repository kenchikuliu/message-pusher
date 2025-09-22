#!/usr/bin/env python3
"""
更新飞书通道URL为mock服务器
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

def update_feishu_to_mock(session):
    """更新飞书通道为mock服务器"""

    # 先获取现有通道
    response = session.get("http://localhost:3000/api/channel/")
    if not response.ok:
        print("ERROR: 无法获取通道列表")
        return False

    result = response.json()
    if not result.get('success'):
        print("ERROR: 获取通道失败 -", result.get('message'))
        return False

    channels = result.get('data', [])
    feishu_channel = None

    for ch in channels:
        if ch.get('type') == 'lark' and ch.get('name') == 'feishu':
            feishu_channel = ch
            break

    if not feishu_channel:
        print("ERROR: 未找到飞书通道")
        return False

    # 更新通道URL为mock服务器
    channel_id = feishu_channel['id']
    update_data = {
        "name": "feishu",
        "type": "lark",
        "description": "飞书群机器人 (Mock测试)",
        "url": "http://localhost:8080/webhook",  # Mock服务器URL
        "status": 1
    }

    response = session.put(f"http://localhost:3000/api/channel/{channel_id}", json=update_data)

    if response.ok:
        try:
            result = response.json()
            if result.get('success'):
                print("SUCCESS: 飞书通道URL更新为mock服务器")
                print("Mock URL: http://localhost:8080/webhook")
                return True
            else:
                print("ERROR: 更新失败 -", result.get('message'))
                return False
        except:
            print("SUCCESS: 飞书通道URL更新成功 (无JSON响应)")
            return True
    else:
        print(f"ERROR: HTTP错误 {response.status_code}")
        return False

def test_mock_webhook():
    """测试mock webhook"""
    data = {
        "title": "[TEST] Mock飞书推送测试",
        "description": "测试mock服务器功能",
        "content": "这是一条测试消息，验证Claude Code + Mock飞书集成",
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    try:
        response = requests.post("http://localhost:3000/push/root", json=data, timeout=10)
        result = response.json()

        if result.get('success'):
            print("[OK] Mock飞书测试成功!")
            print("请检查mock服务器输出以确认消息接收")
            return True
        else:
            print(f"[FAIL] Mock测试失败: {result.get('message')}")
            return False

    except Exception as e:
        print(f"[FAIL] 测试异常: {str(e)}")
        return False

def main():
    print("=== 更新为Mock服务器并测试 ===")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 更新飞书通道
    if update_feishu_to_mock(session):
        print("\n等待2秒让服务器准备好...")
        import time
        time.sleep(2)

        # 3. 测试mock webhook
        print("\n测试mock webhook:")
        test_mock_webhook()

if __name__ == "__main__":
    main()