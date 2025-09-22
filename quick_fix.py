#!/usr/bin/env python3
"""
快速修复配置并测试
"""

import requests
import json

def login_and_fix():
    """登录并修复配置"""
    session = requests.Session()

    # 登录
    session.get("http://localhost:3000/")
    login_data = {"username": "root", "password": "123456"}
    response = session.post("http://localhost:3000/api/user/login", json=login_data)
    result = response.json()

    if not result.get('success'):
        print("LOGIN FAILED")
        return False

    print("LOGIN SUCCESS")

    # 设置用户的推送通道为feishu
    user_data = {"channel": "feishu"}
    response = session.put("http://localhost:3000/api/user/self", json=user_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 用户默认通道设置为feishu")
    else:
        print("ERROR: 用户通道设置失败 -", result.get('message'))

    # 设置系统默认通道
    option_data = {"PushDefaultChannel": "feishu"}
    response = session.put("http://localhost:3000/api/option/", json=option_data)
    result = response.json()

    if result.get('success'):
        print("SUCCESS: 系统默认通道设置为feishu")
    else:
        print("ERROR: 系统默认通道设置失败 -", result.get('message'))

    return session

def test_direct_feishu():
    """直接测试feishu通道"""
    data = {
        "title": "[TEST] 飞书推送测试",
        "description": "测试飞书通道推送功能",
        "content": "这是一条测试消息，验证Claude Code集成功能",
        "token": "claude_task_2025",
        "channel": "feishu"  # 明确指定通道
    }

    try:
        response = requests.post("http://localhost:3000/push/root", json=data, timeout=10)
        result = response.json()

        if result.get('success'):
            print("[OK] 飞书通道测试成功!")
            return True
        else:
            print(f"[FAIL] 飞书通道测试失败: {result.get('message')}")
            return False

    except Exception as e:
        print(f"[FAIL] 测试异常: {str(e)}")
        return False

def main():
    print("=== 快速修复和测试 ===")

    # 1. 登录并修复配置
    session = login_and_fix()
    if not session:
        return

    # 2. 测试飞书通道
    print("\n测试飞书通道:")
    test_direct_feishu()

    # 3. 测试Claude通知脚本
    print("\n测试Claude通知脚本:")
    import subprocess
    try:
        result = subprocess.run(
            ["python", "claude_notify.py", "集成测试", "成功", "飞书通道配置完成"],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            print("[OK] Claude通知脚本执行成功")
            if result.stdout:
                print(f"输出: {result.stdout.strip()}")
        else:
            print(f"[FAIL] Claude通知脚本执行失败")
            if result.stderr:
                print(f"错误: {result.stderr.strip()}")
    except Exception as e:
        print(f"[FAIL] 脚本执行异常: {str(e)}")

if __name__ == "__main__":
    main()