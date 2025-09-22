#!/usr/bin/env python3
"""
Claude Code Hook 集成模块
专为Claude Code设计的Hook系统，符合飞书自动化流程标准

在Claude Code中使用：
from claude_code_hook import notify_task_completion
notify_task_completion("任务名", "success", "结果描述")
"""

import requests
import os
import time
import json
from datetime import datetime
from typing import Optional, Literal

# 飞书Webhook配置
FEISHU_WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

# 类型定义
TaskStatus = Literal["success", "failed", "running"]
TaskType = Literal["Bash", "Write", "Edit", "Custom"]

class ClaudeCodeHook:
    """Claude Code Hook 通知类"""

    def __init__(self, webhook_url: str = FEISHU_WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.start_time = None

    def start_task(self):
        """开始任务计时"""
        self.start_time = time.time()

    def get_duration_seconds(self) -> int:
        """获取任务执行时长（秒）"""
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0

    def detect_task_type(self, task_name: str, context: str = "") -> TaskType:
        """检测任务类型"""
        combined_text = f"{task_name} {context}".lower()

        if any(keyword in combined_text for keyword in [
            "bash", "shell", "命令", "执行", "运行", "脚本", "command"
        ]):
            return "Bash"

        elif any(keyword in combined_text for keyword in [
            "write", "创建", "生成", "新建", "文件创建", "写入"
        ]):
            return "Write"

        elif any(keyword in combined_text for keyword in [
            "edit", "编辑", "修改", "更新", "修复", "重构"
        ]):
            return "Edit"

        else:
            return "Custom"

    def truncate_text(self, text: str, max_length: int = 900) -> str:
        """截断文本到指定长度"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    def build_result_summary(self, result: str = "", **kwargs) -> str:
        """构建结果摘要"""
        if result:
            return self.truncate_text(result)

        # 自动生成基础信息
        summary_parts = []

        # 添加时间信息
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        summary_parts.append(f"执行时间: {current_time}")

        # 添加项目信息
        try:
            current_dir = os.path.basename(os.getcwd())
            summary_parts.append(f"项目: {current_dir}")
        except:
            pass

        # 添加额外信息
        for key, value in kwargs.items():
            if value:
                summary_parts.append(f"{key}: {value}")

        return self.truncate_text(" | ".join(summary_parts))

    def send_notification(self,
                         task_name: str,
                         status: TaskStatus = "success",
                         result: str = "",
                         task_type: Optional[TaskType] = None,
                         duration_sec: Optional[int] = None,
                         **kwargs) -> bool:
        """
        发送飞书Hook通知

        Args:
            task_name: 任务名称
            status: success|failed|running
            result: 结果描述
            task_type: Bash|Write|Edit|Custom
            duration_sec: 执行时长（秒）
            **kwargs: 额外信息用于构建结果

        Returns:
            bool: 发送是否成功
        """

        # 自动检测任务类型
        if not task_type:
            task_type = self.detect_task_type(task_name, result)

        # 自动计算时长
        if duration_sec is None:
            duration_sec = self.get_duration_seconds()

        # 构建结果摘要
        result_summary = self.build_result_summary(result, **kwargs)

        # 构建标准JSON格式
        payload = {
            "msg_type": "text",
            "content": {
                "task_name": task_name,
                "status": status,
                "result": result_summary,
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
                    print(f"[HOOK] ✓ {task_name} ({status}) - {duration_sec}s")
                    return True
                else:
                    print(f"[HOOK] ✗ API错误: {data.get('msg')}")
            else:
                print(f"[HOOK] ✗ HTTP {response.status_code}")

        except Exception as e:
            print(f"[HOOK] ✗ 异常: {e}")

        return False

# 全局Hook实例
_hook = ClaudeCodeHook()

# 便捷函数
def start_task():
    """开始任务（用于计时）"""
    _hook.start_task()

def notify_task_completion(task_name: str,
                          status: TaskStatus = "success",
                          result: str = "",
                          task_type: Optional[TaskType] = None,
                          **kwargs) -> bool:
    """
    通知任务完成

    使用示例:
    notify_task_completion("代码分析", "success", "发现3个问题")
    notify_task_completion("文件生成", "success", "创建了5个文件", "Write")
    notify_task_completion("测试运行", "failed", "2个测试失败", files_processed=50)
    """
    return _hook.send_notification(task_name, status, result, task_type, **kwargs)

def notify_bash_completion(command: str,
                          status: TaskStatus = "success",
                          output: str = "",
                          exit_code: int = 0) -> bool:
    """通知Bash命令完成"""
    result = f"命令: {command}"
    if exit_code != 0:
        result += f" | 退出码: {exit_code}"
    if output:
        result += f" | 输出: {output[:200]}"

    return notify_task_completion(
        f"Bash: {command}",
        "failed" if exit_code != 0 else status,
        result,
        "Bash",
        exit_code=exit_code
    )

def notify_file_operation(operation: str,
                         file_path: str,
                         status: TaskStatus = "success",
                         details: str = "") -> bool:
    """通知文件操作完成"""
    task_type = "Write" if operation in ["create", "write"] else "Edit"
    result = f"文件: {os.path.basename(file_path)}"
    if details:
        result += f" | {details}"

    return notify_task_completion(
        f"{operation}: {os.path.basename(file_path)}",
        status,
        result,
        task_type,
        file_path=file_path
    )

# 装饰器支持
def claude_hook(task_name: str = "", task_type: Optional[TaskType] = None):
    """
    装饰器：自动为函数添加Hook通知

    @claude_hook("数据处理")
    def process_data():
        # 函数实现
        return result
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            actual_task_name = task_name or f"函数: {func.__name__}"
            start_task()

            try:
                result = func(*args, **kwargs)
                notify_task_completion(
                    actual_task_name,
                    "success",
                    f"函数执行成功，返回: {str(result)[:100]}",
                    task_type
                )
                return result
            except Exception as e:
                notify_task_completion(
                    actual_task_name,
                    "failed",
                    f"函数执行失败: {str(e)}",
                    task_type
                )
                raise

        return wrapper
    return decorator

if __name__ == "__main__":
    # 测试示例
    print("Claude Code Hook 测试")

    # 开始任务
    start_task()

    # 模拟一些工作
    import time
    time.sleep(1)

    # 发送通知
    notify_task_completion(
        "Hook系统测试",
        "success",
        "Claude Code Hook 系统配置完成，支持标准飞书Flow格式",
        "Custom"
    )

    # 测试不同类型的通知
    notify_bash_completion("ls -la", "success", "列出了20个文件")
    notify_file_operation("create", "test.py", "success", "包含50行代码")

    print("测试完成！检查飞书是否收到3条通知。")