# 🚀 现代化个人博客系统

欢迎使用这个功能丰富的个人博客系统！这是一个使用现代技术栈构建的全栈博客平台，提供丰富的功能和优雅的用户体验。

## ✨ 主要特性

- 📝 文章管理 - 支持Markdown编辑、草稿保存、版本控制
- 🏷️ 分类与标签 - 灵活组织内容
- 💬 评论系统 - 与读者互动
- 👤 用户管理 - 多角色权限控制
- 📊 数据统计 - 访问量、热门文章分析
- 🔔 通知系统 - 实时通知和邮件提醒
- 📱 响应式设计 - 完美适配各种设备
- 🌙 深色模式 - 保护眼睛，提升阅读体验
- 📋 备忘录/动态 - 轻松分享日常想法
- 🔒 内容加密 - 支持密码保护私密内容
- 📧 邮件订阅 - 读者可订阅更新通知
- 🖼️ 文件管理 - 上传和管理图片与文件

## 🛠️ 技术栈

### 前端

- Vue 3 + Vite - 现代化前端框架
- Pinia - 状态管理
- Tailwind CSS - 实用优先的CSS框架
- Vditor - Markdown编辑器

### 后端

- FastAPI - 高性能Python API框架
- SQLAlchemy - ORM数据库操作
- Redis - 缓存和WebSocket支持
- JWT - 安全认证

## 🔄 环境配置

本项目支持在开发和生产环境之间快速切换，下面是详细配置说明。

### 📁 配置文件

#### 🖥️ 前端配置

前端使用 Vite 的环境变量系统，配置文件位于：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

#### 🔧 后端配置

后端使用 Python 的 dotenv 库，配置文件位于：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

### 🚀 快速启动脚本

#### 🖥️ 前端脚本

- `start_dev.bat` - 启动开发服务器
- `build_dev.bat` - 构建开发环境版本
- `build_prod.bat` - 构建生产环境版本

#### 🔧 后端脚本

- `start_dev.bat` - 启动开发环境服务器
- `start_prod.bat` - 启动生产环境服务器

### 💻 手动启动命令

#### 🖥️ 前端命令

```bash
# 开发环境
npm run dev

# 构建生产环境
npm run build

# 构建开发环境
npm run build:dev
```

#### 🔧 后端命令

```bash
# 开发环境
python run.py --env=development

# 生产环境
python run.py --env=production
```

### ⚙️ 环境变量说明

#### 🖥️ 前端环境变量

- `VITE_API_BASE_URL` - API 基础 URL
  - 开发环境：空字符串（使用相对路径，通过代理转发）
  - 生产环境：`https://brown1u.us.kg`
- `VITE_MODE` - 运行模式
- `VITE_WS_PATH` - WebSocket 路径

#### 🔧 后端环境变量

- `DATABASE_URL` - 数据库连接 URL
- `SECRET_KEY` - 安全密钥
- `BASE_URL` - 服务器基础 URL
  - 开发环境：`http://localhost:8000`
  - 生产环境：`https://brown1u.us.kg`
- `HOST` - 服务器主机
  - 开发环境：`127.0.0.1`
  - 生产环境：`0.0.0.0`
- `PORT` - 服务器端口
- `RELOAD` - 是否启用热重载
- `WORKERS` - 工作进程数
- `TRUSTED_HOSTS` - 信任的主机列表

## 📝 贡献指南

欢迎为项目做出贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加一些很棒的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件
