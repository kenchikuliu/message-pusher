#!/usr/bin/env python3
"""
测试Claude Code集成 - 模拟Claude Code任务完成后的webhook调用
"""

import requests
import json
from datetime import datetime
import subprocess
import sys

def test_notification_api():
    """测试通知API的基本功能"""
    print("=== 测试通知API基本功能 ===")

    # 测试数据
    test_data = {
        "title": "[TEST] Claude Code 任务完成",
        "description": "模拟测试：代码分析任务已完成",
        "content": """**🤖 Claude Code 执行报告**

- **任务**: 代码分析和重构
- **状态**: 成功完成
- **完成时间**: {time}
- **耗时**: 2分30秒
- **详情**: 成功优化了3个函数，修复了2个潜在bug

### 主要改进:
1. ✅ 优化了数据库查询性能
2. ✅ 修复了内存泄漏问题
3. ✅ 添加了错误处理机制

---
_🔔 来自 Claude Code 自动提醒_""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "token": "claude_task_2025"
    }

    try:
        print("发送测试通知...")
        response = requests.post("http://localhost:3000/push/root", json=test_data, timeout=10)
        result = response.json()

        if result.get('success'):
            print("[OK] SUCCESS: 通知API测试成功")
            print(f"   消息ID: {result.get('data', {}).get('id', 'N/A')}")
            return True
        else:
            print(f"[FAIL] ERROR: 通知发送失败 - {result.get('message')}")
            return False

    except Exception as e:
        print(f"[FAIL] ERROR: API调用异常 - {str(e)}")
        return False

def test_claude_notify_script():
    """测试claude_notify.py脚本"""
    print("\n=== 测试Claude通知脚本 ===")

    try:
        # 测试不同的调用方式
        test_cases = [
            # 简单通知
            ["python", "claude_notify.py", "代码审查完成"],
            # 任务状态通知
            ["python", "claude_notify.py", "数据库迁移", "成功完成"],
            # 完整通知
            ["python", "claude_notify.py", "前端构建", "完成", "构建了React应用，生成了生产包", "3分45秒"]
        ]

        for i, cmd in enumerate(test_cases, 1):
            print(f"\n测试用例 {i}: {' '.join(cmd[2:])}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    print(f"[OK] 脚本执行成功")
                    if result.stdout:
                        print(f"   输出: {result.stdout.strip()}")
                else:
                    print(f"[FAIL] 脚本执行失败 (退出码: {result.returncode})")
                    if result.stderr:
                        print(f"   错误: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                print(f"[FAIL] 脚本执行超时")
            except Exception as e:
                print(f"[FAIL] 脚本执行异常: {str(e)}")

        return True

    except Exception as e:
        print(f"[FAIL] ERROR: 脚本测试异常 - {str(e)}")
        return False

def simulate_claude_code_webhook():
    """模拟Claude Code完成任务后的webhook回调"""
    print("\n=== 模拟Claude Code Webhook ===")

    # 模拟不同类型的Claude Code任务完成事件
    webhook_events = [
        {
            "event": "task_completed",
            "task_type": "code_review",
            "task_name": "Python代码审查",
            "status": "success",
            "duration": "1m 45s",
            "details": "审查了5个文件，发现3个改进建议",
            "files_processed": 5,
            "suggestions": 3
        },
        {
            "event": "task_completed",
            "task_type": "refactoring",
            "task_name": "API接口重构",
            "status": "success",
            "duration": "4m 12s",
            "details": "重构了用户认证模块，提升了性能",
            "files_changed": 8,
            "performance_improvement": "35%"
        },
        {
            "event": "task_failed",
            "task_type": "testing",
            "task_name": "自动化测试",
            "status": "failed",
            "duration": "30s",
            "details": "测试配置错误，无法连接数据库",
            "error": "Connection refused: database not available"
        }
    ]

    success_count = 0

    for i, event in enumerate(webhook_events, 1):
        print(f"\n处理事件 {i}: {event['task_name']}")

        # 根据事件构建通知内容
        if event['status'] == 'success':
            icon = "[OK]"
            status_text = "成功完成"
        else:
            icon = "[FAIL]"
            status_text = "执行失败"

        # 构建详细内容
        content_parts = [
            f"**Claude Code 执行报告**\n",
            f"- **任务类型**: {event['task_type']}",
            f"- **任务名称**: {event['task_name']}",
            f"- **执行状态**: {status_text}",
            f"- **完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **执行耗时**: {event['duration']}",
            f"- **详细信息**: {event['details']}"
        ]

        # 添加特定字段
        if event['status'] == 'success':
            if 'files_processed' in event:
                content_parts.append(f"- **处理文件**: {event['files_processed']} 个")
            if 'suggestions' in event:
                content_parts.append(f"- **改进建议**: {event['suggestions']} 条")
            if 'files_changed' in event:
                content_parts.append(f"- **修改文件**: {event['files_changed']} 个")
            if 'performance_improvement' in event:
                content_parts.append(f"- **性能提升**: {event['performance_improvement']}")
        else:
            if 'error' in event:
                content_parts.append(f"- **错误信息**: `{event['error']}`")

        content_parts.append("\n---\n_来自 Claude Code Webhook 自动提醒_")
        content = "\n".join(content_parts)

        # 发送通知
        notification_data = {
            "title": f"{icon} {event['task_name']}",
            "description": f"{event['task_type']} - {status_text}",
            "content": content,
            "token": "claude_task_2025"
        }

        try:
            response = requests.post("http://localhost:3000/push/root", json=notification_data, timeout=10)
            result = response.json()

            if result.get('success'):
                print(f"[OK] Webhook事件处理成功")
                success_count += 1
            else:
                print(f"[FAIL] Webhook事件处理失败: {result.get('message')}")

        except Exception as e:
            print(f"[FAIL] Webhook调用异常: {str(e)}")

    print(f"\n[OK] Webhook测试完成: {success_count}/{len(webhook_events)} 成功")
    return success_count == len(webhook_events)

def main():
    """主测试函数"""
    print("Claude Code + Message Pusher 集成测试")
    print("=" * 50)

    test_results = []

    # 1. 测试基本API
    test_results.append(("API基本功能", test_notification_api()))

    # 2. 测试Claude通知脚本
    test_results.append(("Claude通知脚本", test_claude_notify_script()))

    # 3. 模拟Webhook集成
    test_results.append(("Webhook集成", simulate_claude_code_webhook()))

    # 总结测试结果
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print("=" * 50)

    success_count = 0
    for test_name, result in test_results:
        status = "[OK] 通过" if result else "[FAIL] 失败"
        print(f"{status} {test_name}")
        if result:
            success_count += 1

    print(f"\n总体结果: {success_count}/{len(test_results)} 项测试通过")

    if success_count == len(test_results):
        print("\n恭喜！Claude Code集成测试全部通过!")
        print("现在您可以在Claude Code完成任务后收到飞书通知了！")
    else:
        print(f"\n有 {len(test_results) - success_count} 项测试失败，请检查配置")

    return success_count == len(test_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)