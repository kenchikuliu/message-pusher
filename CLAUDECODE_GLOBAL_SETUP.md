# Claude Code 全局飞书通知配置指南

## 🎯 目标
让每次使用Claude Code时都自动具备飞书通知功能，无需手动添加代码。

## 📋 配置步骤

### 步骤1: 添加到您的 claudecode.md 文件

将以下内容添加到您的全局 `claudecode.md` 文件中：

```markdown
# Claude Code 飞书通知配置

## 自动通知功能

Claude Code 已集成飞书通知系统，每次任务完成时自动发送通知。

### 通知脚本路径
```bash
通知系统路径: G:/AGI/message-pusher
飞书Webhook: https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49
```

### 自动集成代码

在需要通知的 Claude Code 脚本末尾添加以下代码：

```python
# === Claude Code 飞书通知 ===
import sys, os
sys.path.append("G:/AGI/message-pusher")

try:
    from claude_auto_summarizer import send_conversation_summary
    # 智能分析当前交互并发送通知
    user_request = "描述用户的原始需求"  # 修改为实际用户请求
    claude_response = "描述Claude执行的结果"  # 修改为实际执行结果
    send_conversation_summary(user_request, claude_response)
    print("✓ 飞书通知已发送")
except Exception as e:
    print(f"通知发送失败: {e}")
```

### 快速通知版本

如果只需要简单通知：

```python
import sys, requests, os
sys.path.append("G:/AGI/message-pusher")

task_name = "您的任务描述"  # 修改为实际任务
project_name = os.path.basename(os.getcwd()) or "claude-code"
project_path = os.path.abspath(os.getcwd())

requests.post(
    "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49",
    json={
        "msg_type": "text",
        "content": {
            "task_name": task_name,
            "status": "success",
            "result": "任务执行完成",
            "task_type": "Custom",
            "duration_sec": 0,
            "project_name": project_name,
            "project_path": project_path
        }
    },
    timeout=5
)
```

## 指令说明

- **智能分析**: 自动从对话中提取任务信息
- **项目检测**: 自动识别当前项目名称和路径
- **状态判断**: 根据执行结果智能判断成功/失败状态
- **LLM风格总结**: 生成有意义的结果摘要

## 飞书通知格式

```
ClaudeCode 任务完成通知
项目：your-project-name
目录：/path/to/your/project
任务：具体任务描述
状态：success/failed
结果：详细执行结果
```
```

### 步骤2: 设置环境变量（可选）

为了让路径配置更灵活，可以设置环境变量：

```bash
# Windows
set CLAUDE_NOTIFY_PATH=G:/AGI/message-pusher
set CLAUDE_FEISHU_WEBHOOK=https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49

# macOS/Linux
export CLAUDE_NOTIFY_PATH="G:/AGI/message-pusher"
export CLAUDE_FEISHU_WEBHOOK="https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"
```

### 步骤3: 创建通用通知函数

在您的 claudecode.md 中添加这个通用函数：

```python
def notify_claude_completion(task_description, result_summary="", status="success"):
    """
    通用Claude Code任务完成通知
    """
    import sys, os, requests

    # 获取通知路径
    notify_path = os.environ.get("CLAUDE_NOTIFY_PATH", "G:/AGI/message-pusher")
    webhook_url = os.environ.get("CLAUDE_FEISHU_WEBHOOK",
                                "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49")

    sys.path.append(notify_path)

    try:
        # 方法1: 智能分析
        from claude_auto_summarizer import send_conversation_summary
        send_conversation_summary(task_description, result_summary)
        print("✓ 智能通知发送成功")
    except:
        # 方法2: 直接发送
        try:
            project_name = os.path.basename(os.getcwd()) or "claude-code"
            project_path = os.path.abspath(os.getcwd())

            payload = {
                "msg_type": "text",
                "content": {
                    "task_name": task_description,
                    "status": status,
                    "result": result_summary or "Claude Code任务执行完成",
                    "task_type": "Custom",
                    "duration_sec": 0,
                    "project_name": project_name,
                    "project_path": project_path
                }
            }

            requests.post(webhook_url, json=payload, timeout=5)
            print("✓ 直接通知发送成功")
        except Exception as e:
            print(f"✗ 通知发送失败: {e}")

# 使用示例
# notify_claude_completion("您的任务描述", "执行结果摘要")
```

## 🚀 自动化集成

### 选项1: Hook集成（高级）

如果您想要完全自动化，可以设置Hook：

1. 在您的项目根目录创建 `.claude/hooks/` 目录
2. 创建 `post-execute.py`：

```python
#!/usr/bin/env python3
"""
Claude Code 执行后自动通知Hook
"""
import sys, os

# 添加通知系统路径
sys.path.append("G:/AGI/message-pusher")

try:
    from claude_interaction_hook import analyze_and_notify

    # 从环境变量或参数获取交互信息
    user_input = os.environ.get('CLAUDE_USER_INPUT', '用户执行了Claude Code任务')
    claude_output = os.environ.get('CLAUDE_OUTPUT', 'Claude Code任务执行完成')

    analyze_and_notify(user_input, claude_output)
except Exception as e:
    print(f"Hook通知失败: {e}")
```

### 选项2: 别名集成（简单）

在您的shell配置文件中添加别名：

```bash
# ~/.bashrc 或 ~/.zshrc
alias claude-notify='python G:/AGI/message-pusher/quick_notify_enhanced.py'

# 使用方式
# claude-notify "完成了代码分析任务"
```

## 📱 验证配置

运行以下测试代码验证配置是否正确：

```python
# 测试配置
import sys, os
sys.path.append("G:/AGI/message-pusher")

try:
    from claude_auto_summarizer import send_conversation_summary
    send_conversation_summary(
        "测试Claude Code全局配置",
        "配置验证成功，飞书通知系统正常工作"
    )
    print("✅ 全局配置测试成功！")
except Exception as e:
    print(f"❌ 配置测试失败: {e}")
```

## 🎉 完成

配置完成后，每次在Claude Code中执行任务时，只需在脚本末尾调用：

```python
notify_claude_completion("当前任务描述", "执行结果")
```

就能自动发送包含项目信息的飞书通知！