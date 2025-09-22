# Railway 部署指南

## 🚀 快速部署步骤

### 1. 登录 Railway
```bash
railway login
```
这会打开浏览器，请用 GitHub 账号登录 Railway。

### 2. 初始化项目
```bash
railway init
```
选择 "Empty Project"，给项目起个名字，比如 "message-pusher"。

### 3. 连接到项目
```bash
railway link
```

### 4. 配置环境变量
```bash
# 设置端口（Railway 会自动提供 PORT 变量，但我们手动设置以确保兼容）
railway variables set PORT=8080

# 设置会话密钥（重要！用于安全）
railway variables set SESSION_SECRET=your_super_secret_key_here_change_this

# 设置时区
railway variables set TZ=Asia/Shanghai

# 可选：如果要使用 MySQL 而不是 SQLite
# railway variables set SQL_DSN="mysql_connection_string"
```

### 5. 部署项目
```bash
railway up
```

### 6. 获取域名
```bash
railway domain
```

## 📋 配置文件说明

我已经为你创建了以下配置文件：

- `railway.json` - Railway 部署配置
- `nixpacks.toml` - 构建配置
- `Procfile` - 启动命令
- `VERSION` - 版本号

## 🔧 重要配置

### 环境变量
- `PORT`: 服务端口（Railway 自动设置）
- `SESSION_SECRET`: 会话密钥（必须设置）
- `TZ`: 时区设置
- `SQL_DSN`: 数据库连接（可选，默认使用 SQLite）

### 数据持久化
Railway 提供持久化存储，你的 SQLite 数据库会自动保存在 `/data` 目录。

## 🌐 部署后的使用

部署成功后，你会得到一个域名，类似：
```
https://message-pusher-production-xxxx.railway.app
```

### API 调用示例
```bash
# 测试 API
curl -X POST "https://your-domain.railway.app/push/root" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Railway 部署成功",
    "description": "消息推送服务已上线",
    "content": "🎉 恭喜！你的消息推送服务已成功部署到 Railway！",
    "token": "your_token"
  }'
```

### 登录信息
- 用户名: `root`
- 密码: `123456`
- 记得登录后立即修改密码！

## 🔄 更新部署

当你修改代码后，只需要：
```bash
git add .
git commit -m "更新功能"
railway up
```

## 💰 费用说明

Railway 免费计划包括：
- 每月 $5 使用额度
- 512MB RAM
- 1GB 存储
- 对于个人消息推送服务完全够用

## 🆘 故障排除

### 查看日志
```bash
railway logs
```

### 查看服务状态
```bash
railway status
```

### 重新部署
```bash
railway redeploy
```