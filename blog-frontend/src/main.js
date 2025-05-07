import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
// 基础样式
import './assets/css/tailwind.css'
import './assets/css/app.css'
import './assets/css/style.css'

// 按需导入其他样式
const loadStyles = async () => {
  // 基础样式已经在上面同步导入

  // 动态导入其他样式
  await Promise.all([
    import('./assets/css/vditor-custom.css'),
    import('./assets/css/markdown.css'),
    import('./assets/css/highlight-custom.css'),
    import('./assets/css/article-detail.css'),
    import('animate.css')
  ])
}

// 启动样式加载，但不等待它完成
loadStyles()

// 路由和状态管理
import router from './router'
import { useThemeStore } from './stores'

// 按需导入第三方库
import VTooltip from 'v-tooltip'
// 延迟导入非关键库
const Lenis = () => import('lenis').then(module => module.default)
const gsap = () => import('gsap').then(module => module.gsap)

// 全局可用的GSAP和Lenis
window.gsap = gsap
window.Lenis = Lenis

// 创建Pinia实例
const pinia = createPinia()

const app = createApp(App)
app.use(VTooltip)
app.use(router)
app.use(pinia)

// 初始化主题 (在挂载应用后初始化，确保Pinia已经可用)
const themeStore = useThemeStore()
themeStore.initTheme()

app.mount('#app')