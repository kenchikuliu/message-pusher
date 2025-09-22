#!/usr/bin/env python3
"""
Claude Code 交互智能总结Hook
自动从用户输入和Claude输出中提取任务信息，通过LLM总结生成通知
"""

import requests
import sys
import json
import re
from datetime import datetime

WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

class ClaudeInteractionAnalyzer:
    """Claude交互分析器"""

    def __init__(self):
        self.start_time = datetime.now()

    def extract_task_info(self, user_input, claude_output):
        """
        通过LLM风格的分析提取任务信息
        """
        # 分析用户输入中的任务意图
        task_name = self._extract_task_name(user_input)

        # 分析Claude输出确定执行状态
        status = self._determine_status(claude_output)

        # 生成结果摘要
        result = self._generate_result_summary(user_input, claude_output)

        # 检测任务类型
        task_type = self._detect_task_type(user_input, claude_output)

        return task_name, status, result, task_type

    def _extract_task_name(self, user_input):
        """从用户输入中提取任务名称"""
        input_lower = user_input.lower().strip()

        # 常见任务关键词模式
        patterns = [
            r'帮我(.+?)(?:，|。|$)',
            r'请(.+?)(?:，|。|$)',
            r'我想(.+?)(?:，|。|$)',
            r'需要(.+?)(?:，|。|$)',
            r'能否(.+?)(?:，|。|$)',
            r'可以(.+?)(?:，|。|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                task = match.group(1).strip()
                if len(task) > 0 and len(task) < 50:
                    return task

        # 如果没有匹配到模式，提取关键动词
        action_keywords = [
            '分析', '创建', '生成', '修改', '编辑', '删除', '查找', '搜索',
            '配置', '设置', '部署', '测试', '运行', '执行', '处理', '优化',
            '重构', '修复', '调试', '检查', '验证', '更新', '安装'
        ]

        for keyword in action_keywords:
            if keyword in user_input:
                # 尝试提取动作和对象
                parts = user_input.split(keyword)
                if len(parts) > 1:
                    obj = parts[1].strip()[:30]
                    return f"{keyword}{obj}" if obj else keyword
                return keyword

        # 最后的备选方案
        if len(user_input) < 50:
            return user_input.strip()
        else:
            return user_input[:47] + "..."

    def _determine_status(self, claude_output):
        """从Claude输出确定执行状态"""
        output_lower = claude_output.lower()

        # 成功指示词
        success_indicators = [
            '成功', '完成', '已创建', '已生成', '已修改', '已更新', '已配置',
            'success', 'complete', 'finished', 'created', 'generated',
            'updated', 'configured', '✅', '完美', '好的', '已经'
        ]

        # 失败指示词
        failure_indicators = [
            '失败', '错误', '无法', '不能', '异常', '问题',
            'failed', 'error', 'exception', 'cannot', 'unable',
            '❌', '出错', '失效'
        ]

        # 进行中指示词
        running_indicators = [
            '正在', '开始', '执行中', '处理中', '运行中',
            'running', 'executing', 'processing', 'starting'
        ]

        # 检查失败指示词（优先级高）
        for indicator in failure_indicators:
            if indicator in output_lower:
                return "failed"

        # 检查运行中指示词
        for indicator in running_indicators:
            if indicator in output_lower:
                return "running"

        # 检查成功指示词
        for indicator in success_indicators:
            if indicator in output_lower:
                return "success"

        # 默认为成功（Claude通常会给出正面回应）
        return "success"

    def _generate_result_summary(self, user_input, claude_output):
        """生成结果摘要"""
        # 提取Claude输出的关键信息
        lines = claude_output.split('\n')
        important_lines = []

        for line in lines:
            line = line.strip()
            if len(line) < 10 or len(line) > 200:
                continue

            # 过滤掉一些无关的行
            if any(skip in line.lower() for skip in [
                'system-reminder', 'background bash', 'timestamp',
                '===', '---', 'tool_use_error', 'debug'
            ]):
                continue

            # 寻找有价值的信息
            if any(keyword in line.lower() for keyword in [
                '成功', '完成', '创建', '生成', '修改', '配置', '分析',
                '发现', '处理', '执行', '结果', '输出', '文件'
            ]):
                important_lines.append(line)

        # 构建摘要
        if important_lines:
            summary_parts = important_lines[:3]  # 最多3行关键信息
            result = " | ".join(summary_parts)
        else:
            # 备选方案：提取用户需求和简单回应
            result = f"处理用户请求: {user_input[:50]}"

        # 添加时间和统计信息
        current_time = datetime.now().strftime('%H:%M:%S')
        duration = (datetime.now() - self.start_time).total_seconds()

        result += f" | 完成时间: {current_time}"
        if duration > 1:
            result += f" | 耗时: {duration:.1f}秒"

        # 截断到合适长度
        if len(result) > 800:
            result = result[:797] + "..."

        return result

    def _detect_task_type(self, user_input, claude_output):
        """检测任务类型"""
        combined_text = (user_input + " " + claude_output).lower()

        # Bash类型
        if any(keyword in combined_text for keyword in [
            'bash', 'command', '命令', '执行', '运行', 'shell', 'cmd'
        ]):
            return "Bash"

        # Write类型
        elif any(keyword in combined_text for keyword in [
            'write', '创建', '生成', '新建', 'create', '写入'
        ]):
            return "Write"

        # Edit类型
        elif any(keyword in combined_text for keyword in [
            'edit', '编辑', '修改', '更新', 'modify', 'update'
        ]):
            return "Edit"

        # 默认Custom类型
        else:
            return "Custom"

def analyze_and_notify(user_input, claude_output=""):
    """
    分析交互内容并发送通知

    Args:
        user_input: 用户的输入消息
        claude_output: Claude的输出回应（可选）
    """
    if not claude_output:
        claude_output = "Claude正在处理您的请求..."

    analyzer = ClaudeInteractionAnalyzer()
    task_name, status, result, task_type = analyzer.extract_task_info(user_input, claude_output)

    # 获取项目信息
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        from project_detector import detect_project_info
        project_name, project_path = detect_project_info()
    except:
        import os
        project_name = "claude-code"
        project_path = os.getcwd()

    # 构建webhook payload
    payload = {
        "msg_type": "text",
        "content": {
            "task_name": task_name,
            "status": status,
            "result": result,
            "task_type": task_type,
            "duration_sec": int((datetime.now() - analyzer.start_time).total_seconds()),
            "project_name": project_name,
            "project_path": project_path
        }
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                print(f"[INTERACTION-HOOK] SUCCESS: {task_name}")
                return True
            else:
                print(f"[INTERACTION-HOOK] ERROR: {data.get('msg')}")
        else:
            print(f"[INTERACTION-HOOK] HTTP ERROR: {response.status_code}")

    except Exception as e:
        print(f"[INTERACTION-HOOK] EXCEPTION: {e}")

    return False

def main():
    """命令行测试接口"""
    if len(sys.argv) < 2:
        print("Claude交互智能总结Hook")
        print("用法: python claude_interaction_hook.py <用户输入> [Claude输出]")
        print("示例: python claude_interaction_hook.py '帮我分析代码' 'Claude已完成代码分析...'")
        return

    user_input = sys.argv[1]
    claude_output = sys.argv[2] if len(sys.argv) > 2 else ""

    analyze_and_notify(user_input, claude_output)

if __name__ == "__main__":
    main()