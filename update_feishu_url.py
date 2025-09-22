#!/usr/bin/env python3
"""
更新飞书通道URL为测试URL
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

def update_feishu_channel(session):
    """更新飞书通道为测试URL"""

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

    # 更新通道URL为测试webhook URL (这里用httpbin.org作为测试)
    channel_id = feishu_channel['id']
    update_data = {
        "name": "feishu",
        "type": "lark",
        "description": "飞书群机器人 (测试)",
        "url": "https://httpbin.org/post",  # 测试URL，会接收POST数据
        "status": 1
    }

    response = session.put(f"http://localhost:3000/api/channel/{channel_id}", json=update_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 飞书通道URL更新为测试URL")
        print("测试URL: https://httpbin.org/post")
        return True
    else:
        print("ERROR: 更新失败 -", result.get('message'))
        return False

def main():
    session = login()
    if session:
        update_feishu_channel(session)

if __name__ == "__main__":
    main()