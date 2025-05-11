import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { siteSettingsApi } from '@/api'

/**
 * 系统设置状态管理
 */
export const useSiteSettingsStore = defineStore('siteSettings', () => {
  // 状态
  const settings = ref({
    site_title: 'BrownLu的博客',
    site_subtitle: '与你共享美好生活',
    nav_text: {
      Home: '首页',
      ArticleList: '文章',
      CategoryList: '分类',
      MemoList: '备忘录',
      About: '关于',
      Login: '登录'
    },
    nav_visible: {
      Home: true,
      ArticleList: true,
      CategoryList: true,
      MemoList: true,
      About: true,
      Login: true
    },
    footer_text: '© 2024 BrownLu的博客 - 保留所有权利',
    banner_image: '',
    logo_image: '',
    favicon: '',
    meta_description: 'BrownLu的个人博客，分享技术、生活和思考',
    meta_keywords: '博客,技术,编程,生活',
    custom_css: '',
    custom_js: ''
  })

  const loading = ref(false)
  const error = ref(null)

  // 计算属性
  const siteTitle = computed(() => settings.value.site_title)
  const siteSubtitle = computed(() => settings.value.site_subtitle)
  const navText = computed(() => settings.value.nav_text || {})
  const navVisible = computed(() => settings.value.nav_visible || {})
  const footerText = computed(() => settings.value.footer_text)
  const bannerImage = computed(() => settings.value.banner_image)
  const logoImage = computed(() => settings.value.logo_image)
  const favicon = computed(() => settings.value.favicon)
  const metaDescription = computed(() => settings.value.meta_description)
  const metaKeywords = computed(() => settings.value.meta_keywords)
  const customCss = computed(() => settings.value.custom_css)
  const customJs = computed(() => settings.value.custom_js)

  // 方法
  /**
   * 获取系统设置
   */
  const fetchSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await siteSettingsApi.getSiteSettings()

      // 确保 nav_visible 字段存在
      if (!response.nav_visible) {
        response.nav_visible = settings.value.nav_visible
        console.log('后端未返回导航显示控制设置，使用默认值')
      }

      settings.value = { ...settings.value, ...response }

      // 更新网站标题
      updateDocumentTitle()

      // 更新网站图标
      updateFavicon()

      // 更新自定义样式和脚本
      updateCustomCode()

      return response
    } catch (err) {
      console.error('获取系统设置失败:', err)
      error.value = '获取系统设置失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新系统设置
   * @param {Object} data 设置数据
   */
  const updateSettings = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await siteSettingsApi.updateSiteSettings(data)

      // 确保 nav_visible 字段存在
      if (!response.nav_visible && data.nav_visible) {
        response.nav_visible = data.nav_visible
        console.log('后端未返回导航显示控制设置，使用提交的值')
      }

      settings.value = { ...settings.value, ...response }

      // 更新网站标题
      updateDocumentTitle()

      // 更新网站图标
      updateFavicon()

      // 更新自定义样式和脚本
      updateCustomCode()

      return response
    } catch (err) {
      console.error('更新系统设置失败:', err)
      error.value = '更新系统设置失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新文档标题
   */
  const updateDocumentTitle = () => {
    if (settings.value.site_title) {
      document.title = settings.value.site_subtitle
        ? `${settings.value.site_title} - ${settings.value.site_subtitle}`
        : settings.value.site_title
    }
  }

  /**
   * 更新网站图标
   */
  const updateFavicon = () => {
    if (settings.value.favicon) {
      const link = document.querySelector('link[rel="icon"]') || document.createElement('link')
      link.type = 'image/x-icon'
      link.rel = 'icon'
      link.href = settings.value.favicon

      if (!document.querySelector('link[rel="icon"]')) {
        document.head.appendChild(link)
      }
    }
  }

  /**
   * 更新自定义代码
   */
  const updateCustomCode = () => {
    // 更新自定义CSS
    let styleElement = document.getElementById('custom-css')
    if (!styleElement && settings.value.custom_css) {
      styleElement = document.createElement('style')
      styleElement.id = 'custom-css'
      document.head.appendChild(styleElement)
    }

    if (styleElement) {
      styleElement.textContent = settings.value.custom_css || ''
    }

    // 更新自定义JavaScript
    let scriptElement = document.getElementById('custom-js')
    if (scriptElement) {
      document.head.removeChild(scriptElement)
    }

    if (settings.value.custom_js) {
      scriptElement = document.createElement('script')
      scriptElement.id = 'custom-js'
      scriptElement.textContent = settings.value.custom_js
      document.head.appendChild(scriptElement)
    }
  }

  /**
   * 初始化系统设置
   */
  const initSettings = async () => {
    try {
      await fetchSettings()
    } catch (err) {
      console.error('初始化系统设置失败:', err)
    }
  }

  return {
    // 状态
    settings,
    loading,
    error,

    // 计算属性
    siteTitle,
    siteSubtitle,
    navText,
    navVisible,
    footerText,
    bannerImage,
    logoImage,
    favicon,
    metaDescription,
    metaKeywords,
    customCss,
    customJs,

    // 方法
    fetchSettings,
    updateSettings,
    initSettings
  }
})
