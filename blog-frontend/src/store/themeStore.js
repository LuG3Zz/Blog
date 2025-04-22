import { reactive, readonly } from 'vue'

// 创建主题状态
const state = reactive({
  isDark: false
})

// 初始化主题
const initTheme = () => {
  const theme = localStorage.getItem('theme')
  if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    state.isDark = true
    document.documentElement.classList.add('dark')
  } else {
    state.isDark = false
    document.documentElement.classList.remove('dark')
  }
}

// 切换主题
const toggleTheme = () => {
  state.isDark = !state.isDark
  if (state.isDark) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

// 设置主题
const setTheme = (isDark) => {
  if (state.isDark !== isDark) {
    toggleTheme()
  }
}

// 导出主题状态和方法
export const themeStore = {
  state: readonly(state),
  initTheme,
  toggleTheme,
  setTheme
}
