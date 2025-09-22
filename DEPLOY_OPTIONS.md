# 🚀 三种超简单部署方案

## 方案1：Render.com 一键部署（最推荐）

### 步骤：
1. **访问**: https://render.com
2. **注册**: 用 GitHub 账号登录
3. **创建服务**:
   - 点击 "New Web Service"
   - 选择 "Deploy an existing image from a registry"
   - 输入镜像: `justsong/message-pusher:latest`
4. **配置**:
   - Name: `message-pusher`
   - Region: `Oregon`
   - Instance Type: `Free`
   - 添加环境变量:
     ```
     TZ = Asia/Shanghai
     SESSION_SECRET = your_random_secret_123456
     ```
5. **部署**: 点击 "Create Web Service"

**结果**: 5分钟后获得免费域名 `https://message-pusher-xxxx.onrender.com`

---

## 方案2：Railway Web 界面部署

### 步骤：
1. **访问**: https://railway.app
2. **登录**: GitHub 账号
3. **部署**:
   - 点击 "Deploy from Docker Image"
   - 输入: `justsong/message-pusher:latest`
   - 设置环境变量:
     ```
     SESSION_SECRET=your_secret_key
     TZ=Asia/Shanghai
     ```
4. **获取域名**: 在 Settings → Domains 添加域名

**结果**: 获得域名 `https://xxx.railway.app`

---

## 方案3：Fly.io 简单部署

### 步骤：
1. **安装 Fly CLI**:
   ```bash
   # Windows
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **登录并部署**:
   ```bash
   fly auth login
   fly launch --image justsong/message-pusher:latest
   ```

**结果**: 全球CDN加速的域名

---

## 🎯 推荐选择

| 平台 | 免费额度 | 部署难度 | 推荐指数 |
|------|----------|----------|----------|
| **Render** | 750小时/月 | ⭐ | ⭐⭐⭐⭐⭐ |
| **Railway** | $5额度/月 | ⭐⭐ | ⭐⭐⭐⭐ |
| **Fly.io** | 3个小应用 | ⭐⭐⭐ | ⭐⭐⭐ |

## 💡 部署后的使用

无论选择哪种方案，部署成功后：

1. **访问Web界面**: `https://your-domain.com`
2. **默认登录**: 用户名 `root`，密码 `123456`
3. **API调用**:
   ```bash
   curl -X POST "https://your-domain.com/push/root" \
     -d "title=测试&description=部署成功&token=your_token"
   ```

## 🚨 重要提醒

1. **立即修改密码**: 登录后在用户管理中修改
2. **设置推送Token**: 在推送设置中配置API鉴权
3. **配置推送渠道**: 添加微信、邮件等推送方式