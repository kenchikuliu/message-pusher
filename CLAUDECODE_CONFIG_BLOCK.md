# Claude Code 飞书通知 - 全局配置块

## 📋 将以下内容直接复制到您的全局 claudecode.md 文件中

```markdown
# Claude Code 飞书通知系统

## 自动通知配置
Claude Code 已集成飞书通知，每次任务完成时自动发送通知到您的飞书群。

### 通知系统路径
- 系统路径: `G:/AGI/message-pusher`
- 飞书Webhook: `https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49`

### 标准集成方法
在任何Claude Code脚本末尾添加以下代码以启用通知：

```python
# === Claude Code 飞书通知 ===
import sys, os, requests
sys.path.append("G:/AGI/message-pusher")

def send_claude_notification(task_desc, result_summary="任务执行完成", status="success"):
    try:
        # 智能分析方式
        from claude_auto_summarizer import send_conversation_summary
        send_conversation_summary(task_desc, result_summary)
        print("✓ 飞书通知发送成功")
    except:
        # 直接发送方式
        project_name = os.path.basename(os.getcwd()) or "claude-code"
        project_path = os.path.abspath(os.getcwd())

        payload = {
            "msg_type": "text",
            "content": {
                "task_name": task_desc,
                "status": status,
                "result": result_summary,
                "task_type": "Custom",
                "duration_sec": 0,
                "project_name": project_name,
                "project_path": project_path
            }
        }

        try:
            requests.post(
                "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49",
                json=payload, timeout=5
            )
            print("✓ 飞书通知发送成功（直接方式）")
        except Exception as e:
            print(f"✗ 通知发送失败: {e}")

# 调用通知 - 修改为您的实际任务信息
send_claude_notification(
    "描述您执行的任务",
    "任务执行结果摘要"
)
```

### 快速版本（仅3行）
如果只需要最简单的通知：

```python
import requests, os
task = "您的任务描述"; project = os.path.basename(os.getcwd()); path = os.getcwd()
requests.post("https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49", json={"msg_type":"text","content":{"task_name":task,"status":"success","result":"任务完成","project_name":project,"project_path":path}})
```

### 飞书通知格式
您将在飞书中收到格式化的通知：
```
ClaudeCode 任务完成通知
项目：your-project-name
目录：/path/to/project
任务：具体任务描述
状态：success
结果：详细执行结果
```

### 使用指南
1. **每次任务开始时**: 简单描述要执行的任务
2. **任务完成时**: 调用通知函数，描述执行结果
3. **自动检测**: 系统自动检测项目信息和执行状态
4. **智能分析**: LLM风格的结果总结和状态判断

### 验证配置
运行以下代码测试通知系统：

```python
import sys; sys.path.append("G:/AGI/message-pusher")
from claude_auto_summarizer import send_conversation_summary
send_conversation_summary("Claude Code配置测试", "全局通知系统配置成功")
```
```

---

## 🎯 具体操作步骤

### 1. 找到您的 claudecode.md 文件
通常位于：
- Windows: `%USERPROFILE%\.claude\claudecode.md`
- macOS: `~/.claude/claudecode.md`
- Linux: `~/.claude/claudecode.md`

### 2. 将上面的配置块添加到文件末尾

### 3. 设置完成！
以后每次使用Claude Code时，只需在脚本末尾调用：
```python
send_claude_notification("您的任务描述", "执行结果")
```