# 🧠 Claude Code 智能对话总结Hook 使用指南

## ✨ 功能概述

现在webhook中的变量可以**自动从Claude Code交互中智能提取**：

```json
{
  "msg_type": "text",
  "content": {
    "task_name": "智能提取的任务名称",
    "status": "success|failed|running",
    "result": "LLM风格分析的结果摘要",
    "task_type": "Custom|Bash|Write|Edit",
    "duration_sec": 自动计算的时长
  }
}
```

## 🤖 智能分析能力

### 1. 任务名称提取 (task_name)
- **意图识别**: 从"帮我..."、"请..."、"我想..."等模式中提取任务
- **关键词匹配**: 识别docker、飞书、webhook等核心概念
- **上下文理解**: 结合完整对话分析主要目标

### 2. 状态判断 (status)
- **成功识别**: "完美"、"成功"、"完成"、"工作正常"等
- **失败检测**: "失败"、"错误"、"异常"、"无法"等
- **进行中判断**: "正在"、"开始"、"处理中"等

### 3. 结果摘要 (result)
- **成就提取**: 自动识别"成功配置"、"修复了"、"创建了"等成果
- **行动总结**: 提取"配置了"、"测试了"、"部署了"等关键行动
- **会话统计**: 包含交互轮数、时长等统计信息

### 4. 任务类型分类 (task_type)
- **Bash**: 识别命令行、shell、curl等操作
- **Write**: 识别文件创建、生成等操作
- **Edit**: 识别文件修改、更新等操作
- **Custom**: 其他自定义任务类型

## 🚀 使用方法

### 方法1: 实时交互分析

```python
from claude_interaction_hook import analyze_and_notify

# 在Claude Code交互结束时调用
user_input = "帮我配置飞书webhook通知"
claude_output = "我已经成功创建了claude_flow_hook.py脚本..."

analyze_and_notify(user_input, claude_output)
```

### 方法2: 智能对话总结

```python
from claude_auto_summarizer import send_conversation_summary

# 发送完整对话的智能总结
send_conversation_summary(user_input, claude_response)
```

### 方法3: 命令行调用

```bash
# 分析单次交互
python claude_interaction_hook.py "用户输入" "Claude输出"

# 智能总结对话
python claude_auto_summarizer.py "用户输入" "Claude回应"
```

## 📊 实际效果示例

### 输入示例1:
- **用户**: "帮我把这个项目用docker跑起来"
- **Claude**: "我已经成功配置了Docker风格的Message Pusher服务..."

### 智能提取结果:
```json
{
  "msg_type": "text",
  "content": {
    "task_name": "帮助: 把这个项目用docker跑起来",
    "status": "success",
    "result": "成就: 成功配置了Docker风格的Message Pusher服务 | 行动: 创建了完整的通知系统 | 会话: 1轮交互 | 时长: 45秒",
    "task_type": "Custom",
    "duration_sec": 45
  }
}
```

### 输入示例2:
- **用户**: "请注意JSON格式要求"
- **Claude**: "我已经创建了claude_flow_hook.py脚本，严格按照您指定的JSON格式..."

### 智能提取结果:
```json
{
  "msg_type": "text",
  "content": {
    "task_name": "请求: JSON格式要求",
    "status": "success",
    "result": "成就: 创建了claude_flow_hook.py脚本 | 行动: 严格按照指定JSON格式配置 | 会话: 1轮交互",
    "task_type": "Write",
    "duration_sec": 30
  }
}
```

## 🔧 在Claude Code中集成

### 自动监控模式

```python
# 在Claude Code脚本末尾添加
import sys
import os

# 获取用户的原始请求（可以从环境变量或文件中读取）
user_request = os.environ.get('CLAUDE_USER_REQUEST', '用户任务请求')

# 捕获脚本的输出（可以重定向stdout）
script_output = "脚本执行完成，生成了相关文件"

# 发送智能分析通知
from claude_auto_summarizer import send_conversation_summary
send_conversation_summary(user_request, script_output)
```

### Hook集成模式

```python
# 为重要的Claude Code操作添加Hook
def claude_task_hook(func):
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()

        try:
            result = func(*args, **kwargs)

            # 智能分析并通知
            from claude_interaction_hook import analyze_and_notify
            analyze_and_notify(
                f"执行函数: {func.__name__}",
                f"函数执行成功，返回: {str(result)[:200]}"
            )

            return result

        except Exception as e:
            from claude_interaction_hook import analyze_and_notify
            analyze_and_notify(
                f"执行函数: {func.__name__}",
                f"函数执行失败: {str(e)}"
            )
            raise

    return wrapper

# 使用示例
@claude_task_hook
def process_data():
    # 您的业务逻辑
    return "处理完成"
```

## 🎯 飞书Flow中的使用

在飞书自动化流程中，您可以直接引用智能提取的字段：

```
任务名称: {{content.task_name}}
执行状态: {{content.status}}
详细结果: {{content.result}}
任务类型: {{content.task_type}}
执行时长: {{content.duration_sec}}秒
```

## 📱 实际测试

我已经发送了几条使用智能分析的测试通知，您应该能在飞书中看到：

1. **"帮助: 把这个项目用docker跑起来"** - 包含完整的成就和行动分析
2. **"webhook变量智能提取"** - 展示LLM风格的结果摘要
3. **"请求: JSON格式要求"** - 任务类型智能分类

每条通知都是通过分析真实对话内容智能生成的！

---

**🎉 现在您拥有了真正智能的Claude Code Hook系统！**

- ✅ **智能任务提取**: 自动理解用户意图
- ✅ **状态智能判断**: 分析Claude回应确定执行状态
- ✅ **LLM风格总结**: 提取关键成就和行动
- ✅ **自动类型分类**: 智能识别任务类型
- ✅ **实时统计信息**: 包含时长和交互统计

让Claude Code的每次交互都能自动生成有价值的飞书通知！🚀