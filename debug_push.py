#!/usr/bin/env python3
"""
调试推送配置
"""

import requests
import json

# 配置
SERVER_URL = "http://localhost:3000"
USERNAME = "root"
PASSWORD = "123456"

def test_push_with_explicit_channel():
    """使用明确指定通道进行推送测试"""

    # 测试数据，明确指定使用飞书通道
    test_data = {
        "title": "[DEBUG] 明确指定通道测试",
        "description": "使用飞书通道推送",
        "content": "这是通过明确指定飞书通道的测试消息",
        "token": "claude_task_2025",
        "channel": "feishu"  # 明确指定通道名称
    }

    print("测试数据:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)

    print(f"\n响应状态码: {response.status_code}")
    print("响应内容:")
    try:
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_push_without_channel():
    """不指定通道的推送测试（依赖默认通道）"""

    test_data = {
        "title": "[DEBUG] 默认通道测试",
        "description": "使用默认通道推送",
        "content": "这是使用默认通道的测试消息",
        "token": "claude_task_2025"
        # 不指定 channel，使用默认通道
    }

    print("测试数据:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))

    response = requests.post(f"{SERVER_URL}/push/{USERNAME}", json=test_data)

    print(f"\n响应状态码: {response.status_code}")
    print("响应内容:")
    try:
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def main():
    print("=== 推送配置调试 ===")

    print("\n1. 测试明确指定飞书通道的推送:")
    test_push_with_explicit_channel()

    print("\n" + "="*50)
    print("\n2. 测试使用默认通道的推送:")
    test_push_without_channel()

if __name__ == "__main__":
    main()