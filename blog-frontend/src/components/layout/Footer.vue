<template>
  <footer class="bg-secondary dark:bg-dark-primary text-primary dark:text-dark-secondary py-8 px-8 mt-auto">
    <div class="container mx-auto">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <h3 class="text-xl font-bold uppercase">{{ siteTitle }}</h3>
          <p class="text-sm mt-2">{{ siteSubtitle }}</p>
        </div>

        <div class="flex flex-col md:flex-row gap-8">
          <div>
            <h4 class="text-lg font-medium mb-2">链接</h4>
            <ul class="space-y-1">
              <li><router-link to="/" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">{{ navItems.Home || '首页' }}</router-link></li>
              <li><router-link to="/articles" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">{{ navItems.ArticleList || '文章' }}</router-link></li>
              <li><router-link to="/categories" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">{{ navItems.CategoryList || '分类' }}</router-link></li>
              <li><router-link to="/about" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">{{ navItems.About || '关于' }}</router-link></li>
            </ul>
          </div>

          <div>
            <h4 class="text-lg font-medium mb-2">联系我</h4>
            <ul class="space-y-1">
              <li><a href="mailto:contact@example.com" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">Email</a></li>
              <li><a href="https://github.com/brownlu" target="_blank" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">GitHub</a></li>
              <li><a href="https://twitter.com/brownlu" target="_blank" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">Twitter</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-700 mt-8 pt-6 text-center text-sm">
        <p>{{ footerText }}</p>
      </div>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue'
import { useSiteSettingsStore } from '@/stores'

export default {
  name: 'Footer',
  setup() {
    const siteSettingsStore = useSiteSettingsStore()

    // 获取网站设置
    const siteTitle = computed(() => siteSettingsStore.siteTitle || 'BrownLu的博客')
    const siteSubtitle = computed(() => siteSettingsStore.siteSubtitle || '与你共享美好生活')
    const footerText = computed(() => siteSettingsStore.footerText || `© ${new Date().getFullYear()} BrownLu的博客. 保留所有权利.`)
    const navItems = computed(() => siteSettingsStore.navText || {
      Home: '首页',
      ArticleList: '文章',
      CategoryList: '分类',
      About: '关于'
    })

    return {
      siteTitle,
      siteSubtitle,
      footerText,
      navItems
    }
  }
}
</script>

<style scoped>
/* 使用Tailwind类，无需额外样式 */
</style>
