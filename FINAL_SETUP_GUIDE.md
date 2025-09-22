# 🎉 飞书推送配置完成指南

## ✅ 已完成的配置

您的消息推送系统已经成功配置了飞书通道！以下步骤已完成：

1. ✅ **消息推送服务运行中** - http://localhost:3000
2. ✅ **推送 Token 已设置** - `claude_task_2025`
3. ✅ **飞书通道已创建** - 系统可以识别飞书通道
4. ✅ **默认通道已设置** - 使用飞书作为默认推送方式
5. ✅ **推送脚本已配置** - `claude_notify.py` 已更新

## 🔧 最后一步：更新 Webhook URL

**当前状态**: 系统配置正确，但使用的是示例 Webhook URL

### 操作步骤

1. **访问管理界面**
   ```
   http://localhost:3000
   ```

2. **登录账户**
   ```
   用户名: root
   密码: 123456
   ```

3. **更新飞书 Webhook URL**
   - 进入 **"推送设置"**
   - 找到 **"feishu"** 通道
   - 点击 **"编辑"**
   - 将 URL 更新为您真实的飞书机器人 Webhook URL
   - 保存设置

4. **测试推送**
   - 在通道设置页面点击 **"测试"** 按钮
   - 或运行命令测试：
     ```bash
     python claude_notify.py "测试完成" "成功" "飞书推送配置成功！"
     ```

## 📱 使用方法

### 基本命令
```bash
# 简单通知
python claude_notify.py "任务完成"

# 带状态的通知
python claude_notify.py "代码分析" "完成"

# 完整通知
python claude_notify.py "数据处理" "完成" "成功处理了1000条记录"

# 带时间的通知
python claude_notify.py "训练模型" "完成" "准确率95%" "2小时"
```

### API 调用
```bash
curl -X POST "http://localhost:3000/push/root" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API测试",
    "description": "任务完成",
    "content": "这是通过API发送的消息",
    "token": "claude_task_2025",
    "channel": "feishu"
  }'
```

## 🔍 故障排除

### 问题1: "incoming webhook access token invalid"
- **原因**: Webhook URL 无效或过期
- **解决**: 在飞书群中重新生成机器人 Webhook URL

### 问题2: 没有收到消息
- **检查项**:
  - 飞书机器人是否已添加到群中
  - Webhook URL 是否正确
  - 机器人安全设置是否配置正确

### 问题3: 消息格式异常
- **确认**: 通道类型应为 `lark`
- **检查**: JSON 格式是否正确

## 📊 推送效果

配置成功后，您将在飞书群收到如下格式的消息：

```
[OK] 代码分析

状态: 完成

**🤖 Claude Code 执行报告**

- **任务**: 代码分析
- **状态**: 完成
- **完成时间**: 2025-09-20 19:10:30
- **详情**: 成功分析了 50 个文件

---
_🔔 来自 Claude Code 自动提醒_
```

## 🚀 下一步

- 将 `claude_notify.py` 脚本路径添加到系统 PATH
- 在其他自动化脚本中集成通知功能
- 设置定时任务完成时的自动提醒

---

**🎯 系统已就绪！只需要更新一个真实的飞书 Webhook URL 即可开始使用！**