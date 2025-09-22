#!/usr/bin/env python3
"""
Claude Code 自动对话总结器
实时分析Claude Code对话，自动提取任务信息并发送飞书通知
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

WEBHOOK_URL = "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"

class ConversationSummarizer:
    """对话总结器 - 模拟LLM分析"""

    def __init__(self):
        self.conversation_history = []
        self.session_start = datetime.now()

    def add_interaction(self, user_input: str, claude_response: str):
        """添加一轮对话"""
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'claude': claude_response
        })

    def analyze_conversation(self) -> Dict:
        """
        分析整个对话历史，模拟LLM总结能力
        """
        if not self.conversation_history:
            return self._create_default_summary()

        # 获取最新的交互
        latest = self.conversation_history[-1]

        # 分析任务名称（从用户输入中提取意图）
        task_name = self._extract_primary_task(latest['user'])

        # 分析执行状态（从Claude回应中判断）
        status = self._analyze_execution_status(latest['claude'])

        # 生成详细结果摘要
        result = self._generate_comprehensive_summary()

        # 确定任务类型
        task_type = self._classify_task_type()

        # 计算会话时长
        duration_sec = int((datetime.now() - self.session_start).total_seconds())

        return {
            'task_name': task_name,
            'status': status,
            'result': result,
            'task_type': task_type,
            'duration_sec': duration_sec
        }

    def _extract_primary_task(self, user_input: str) -> str:
        """提取主要任务（模拟LLM理解用户意图）"""
        input_text = user_input.lower()

        # 任务意图模式匹配
        intent_patterns = [
            (r'帮我(.{5,40}?)(?:[，。！？]|$)', '帮助'),
            (r'请(.{5,40}?)(?:[，。！？]|$)', '请求'),
            (r'我想(.{5,40}?)(?:[，。！？]|$)', '需求'),
            (r'能否(.{5,40}?)(?:[，。！？]|$)', '询问'),
            (r'如何(.{5,40}?)(?:[，。！？]|$)', '指导'),
            (r'配置(.{5,40}?)(?:[，。！？]|$)', '配置'),
            (r'测试(.{5,40}?)(?:[，。！？]|$)', '测试'),
            (r'运行(.{5,40}?)(?:[，。！？]|$)', '运行')
        ]

        for pattern, category in intent_patterns:
            match = re.search(pattern, user_input)
            if match:
                task_detail = match.group(1).strip()
                if len(task_detail) > 5:
                    return f"{category}: {task_detail}"

        # 关键词提取（模拟LLM关键概念识别）
        key_concepts = [
            'docker', '飞书', 'webhook', 'claude code', 'message pusher',
            '通知', '配置', '测试', '部署', 'hook', 'flow', '集成'
        ]

        found_concepts = [concept for concept in key_concepts if concept in input_text]

        if found_concepts:
            primary_concept = found_concepts[0]
            return f"{primary_concept}相关任务"

        # 备选方案
        if len(user_input) < 50:
            return user_input.strip()
        else:
            return user_input[:47] + "..."

    def _analyze_execution_status(self, claude_response: str) -> str:
        """分析执行状态（模拟LLM情感和状态理解）"""
        response_lower = claude_response.lower()

        # 成功指标（强烈程度排序）
        strong_success = ['完美', '成功', '太好了', '完成', '已经配置好', '工作正常']
        moderate_success = ['好的', '已创建', '已修复', '已更新', '运行中']

        # 失败指标
        failure_indicators = ['失败', '错误', '异常', '无法', '不能', '问题']

        # 运行中指标
        running_indicators = ['正在', '开始', '处理中', '执行中']

        # 检查失败（优先级最高）
        if any(indicator in response_lower for indicator in failure_indicators):
            return "failed"

        # 检查运行中
        if any(indicator in response_lower for indicator in running_indicators):
            return "running"

        # 检查成功（分强弱程度）
        if any(indicator in response_lower for indicator in strong_success):
            return "success"

        if any(indicator in response_lower for indicator in moderate_success):
            return "success"

        # 默认成功（Claude通常给正面回应）
        return "success"

    def _generate_comprehensive_summary(self) -> str:
        """生成综合摘要（模拟LLM文本总结能力）"""
        if not self.conversation_history:
            return "Claude Code会话进行中"

        # 提取关键成就和行动
        achievements = []
        actions = []

        for interaction in self.conversation_history[-3:]:  # 分析最近3轮对话
            claude_text = interaction['claude'].lower()

            # 提取成就关键词
            achievement_keywords = [
                '成功', '完成', '创建', '配置', '修复', '更新', '部署',
                '测试通过', '工作正常', '已解决'
            ]

            for keyword in achievement_keywords:
                if keyword in claude_text:
                    # 尝试提取上下文
                    sentences = interaction['claude'].split('。')
                    for sentence in sentences:
                        if keyword in sentence and len(sentence) < 100:
                            achievements.append(sentence.strip())
                            break

            # 提取行动关键词
            action_keywords = [
                '创建了', '配置了', '修复了', '更新了', '测试了', '部署了'
            ]

            for keyword in action_keywords:
                if keyword in claude_text:
                    sentences = interaction['claude'].split('。')
                    for sentence in sentences:
                        if keyword in sentence and len(sentence) < 80:
                            actions.append(sentence.strip())
                            break

        # 构建摘要
        summary_parts = []

        if achievements:
            summary_parts.append(f"成就: {' | '.join(achievements[:2])}")

        if actions:
            summary_parts.append(f"行动: {' | '.join(actions[:2])}")

        # 添加会话统计
        session_duration = (datetime.now() - self.session_start).total_seconds()
        interaction_count = len(self.conversation_history)

        summary_parts.append(f"会话: {interaction_count}轮交互")

        if session_duration > 60:
            summary_parts.append(f"时长: {session_duration/60:.1f}分钟")
        else:
            summary_parts.append(f"时长: {session_duration:.0f}秒")

        result = " | ".join(summary_parts)

        # 截断到合适长度
        if len(result) > 800:
            result = result[:797] + "..."

        return result

    def _classify_task_type(self) -> str:
        """分类任务类型（模拟LLM分类能力）"""
        if not self.conversation_history:
            return "Custom"

        # 分析所有对话文本
        all_text = " ".join([
            f"{item['user']} {item['claude']}"
            for item in self.conversation_history
        ]).lower()

        # 类型判断逻辑
        if any(keyword in all_text for keyword in [
            'bash', 'command', 'shell', '命令行', '执行命令', 'curl'
        ]):
            return "Bash"

        elif any(keyword in all_text for keyword in [
            'write', 'create', '创建文件', '生成文件', '写入'
        ]):
            return "Write"

        elif any(keyword in all_text for keyword in [
            'edit', 'modify', '编辑', '修改文件', '更新文件'
        ]):
            return "Edit"

        else:
            return "Custom"

    def _create_default_summary(self) -> Dict:
        """创建默认摘要"""
        return {
            'task_name': 'Claude Code会话',
            'status': 'running',
            'result': 'Claude Code会话正在进行中',
            'task_type': 'Custom',
            'duration_sec': 0
        }

def send_conversation_summary(user_input: str, claude_response: str) -> bool:
    """
    发送对话总结通知

    Args:
        user_input: 用户输入
        claude_response: Claude回应

    Returns:
        bool: 发送是否成功
    """
    # 创建总结器并分析
    summarizer = ConversationSummarizer()
    summarizer.add_interaction(user_input, claude_response)

    # 获取分析结果
    analysis = summarizer.analyze_conversation()

    # 获取项目信息
    try:
        from project_detector import detect_project_info
        project_name, project_path = detect_project_info()
    except:
        project_name = "claude-code"
        project_path = os.getcwd()

    # 添加项目信息到分析结果
    analysis['project_name'] = project_name
    analysis['project_path'] = project_path

    # 构建webhook payload
    payload = {
        "msg_type": "text",
        "content": analysis
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
                print(f"[AUTO-SUMMARY] SUCCESS: {analysis['task_name']}")
                return True
            else:
                print(f"[AUTO-SUMMARY] ERROR: {data.get('msg')}")
        else:
            print(f"[AUTO-SUMMARY] HTTP ERROR: {response.status_code}")

    except Exception as e:
        print(f"[AUTO-SUMMARY] EXCEPTION: {e}")

    return False

def main():
    """测试接口"""
    if len(sys.argv) < 3:
        print("Claude对话自动总结器")
        print("用法: python claude_auto_summarizer.py <用户输入> <Claude回应>")
        return

    user_input = sys.argv[1]
    claude_response = sys.argv[2]

    send_conversation_summary(user_input, claude_response)

if __name__ == "__main__":
    import sys
    main()