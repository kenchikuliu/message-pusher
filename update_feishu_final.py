#!/usr/bin/env python3
"""
最终更新飞书配置并测试
"""

import requests
import json

# 配置
SERVER_URL = "http://localhost:3000"
USERNAME = "root"
PASSWORD = "123456"
WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/5f57f0a2814076ad7e269d09f56e0ad2"

def login():
    """登录"""
    session = requests.Session()
    session.get(f"{SERVER_URL}/")

    login_data = {"username": USERNAME, "password": PASSWORD}
    response = session.post(f"{SERVER_URL}/api/user/login", json=login_data)

    if response.json().get('success'):
        print("SUCCESS: 登录成功")
        return session
    return None

def update_feishu_channel(session):
    """更新飞书通道"""

    # 更新飞书通道配置
    channel_data = {
        "name": "feishu",
        "type": "lark",
        "description": "飞书群机器人",
        "url": WEBHOOK_URL,
        "status": 1
    }

    # 尝试PUT更新
    response = session.put(f"{SERVER_URL}/api/channel/1", json=channel_data)

    if response.status_code == 200:
        print("SUCCESS: 飞书通道URL更新成功")
        return True
    else:
        print(f"更新失败: {response.status_code} - {response.text}")
        return False

def test_system_push():
    """测试系统推送"""

    # 通过系统API测试推送
    test_data = {
        "title": "系统测试成功",
        "description": "飞书推送配置完成",
        "content": "Claude Code 任务完成提醒系统已就绪！",
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)
    result = response.json()

    print(f"系统推送测试结果: {result}")
    return result.get('success', False)

def main():
    print("=== 最终飞书配置更新 ===")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 更新飞书通道
    print("\n2. 更新飞书通道配置...")
    if not update_feishu_channel(session):
        return

    # 3. 测试系统推送
    print("\n3. 测试系统推送...")
    if test_system_push():
        print("✅ SUCCESS: 系统推送测试成功！")
    else:
        print("❌ 系统推送测试失败，但直接Webhook可用")

    print("\n4. 测试命令行脚本...")
    print("现在请运行: python claude_notify.py \"最终测试\" \"完成\" \"系统配置成功\"")

if __name__ == "__main__":
    main()