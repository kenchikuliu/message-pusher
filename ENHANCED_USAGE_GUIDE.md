# 🚀 Claude Code 增强提醒系统使用指南

## 📋 概述

增强版 `claude_notify_enhanced.py` 提供了丰富的任务类型支持和详细的执行信息展示，让您能更好地跟踪 Claude Code 的工作进展。

## 🎯 主要特性

- 🏷️ **任务类型分类**：支持16种常用任务类型，每种都有专属图标
- 📊 **详细执行信息**：显示 Claude Code 具体执行了什么操作
- ⏱️ **执行时长跟踪**：记录任务耗时
- 🎨 **智能状态识别**：自动识别成功/失败/警告状态并设置对应颜色
- 📁 **环境信息**：自动包含工作目录信息
- 🔧 **预定义函数**：为常用场景提供便捷的调用方式

## 📝 支持的任务类型

| 任务类型 | 图标 | 适用场景 |
|---------|------|---------|
| 代码分析 | 🔍 | 代码质量检查、静态分析 |
| 代码生成 | ✨ | 自动生成代码、模板创建 |
| 代码重构 | 🔧 | 代码优化、重构改进 |
| bug修复 | 🐛 | 问题修复、错误处理 |
| 测试 | 🧪 | 单元测试、集成测试 |
| 部署 | 🚀 | 应用部署、发布 |
| 文档 | 📝 | 文档生成、说明编写 |
| 数据处理 | 📊 | 数据分析、ETL操作 |
| 文件操作 | 📁 | 文件管理、批量处理 |
| 网络请求 | 🌐 | API调用、网络操作 |
| 数据库 | 🗃️ | 数据库操作、迁移 |
| AI训练 | 🤖 | 模型训练、机器学习 |
| 脚本执行 | ⚡ | 脚本运行、自动化 |
| 系统配置 | ⚙️ | 环境配置、系统设置 |
| 安全检查 | 🔒 | 安全扫描、漏洞检测 |
| 性能优化 | ⚡ | 性能调优、优化改进 |

## 🎮 使用方法

### 基础用法

```bash
# 最简单的使用
python claude_notify_enhanced.py "任务完成"

# 指定任务类型
python claude_notify_enhanced.py "代码分析" "代码分析"

# 包含状态
python claude_notify_enhanced.py "代码分析" "代码分析" "完成"

# 包含执行内容
python claude_notify_enhanced.py "代码分析" "代码分析" "完成" "分析了50个Python文件"

# 完整信息
python claude_notify_enhanced.py "代码分析" "代码分析" "完成" "分析了50个Python文件，发现3个问题" "建议优化性能" "2分钟30秒"
```

### 高级用法示例

```bash
# 代码重构完成
python claude_notify_enhanced.py \
  "用户认证模块重构" \
  "代码重构" \
  "完成" \
  "重构了登录验证逻辑，优化了数据库查询，添加了Redis缓存" \
  "性能提升40%，代码行数减少200行" \
  "3小时15分钟"

# 安全检查警告
python claude_notify_enhanced.py \
  "安全漏洞扫描" \
  "安全检查" \
  "警告" \
  "扫描了整个项目，发现3个中等风险漏洞" \
  "包括SQL注入和XSS风险，建议立即修复"

# Bug修复失败
python claude_notify_enhanced.py \
  "内存泄漏修复" \
  "bug修复" \
  "失败" \
  "尝试修复内存泄漏问题" \
  "需要更深入的分析，可能涉及第三方库"
```

## 🛠️ 预定义函数

### 代码分析
```python
from claude_notify_enhanced import notify_code_analysis

notify_code_analysis(
    files_analyzed=50,    # 分析的文件数
    issues_found=3,       # 发现的问题数
    duration="2分钟30秒", # 执行时长
    additional_info="发现性能和规范问题"  # 额外信息
)
```

### 代码生成
```python
from claude_notify_enhanced import notify_code_generation

notify_code_generation(
    files_created=5,      # 创建的文件数
    lines_generated=500,  # 生成的代码行数
    duration="1分钟",
    additional_info="生成了完整的REST API"
)
```

### Bug修复
```python
from claude_notify_enhanced import notify_bug_fix

notify_bug_fix(
    bugs_fixed=3,         # 修复的Bug数
    files_modified=8,     # 修改的文件数
    duration="45分钟",
    additional_info="修复了登录、支付和数据同步问题"
)
```

### 测试执行
```python
from claude_notify_enhanced import notify_test_execution

notify_test_execution(
    tests_run=120,        # 运行的测试数
    tests_passed=118,     # 通过的测试数
    duration="5分钟",
    additional_info="单元测试覆盖率达到85%"
)
```

### 部署操作
```python
from claude_notify_enhanced import notify_deployment

notify_deployment(
    environment="生产环境",  # 部署环境
    services_deployed=3,    # 部署的服务数
    duration="10分钟",
    additional_info="包括API、前端和数据库"
)
```

## 🎨 状态类型和颜色

| 状态关键字 | 图标 | 卡片颜色 | 示例 |
|-----------|------|---------|------|
| 完成/成功/success | ✅ | 绿色 | "完成"、"成功"、"success" |
| 失败/错误/error/fail | ❌ | 红色 | "失败"、"错误"、"error" |
| 进行/运行/执行/running | 🔄 | 蓝色 | "进行中"、"running" |
| 警告/warning | ⚠️ | 橙色 | "警告"、"warning" |
| 其他 | 📋 | 蓝色 | 任何其他状态 |

## 📊 消息格式示例

您的飞书群将收到如下格式的卡片消息：

```
🔧 Claude Code - 用户认证模块重构
[绿色卡片]

🔧 任务名称: 用户认证模块重构
🏷️ 任务类型: 代码重构
✅ 执行状态: 完成
⏰ 完成时间: 2025-09-20 19:30:15
⏱️ 执行时长: 3小时15分钟

🔧 Claude Code 执行内容:
重构了登录验证逻辑，优化了数据库查询，添加了Redis缓存

📝 详细信息:
性能提升40%，代码行数减少200行

📁 工作目录: `G:\AGI\message-pusher`

---
🤖 来自 Claude Code 自动提醒系统
```

## 🔗 集成到其他脚本

### Python脚本集成
```python
import subprocess
import time

start_time = time.time()

# 你的代码逻辑...
files_processed = 100
errors_found = 2

# 计算执行时间
duration = f"{int(time.time() - start_time)}秒"

# 发送通知
subprocess.run([
    'python', 'claude_notify_enhanced.py',
    '数据处理任务',           # 任务名称
    '数据处理',               # 任务类型
    '完成' if errors_found == 0 else '警告',  # 状态
    f'处理了{files_processed}个文件',        # 执行内容
    f'发现{errors_found}个问题' if errors_found > 0 else '处理完成，无错误',  # 详细信息
    duration                  # 执行时长
])
```

### 批处理集成
```batch
@echo off
set start_time=%time%

rem 你的批处理逻辑...

python claude_notify_enhanced.py ^
  "批处理任务" ^
  "脚本执行" ^
  "完成" ^
  "执行了文件备份和清理操作" ^
  "备份了500MB数据，清理了临时文件"
```

## 🎯 最佳实践

1. **任务开始时**：可以发送"运行中"状态
2. **任务完成时**：包含详细的执行结果
3. **出现错误时**：使用"失败"状态并说明具体问题
4. **长时间任务**：记录执行时长
5. **重要任务**：包含更多上下文信息

---

**🎉 使用增强版推送系统，让您的 Claude Code 工作进展一目了然！**