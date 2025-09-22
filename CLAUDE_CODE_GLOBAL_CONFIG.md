# Claude Code 全局飞书通知配置

## 🎯 系统概述

Claude Code 已集成智能飞书通知系统，能够自动从对话交互中提取任务信息并发送到飞书群。

## 📋 核心配置

### 飞书Webhook配置
```
Webhook URL: https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49
格式: 飞书自动化流程标准JSON格式
```

### JSON标准格式
```json
{
  "msg_type": "text",
  "content": {
    "task_name": "智能提取的任务名称",
    "status": "success|failed|running",
    "result": "LLM风格分析的结果摘要",
    "task_type": "Custom|Bash|Write|Edit",
    "duration_sec": 自动计算的执行时长,
    "project_name": "自动检测的项目名称",
    "project_path": "项目完整路径"
  }
}
```

## 🚀 使用方法

### 方法1: 智能对话分析（推荐）

在Claude Code脚本中添加：

```python
# 导入智能分析模块
import sys
sys.path.append("G:/AGI/message-pusher")

from claude_auto_summarizer import send_conversation_summary

# 在任务完成时调用
user_input = "用户的原始请求"
claude_output = "Claude的完整回应"

send_conversation_summary(user_input, claude_output)
```

### 方法2: 手动通知

```python
import sys
sys.path.append("G:/AGI/message-pusher")

from claude_notify_final import send_claude_notification

send_claude_notification(
    task_name="任务名称",
    status="success",  # success|failed|running
    result="任务结果描述",
    task_type="Custom",  # Custom|Bash|Write|Edit
    duration_sec=30
)
```

### 方法3: 命令行调用

```bash
# 智能分析方式
python "G:/AGI/message-pusher/claude_auto_summarizer.py" "用户输入" "Claude输出"

# 手动指定方式
python "G:/AGI/message-pusher/claude_notify_final.py" "任务名" "success" "结果" "Custom" 30
```

## 🤖 智能分析能力

### 任务名称智能提取
- 从"帮我..."、"请..."、"我想..."等模式提取任务
- 识别关键概念：docker、飞书、webhook、配置等
- 自动生成有意义的任务名称

### 状态智能判断
- **Success**: "成功"、"完成"、"完美"、"工作正常"
- **Failed**: "失败"、"错误"、"异常"、"无法"
- **Running**: "正在"、"处理中"、"执行中"

### 任务类型自动分类
- **Bash**: 命令行、shell、curl等操作
- **Write**: 文件创建、生成等操作
- **Edit**: 文件修改、更新等操作
- **Custom**: 其他自定义任务

### 结果摘要生成
- 提取关键成就："成功配置"、"创建了"、"修复了"
- 包含行动总结："测试了"、"部署了"、"更新了"
- 添加统计信息：交互次数、执行时长

## 🔧 高级集成

### 装饰器模式

```python
import sys
sys.path.append("G:/AGI/message-pusher")

from claude_interaction_hook import analyze_and_notify

def claude_notify(task_name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                # 自动通知成功
                analyze_and_notify(
                    task_name or f"执行函数: {func.__name__}",
                    f"函数执行成功，返回: {str(result)[:200]}"
                )

                return result
            except Exception as e:
                # 自动通知失败
                analyze_and_notify(
                    task_name or f"执行函数: {func.__name__}",
                    f"函数执行失败: {str(e)}"
                )
                raise
        return wrapper
    return decorator

# 使用示例
@claude_notify("数据处理任务")
def process_data():
    # 您的业务逻辑
    return "处理完成"
```

### 环境变量配置

```bash
# 设置Claude Code通知路径
export CLAUDE_NOTIFY_PATH="G:/AGI/message-pusher"

# 设置webhook URL
export CLAUDE_FEISHU_WEBHOOK="https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49"
```

### 通用集成函数

```python
def notify_claude_task_completion(task_description, output_summary="", status="success"):
    """
    通用的Claude Code任务完成通知函数

    Args:
        task_description: 任务描述
        output_summary: 输出摘要
        status: 执行状态
    """
    import sys
    import os

    notify_path = os.environ.get("CLAUDE_NOTIFY_PATH", "G:/AGI/message-pusher")
    sys.path.append(notify_path)

    try:
        from claude_auto_summarizer import send_conversation_summary
        send_conversation_summary(task_description, output_summary)
    except ImportError:
        print("Claude通知系统未找到，请检查路径配置")
    except Exception as e:
        print(f"发送Claude通知失败: {e}")

# 在任何Claude Code脚本末尾添加：
notify_claude_task_completion(
    "当前脚本执行的任务描述",
    "脚本执行的结果和输出摘要"
)
```

## 📱 飞书Flow字段引用

在飞书自动化流程中，直接引用以下字段：

```
ClaudeCode 任务完成通知
项目：{{content.project_name}}
目录：{{content.project_path}}
任务：{{content.task_name}}
状态：{{content.status}}
结果：{{content.result}}
```

### 完整字段列表：
```
任务名称: {{content.task_name}}
执行状态: {{content.status}}
结果详情: {{content.result}}
任务类型: {{content.task_type}}
执行时长: {{content.duration_sec}}秒
项目名称: {{content.project_name}}
项目路径: {{content.project_path}}
```

## 🛠️ 故障排除

### 1. 通知发送失败
```python
# 测试基础连接
import requests, os
project_name = os.path.basename(os.getcwd()) or "test-project"
project_path = os.path.abspath(os.getcwd())
response = requests.post(
    "https://www.feishu.cn/flow/api/trigger-webhook/e6704c788710bd238211e9d833129b49",
    json={"msg_type":"text","content":{"task_name":"连接测试","status":"success","result":"测试消息","project_name":project_name,"project_path":project_path}},
    timeout=10
)
print(f"状态: {response.status_code}, 响应: {response.text}")
```

### 2. 路径问题
```python
# 确保正确添加路径
import sys
import os

claude_notify_path = "G:/AGI/message-pusher"
if claude_notify_path not in sys.path:
    sys.path.append(claude_notify_path)

# 验证模块可用性
try:
    from claude_auto_summarizer import send_conversation_summary
    print("✓ 智能分析模块加载成功")
except ImportError as e:
    print(f"✗ 模块加载失败: {e}")
```

### 3. 编码问题
```python
# 处理中文编码
import locale
print(f"系统编码: {locale.getpreferredencoding()}")

# 确保UTF-8编码
import sys
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 📊 使用示例

### 代码分析任务
```python
notify_claude_task_completion(
    "Python代码质量分析",
    "扫描了150个文件，发现5个潜在问题：2个性能优化点，3个代码规范问题。生成了详细报告并提供修复建议。"
)
```

### 文件操作任务
```python
notify_claude_task_completion(
    "批量文件处理",
    "成功处理了25个CSV文件，转换为JSON格式，总计处理数据行数：50,000行。所有文件已保存到output目录。"
)
```

### 部署任务
```python
notify_claude_task_completion(
    "Docker应用部署",
    "成功构建Docker镜像，部署到生产环境。服务已启动并通过健康检查，端口3000正常监听。"
)
```

## ⚙️ 性能优化

### 异步通知（避免阻塞）
```python
import threading

def async_notify(task_desc, output_summary):
    """异步发送通知，不阻塞主程序"""
    def send_in_background():
        try:
            notify_claude_task_completion(task_desc, output_summary)
        except Exception as e:
            print(f"后台通知失败: {e}")

    thread = threading.Thread(target=send_in_background)
    thread.daemon = True
    thread.start()

# 使用异步通知
async_notify("任务描述", "输出摘要")
```

### 批量通知
```python
def batch_notify(notifications):
    """批量发送通知"""
    for task_desc, output_summary in notifications:
        notify_claude_task_completion(task_desc, output_summary)
        time.sleep(0.5)  # 避免频率限制

# 批量使用
notifications = [
    ("文件A处理", "处理完成"),
    ("文件B处理", "处理完成"),
    ("文件C处理", "发现错误")
]
batch_notify(notifications)
```

---

## 🎉 总结

Claude Code 飞书通知系统特点：
- ✅ **零配置**: 开箱即用，自动智能分析
- ✅ **多方式**: 支持智能分析、手动指定、命令行调用
- ✅ **高兼容**: 严格符合飞书Flow标准JSON格式
- ✅ **智能化**: LLM风格的任务理解和状态判断
- ✅ **易集成**: 一行代码即可添加到任何Claude Code脚本

将此配置添加到您的claudecode.md后，每个Claude Code任务都能自动生成有价值的飞书通知！🚀