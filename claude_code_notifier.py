#!/usr/bin/env python3
"""
Claude Code 完整任务提醒系统
集成智能检测、详细信息和多种使用方式

用法:
1. 智能模式: python claude_code_notifier.py "任务描述" [状态] [详细信息] [时长]
2. 手动模式: python claude_code_notifier.py --manual "任务名" "类型" "状态" "执行内容" [详细信息] [时长]
3. 快速模式: python claude_code_notifier.py --quick "简短描述"
"""

import requests
import sys
import json
import os
import re
import argparse
from datetime import datetime

# 配置 - 使用 Message Pusher API
MESSAGE_PUSHER_API = "http://localhost:3000/push/root"
CLAUDE_TASK_TOKEN = "claude_task_2025"
FEISHU_CHANNEL = "feishu"

# 任务类型配置
TASK_TYPES = {
    "代码分析": {"icon": "🔍", "keywords": ["分析", "检查", "扫描", "review", "analyze", "inspect", "lint", "audit"]},
    "代码生成": {"icon": "✨", "keywords": ["生成", "创建", "generate", "create", "build", "构建", "编写"]},
    "代码重构": {"icon": "🔧", "keywords": ["重构", "优化", "refactor", "optimize", "improve", "修改", "更新"]},
    "bug修复": {"icon": "🐛", "keywords": ["修复", "fix", "bug", "错误", "问题", "解决", "repair"]},
    "测试": {"icon": "🧪", "keywords": ["测试", "test", "验证", "verify", "check", "单元测试", "集成测试"]},
    "部署": {"icon": "🚀", "keywords": ["部署", "deploy", "发布", "release", "上线", "publish"]},
    "文档": {"icon": "📝", "keywords": ["文档", "说明", "doc", "readme", "guide", "manual"]},
    "数据处理": {"icon": "📊", "keywords": ["数据", "处理", "分析", "data", "process", "analyze", "ETL", "清洗"]},
    "文件操作": {"icon": "📁", "keywords": ["文件", "目录", "file", "folder", "copy", "move", "delete", "批量"]},
    "网络请求": {"icon": "🌐", "keywords": ["API", "请求", "调用", "http", "rest", "接口", "网络"]},
    "数据库": {"icon": "🗃️", "keywords": ["数据库", "database", "SQL", "查询", "migration", "迁移"]},
    "AI训练": {"icon": "🤖", "keywords": ["训练", "模型", "AI", "机器学习", "train", "model", "neural", "深度学习"]},
    "脚本执行": {"icon": "⚡", "keywords": ["脚本", "执行", "运行", "script", "run", "execute", "自动化"]},
    "系统配置": {"icon": "⚙️", "keywords": ["配置", "设置", "config", "setup", "install", "环境"]},
    "安全检查": {"icon": "🔒", "keywords": ["安全", "漏洞", "security", "vulnerability", "检测", "扫描"]},
    "性能优化": {"icon": "⚡", "keywords": ["性能", "优化", "performance", "optimize", "加速", "提升"]},
    "其他": {"icon": "🔖", "keywords": []}
}

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

def detect_task_type(description):
    """智能检测任务类型"""
    description_lower = description.lower()
    scores = {}

    for task_type, config in TASK_TYPES.items():
        score = 0
        for keyword in config["keywords"]:
            if keyword.lower() in description_lower:
                score += 1
        if score > 0:
            scores[task_type] = score

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return "其他"

def extract_numbers_and_context(text):
    """提取文本中的数字和上下文"""
    pattern = r'(\d+)\s*([^，。,.\n]*?)(?:[，。,.\n]|$)'
    matches = re.findall(pattern, text)
    return [(int(num), context.strip()) for num, context in matches]

def generate_execution_summary(description, task_type):
    """生成执行摘要"""
    numbers_context = extract_numbers_and_context(description)

    if task_type == "代码分析" and numbers_context:
        for num, context in numbers_context:
            if "文件" in context:
                return f"分析了 {num} 个文件"
    elif task_type == "代码生成" and numbers_context:
        for num, context in numbers_context:
            if "文件" in context or "接口" in context:
                return f"生成了 {num} 个{'接口' if '接口' in context else '文件'}"
    elif task_type == "测试" and numbers_context:
        for num, context in numbers_context:
            if "测试" in context:
                return f"运行了 {num} 个测试"

    # 如果无法智能提取，返回原描述的关键部分
    if len(description) > 50:
        return description[:50] + "..."
    return description

def send_notification(task_name, task_type="其他", status="完成", execution_details="", additional_info="", duration="", mode="smart"):
    """发送通知"""

    # 如果是智能模式，进行智能检测
    if mode == "smart" and task_type == "其他":
        task_type = detect_task_type(task_name)

    # 如果没有执行详情，尝试生成
    if not execution_details and mode == "smart":
        execution_details = generate_execution_summary(task_name, task_type)

    task_icon = TASK_TYPES.get(task_type, TASK_TYPES["其他"])["icon"]
    status_icon, card_color = get_status_info(status)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 构建消息标题
    title = f"[{status_icon}] {task_icon} {task_name}"

    # 构建详细描述
    description = f"Claude Code {mode.title()} - {task_type}"
    if execution_details:
        description += f" | {execution_details}"

    # 构建详细内容
    content_parts = []
    content_parts.append(f"任务类型: {task_type}")
    content_parts.append(f"状态: {status}")
    content_parts.append(f"时间: {current_time}")

    if duration:
        content_parts.append(f"耗时: {duration}")

    if execution_details:
        content_parts.append(f"执行内容: {execution_details}")

    if additional_info:
        content_parts.append(f"详细信息: {additional_info}")

    # 添加工作目录信息
    try:
        current_dir = os.path.basename(os.getcwd())
        content_parts.append(f"项目: {current_dir}")
    except:
        pass

    content_parts.append("--- 来自 Claude Code 自动提醒")
    content = "\n".join(content_parts)

    # 构建 Message Pusher API 请求数据
    api_data = {
        "title": title,
        "description": description,
        "content": content,
        "token": CLAUDE_TASK_TOKEN,
        "channel": FEISHU_CHANNEL
    }

    try:
        response = requests.post(MESSAGE_PUSHER_API, json=api_data, timeout=15)

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"SUCCESS: 通知发送成功 - {title}")
                return True
            else:
                print(f"ERROR: Message Pusher错误: {result.get('message')}")
        else:
            print(f"ERROR: HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"ERROR: 发送失败: {e}")

    return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Claude Code 任务完成提醒系统')
    parser.add_argument('--manual', action='store_true', help='手动指定所有参数模式')
    parser.add_argument('--quick', action='store_true', help='快速发送模式')
    parser.add_argument('--list-types', action='store_true', help='列出支持的任务类型')
    parser.add_argument('args', nargs='*', help='任务参数')

    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n📋 使用示例:")
        print("1. 智能模式: python claude_code_notifier.py '分析了50个Python文件' '完成' '发现3个问题'")
        print("2. 手动模式: python claude_code_notifier.py --manual '代码分析' '代码分析' '完成' '扫描项目文件' '发现性能问题'")
        print("3. 快速模式: python claude_code_notifier.py --quick '任务完成'")
        print("4. 查看类型: python claude_code_notifier.py --list-types")
        return

    args = parser.parse_args()

    # 列出任务类型
    if args.list_types:
        print("📋 支持的任务类型:")
        for task_type, config in TASK_TYPES.items():
            if task_type != "其他":
                keywords = ", ".join(config["keywords"][:3])
                print(f"  {config['icon']} {task_type}: {keywords}...")
        return

    # 快速模式
    if args.quick:
        if args.args:
            send_notification(args.args[0], mode="quick")
        else:
            send_notification("Claude Code 任务完成", mode="quick")
        return

    # 手动模式
    if args.manual:
        if len(args.args) >= 4:
            task_name = args.args[0]
            task_type = args.args[1]
            status = args.args[2]
            execution_details = args.args[3]
            additional_info = args.args[4] if len(args.args) > 4 else ""
            duration = args.args[5] if len(args.args) > 5 else ""

            send_notification(task_name, task_type, status, execution_details, additional_info, duration, "manual")
        else:
            print("❌ 手动模式需要至少4个参数: 任务名 类型 状态 执行内容")
        return

    # 智能模式（默认）
    if args.args:
        task_name = args.args[0]
        status = args.args[1] if len(args.args) > 1 else "完成"
        additional_info = args.args[2] if len(args.args) > 2 else ""
        duration = args.args[3] if len(args.args) > 3 else ""

        send_notification(task_name, status=status, additional_info=additional_info, duration=duration, mode="smart")
    else:
        # 默认测试
        send_notification("Claude Code 提醒系统配置完成", "系统配置", "完成",
                         "成功配置飞书推送，支持智能检测和详细信息展示",
                         "包含3种使用模式：智能、手动、快速", mode="smart")

if __name__ == "__main__":
    main()