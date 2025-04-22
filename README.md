# 博客系统环境配置说明

本文档说明如何在开发和生产环境之间快速切换。

## 环境配置文件

### 前端环境配置

前端使用 Vite 的环境变量系统，配置文件位于：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

### 后端环境配置

后端使用 Python 的 dotenv 库，配置文件位于：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

## 快速启动脚本

### 前端

- `start_dev.bat` - 启动开发服务器
- `build_dev.bat` - 构建开发环境版本
- `build_prod.bat` - 构建生产环境版本

### 后端

- `start_dev.bat` - 启动开发环境服务器
- `start_prod.bat` - 启动生产环境服务器

## 手动启动命令

### 前端

```bash
# 开发环境
npm run dev

# 构建生产环境
npm run build

# 构建开发环境
npm run build:dev
```

### 后端

```bash
# 开发环境
python run.py --env=development

# 生产环境
python run.py --env=production
```

## 环境变量说明

### 前端环境变量

- `VITE_API_BASE_URL` - API 基础 URL
  - 开发环境：空字符串（使用相对路径，通过代理转发）
  - 生产环境：`https://brown1u.us.kg`
- `VITE_MODE` - 运行模式
- `VITE_WS_PATH` - WebSocket 路径

### 后端环境变量

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
