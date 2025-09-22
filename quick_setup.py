#!/usr/bin/env python3
"""
快速配置消息推送服务
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

def setup_token(session):
    """设置推送 Token"""

    # 获取当前配置
    response = session.get(f"{SERVER_URL}/api/option/")
    if not response.ok:
        print("ERROR: 获取配置失败")
        return False

    # 设置推送 Token
    token_data = {
        "PushToken": "claude_task_2025"
    }

    response = session.put(f"{SERVER_URL}/api/option/", json=token_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 推送 Token 设置成功")
        return True
    else:
        print("ERROR: Token 设置失败 -", result.get('message'))
        return False

def setup_email_channel(session, email, smtp_server="", smtp_port="", smtp_user="", smtp_pass=""):
    """设置邮件推送通道（简化版）"""

    # 创建一个默认的邮件通道
    channel_data = {
        "name": "默认邮件",
        "type": "email",
        "email": email,
        "status": 1
    }

    response = session.post(f"{SERVER_URL}/api/channel/", json=channel_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 邮件通道设置成功")
        return True
    else:
        print("ERROR: 邮件通道设置失败 -", result.get('message'))
        return False

def test_notification():
    """测试通知"""
    test_data = {
        "title": "[TEST] 配置测试",
        "description": "消息推送系统配置完成",
        "content": "这是一条测试消息，说明您的推送配置已经生效！",
        "token": "claude_task_2025"
    }

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 测试通知发送成功！")
        return True
    else:
        print("ERROR: 测试通知失败 -", result.get('message'))
        return False

def main():
    print("=== 消息推送快速配置 ===")
    print()

    # 1. 登录
    print("1. 正在登录...")
    session = login()
    if not session:
        return

    # 2. 设置 Token
    print("\n2. 正在设置推送 Token...")
    if not setup_token(session):
        return

    # 3. 询问邮箱
    print("\n3. 设置邮件推送（可选）")
    email = input("请输入您的邮箱地址（直接回车跳过）: ").strip()

    if email:
        setup_email_channel(session, email)
    else:
        print("跳过邮件配置")

    # 4. 测试通知
    print("\n4. 正在测试通知...")
    test_notification()

    print("\n=== 配置完成 ===")
    print("现在您可以使用以下命令发送通知：")
    print("python claude_notify.py \"任务名称\" \"完成\" \"详细信息\"")
    print()
    print("API 调用示例：")
    print(f'curl -X POST "{SERVER_URL}/push/{USERNAME}" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"title":"测试","description":"消息内容","token":"claude_task_2025"}\'')

if __name__ == "__main__":
    main()