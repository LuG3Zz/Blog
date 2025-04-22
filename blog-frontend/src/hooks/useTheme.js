import { ref, onMounted } from 'vue'

/**
 * 主题切换钩子
 * 提供暗黑模式和亮色模式的切换功能
 * @returns {Object} 包含isDark状态和toggleTheme方法的对象
 */
export function useTheme() {
  const isDark = ref(false)

  // 切换主题
  const toggleTheme = () => {
    isDark.value = !isDark.value
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  // 初始化主题
  const initTheme = () => {
    const theme = localStorage.getItem('theme')
    if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      isDark.value = true
      document.documentElement.classList.add('dark')
    }
  }

  onMounted(() => {
    initTheme()
  })

  return {
    isDark,
    toggleTheme
  }
}
