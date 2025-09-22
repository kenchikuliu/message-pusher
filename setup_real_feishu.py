#!/usr/bin/env python3
"""
配置真实的飞书webhook并测试Claude Code集成
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

def update_feishu_webhook(session, webhook_url):
    """更新飞书webhook地址"""
    print(f"[INFO] 更新飞书webhook: {webhook_url}")

    # 先获取现有通道
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
        if ch.get('type') == 'lark' and ch.get('name') == 'feishu':
            feishu_channel = ch
            break

    if feishu_channel:
        # 更新现有通道
        channel_id = feishu_channel['id']
        update_data = {
            "name": "feishu",
            "type": "lark",
            "description": "飞书Claude Code提醒",
            "url": webhook_url,
            "secret": "",  # 飞书webhook通常不需要secret
            "status": 1
        }

        response = session.put(f"http://localhost:3000/api/channel/{channel_id}", json=update_data)

        if response.ok:
            print("[OK] 飞书webhook更新成功")
            return True
        else:
            print(f"ERROR: 更新失败 {response.status_code}")
            return False
    else:
        # 创建新通道
        channel_data = {
            "name": "feishu",
            "type": "lark",
            "description": "飞书Claude Code提醒",
            "url": webhook_url,
            "secret": "",
            "status": 1
        }

        response = session.post("http://localhost:3000/api/channel/", json=channel_data)
        result = response.json()

        if result.get('success'):
            print("[OK] 飞书通道创建成功")
            return True
        else:
            print("ERROR: 创建失败 -", result.get('message'))
            return False

def test_claude_code_notification():
    """测试Claude Code完成通知"""
    print("\n=== 测试Claude Code完成通知 ===")

    # 模拟Claude Code任务完成的通知
    test_data = {
        "title": "[SUCCESS] Claude Code 任务完成",
        "description": "飞书集成测试 - 代码分析任务已完成",
        "content": """**🤖 Claude Code 执行报告**

- **任务类型**: 代码分析和优化
- **执行状态**: 成功完成
- **完成时间**: {time}
- **执行耗时**: 2分30秒
- **处理文件**: 8个Python文件

### 主要成果:
✅ 发现3个性能优化点
✅ 修复2个潜在bug
✅ 代码质量评分: 95/100
✅ 测试覆盖率: 89%

### 优化建议:
1. 数据库查询优化 - 预计提升30%性能
2. 内存使用优化 - 减少15%内存占用
3. 错误处理增强 - 提升系统稳定性

---
_🔔 来自 Claude Code 自动提醒_""".format(time=time.strftime('%Y-%m-%d %H:%M:%S')),
        "token": "claude_task_2025",
        "channel": "feishu"
    }

    try:
        response = requests.post("http://localhost:3000/push/root", json=test_data, timeout=15)

        if response.ok:
            result = response.json()
            if result.get('success'):
                print("🎉 [SUCCESS] 飞书通知发送成功!")
                print("请检查您的飞书群，应该能看到Claude Code完成通知")
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

def test_multiple_scenarios():
    """测试多种Claude Code场景"""
    print("\n=== 测试多种Claude Code场景 ===")

    scenarios = [
        {
            "title": "[OK] 单元测试完成",
            "task": "单元测试执行",
            "status": "全部通过",
            "details": "执行了156个测试用例，全部通过，覆盖率93%",
            "duration": "45秒"
        },
        {
            "title": "[WARN] 代码审查发现问题",
            "task": "代码质量检查",
            "status": "发现问题",
            "details": "发现5个代码质量问题，2个安全隐患，已生成修复建议",
            "duration": "1分20秒"
        },
        {
            "title": "[INFO] 文档生成完成",
            "task": "API文档自动生成",
            "status": "成功完成",
            "details": "生成了完整的API文档，包含23个接口的详细说明",
            "duration": "30秒"
        }
    ]

    success_count = 0

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. 发送场景: {scenario['task']}")

        notification_data = {
            "title": scenario['title'],
            "description": f"Claude Code: {scenario['task']} - {scenario['status']}",
            "content": f"""**Claude Code 任务报告**

- **任务**: {scenario['task']}
- **状态**: {scenario['status']}
- **详情**: {scenario['details']}
- **耗时**: {scenario['duration']}
- **时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}

---
_🔔 Claude Code 自动提醒_""",
            "token": "claude_task_2025",
            "channel": "feishu"
        }

        try:
            response = requests.post("http://localhost:3000/push/root", json=notification_data, timeout=10)

            if response.ok:
                result = response.json()
                if result.get('success'):
                    print(f"   ✅ 发送成功")
                    success_count += 1
                else:
                    print(f"   ❌ 发送失败: {result.get('message')}")
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")

        except Exception as e:
            print(f"   ❌ 异常: {e}")

        time.sleep(2)  # 避免发送太频繁

    print(f"\n📊 场景测试完成: {success_count}/{len(scenarios)} 成功")

def main():
    """主函数"""
    print("=== 配置真实飞书Webhook并测试Claude Code集成 ===")

    # 飞书webhook地址
    webhook_url = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

    print(f"飞书Webhook: {webhook_url}")
    print("用途: Claude Code任务完成提醒")

    # 1. 登录
    session = login()
    if not session:
        return

    # 2. 更新飞书webhook
    if update_feishu_webhook(session, webhook_url):
        print("\n等待3秒让配置生效...")
        time.sleep(3)

        # 3. 测试通知
        if test_claude_code_notification():
            # 4. 测试多种场景
            print("\n继续测试多种场景? (按回车继续，Ctrl+C取消)")
            try:
                input()
                test_multiple_scenarios()
            except KeyboardInterrupt:
                print("\n用户取消")

        print("\n🎉 飞书集成配置完成!")
        print("现在您可以在Claude Code中使用:")
        print("  python claude_notify.py \"任务名\" \"状态\" \"详情\"")
        print("\n每次Claude Code完成任务都会发送到您的飞书群! 🚀")

if __name__ == "__main__":
    main()