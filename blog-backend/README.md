# Blog API

这是一个使用FastAPI构建的博客API系统，提供了用户管理、文章管理、评论管理等功能。

## 功能特性

- 用户注册、登录和认证
- 文章的创建、更新、删除和查询
- 评论的添加和管理
- 文章分类管理
- 文件上传功能
- 用户活动记录

## 项目结构

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
│   │   └── __init__.py     # 模型初始化
│   ├── schemas/            # Pydantic模式
│   │   ├── activity.py     # 活动相关模式
│   │   ├── ai_assist.py    # AI辅助相关模式
│   │   ├── article.py      # 文章相关模式
│   │   ├── article_extended.py # 扩展文章模式
│   │   ├── comment.py      # 评论相关模式
│   │   ├── heatmap.py      # 热力图相关模式
│   │   ├── subscription.py # 订阅相关模式
│   │   ├── tag.py          # 标签相关模式
│   │   ├── token.py        # 认证令牌模式
│   │   ├── user.py         # 用户相关模式
│   │   ├── version.py      # 版本控制相关模式
│   │   └── __init__.py     # 模式初始化
│   ├── services/           # 业务逻辑服务
│   │   ├── activity_service.py    # 活动服务
│   │   ├── article_service.py     # 文章服务
│   │   ├── comment_service.py     # 评论服务
│   │   ├── content_filter_service.py # 内容过滤服务
│   │   ├── ip_location_service.py # IP位置服务
│   │   ├── subscription_service.py # 订阅服务
│   │   ├── tag_service.py         # 标签服务
│   │   ├── user_service.py        # 用户服务
│   │   ├── version_service.py     # 版本控制服务
│   │   └── __init__.py            # 服务初始化
│   ├── routers/            # API路由
│   │   ├── activities.py   # 活动路由
│   │   ├── admin.py        # 管理员路由
│   │   ├── articles.py     # 文章路由
│   │   ├── auth.py         # 认证路由
│   │   ├── categories.py   # 分类路由
│   │   ├── comments.py     # 评论路由
│   │   ├── files.py        # 文件路由
│   │   ├── search.py       # 搜索路由
│   │   ├── stats.py        # 统计路由
│   │   ├── subscriptions.py # 订阅路由
│   │   ├── tags.py         # 标签路由
│   │   ├── users.py        # 用户路由
│   │   ├── versions.py     # 版本控制路由
│   │   └── __init__.py     # 路由初始化
│   ├── utils/              # 工具函数
│   │   ├── logging.py      # 日志工具
│   │   ├── pagination.py   # 分页工具
│   │   ├── validators.py   # 验证工具
│   │   └── __init__.py     # 工具初始化
│   ├── auth.py             # 认证兼容模块
│   ├── database.py         # 数据库兼容模块
│   ├── main.py             # 应用入口
│   ├── models.py           # 模型兼容模块
│   ├── schemas.py          # 模式兼容模块
│   └── __init__.py         # 应用初始化
├── scripts/                # 脚本目录
│   ├── migrations/         # 数据库迁移脚本
│   │   ├── add_user_role.py # 添加用户角色
│   │   ├── create_article_tags_table.py # 创建文章标签表
│   │   ├── migrate_tags_to_relationships.py # 迁移标签关系
│   │   ├── remove_tags_column.py # 移除标签列
│   │   ├── update_comments_table.py # 更新评论表
│   │   └── __init__.py     # 迁移脚本初始化
│   └── update_charset.py   # 更新字符集脚本
├── static/                 # 静态文件
│   └── images/             # 上传的图片
├── .env                    # 环境变量
├── blog.db                 # SQLite数据库文件
└── requirements.txt        # 依赖列表
```

## 技术栈

- FastAPI: 现代、快速的Web框架
- SQLAlchemy: ORM工具
- Pydantic: 数据验证和设置管理
- JWT: 用户认证
- MySQL: 数据存储

## 如何在Swagger UI中使用JWT令牌进行接口测试

1. 访问API文档：http://localhost:8000/docs

2. 获取JWT令牌：
   - 点击 `/auth/login` 接口
   - 点击 "Try it out" 按钮
   - 输入用户名和密码
   - 点击 "Execute" 按钮
   - 从响应中复制 `access_token` 的值

3. 使用JWT令牌进行授权：
   - 点击Swagger UI界面右上角的 "Authorize" 按钮
   - 在弹出的对话框中，输入 `Bearer` 加上空格，然后粘贴你的令牌
     例如：`Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - 点击 "Authorize" 按钮

## 安装和运行

1. 克隆仓库

```bash
git clone https://github.com/yourusername/blog-api.git
cd blog-api
```

2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
pip install -r requirements.txt
```

3. 配置环境变量

创建一个`.env`文件，包含以下内容：

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/blog
SECRET_KEY=your-secret-key-change-in-production
HOST=127.0.0.1
PORT=8000
RELOAD=True
WORKERS=1
TRUSTED_HOSTS=127.0.0.1,localhost,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

4. 运行应用

使用提供的启动脚本运行应用，它会正确配置代理头处理：

```bash
python run.py
```

或者直接使用 uvicorn 命令（不推荐，因为没有配置代理头处理）：

```bash
uvicorn app.main:app --reload
```

5. 访问API文档

打开浏览器访问 http://localhost:8000/docs

## 代码风格和最佳实践

- 使用依赖注入模式进行服务和数据库访问
- 业务逻辑与API路由分离
- 使用Pydantic模型进行数据验证
- 统一的错误处理和日志记录
- 分页和过滤支持

## 配置前端代理服务器

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

## AI 辅助接口

### 接口功能

接收文章正文内容，自动生成摘要（150字内）和3-5个标签

### 请求方式

```http
POST /articles/ai-assist
```

### 请求头

```http
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

### 请求体示例

```json
{
  "content": "文章正文内容（不少于50字）"
}
```

### 响应示例

```json
{
  "excerpt": "文章摘要内容...",
  "tags": ["标签1", "标签2", "标签3"]
}
```

### 认证方式

使用JWT Bearer令牌，需在Authorization头中携带有效token

### 错误代码

- 401 Unauthorized: 缺少或无效的认证信息
- 500 Internal Server Error: 服务器配置错误
- 503 Service Unavailable: AI服务不可用

### 调用示例（cURL）

```bash
curl -X POST http://localhost:8000/articles/ai-assist \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{"content": "你的文章内容..."}'
```

### 注意事项

1. 需在.env文件中配置有效的OPENROUTER_API_KEY
2. 文章内容需不少于50个字符
3. 确保服务端已安装python-dotenv依赖
4. API密钥请妥善保管，不要提交到版本库
