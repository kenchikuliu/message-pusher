#!/usr/bin/env python3
"""
修复飞书自动化流程数据格式问题
错误码10185227通常表示数据格式不匹配
"""

import requests
import json
import time

def test_feishu_webhook_formats():
    """测试不同的飞书webhook数据格式"""
    webhook_url = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

    print("=== 测试飞书自动化流程webhook数据格式 ===")
    print(f"Webhook: {webhook_url}")

    # 测试多种数据格式
    test_formats = [
        {
            "name": "格式1: 简单文本",
            "data": {
                "text": "Claude Code 任务完成：代码分析已完成"
            }
        },
        {
            "name": "格式2: 标题+内容",
            "data": {
                "title": "Claude Code 通知",
                "content": "代码分析任务已完成，发现3个优化建议"
            }
        },
        {
            "name": "格式3: 消息结构",
            "data": {
                "message": {
                    "title": "Claude Code 任务完成",
                    "description": "代码分析已完成",
                    "status": "success"
                }
            }
        },
        {
            "name": "格式4: 通用字段",
            "data": {
                "msg_type": "text",
                "content": {
                    "text": "Claude Code 任务完成\n任务：代码分析\n状态：成功\n时间：{time}".format(
                        time=time.strftime('%Y-%m-%d %H:%M:%S')
                    )
                }
            }
        },
        {
            "name": "格式5: 飞书富文本",
            "data": {
                "msg_type": "interactive",
                "card": {
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "content": "**Claude Code 任务完成**\n\n任务：代码分析\n状态：成功完成\n时间：{time}".format(
                                    time=time.strftime('%Y-%m-%d %H:%M:%S')
                                ),
                                "tag": "lark_md"
                            }
                        }
                    ]
                }
            }
        },
        {
            "name": "格式6: 直接字符串",
            "data": "Claude Code 任务完成：代码分析已完成"
        }
    ]

    success_formats = []

    for i, test in enumerate(test_formats, 1):
        print(f"\n{i}. 测试 {test['name']}:")

        try:
            response = requests.post(webhook_url, json=test['data'], timeout=10)

            print(f"   状态码: {response.status_code}")
            print(f"   响应: {response.text}")

            if response.ok:
                response_data = response.json() if response.text else {}
                if response_data.get('code') == 0:
                    print("   ✅ 格式正确!")
                    success_formats.append(test)
                else:
                    print(f"   ❌ 错误码: {response_data.get('code')}")
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")

        except Exception as e:
            print(f"   ❌ 异常: {e}")

        time.sleep(1)  # 避免请求太频繁

    return success_formats

def update_custom_channel_format(session, webhook_url, format_data):
    """更新custom通道的数据格式"""
    print(f"\n=== 更新Message Pusher通道配置 ===")

    # 检查现有通道
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

    # 检查custom通道的模板配置
    print("当前通道配置:")
    print(f"  URL: {feishu_channel.get('url')}")
    print(f"  其他配置: {feishu_channel.get('other', '')}")

    return True

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

def test_simple_notification():
    """测试简单格式的通知"""
    print("\n=== 测试简化格式通知 ===")

    # 使用最简单的格式
    simple_data = {
        "title": "[OK] Claude Code 完成",
        "description": "代码分析任务已完成",
        "content": "任务成功完成，发现3个优化建议",
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    try:
        response = requests.post("http://localhost:3000/push/root", json=simple_data, timeout=10)

        if response.ok:
            result = response.json()
            if result.get('success'):
                print("✅ Message Pusher 发送成功")
                print("请检查飞书是否收到消息")
                return True
            else:
                print(f"❌ Message Pusher 错误: {result.get('message')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def main():
    """主函数"""
    print("=== 修复飞书自动化流程格式问题 ===")
    print("错误码 10185227 通常表示数据格式不匹配")

    # 1. 测试不同的webhook格式
    success_formats = test_feishu_webhook_formats()

    if success_formats:
        print(f"\n✅ 找到 {len(success_formats)} 个有效格式:")
        for fmt in success_formats:
            print(f"  - {fmt['name']}")
    else:
        print("\n❌ 所有格式都失败了")
        print("建议检查飞书自动化流程配置")

    # 2. 登录并检查系统配置
    session = login()
    if session:
        update_custom_channel_format(session,
            "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49",
            success_formats[0] if success_formats else None)

    # 3. 测试系统通知
    test_simple_notification()

    print("\n📋 调试建议:")
    print("1. 检查飞书自动化流程的输入参数配置")
    print("2. 确认webhook触发条件")
    print("3. 查看飞书流程的执行日志")
    print("4. 尝试在飞书中手动测试webhook")

if __name__ == "__main__":
    main()