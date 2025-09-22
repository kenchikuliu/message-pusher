#!/usr/bin/env python3
"""
Claude Code 智能任务检测提醒脚本
自动识别任务类型和执行内容
用法: python claude_notify_smart.py [任务描述] [状态] [详细信息]
"""

import requests
import sys
import json
import os
import re
from datetime import datetime

# 配置
FEISHU_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/5f57f0a2814076ad7e269d09f56e0ad2"

# 智能任务类型检测规则
TASK_DETECTION_RULES = {
    "代码分析": {
        "keywords": ["分析", "检查", "扫描", "review", "analyze", "inspect", "lint", "audit"],
        "file_patterns": [".py", ".js", ".java", ".cpp", ".go", ".rs"],
        "icon": "🔍"
    },
    "代码生成": {
        "keywords": ["生成", "创建", "generate", "create", "build", "构建", "编写"],
        "file_patterns": [".py", ".js", ".java", ".cpp", ".go", ".rs", ".html", ".css"],
        "icon": "✨"
    },
    "代码重构": {
        "keywords": ["重构", "优化", "refactor", "optimize", "improve", "修改", "更新"],
        "file_patterns": [".py", ".js", ".java", ".cpp", ".go", ".rs"],
        "icon": "🔧"
    },
    "bug修复": {
        "keywords": ["修复", "fix", "bug", "错误", "问题", "解决", "repair"],
        "icon": "🐛"
    },
    "测试": {
        "keywords": ["测试", "test", "验证", "verify", "check", "单元测试", "集成测试"],
        "file_patterns": ["test_", "_test.", "spec_", ".spec.", ".test."],
        "icon": "🧪"
    },
    "部署": {
        "keywords": ["部署", "deploy", "发布", "release", "上线", "publish"],
        "file_patterns": ["docker", "k8s", "yaml", "yml"],
        "icon": "🚀"
    },
    "文档": {
        "keywords": ["文档", "说明", "doc", "readme", "guide", "manual"],
        "file_patterns": [".md", ".txt", ".doc", ".pdf"],
        "icon": "📝"
    },
    "数据处理": {
        "keywords": ["数据", "处理", "分析", "data", "process", "analyze", "ETL", "清洗"],
        "file_patterns": [".csv", ".json", ".xml", ".sql"],
        "icon": "📊"
    },
    "文件操作": {
        "keywords": ["文件", "目录", "file", "folder", "copy", "move", "delete", "批量"],
        "icon": "📁"
    },
    "网络请求": {
        "keywords": ["API", "请求", "调用", "http", "rest", "接口", "网络"],
        "icon": "🌐"
    },
    "数据库": {
        "keywords": ["数据库", "database", "SQL", "查询", "migration", "迁移"],
        "file_patterns": [".sql", "migration"],
        "icon": "🗃️"
    },
    "AI训练": {
        "keywords": ["训练", "模型", "AI", "机器学习", "train", "model", "neural", "深度学习"],
        "icon": "🤖"
    },
    "脚本执行": {
        "keywords": ["脚本", "执行", "运行", "script", "run", "execute", "自动化"],
        "file_patterns": [".sh", ".bat", ".ps1"],
        "icon": "⚡"
    },
    "系统配置": {
        "keywords": ["配置", "设置", "config", "setup", "install", "环境"],
        "file_patterns": ["config", ".env", ".ini", ".conf"],
        "icon": "⚙️"
    },
    "安全检查": {
        "keywords": ["安全", "漏洞", "security", "vulnerability", "检测", "扫描"],
        "icon": "🔒"
    },
    "性能优化": {
        "keywords": ["性能", "优化", "performance", "optimize", "加速", "提升"],
        "icon": "⚡"
    }
}

def detect_task_type(description, current_dir=None):
    """智能检测任务类型"""

    description_lower = description.lower()
    scores = {}

    # 基于关键词检测
    for task_type, rules in TASK_DETECTION_RULES.items():
        score = 0

        # 检查关键词
        for keyword in rules["keywords"]:
            if keyword.lower() in description_lower:
                score += 2

        # 检查文件模式（如果提供了当前目录）
        if current_dir and "file_patterns" in rules:
            try:
                for root, dirs, files in os.walk(current_dir):
                    for file in files:
                        for pattern in rules["file_patterns"]:
                            if pattern in file.lower():
                                score += 1
                    # 只检查一层避免太慢
                    break
            except:
                pass

        if score > 0:
            scores[task_type] = score

    # 返回得分最高的任务类型
    if scores:
        best_type = max(scores.items(), key=lambda x: x[1])[0]
        return best_type

    return "其他"

def extract_execution_details(description, task_type):
    """提取执行详情"""

    details = []
    description_lower = description.lower()

    # 数字提取模式
    numbers = re.findall(r'\d+', description)

    if task_type == "代码分析":
        if "文件" in description and numbers:
            details.append(f"分析了 {numbers[0]} 个文件")
        if "问题" in description or "错误" in description:
            if len(numbers) > 1:
                details.append(f"发现 {numbers[1]} 个问题")

    elif task_type == "代码生成":
        if "文件" in description and numbers:
            details.append(f"生成了 {numbers[0]} 个文件")
        if "行" in description and len(numbers) > 1:
            details.append(f"共 {numbers[1]} 行代码")

    elif task_type == "测试":
        if "测试" in description and numbers:
            details.append(f"运行了 {numbers[0]} 个测试")
            if len(numbers) > 1:
                details.append(f"{numbers[1]} 个通过")

    elif task_type == "数据处理":
        if numbers:
            details.append(f"处理了 {numbers[0]} 条数据")

    elif task_type == "文件操作":
        if numbers:
            details.append(f"处理了 {numbers[0]} 个文件")

    # 如果没有提取到具体细节，使用原始描述
    if not details:
        details.append(description)

    return "，".join(details)

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

def send_smart_notification(description, status="完成", additional_info="", duration=""):
    """发送智能检测的通知"""

    # 获取当前工作目录
    try:
        current_dir = os.getcwd()
    except:
        current_dir = None

    # 智能检测任务类型
    task_type = detect_task_type(description, current_dir)
    task_icon = TASK_DETECTION_RULES.get(task_type, {}).get("icon", "🔖")

    # 提取执行详情
    execution_details = extract_execution_details(description, task_type)

    # 获取状态信息
    status_icon, card_color = get_status_info(status)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构建卡片内容
    card_content = f"**{task_icon} 任务描述**: {description}\n"
    card_content += f"**🏷️ 智能识别类型**: {task_type}\n"
    card_content += f"**{status_icon} 执行状态**: {status}\n"
    card_content += f"**⏰ 完成时间**: {current_time}\n"

    if duration:
        card_content += f"**⏱️ 执行时长**: {duration}\n"

    card_content += f"\n**🔧 Claude Code 执行内容**:\n{execution_details}\n"

    if additional_info:
        card_content += f"\n**📝 详细信息**:\n{additional_info}\n"

    if current_dir:
        card_content += f"\n**📁 工作目录**: `{current_dir}`\n"

    card_content += "\n---\n_🤖 来自 Claude Code 智能提醒系统_"

    # 飞书卡片消息
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
                    "content": f"{task_icon} Claude Code 智能识别 - {task_type}",
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
                print(f"SUCCESS: 智能提醒发送成功 - {description} (识别为: {task_type})")
                return True
            else:
                print(f"ERROR: 飞书API错误 - {result.get('msg', '未知错误')}")
        else:
            print(f"ERROR: HTTP错误 - {response.status_code}")

    except Exception as e:
        print(f"ERROR: 发送失败 - {str(e)}")

    return False

def main():
    """命令行入口"""
    if len(sys.argv) == 1:
        # 默认测试
        send_smart_notification("分析了50个Python文件，发现3个性能问题", "完成", "代码质量整体良好")
    elif len(sys.argv) == 2:
        # 只有描述
        send_smart_notification(sys.argv[1])
    elif len(sys.argv) == 3:
        # 描述 + 状态
        send_smart_notification(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        # 描述 + 状态 + 详细信息
        send_smart_notification(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 5:
        # 完整参数
        send_smart_notification(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    main()