# Claude Code 飞书通知 - 快速集成

## 🚀 一键添加通知（复制粘贴即用）

在任何Claude Code脚本末尾添加以下代码：

```python
# === Claude Code 飞书通知 ===
def notify_completion(task_desc="Claude Code任务", result_summary=""):
    import sys, requests, os
    sys.path.append("G:/AGI/message-pusher")

    try:
        from claude_auto_summarizer import send_conversation_summary
        send_conversation_summary(task_desc, result_summary or "任务执行完成")
        print("✓ 飞书通知已发送")
    except:
        # 备用直接发送方式（含项目信息）
        import os
        import json

        # 自动检测项目信息
        current_dir = os.getcwd()
        project_path = os.path.abspath(current_dir)
        project_name = os.path.basename(current_dir) or "claude-code"

        # 尝试从package.json获取项目名
        package_json = os.path.join(current_dir, 'package.json')
        if os.path.exists(package_json):
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'name' in data:
                        project_name = data['name']
            except:
                pass

        payload = {
            "msg_type": "text",
            "content": {
                "task_name": task_desc,
                "status": "success",
                "result": result_summary or "Claude Code任务执行完成",
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
            print("✓ 飞书通知已发送（备用方式）")
        except:
            print("✗ 飞书通知发送失败")

# 调用通知（修改任务描述）
notify_completion(
    "您的任务描述",  # 修改为实际任务描述
    "任务执行结果摘要"    # 修改为实际结果摘要
)
```

## 📋 使用示例

### 代码分析脚本
```python
# 您的代码分析逻辑
def analyze_code():
    # ... 分析逻辑 ...
    return "发现3个问题，已生成报告"

result = analyze_code()

# 添加通知
notify_completion("Python代码质量分析", f"分析完成：{result}")
```

### 文件处理脚本
```python
# 您的文件处理逻辑
processed_files = process_batch_files()

# 添加通知
notify_completion("批量文件处理", f"成功处理{len(processed_files)}个文件")
```

### 数据库操作脚本
```python
# 您的数据库操作
records = update_database()

# 添加通知
notify_completion("数据库更新", f"更新了{records}条记录")
```

## 🎯 飞书接收格式

您的飞书会收到如下格式的消息：

```
ClaudeCode 任务完成通知
项目：my-app
目录：/Users/xxx/work/my-app
任务：Python代码质量分析
状态：success
结果：分析完成：发现3个问题，已生成报告
```

## ⚡ 超简版（仅3行代码）

如果只需要最基本的通知：

```python
import requests, os
task_name = "您的任务名称"  # 修改这里
project_name = os.path.basename(os.getcwd()) or "claude-code"
project_path = os.path.abspath(os.getcwd())
requests.post("https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49", json={"msg_type":"text","content":{"task_name":task_name,"status":"success","result":"任务完成","project_name":project_name,"project_path":project_path}})
```

---

**📱 配置完成后，每次Claude Code执行都会自动发送通知到您的飞书！**