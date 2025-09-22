#!/usr/bin/env python3
"""
配置Claude Code全局环境变量
让每次Claude Code执行都能自动发送通知
"""

import os
import sys
import subprocess
import platform

def get_current_script_dir():
    """获取当前脚本所在目录"""
    return os.path.dirname(os.path.abspath(__file__))

def setup_windows_env():
    """配置Windows环境变量"""
    script_dir = get_current_script_dir()
    notify_script = os.path.join(script_dir, "claude_notify_global.py")

    print("=== 配置Windows全局环境变量 ===")
    print(f"脚本路径: {notify_script}")

    # 配置环境变量
    env_vars = {
        "CLAUDE_NOTIFY_SCRIPT": notify_script,
        "CLAUDE_NOTIFY_API": "http://localhost:3000/push/root",
        "CLAUDE_NOTIFY_TOKEN": "claude_task_2025",
        "CLAUDE_NOTIFY_CHANNEL": "feishu"
    }

    print("\n设置环境变量:")
    for key, value in env_vars.items():
        try:
            # 设置用户环境变量（永久）
            subprocess.run([
                "setx", key, value
            ], check=True, capture_output=True)
            print(f"  {key} = {value}")
        except subprocess.CalledProcessError as e:
            print(f"  错误设置 {key}: {e}")

    # 创建快捷命令
    create_claude_command_script(script_dir)

    print("\n✅ Windows环境变量配置完成!")
    print("重启命令行后可以使用以下命令:")
    print("  claude-notify \"任务名\" [状态] [详情] [耗时]")

def create_claude_command_script(script_dir):
    """创建claude-notify命令脚本"""

    # 创建.bat文件
    bat_content = f'''@echo off
python "{os.path.join(script_dir, 'claude_notify_global.py')}" %*
'''

    bat_file = os.path.join(script_dir, "claude-notify.bat")
    with open(bat_file, 'w', encoding='utf-8') as f:
        f.write(bat_content)

    print(f"\n创建命令脚本: {bat_file}")
    print("将此目录添加到PATH中，即可在任何位置使用claude-notify命令")

def create_claude_env_file():
    """创建.env文件用于配置"""
    script_dir = get_current_script_dir()
    env_file = os.path.join(script_dir, ".claude_env")

    env_content = f'''# Claude Code 全局通知配置
# Message Pusher API配置
MESSAGE_PUSHER_API=http://localhost:3000/push/root
CLAUDE_TASK_TOKEN=claude_task_2025
FEISHU_CHANNEL=feishu

# 通知脚本路径
CLAUDE_NOTIFY_SCRIPT={os.path.join(script_dir, "claude_notify_global.py")}

# 启用状态
CLAUDE_NOTIFY_ENABLED=true

# 使用说明:
# 在Claude Code中调用: python %CLAUDE_NOTIFY_SCRIPT% "任务名" "状态" "详情" "耗时"
# 或使用: claude-notify "任务名" "状态" "详情" "耗时"
'''

    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)

    print(f"创建配置文件: {env_file}")

def test_notification_setup():
    """测试通知设置"""
    script_dir = get_current_script_dir()
    notify_script = os.path.join(script_dir, "claude_notify_global.py")

    print("\n=== 测试通知系统 ===")

    try:
        result = subprocess.run([
            sys.executable, notify_script,
            "Claude Code全局通知配置",
            "完成",
            "环境变量和脚本配置成功",
            "30秒"
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ 通知测试成功!")
            print("输出:", result.stdout.strip())
        else:
            print("❌ 通知测试失败!")
            print("错误:", result.stderr.strip())
    except Exception as e:
        print(f"❌ 测试异常: {e}")

def create_usage_guide():
    """创建使用指南"""
    script_dir = get_current_script_dir()
    guide_file = os.path.join(script_dir, "CLAUDE_NOTIFY_USAGE.md")

    guide_content = '''# Claude Code 全局通知使用指南

## 配置完成后的使用方式

### 1. 直接调用Python脚本
```bash
python claude_notify_global.py "任务名" [状态] [详情] [耗时]
```

### 2. 使用快捷命令（需要将目录添加到PATH）
```bash
claude-notify "任务名" [状态] [详情] [耗时]
```

### 3. 在Claude Code中集成
将以下代码添加到您的Claude Code工作流中：

```python
import subprocess
import os

def notify_claude_completion(task, status="完成", details="", duration=""):
    """Claude Code完成通知"""
    script = os.environ.get("CLAUDE_NOTIFY_SCRIPT")
    if script and os.path.exists(script):
        try:
            subprocess.run([
                "python", script, task, status, details, duration
            ], check=True)
        except Exception as e:
            print(f"通知发送失败: {e}")

# 使用示例
notify_claude_completion(
    "代码分析任务",
    "成功完成",
    "分析了50个文件，发现3个优化点",
    "2分30秒"
)
```

## 环境变量

- `CLAUDE_NOTIFY_SCRIPT`: 通知脚本路径
- `CLAUDE_NOTIFY_API`: Message Pusher API地址
- `CLAUDE_NOTIFY_TOKEN`: 认证Token
- `CLAUDE_NOTIFY_CHANNEL`: 通知渠道名

## 示例

```bash
# 基本通知
claude-notify "代码重构完成"

# 带状态通知
claude-notify "单元测试" "成功"

# 完整通知
claude-notify "API接口开发" "完成" "实现了用户管理相关的5个接口" "3小时"
```

## 任务类型自动检测

系统会根据任务名自动检测类型：
- 代码分析: 分析、检查、扫描、review
- 代码生成: 生成、创建、build、构建
- 代码重构: 重构、优化、refactor
- bug修复: 修复、fix、bug、错误
- 测试: 测试、test、验证
- 部署: 部署、deploy、发布
- 其他: 其他任务

通知会自动发送到您配置的飞书群！
'''

    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print(f"创建使用指南: {guide_file}")

def main():
    """主函数"""
    print("=== Claude Code 全局通知环境配置 ===")
    print("配置完成后，每次Claude Code执行都可以自动发送通知到飞书")

    # 检查系统
    system = platform.system()
    print(f"系统: {system}")

    if system == "Windows":
        # 创建配置文件
        create_claude_env_file()

        # 配置环境变量
        setup_windows_env()

        # 创建使用指南
        create_usage_guide()

        # 测试通知
        test_notification_setup()

        print("\n🎉 配置完成!")
        print("\n📋 下一步:")
        print("1. 重启命令行或IDE")
        print("2. 确保Message Pusher服务运行在localhost:3000")
        print("3. 在Claude Code中使用环境变量CLAUDE_NOTIFY_SCRIPT调用通知")
        print("4. 查看CLAUDE_NOTIFY_USAGE.md了解详细使用方法")

    else:
        print(f"暂不支持 {system} 系统的自动配置")
        print("请手动设置相关环境变量和脚本")

if __name__ == "__main__":
    main()