# 🚀 博客系统后端 API

这是一个使用 FastAPI 构建的现代化博客 API 系统，提供了丰富的功能和优秀的性能表现。作为博客平台的核心引擎，它支持从用户管理到内容发布的全方位功能。

## ✨ 功能特性

- 👤 **用户管理** - 注册、登录、权限控制和角色管理
- 📧 **邮箱验证** - 安全的邮箱验证码注册功能
- 📝 **文章管理** - 创建、编辑、发布和版本控制
- 💬 **评论系统** - 多级评论、点赞和审核功能
- 🏷️ **分类与标签** - 灵活的内容组织和管理
- 📊 **数据统计** - 访问量、热门文章和用户活跃度分析
- 📁 **文件管理** - 图片和文件的上传、存储和管理
- 📋 **备忘录系统** - 支持加密的个人笔记功能
- 🔔 **通知系统** - 实时通知和邮件提醒
- 📈 **活动记录** - 详细的用户行为跟踪
- 🔍 **全文搜索** - 高效的内容检索功能
- 🤖 **AI 辅助** - 自动生成文章摘要和标签

## 🗂️ 项目结构

```text
blog/
├── app/                    # 应用主目录
│   ├── core/               # 核心配置
│   │   ├── cache.py        # 缓存配置
│   │   ├── config.py       # 应用配置
│   │   ├── database.py     # 数据库配置
│   │   ├── permissions.py  # 权限控制
│   │   └── security.py     # 安全和认证
│   ├── models/             # 数据库模型
│   │   ├── activity.py     # 活动记录模型
│   │   ├── article.py      # 文章和分类模型
│   │   ├── comment.py      # 评论模型
│   │   ├── subscription.py # 订阅模型
│   │   ├── user.py         # 用户模型
│   │   ├── version.py      # 版本控制模型
│   │   ├── memo.py         # 备忘录模型
│   │   └── __init__.py     # 模型初始化
│   ├── schemas/            # Pydantic模式
│   │   ├── activity.py     # 活动相关模式
│   │   ├── ai_assist.py    # AI辅助相关模式
│   │   ├── article.py      # 文章相关模式
│   │   ├── comment.py      # 评论相关模式
│   │   ├── memo.py         # 备忘录相关模式
│   │   ├── subscription.py # 订阅相关模式
│   │   ├── tag.py          # 标签相关模式
│   │   ├── token.py        # 认证令牌模式
│   │   ├── user.py         # 用户相关模式
│   │   └── __init__.py     # 模式初始化
│   ├── services/           # 业务逻辑服务
│   │   ├── activity_service.py    # 活动服务
│   │   ├── article_service.py     # 文章服务
│   │   ├── comment_service.py     # 评论服务
│   │   ├── memo_service.py        # 备忘录服务
│   │   ├── subscription_service.py # 订阅服务
│   │   ├── tag_service.py         # 标签服务
│   │   ├── user_service.py        # 用户服务
│   │   └── __init__.py            # 服务初始化
│   ├── routers/            # API路由
│   │   ├── activities.py   # 活动路由
│   │   ├── admin.py        # 管理员路由
│   │   ├── articles.py     # 文章路由
│   │   ├── auth.py         # 认证路由
│   │   ├── categories.py   # 分类路由
│   │   ├── comments.py     # 评论路由
│   │   ├── files.py        # 文件路由
│   │   ├── memos.py        # 备忘录路由
│   │   ├── search.py       # 搜索路由
│   │   ├── stats.py        # 统计路由
│   │   ├── tags.py         # 标签路由
│   │   ├── users.py        # 用户路由
│   │   └── __init__.py     # 路由初始化
│   ├── utils/              # 工具函数
│   │   ├── logging.py      # 日志工具
│   │   ├── pagination.py   # 分页工具
│   │   ├── ip_utils.py     # IP工具
│   │   └── __init__.py     # 工具初始化
│   ├── main.py             # 应用入口
│   └── __init__.py         # 应用初始化
├── static/                 # 静态文件
│   ├── images/             # 上传的图片
│   └── files/              # 上传的文件
├── .env                    # 环境变量
└── requirements.txt        # 依赖列表
```

## 🛠️ 技术栈

- ⚡ **FastAPI** - 现代、高性能的 Web 框架
- 🗃️ **SQLAlchemy** - 强大的 ORM 工具
- 📊 **Pydantic** - 数据验证和设置管理
- 🔐 **JWT** - 安全的用户认证
- 🗄️ **MySQL/SQLite** - 灵活的数据存储选项
- 🔄 **Redis** - 缓存和 WebSocket 支持
- 📧 **Resend** - 邮件发送服务
- 🤖 **OpenRouter** - AI 辅助功能
- 🔍 **全文搜索** - 基于数据库的搜索功能
- 🌐 **WebSocket** - 实时通知和状态更新

## 🔍 API 文档与测试

### 使用 Swagger UI 进行接口测试

1. 访问 API 文档：[http://localhost:8000/docs](http://localhost:8000/docs)

2. 获取 JWT 令牌：
   - 点击 `/auth/login` 接口
   - 点击 "Try it out" 按钮
   - 输入用户名和密码
   - 点击 "Execute" 按钮
   - 从响应中复制 `access_token` 的值

3. 使用 JWT 令牌进行授权：
   - 点击 Swagger UI 界面右上角的 "Authorize" 按钮
   - 在弹出的对话框中，输入 `Bearer` 加上空格，然后粘贴你的令牌
     例如：`Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - 点击 "Authorize" 按钮

## 🚀 安装和运行

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/blog-api.git
cd blog-api
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 配置环境变量

创建一个`.env`文件，包含以下内容：

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/blog
SECRET_KEY=your-secret-key-change-in-production
HOST=127.0.0.1
PORT=8000
RELOAD=True
WORKERS=1
TRUSTED_HOSTS=127.0.0.1,localhost,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16

# 邮件配置（用于邮箱验证功能）
RESEND_API_KEY=re_your_resend_api_key
SITE_NAME=BrownLu的博客
EMAIL_FROM=noreply@yourdomain.com
```

### 4. 运行应用

使用提供的启动脚本运行应用，它会正确配置代理头处理：

```bash
python run.py
```

或者直接使用 uvicorn 命令（不推荐，因为没有配置代理头处理）：

```bash
uvicorn app.main:app --reload
```

### 5. 访问 API 文档

打开浏览器访问 [http://localhost:8000/docs](http://localhost:8000/docs)

## 💻 代码风格和最佳实践

- 🧩 **依赖注入模式** - 清晰的服务和数据库访问
- 🔄 **业务逻辑分离** - 路由与服务层明确分离
- ✅ **数据验证** - 使用 Pydantic 模型进行严格验证
- 🛡️ **统一错误处理** - 一致的错误响应格式
- 📊 **分页和过滤** - 支持高效的数据检索
- 📝 **详细日志记录** - 便于问题排查和监控
- 🔒 **安全最佳实践** - JWT 认证和密码哈希

## 🌐 配置前端代理服务器

如果你使用 Nginx、Apache 或其他代理服务器作为前端，需要确保它们正确转发客户端 IP 地址。

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Apache 配置示例

```apache
<VirtualHost *:80>
    ServerName yourdomain.com

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    RequestHeader set X-Forwarded-For %{REMOTE_ADDR}s
    RequestHeader set X-Forwarded-Proto %{REQUEST_SCHEME}s
</VirtualHost>
```

## 🤖 AI 辅助功能

### 自动摘要与标签生成

接收文章正文内容，自动生成摘要（150字内）和3-5个标签，帮助作者快速完成内容整理。

### API 详情

#### 请求方式

```http
POST /articles/ai-assist
```

#### 请求头

```http
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

#### 请求体示例

```json
{
  "content": "文章正文内容（不少于50字）"
}
```

#### 响应示例

```json
{
  "excerpt": "文章摘要内容...",
  "tags": ["标签1", "标签2", "标签3"]
}
```

#### 认证方式

使用JWT Bearer令牌，需在Authorization头中携带有效token

#### 错误代码

- 401 Unauthorized: 缺少或无效的认证信息
- 500 Internal Server Error: 服务器配置错误
- 503 Service Unavailable: AI服务不可用

#### 调用示例（cURL）

```bash
curl -X POST http://localhost:8000/articles/ai-assist \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{"content": "你的文章内容..."}'
```

### 配置说明

1. 需在`.env`文件中配置有效的`OPENROUTER_API_KEY`
2. 文章内容需不少于50个字符
3. 确保服务端已安装python-dotenv依赖
4. API密钥请妥善保管，不要提交到版本库

## 📧 邮箱验证功能

### 功能概述

系统支持用户注册时进行邮箱验证，提高账户安全性。管理员可以在系统设置中开启或关闭此功能。

### 配置步骤

1. 在 `.env` 文件中配置以下参数：

   ```env
   RESEND_API_KEY=re_your_resend_api_key  # 从 Resend.com 获取
   SITE_NAME=您的网站名称
   EMAIL_FROM=noreply@yourdomain.com      # 发件人邮箱
   ```

2. 运行数据库迁移脚本添加必要的字段：

   ```bash
   python -m migrations.add_email_verification
   ```

3. 在管理后台的系统设置中开启"要求邮箱验证"选项。

### API 接口

#### 发送验证码

```http
POST /api/v1/email/send-verification
Content-Type: application/json

{
  "email": "user@example.com"
}
```

#### 验证验证码

```http
POST /api/v1/email/verify-code
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456"
}
```

### 使用说明

- 验证码有效期为10分钟
- 同一邮箱60秒内只能请求一次验证码
- 需要有效的Resend API密钥才能发送邮件
- 验证成功后用户的`email_verified`字段会被设置为`true`

## 📈 性能优化

### 缓存策略

- 使用Redis缓存热门文章和统计数据
- 实现数据库查询结果缓存
- 支持缓存失效和手动刷新

### WebSocket 实时通知

- 管理员通知系统
- 在线用户状态监控
- 实时数据更新

## 🔒 安全特性

- JWT 令牌认证
- 密码哈希存储
- CORS 保护
- 请求速率限制
- 输入验证和清理

## 🌟 总结

这个博客API系统提供了丰富的功能和灵活的配置选项，适合构建现代化的个人博客或内容管理系统。通过模块化的设计和清晰的代码结构，系统易于扩展和维护。无论是个人博客还是小型内容平台，都能满足多样化的需求。

如有问题或建议，欢迎提交 Issue 或 Pull Request！
