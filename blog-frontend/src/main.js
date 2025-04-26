import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/css/tailwind.css'
import './assets/css/app.css'
import './assets/css/style.css'
import './assets/css/vditor-custom.css' // 导入 Vditor 自定义样式
import './assets/css/markdown.css' // 导入 Markdown 样式
import './assets/css/highlight-custom.css' // 导入 highlight.js 代码高亮样式
import './assets/css/article-detail.css' // 导入文章详情页面样式
import 'animate.css' // 导入 Animate.css 动画库

import Lenis from 'lenis'
import { gsap } from 'gsap'
import VTooltip from 'v-tooltip'
import router from './router'
import { useThemeStore } from './stores'

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