import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/tailwind.css'
import './assets/css/app.css'
import './assets/css/style.css'
import './assets/css/vditor-custom.css' // 导入 Vditor 自定义样式
import './assets/css/markdown.css' // 导入 Markdown 样式
import 'animate.css' // 导入 Animate.css 动画库

import Lenis from 'lenis'
import { gsap } from 'gsap'
import VTooltip from 'v-tooltip'
import router from './router'
import { themeStore } from './store'

// 全局可用的GSAP和Lenis
window.gsap = gsap
window.Lenis = Lenis

// 初始化主题
themeStore.initTheme()

const app = createApp(App)
app.use(VTooltip)
app.use(router)
app.mount('#app')