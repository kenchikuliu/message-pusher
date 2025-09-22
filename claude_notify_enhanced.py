#!/usr/bin/env python3
"""
Claude Code 增强任务完成提醒脚本
用法: python claude_notify_enhanced.py [任务名称] [任务类型] [状态] [执行内容] [详细信息]
"""

import requests
import sys
import json
import os
from datetime import datetime

# 配置 - 您的飞书 Webhook URL
FEISHU_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/5f57f0a2814076ad7e269d09f56e0ad2"

# 任务类型图标映射
TASK_TYPE_ICONS = {
    "代码分析": "🔍",
    "代码生成": "✨",
    "代码重构": "🔧",
    "bug修复": "🐛",
    "测试": "🧪",
    "部署": "🚀",
    "文档": "📝",
    "数据处理": "📊",
    "文件操作": "📁",
    "网络请求": "🌐",
    "数据库": "🗃️",
    "AI训练": "🤖",
    "脚本执行": "⚡",
    "系统配置": "⚙️",
    "安全检查": "🔒",
    "性能优化": "⚡",
    "其他": "🔖"
}

def get_task_icon(task_type):
    """获取任务类型对应的图标"""
    return TASK_TYPE_ICONS.get(task_type, "🔖")

def get_status_info(status):
    """获取状态信息"""
    status_lower = status.lower()
    if "完成" in status or "成功" in status or "success" in status_lower:
        return "✅", "green"
    elif "失败" in status or "错误" in status or "error" in status_lower or "fail" in status_lower:
        return "❌", "red"
    elif "进行" in status or "运行" in status or "执行" in status or "running" in status_lower:
        return "🔄", "blue"
    elif "警告" in status or "warning" in status_lower:
        return "⚠️", "orange"
    else:
        return "📋", "blue"

def send_enhanced_feishu_notification(task_name, task_type="其他", status="完成", execution_details="", additional_info="", duration=""):
    """发送增强的飞书通知"""

    task_icon = get_task_icon(task_type)
    status_icon, card_color = get_status_info(status)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构建卡片内容
    card_content = f"**{task_icon} 任务名称**: {task_name}\n"
    card_content += f"**🏷️ 任务类型**: {task_type}\n"
    card_content += f"**{status_icon} 执行状态**: {status}\n"
    card_content += f"**⏰ 完成时间**: {current_time}\n"

    if duration:
        card_content += f"**⏱️ 执行时长**: {duration}\n"

    if execution_details:
        card_content += f"\n**🔧 Claude Code 执行内容**:\n{execution_details}\n"

    if additional_info:
        card_content += f"\n**📝 详细信息**:\n{additional_info}\n"

    # 添加环境信息
    try:
        current_dir = os.getcwd()
        card_content += f"\n**📁 工作目录**: `{current_dir}`\n"
    except:
        pass

    card_content += "\n---\n_🤖 来自 Claude Code 自动提醒系统_"

    # 飞书卡片消息格式
    card_data = {
        "msg_type": "interactive",
        "card": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": card_content,
                        "tag": "lark_md"
                    }
                }
            ],
            "header": {
                "title": {
                    "content": f"{task_icon} Claude Code - {task_name}",
                    "tag": "plain_text"
                },
                "template": card_color
            }
        }
    }

    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=card_data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"SUCCESS: 增强提醒发送成功 - {task_name} ({task_type})")
                return True
            else:
                print(f"ERROR: 飞书API错误 - {result.get('msg', '未知错误')}")
                return False
        else:
            print(f"ERROR: HTTP错误 - {response.status_code}")
            return False

    except Exception as e:
        print(f"ERROR: 发送失败 - {str(e)}")
        # 尝试发送简化版本
        return send_simple_notification(task_name, task_type, status, execution_details, additional_info)

def send_simple_notification(task_name, task_type="其他", status="完成", execution_details="", additional_info=""):
    """发送简化的文本通知（备用）"""

    task_icon = get_task_icon(task_type)
    status_icon, _ = get_status_info(status)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    message_text = f"{task_icon} Claude Code 任务报告\n\n"
    message_text += f"任务: {task_name}\n"
    message_text += f"类型: {task_type}\n"
    message_text += f"状态: {status_icon} {status}\n"
    message_text += f"时间: {current_time}\n"

    if execution_details:
        message_text += f"\nClaude Code 执行:\n{execution_details}\n"

    if additional_info:
        message_text += f"\n详细信息:\n{additional_info}\n"

    message_text += "\n---\n来自 Claude Code 自动提醒"

    feishu_data = {
        "msg_type": "text",
        "content": {
            "text": message_text
        }
    }

    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=feishu_data, timeout=10)
        if response.status_code == 200 and response.json().get('code') == 0:
            print(f"SUCCESS: 简化提醒发送成功 - {task_name}")
            return True
    except:
        pass

    return False

# 预定义常用任务场景
def notify_code_analysis(files_analyzed=0, issues_found=0, duration="", additional_info=""):
    """代码分析完成通知"""
    execution_details = f"分析了 {files_analyzed} 个文件"
    if issues_found > 0:
        execution_details += f"，发现 {issues_found} 个潜在问题"
    else:
        execution_details += "，未发现问题"

    return send_enhanced_feishu_notification(
        "代码质量分析", "代码分析", "完成",
        execution_details, additional_info, duration
    )

def notify_code_generation(files_created=0, lines_generated=0, duration="", additional_info=""):
    """代码生成完成通知"""
    execution_details = f"生成了 {files_created} 个文件，共 {lines_generated} 行代码"

    return send_enhanced_feishu_notification(
        "代码自动生成", "代码生成", "完成",
        execution_details, additional_info, duration
    )

def notify_bug_fix(bugs_fixed=0, files_modified=0, duration="", additional_info=""):
    """Bug修复完成通知"""
    execution_details = f"修复了 {bugs_fixed} 个问题，修改了 {files_modified} 个文件"

    return send_enhanced_feishu_notification(
        "Bug修复任务", "bug修复", "完成",
        execution_details, additional_info, duration
    )

def notify_test_execution(tests_run=0, tests_passed=0, duration="", additional_info=""):
    """测试执行完成通知"""
    tests_failed = tests_run - tests_passed
    status = "完成" if tests_failed == 0 else f"完成({tests_failed}个失败)"
    execution_details = f"运行了 {tests_run} 个测试，{tests_passed} 个通过"
    if tests_failed > 0:
        execution_details += f"，{tests_failed} 个失败"

    return send_enhanced_feishu_notification(
        "自动化测试", "测试", status,
        execution_details, additional_info, duration
    )

def notify_deployment(environment="", services_deployed=0, duration="", additional_info=""):
    """部署完成通知"""
    execution_details = f"部署到 {environment} 环境"
    if services_deployed > 0:
        execution_details += f"，部署了 {services_deployed} 个服务"

    return send_enhanced_feishu_notification(
        "应用部署", "部署", "完成",
        execution_details, additional_info, duration
    )

def main():
    """命令行入口"""
    if len(sys.argv) == 1:
        # 默认测试通知
        send_enhanced_feishu_notification(
            "Claude Code 测试", "系统配置", "完成",
            "成功配置增强提醒系统", "支持任务类型、执行内容等详细信息"
        )
    elif len(sys.argv) == 2:
        # 简单任务名称
        send_enhanced_feishu_notification(sys.argv[1])
    elif len(sys.argv) == 3:
        # 任务名称 + 类型 或 任务名称 + 状态
        send_enhanced_feishu_notification(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        # 任务名称 + 类型 + 状态
        send_enhanced_feishu_notification(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        # 任务名称 + 类型 + 状态 + 执行内容
        send_enhanced_feishu_notification(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) >= 6:
        # 完整参数
        task_name = sys.argv[1]
        task_type = sys.argv[2]
        status = sys.argv[3]
        execution_details = sys.argv[4]
        additional_info = sys.argv[5]
        duration = sys.argv[6] if len(sys.argv) > 6 else ""
        send_enhanced_feishu_notification(task_name, task_type, status, execution_details, additional_info, duration)

if __name__ == "__main__":
    main()