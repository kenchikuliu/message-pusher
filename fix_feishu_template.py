#!/usr/bin/env python3
"""
修复飞书自动化流程的模板配置
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
        print("[OK] 登录成功")
        return session
    else:
        print("登录失败:", result.get('message'))
        return None

def update_feishu_template(session):
    """更新飞书通道模板"""
    print("=== 更新飞书通道模板 ===")

    # 获取现有通道
    response = session.get("http://localhost:3000/api/channel/")
    if not response.ok:
        print("ERROR: 无法获取通道列表")
        return False

    result = response.json()
    if not result.get('success'):
        print("ERROR: 获取通道失败")
        return False

    channels = result.get('data', [])
    feishu_channel = None

    for ch in channels:
        if ch.get('name') == 'feishu' and ch.get('type') == 'custom':
            feishu_channel = ch
            break

    if not feishu_channel:
        print("ERROR: 未找到飞书custom通道")
        return False

    # 创建正确的模板 - 基于测试成功的格式
    feishu_template = '{"text":"$title: $description"}'

    # 更新通道配置
    channel_id = feishu_channel['id']
    update_data = {
        "name": "feishu",
        "type": "custom",
        "description": "飞书自动化流程 - Claude Code提醒",
        "url": "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49",
        "other": feishu_template,  # 关键：设置模板
        "secret": "",
        "status": 1
    }

    print(f"设置模板: {feishu_template}")

    response = session.put(f"http://localhost:3000/api/channel/{channel_id}", json=update_data)

    if response.ok:
        try:
            result = response.json()
            if result.get('success'):
                print("[OK] 飞书模板更新成功")
                return True
            else:
                print("ERROR: 更新失败 -", result.get('message'))
                return False
        except:
            if response.status_code < 300:
                print("[OK] 飞书模板更新成功")
                return True
            else:
                print(f"ERROR: HTTP错误 {response.status_code}")
                return False
    else:
        print(f"ERROR: HTTP错误 {response.status_code}")
        return False

def test_fixed_notification():
    """测试修复后的通知"""
    print("\n=== 测试修复后的通知 ===")

    test_data = {
        "title": "[OK] Claude Code 测试",
        "description": "模板修复测试 - 应该能正常发送到飞书",
        "content": "这是测试修复后的飞书通知功能",
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    try:
        response = requests.post("http://localhost:3000/push/root", json=test_data, timeout=15)

        if response.ok:
            result = response.json()
            if result.get('success'):
                print("[SUCCESS] 通知发送成功!")
                print("请检查飞书是否收到了格式正确的消息")
                return True
            else:
                print(f"[FAIL] 发送失败: {result.get('message')}")
                return False
        else:
            print(f"[FAIL] HTTP错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"[FAIL] 发送异常: {e}")
        return False

def test_multiple_templates():
    """测试多种模板格式"""
    print("\n=== 测试多种模板格式 ===")

    templates = [
        {
            "name": "简单文本模板",
            "template": '{"text":"$title: $description"}'
        },
        {
            "name": "富文本模板",
            "template": '{"text":"Claude Code 通知\\n标题: $title\\n描述: $description\\n内容: $content"}'
        },
        {
            "name": "结构化模板",
            "template": '{"title":"$title","message":"$description","details":"$content"}'
        }
    ]

    session = login()
    if not session:
        return

    for i, template_config in enumerate(templates, 1):
        print(f"\n{i}. 测试 {template_config['name']}:")

        # 获取通道
        response = session.get("http://localhost:3000/api/channel/")
        if response.ok:
            result = response.json()
            if result.get('success'):
                channels = result.get('data', [])
                for ch in channels:
                    if ch.get('name') == 'feishu' and ch.get('type') == 'custom':
                        channel_id = ch['id']

                        # 更新模板
                        update_data = {
                            "name": "feishu",
                            "type": "custom",
                            "description": f"飞书测试 - {template_config['name']}",
                            "url": "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49",
                            "other": template_config['template'],
                            "secret": "",
                            "status": 1
                        }

                        session.put(f"http://localhost:3000/api/channel/{channel_id}", json=update_data)

                        # 测试发送
                        test_data = {
                            "title": f"[TEST{i}] 模板测试",
                            "description": f"测试模板 {template_config['name']}",
                            "content": "这是内容测试",
                            "token": "claude_task_2025",
                            "channel": "feishu"
                        }

                        response = requests.post("http://localhost:3000/push/root", json=test_data, timeout=10)
                        if response.ok:
                            result = response.json()
                            if result.get('success'):
                                print(f"   [OK] {template_config['name']} 发送成功")
                            else:
                                print(f"   [FAIL] {template_config['name']} 失败: {result.get('message')}")
                        break

        import time
        time.sleep(2)  # 间隔测试

def main():
    """主函数"""
    print("=== 修复飞书自动化流程模板 ===")
    print("错误码 10185227 - 修复数据格式问题")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 更新模板
    if update_feishu_template(session):
        print("\n等待3秒让模板生效...")
        import time
        time.sleep(3)

        # 3. 测试修复后的通知
        test_fixed_notification()

        # 4. 如果用户需要，测试多种模板
        print("\n是否测试多种模板格式? (按回车跳过，输入y测试)")
        try:
            choice = input().strip().lower()
            if choice == 'y':
                test_multiple_templates()
        except:
            pass

    print("\n修复完成!")
    print("如果仍有问题，请检查飞书自动化流程的配置")

if __name__ == "__main__":
    main()