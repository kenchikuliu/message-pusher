#!/usr/bin/env python3
"""
Claude Code 飞书Flow Hook
专为飞书自动化流程设计的标准格式通知系统
完全符合您指定的JSON结构要求
"""

import requests
import os
import time
import json
from datetime import datetime

# 飞书Webhook配置
FEISHU_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

class ClaudeFlowHook:
    """Claude Code 飞书Flow Hook类"""

    def __init__(self):
        self.webhook_url = FEISHU_WEBHOOK_URL
        self.start_time = None

    def start_task(self):
        """开始任务计时"""
        self.start_time = time.time()

    def get_duration_seconds(self):
        """获取执行时长"""
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0

    def detect_task_type(self, task_name):
        """检测Claude Code任务类型"""
        task_lower = task_name.lower()

        if any(word in task_lower for word in ["bash", "shell", "命令", "执行", "运行"]):
            return "Bash"
        elif any(word in task_lower for word in ["write", "创建", "生成", "新建", "写入"]):
            return "Write"
        elif any(word in task_lower for word in ["edit", "编辑", "修改", "更新"]):
            return "Edit"
        else:
            return "Custom"

    def send_hook_notification(self, task_name, status="success", result="", task_type=None, duration_sec=None):
        """
        发送符合飞书Flow标准的Hook通知

        严格按照您指定的JSON结构:
        {
          "msg_type": "text",
          "content": {
            "task_name": "任意任务名",
            "status": "success|failed|running",
            "result": "任意文本摘要（截断到800-1000字符）",
            "task_type": "Bash|Write|Edit|Custom",
            "duration_sec": 123
          }
        }
        """

        # 自动检测任务类型
        if not task_type:
            task_type = self.detect_task_type(task_name)

        # 自动计算时长
        if duration_sec is None:
            duration_sec = self.get_duration_seconds()

        # 构建结果摘要（截断到合适长度）
        if not result:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                current_dir = os.path.basename(os.getcwd())
                result = f"Claude Code 任务于 {current_time} 在项目 {current_dir} 中执行完成"
            except:
                result = f"Claude Code 任务于 {current_time} 执行完成"

        # 截断结果到900字符以内
        if len(result) > 900:
            result = result[:897] + "..."

        # 构建标准JSON - 严格按照curl测试成功的格式
        payload = {
            "msg_type": "text",
            "content": {
                "task_name": task_name,
                "status": status,
                "result": result,
                "task_type": task_type,
                "duration_sec": duration_sec
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    print(f"[FLOW-HOOK] SUCCESS: {task_name} ({status}) - {duration_sec}s")
                    return True
                else:
                    print(f"[FLOW-HOOK] ERROR: {data.get('msg', 'Unknown error')}")
            else:
                print(f"[FLOW-HOOK] HTTP ERROR: {response.status_code}")

        except Exception as e:
            print(f"[FLOW-HOOK] EXCEPTION: {e}")

        return False

# 全局实例
_flow_hook = ClaudeFlowHook()

# 便捷函数
def start_claude_task():
    """开始Claude任务（用于计时）"""
    _flow_hook.start_task()

def notify_claude_completion(task_name, status="success", result="", task_type=None):
    """
    通知Claude任务完成

    参数:
    - task_name: 任务名称
    - status: success|failed|running
    - result: 结果描述（会自动截断）
    - task_type: Bash|Write|Edit|Custom（可选，会自动检测）
    """
    return _flow_hook.send_hook_notification(task_name, status, result, task_type)

def notify_bash_task(command, status="success", output="", exit_code=0):
    """通知Bash任务"""
    result = f"命令: {command}"
    if exit_code != 0:
        result += f" | 退出码: {exit_code}"
    if output:
        result += f" | 输出: {output[:300]}"

    actual_status = "failed" if exit_code != 0 else status
    return notify_claude_completion(f"Bash: {command}", actual_status, result, "Bash")

def notify_write_task(file_path, status="success", details=""):
    """通知文件写入任务"""
    filename = os.path.basename(file_path)
    result = f"文件: {filename}"
    if details:
        result += f" | {details}"

    return notify_claude_completion(f"Write: {filename}", status, result, "Write")

def notify_edit_task(file_path, status="success", changes=""):
    """通知文件编辑任务"""
    filename = os.path.basename(file_path)
    result = f"文件: {filename}"
    if changes:
        result += f" | 修改: {changes}"

    return notify_claude_completion(f"Edit: {filename}", status, result, "Edit")

def main():
    """测试函数"""
    print("Claude Flow Hook 测试")
    print("发送标准飞书自动化流程格式...")

    # 开始计时
    start_claude_task()

    # 模拟工作
    time.sleep(1)

    # 测试各种类型的通知
    print("\n1. 测试Custom任务:")
    notify_claude_completion(
        "Flow Hook系统配置",
        "success",
        "配置完成，严格按照飞书自动化流程JSON格式，支持content.*字段引用",
        "Custom"
    )

    print("\n2. 测试Bash任务:")
    notify_bash_task("ls -la", "success", "列出20个文件", 0)

    print("\n3. 测试Write任务:")
    notify_write_task("test.py", "success", "创建50行Python代码")

    print("\n4. 测试Edit任务:")
    notify_edit_task("config.json", "success", "更新3个配置项")

    print("\n测试完成！您的飞书Flow应该收到4条通知。")
    print("每条通知都严格按照您指定的JSON结构发送。")

if __name__ == "__main__":
    main()