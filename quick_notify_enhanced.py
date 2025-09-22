#!/usr/bin/env python3
"""
增强版快速通知 - 支持项目信息字段
"""

import requests
import os
import json

WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

def quick_notify_with_project(task_name, status="success", result="任务完成", task_type="Custom", duration_sec=0):
    """
    快速发送Claude Code通知（包含项目信息）

    Args:
        task_name: 任务名称
        status: 状态 (success/failed/running)
        result: 结果描述
        task_type: 任务类型 (Custom/Bash/Write/Edit)
        duration_sec: 执行时长（秒）
    """

    # 自动检测项目信息
    project_name, project_path = _detect_project_info()

    payload = {
        "msg_type": "text",
        "content": {
            "task_name": task_name,
            "status": status,
            "result": result,
            "task_type": task_type,
            "duration_sec": duration_sec,
            "project_name": project_name,
            "project_path": project_path
        }
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"通知发送成功: {task_name} [项目: {project_name}]")
            return True
        else:
            print(f"通知发送失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"通知发送异常: {e}")
        return False

def _detect_project_info():
    """检测项目信息"""
    current_dir = os.getcwd()
    project_path = os.path.abspath(current_dir)

    # 尝试从package.json获取项目名
    package_json = os.path.join(current_dir, 'package.json')
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'name' in data:
                    return data['name'], project_path
        except:
            pass

    # 尝试从go.mod获取项目名
    go_mod = os.path.join(current_dir, 'go.mod')
    if os.path.exists(go_mod):
        try:
            with open(go_mod, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('module '):
                    module_name = first_line[7:].strip()
                    return module_name.split('/')[-1], project_path
        except:
            pass

    # 使用目录名作为项目名
    project_name = os.path.basename(current_dir) or "claude-code"
    return project_name, project_path

# 兼容性函数 - 超简版（自动包含项目信息）
def super_quick_notify(task_name):
    """超简版通知 - 仅需任务名称"""
    return quick_notify_with_project(task_name)

if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        task_name = sys.argv[1]
        quick_notify_with_project(task_name)
    else:
        print("用法: python quick_notify_enhanced.py '任务名称'")