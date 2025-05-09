# ✨ 现代化博客前端

🌈 一个精心设计的现代博客前端应用，基于 Vue 3、Vite 和 TailwindCSS 构建，具有流畅的动画效果、优雅的用户界面和清晰的代码结构。

![博客前端预览](https://via.placeholder.com/800x400?text=博客前端预览)

## 🚀 主要特性

- 📝 **文章管理** - 创建、编辑和发布文章，支持 Markdown 编辑
- 🏷️ **分类与标签** - 灵活组织内容，便于导航和发现
- 💬 **评论系统** - 与读者互动，支持多级评论和点赞
- 👤 **用户管理** - 完整的用户认证和权限控制
- 🌙 **深色模式** - 自动和手动切换，保护眼睛
- 📱 **响应式设计** - 完美适配各种设备尺寸
- 🎨 **精美动画** - 使用 GSAP 实现流畅的交互体验
- 📋 **备忘录系统** - 轻松分享日常想法和笔记
- 🔍 **全文搜索** - 快速找到所需内容
- 📊 **数据统计** - 直观展示博客数据和趋势
- 🔔 **通知系统** - 实时接收重要更新和消息

## 🧩 项目结构

项目采用模块化、组件化的结构组织，便于维护和扩展：

```text
src/
├── api/                  # 🌐 API 服务和数据获取
│   ├── core/             # 🧠 核心 API 配置
│   ├── modules/          # 📦 API 模块
│   └── index.js          # 📑 API 导出
├── assets/               # 🖼️ 静态资源
│   ├── css/              # 🎨 CSS 文件
│   ├── fonts/            # 🔤 字体文件
│   └── images/           # 🏞️ 图片资源
├── components/           # 🧱 Vue 组件
│   ├── admin/            # 👑 管理员组件
│   ├── blog/             # 📰 博客相关组件
│   ├── memo/             # 📝 备忘录组件
│   ├── layout/           # 🏗️ 布局组件
│   └── ui/               # 🎛️ UI 组件库
├── composables/          # 🎣 Vue 组合式函数
├── hooks/                # 🪝 自定义钩子
│   ├── usePostAnimation.js # ✨ 文章动画钩子
│   └── useTheme.js       # 🌓 主题管理钩子
├── router/               # 🧭 Vue 路由配置
├── stores/               # 🗄️ 状态管理
├── utils/                # 🛠️ 工具函数
│   ├── date.js           # 📅 日期处理
│   ├── message.js        # 💌 消息工具
│   └── permission.js     # 🔐 权限控制
└── views/                # 📄 页面视图
    ├── admin/            # 🔧 管理页面
    ├── blog/             # 📚 博客页面
    ├── memo/             # 📒 备忘录页面
    └── auth/             # 🔑 认证页面
```

## 🛠️ 技术栈

- ⚡ **Vue 3** - 使用 Composition API 的现代化框架
- 🔥 **Vite** - 极速的开发与构建工具
- 💨 **TailwindCSS** - 实用优先的 CSS 框架
- 🗄️ **Pinia** - 直观、类型安全的状态管理
- 🎭 **GSAP** - 专业级动画库
- 🔄 **Axios** - 强大的 HTTP 客户端
- 📝 **Vditor** - Markdown 编辑器
- 🌓 **深色模式** - 自动和手动主题切换
- 📱 **响应式设计** - 移动优先的界面设计

## 📦 环境配置

### 🔧 前置要求

- Node.js (v16+)
- npm 或 yarn 或 pnpm

### 🚀 安装步骤

1. 克隆仓库

   ```bash
   git clone https://github.com/yourusername/blog-frontend.git
   cd blog-frontend
   ```

2. 安装依赖

   ```bash
   npm install
   # 或
   yarn
   # 或
   pnpm install
   ```

3. 启动开发服务器

   ```bash
   npm run dev
   # 或
   yarn dev
   # 或
   pnpm dev
   ```

4. 在浏览器中访问 `http://localhost:5173`

## 📝 开发指南

### 🔄 环境变量

项目使用 Vite 的环境变量系统，配置文件位于：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

主要环境变量：

- `VITE_API_BASE_URL` - API 基础 URL
- `VITE_MODE` - 运行模式
- `VITE_WS_PATH` - WebSocket 路径

### 🏗️ 构建生产版本

```bash
npm run build
# 或
yarn build
# 或
pnpm build
```

构建后的文件将位于 `dist` 目录中。

## 🎨 主要功能展示

### 📝 文章编辑器

![文章编辑器](https://via.placeholder.com/600x300?text=文章编辑器)

支持 Markdown 语法，实时预览，图片上传等功能。

### 🌙 深色模式

![深色模式](https://via.placeholder.com/600x300?text=深色模式)

自动检测系统主题，也可手动切换。

### 📊 数据统计

![数据统计](https://via.placeholder.com/600x300?text=数据统计)

直观展示访问量、文章数、评论数等统计数据。

## 🤝 贡献指南

欢迎为项目做出贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加一些很棒的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件
