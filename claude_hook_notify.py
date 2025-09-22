#!/usr/bin/env python3
"""
Claude Code Hook 通知系统
使用标准飞书自动化流程格式，确保与Flow完全兼容
"""

import requests
import sys
import os
import time
from datetime import datetime

# 配置
FEISHU_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

def map_status_to_standard(status):
    """将状态映射到标准格式"""
    status_lower = status.lower()
    if "完成" in status or "成功" in status or "success" in status_lower or "ok" in status_lower:
        return "success"
    elif "失败" in status or "错误" in status or "error" in status_lower or "fail" in status_lower:
        return "failed"
    elif "运行" in status or "进行" in status or "running" in status_lower or "executing" in status_lower:
        return "running"
    else:
        return "success"  # 默认为成功

def detect_claude_task_type(task_name):
    """检测Claude Code任务类型"""
    task_lower = task_name.lower()

    # 检测是否是bash命令
    if any(word in task_lower for word in ["命令", "执行", "bash", "shell", "运行脚本"]):
        return "Bash"

    # 检测是否是文件写入
    elif any(word in task_lower for word in ["写入", "创建文件", "生成文件", "write", "create"]):
        return "Write"

    # 检测是否是文件编辑
    elif any(word in task_lower for word in ["编辑", "修改文件", "更新文件", "edit", "modify"]):
        return "Edit"

    # 其他自定义任务
    else:
        return "Custom"

def parse_duration(duration_str):
    """解析时长字符串为秒数"""
    if not duration_str:
        return 0

    duration_str = duration_str.lower()
    try:
        # 提取数字
        import re
        numbers = re.findall(r'\d+\.?\d*', duration_str)
        if not numbers:
            return 0

        value = float(numbers[0])

        # 根据单位转换
        if "分" in duration_str or "min" in duration_str:
            return int(value * 60)
        elif "时" in duration_str or "hour" in duration_str or "hr" in duration_str:
            return int(value * 3600)
        elif "秒" in duration_str or "sec" in duration_str or "s" in duration_str:
            return int(value)
        else:
            return int(value)  # 默认当作秒
    except:
        return 0

def truncate_result(result_text, max_length=800):
    """截断结果文本到指定长度"""
    if len(result_text) <= max_length:
        return result_text

    return result_text[:max_length-3] + "..."

def send_feishu_hook_notification(task_name, status="success", result="", task_type=None, duration=""):
    """
    发送符合飞书自动化流程标准的通知

    参数:
    - task_name: 任务名称
    - status: success|failed|running
    - result: 结果摘要（会自动截断到800-1000字符）
    - task_type: Bash|Write|Edit|Custom（可选，会自动检测）
    - duration: 时长（支持多种格式）
    """

    # 自动检测任务类型
    if not task_type:
        task_type = detect_claude_task_type(task_name)

    # 标准化状态
    standard_status = map_status_to_standard(status)

    # 解析时长
    duration_sec = parse_duration(duration)

    # 构建结果摘要
    if not result:
        # 自动生成基本结果信息
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            current_dir = os.path.basename(os.getcwd())
            result = f"Claude Code 任务于 {current_time} 在项目 {current_dir} 中执行"
        except:
            result = f"Claude Code 任务于 {current_time} 执行"

    # 截断结果文本
    result = truncate_result(result, 900)  # 留一些余量

    # 构建标准飞书自动化流程JSON格式
    webhook_data = {
        "msg_type": "text",
        "content": {
            "task_name": task_name,
            "status": standard_status,
            "result": result,
            "task_type": task_type,
            "duration_sec": duration_sec
        }
    }

    try:
        # 直接发送到飞书Webhook
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json=webhook_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('code') == 0:
                print(f"SUCCESS: 飞书Hook通知发送成功 - {task_name} ({standard_status})")
                return True
            else:
                print(f"ERROR: 飞书API错误 - code: {response_data.get('code')}, msg: {response_data.get('msg')}")
        else:
            print(f"ERROR: HTTP错误 {response.status_code} - {response.text}")

    except Exception as e:
        print(f"ERROR: 发送异常 - {e}")

    return False

def main():
    """主函数 - 命令行接口"""
    if len(sys.argv) < 2:
        print("Claude Code Hook 通知系统")
        print("使用标准飞书自动化流程格式")
        print()
        print("用法:")
        print("  python claude_hook_notify.py <任务名> [状态] [结果] [任务类型] [时长]")
        print()
        print("参数说明:")
        print("  任务名: 必需，任务描述")
        print("  状态: 可选，success|failed|running（默认success）")
        print("  结果: 可选，任务结果摘要")
        print("  任务类型: 可选，Bash|Write|Edit|Custom（默认自动检测）")
        print("  时长: 可选，如'2分钟'、'30秒'、'1.5小时'")
        print()
        print("示例:")
        print("  python claude_hook_notify.py '代码分析' 'success' '发现3个问题，已修复2个'")
        print("  python claude_hook_notify.py '文件生成' 'success' '成功创建5个文件' 'Write' '2分钟'")
        print("  python claude_hook_notify.py '测试运行' 'failed' '3个测试失败' 'Bash' '45秒'")
        return

    # 解析命令行参数
    task_name = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else "success"
    result = sys.argv[3] if len(sys.argv) > 3 else ""
    task_type = sys.argv[4] if len(sys.argv) > 4 else None
    duration = sys.argv[5] if len(sys.argv) > 5 else ""

    # 发送通知
    send_feishu_hook_notification(task_name, status, result, task_type, duration)

if __name__ == "__main__":
    main()