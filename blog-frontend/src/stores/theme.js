/**
 * 主题状态存储
 * 使用 Pinia 管理主题状态
 */

import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  // 状态
  state: () => ({
    isDark: false
  }),

  // getters
  getters: {
    // 获取当前主题模式
    currentTheme: (state) => state.isDark ? 'dark' : 'light'
  },

  // actions
  actions: {
    // 初始化主题
    initTheme() {
      const theme = localStorage.getItem('theme')
      if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        this.isDark = true
        document.documentElement.classList.add('dark')
      } else {
        this.isDark = false
        document.documentElement.classList.remove('dark')
      }
    },

    // 切换主题
    toggleTheme() {
      this.isDark = !this.isDark
      if (this.isDark) {
        document.documentElement.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      } else {
        document.documentElement.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      }
    },

    // 设置主题
    setTheme(isDark) {
      if (this.isDark !== isDark) {
        this.toggleTheme()
      }
    }
  }
})
