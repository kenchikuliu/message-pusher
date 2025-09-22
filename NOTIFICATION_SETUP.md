# 🔔 任务完成提醒配置指南

## 🎯 目标
配置消息推送服务，让它在任务完成后自动提醒你。

## 📱 第一步：配置推送通道

### 1. 访问 Web 界面
打开：http://localhost:3000
登录：用户名 `root`，密码 `123456`

### 2. 配置推送 Token
1. 进入 **推送设置**
2. 设置 **推送 Token**：`claude_task_2025`
3. 保存设置

### 3. 选择推送方式（任选一种）

#### 🔰 **方案A：邮件推送（最简单）**
1. **系统设置** → **SMTP 配置**：
   ```
   SMTP 服务器: smtp.qq.com
   端口: 587
   用户名: your_email@qq.com
   密码: QQ邮箱授权码
   发件人: your_email@qq.com
   ```
2. **个人设置** → **绑定邮箱**：输入你的邮箱
3. **推送设置** → **默认推送方式**：选择 "邮件"
4. 点击 **测试** 验证

#### 🔰 **方案B：飞书群推送（推荐）**
1. 在飞书群中添加机器人，获取 Webhook URL
2. **推送设置** → **添加飞书通道**：
   ```
   通道名称: 飞书提醒
   Webhook URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
   ```
3. **设为默认通道**
4. 点击 **测试** 验证

#### 🔰 **方案C：微信推送**
1. 申请微信测试号：https://developers.weixin.qq.com/sandbox
2. **推送设置** → **添加微信测试号**：
   ```
   AppID: wxxxxxxxxxxx
   AppSecret: xxxxxxxxxxxxxxxx
   模板ID: xxxxxxxxxxxxxxxx
   用户OpenID: xxxxxxxxxxxxxxxx
   ```

## 🛠️ 第二步：创建提醒脚本

### Windows 通用脚本
```batch
@echo off
set SERVER=http://localhost:3000
set USERNAME=root
set TOKEN=claude_task_2025

curl -s -X POST "%SERVER%/push/%USERNAME%" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"%1\",\"description\":\"%2\",\"content\":\"%3\",\"token\":\"%TOKEN%\"}"

echo 提醒已发送
```
**保存为**：`send_notification.bat`

### Python 脚本（推荐）
```python
import requests
import sys
from datetime import datetime

def send_notification(title, description, content=""):
    data = {
        "title": title,
        "description": description,
        "content": content,
        "token": "claude_task_2025"
    }

    try:
        response = requests.post('http://localhost:3000/push/root', json=data)
        result = response.json()
        if result.get('success'):
            print("✅ 提醒发送成功")
        else:
            print(f"❌ 发送失败: {result.get('message')}")
    except Exception as e:
        print(f"❌ 发送失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        title = sys.argv[1]
        desc = sys.argv[2]
        content = sys.argv[3] if len(sys.argv) > 3 else ""
        send_notification(title, desc, content)
    else:
        send_notification("🤖 Claude Code 完成", "任务执行完成", f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```
**保存为**：`send_notification.py`

## 🎮 第三步：使用方法

### 手动测试
```bash
# 使用 Python 脚本
python send_notification.py "测试标题" "测试内容"

# 使用 curl 直接调用
curl -X POST "http://localhost:3000/push/root" \
  -H "Content-Type: application/json" \
  -d '{"title":"测试","description":"任务完成","token":"claude_task_2025"}'
```

### 在其他脚本中集成
```python
# 在你的 Python 代码最后添加
import subprocess
subprocess.run(['python', 'send_notification.py', '训练完成', f'模型准确率: {accuracy}'])
```

```bash
# 在 bash 脚本最后添加
python send_notification.py "脚本执行完成" "GitHub Star 检查完成"
```

### Claude Code 任务完成自动提醒
```python
# 保存为 claude_notify.py
import requests

def notify_claude_completion(task_name="Claude Code 任务", status="完成", details=""):
    message = {
        "title": f"🤖 {task_name}",
        "description": f"状态: {status}",
        "content": f"""**Claude Code 执行报告**

- **任务**: {task_name}
- **状态**: {status}
- **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **详情**: {details}

---
_来自 Claude Code 自动提醒_""",
        "token": "claude_task_2025"
    }

    requests.post('http://localhost:3000/push/root', json=message)

# 使用示例
notify_claude_completion("代码分析", "完成", "成功分析了 50 个文件")
```

## 🚀 第四步：自动化集成

### 1. 环境变量设置
```bash
# 添加到系统环境变量
set NOTIFICATION_SERVER=http://localhost:3000/push/root
set NOTIFICATION_TOKEN=claude_task_2025
```

### 2. 快捷命令
将脚本路径添加到 PATH，这样就可以在任何地方使用：
```bash
# 任何地方都可以调用
send_notification.py "任务完成" "详细信息"
```

## 📋 配置检查清单

- [ ] 消息推送服务运行正常 (http://localhost:3000)
- [ ] 已设置推送 Token: `claude_task_2025`
- [ ] 已配置至少一种推送通道（邮件/微信/飞书）
- [ ] 推送通道测试成功
- [ ] 提醒脚本创建完成
- [ ] 手动测试推送成功

## 🎉 完成后的效果

配置完成后，你将收到：
- 📧 **邮件提醒**：详细的任务完成报告
- 📱 **即时通知**：微信/飞书群消息
- 🕐 **实时反馈**：任务完成立即知道
- 📊 **执行记录**：所有提醒都有历史记录