# 🎯 Claude Code 飞书Flow Hook 使用指南

## ✅ 标准JSON格式

系统完全按照您指定的飞书自动化流程标准格式发送通知：

```json
{
  "msg_type": "text",
  "content": {
    "task_name": "任意任务名",
    "status": "success|failed|running",
    "result": "任意文本摘要（自动截断到800~1000字符）",
    "task_type": "Bash|Write|Edit|Custom",
    "duration_sec": 123
  }
}
```

## 🚀 在Claude Code中使用

### 方法1: Python集成（推荐）

在您的Claude Code脚本中添加：

```python
# 导入Hook模块
from claude_flow_hook import start_claude_task, notify_claude_completion

# 在任务开始时
start_claude_task()

# 在任务完成时
notify_claude_completion(
    "代码分析任务",           # task_name
    "success",              # status: success|failed|running
    "分析了50个文件，发现3个问题",  # result (会自动截断)
    "Custom"                # task_type: Bash|Write|Edit|Custom (可选)
)
```

### 方法2: 便捷函数

```python
from claude_flow_hook import notify_bash_task, notify_write_task, notify_edit_task

# Bash任务
notify_bash_task("npm run build", "success", "构建成功", 0)

# 文件写入
notify_write_task("src/main.py", "success", "创建了主程序文件")

# 文件编辑
notify_edit_task("config.json", "success", "更新了数据库配置")
```

### 方法3: 命令行调用

```bash
cd "G:\AGI\message-pusher"
python claude_flow_hook.py
```

## 📋 字段说明

### task_name
- 任务名称，可以是任意描述
- 示例：`"代码分析"`、`"API接口开发"`、`"单元测试运行"`

### status
- `"success"`: 任务成功完成
- `"failed"`: 任务执行失败
- `"running"`: 任务正在运行中

### result
- 任务结果的详细描述
- 自动截断到900字符以内
- 可以包含任何相关信息

### task_type
- `"Bash"`: Bash命令执行类任务
- `"Write"`: 文件创建/写入类任务
- `"Edit"`: 文件修改/编辑类任务
- `"Custom"`: 自定义任务类型

### duration_sec
- 任务执行时长（秒）
- 自动计算（从start_claude_task开始）

## 🎯 飞书Flow集成

在您的飞书自动化流程中，可以直接引用这些字段：

```
{{content.task_name}}    // 获取任务名
{{content.status}}       // 获取状态
{{content.result}}       // 获取结果描述
{{content.task_type}}    // 获取任务类型
{{content.duration_sec}} // 获取执行时长
```

## 📱 实际使用示例

### 示例1: 代码分析任务

```python
from claude_flow_hook import start_claude_task, notify_claude_completion

start_claude_task()

# 执行代码分析
# ... 您的代码分析逻辑 ...

notify_claude_completion(
    "Python代码质量分析",
    "success",
    "扫描了150个文件，发现5个潜在问题：2个性能优化点，3个代码规范问题",
    "Custom"
)
```

**飞书会收到：**
```json
{
  "msg_type": "text",
  "content": {
    "task_name": "Python代码质量分析",
    "status": "success",
    "result": "扫描了150个文件，发现5个潜在问题：2个性能优化点，3个代码规范问题",
    "task_type": "Custom",
    "duration_sec": 45
  }
}
```

### 示例2: 批量文件处理

```python
from claude_flow_hook import notify_write_task

for i in range(10):
    # 处理文件
    process_file(f"file_{i}.py")

    # 通知每个文件处理完成
    notify_write_task(
        f"processed/file_{i}.py",
        "success",
        f"处理完成，添加了{i*10}行代码"
    )
```

### 示例3: 测试运行

```python
from claude_flow_hook import notify_bash_task

import subprocess

result = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)

notify_bash_task(
    "pytest tests/",
    "success" if result.returncode == 0 else "failed",
    result.stdout + result.stderr,
    result.returncode
)
```

## 🔧 高级用法

### 自定义Webhook URL

```python
from claude_flow_hook import ClaudeFlowHook

# 使用自定义Webhook
hook = ClaudeFlowHook()
hook.webhook_url = "https://your-custom-webhook-url"

hook.send_hook_notification(
    "自定义任务",
    "success",
    "使用自定义Webhook发送"
)
```

### 批量通知

```python
from claude_flow_hook import notify_claude_completion

tasks = [
    ("文件A处理", "success", "处理完成"),
    ("文件B处理", "success", "处理完成"),
    ("文件C处理", "failed", "权限不足")
]

for task_name, status, result in tasks:
    notify_claude_completion(task_name, status, result, "Custom")
```

## 🎊 完整工作流程

```
Claude Code 执行
    ↓
start_claude_task() // 开始计时
    ↓
执行业务逻辑
    ↓
notify_claude_completion() // 发送通知
    ↓
标准JSON格式 → 飞书Webhook
    ↓
飞书自动化流程 (引用content.*)
    ↓
飞书群消息/其他自动化操作
```

## ✅ 验证测试

运行完整测试：

```bash
cd "G:\AGI\message-pusher"
python claude_flow_hook.py
```

您的飞书应该收到4条通知，每条都包含完整的content字段！

---

**🎉 现在您拥有了完全符合飞书Flow标准的Claude Code Hook系统！**

- ✅ 严格按照您指定的JSON结构
- ✅ 支持content.*字段引用
- ✅ 自动任务类型检测
- ✅ 自动时长计算
- ✅ 结果文本自动截断
- ✅ 多种便捷调用方式

享受您的智能飞书Flow集成吧！🚀