#!/usr/bin/env python3
"""
配置飞书自动化流程webhook (使用custom通道类型)
"""

import requests
import json
import time

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
        print("[OK] 登录成功")
        return session
    else:
        print("登录失败:", result.get('message'))
        return None

def setup_feishu_flow_webhook(session, webhook_url):
    """设置飞书自动化流程webhook (使用custom类型)"""
    print(f"[INFO] 配置飞书自动化流程webhook")
    print(f"[INFO] URL: {webhook_url}")

    # 先检查是否有现有的飞书通道
    response = session.get("http://localhost:3000/api/channel/")
    if response.ok:
        result = response.json()
        if result.get('success'):
            channels = result.get('data', [])

            # 查找并删除旧的飞书通道
            for ch in channels:
                if ch.get('name') == 'feishu':
                    print(f"[INFO] 删除旧的飞书通道: {ch.get('type')}")
                    session.delete(f"http://localhost:3000/api/channel/{ch.get('id')}")

    # 创建新的custom类型通道用于飞书自动化流程
    channel_data = {
        "name": "feishu",
        "type": "custom",
        "description": "飞书自动化流程 - Claude Code提醒",
        "url": webhook_url,
        "secret": "",
        "status": 1
    }

    response = session.post("http://localhost:3000/api/channel/", json=channel_data)

    if response.ok:
        try:
            result = response.json()
            if result.get('success'):
                print("[OK] 飞书自动化流程通道创建成功")
                return True
            else:
                print("ERROR: 创建失败 -", result.get('message'))
                return False
        except:
            if response.status_code < 300:
                print("[OK] 飞书自动化流程通道创建成功")
                return True
            else:
                print(f"ERROR: HTTP错误 {response.status_code}")
                return False
    else:
        print(f"ERROR: HTTP错误 {response.status_code}")
        return False

def test_feishu_flow_notification():
    """测试飞书自动化流程通知"""
    print("\n=== 测试飞书自动化流程通知 ===")

    # Claude Code完成任务的通知数据
    test_data = {
        "title": "[SUCCESS] Claude Code 任务完成",
        "description": "飞书自动化流程测试 - 代码分析任务已完成",
        "content": """Claude Code 执行报告:

任务: 代码分析和优化
状态: 成功完成
时间: {time}
耗时: 2分30秒

主要成果:
- 发现3个性能优化点
- 修复2个潜在bug
- 代码质量评分: 95/100

来自 Claude Code 自动提醒""".format(time=time.strftime('%Y-%m-%d %H:%M:%S')),
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    try:
        response = requests.post("http://localhost:3000/push/root", json=test_data, timeout=15)

        if response.ok:
            result = response.json()
            if result.get('success'):
                print("[SUCCESS] 飞书自动化流程通知发送成功!")
                print("请检查您的飞书，应该能看到Claude Code完成通知")
                return True
            else:
                print(f"[INFO] 通知结果: {result.get('message')}")
                return False
        else:
            print(f"[FAIL] HTTP错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"[FAIL] 发送异常: {e}")
        return False

def test_direct_webhook():
    """直接测试webhook地址"""
    print("\n=== 直接测试webhook地址 ===")

    webhook_url = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

    # 构建测试数据
    test_payload = {
        "title": "Claude Code 测试",
        "message": "这是来自Claude Code的测试消息",
        "status": "success",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        print(f"[INFO] 直接POST到: {webhook_url}")
        response = requests.post(webhook_url, json=test_payload, timeout=10)

        print(f"[INFO] 响应状态: {response.status_code}")
        print(f"[INFO] 响应内容: {response.text}")

        if response.ok:
            print("[SUCCESS] 直接webhook调用成功!")
            return True
        else:
            print(f"[FAIL] webhook调用失败: {response.status_code}")
            return False

    except Exception as e:
        print(f"[FAIL] webhook调用异常: {e}")
        return False

def main():
    """主函数"""
    print("=== 配置飞书自动化流程Webhook ===")

    webhook_url = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

    print(f"飞书自动化流程Webhook: {webhook_url}")
    print("用途: Claude Code任务完成提醒")

    # 1. 直接测试webhook
    print("\n1. 直接测试webhook地址:")
    test_direct_webhook()

    # 2. 登录并配置系统
    print("\n2. 配置Message Pusher系统:")
    session = login()
    if not session:
        return

    # 3. 设置飞书自动化流程webhook
    if setup_feishu_flow_webhook(session, webhook_url):
        print("\n等待3秒让配置生效...")
        time.sleep(3)

        # 4. 测试系统通知
        print("\n3. 测试系统通知:")
        test_feishu_flow_notification()

    print("\n配置完成!")
    print("现在您可以在Claude Code中使用:")
    print("  python claude_notify.py \"任务名\" \"状态\" \"详情\"")

if __name__ == "__main__":
    main()