<template>
  <div class="container mx-auto px-4 py-8">
    <Breadcrumb :items="getBreadcrumbItems()" />

    <div class="flex flex-col md:flex-row gap-8">
      <!-- 左侧分类列表 -->
      <div class="w-full md:w-1/4">
        <Categories v-model="selectedCategory" />
      </div>

      <!-- 右侧文章列表 -->
      <div class="w-full md:w-3/4">
        <PostsList :selectedCategory="selectedCategory" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Breadcrumb } from '../../components/ui'
import { Categories, PostsList } from '../../components/blog'

export default {
  name: 'ArticleList',
  components: {
    Breadcrumb,
    Categories,
    PostsList
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const selectedCategory = ref('')

    // 从 URL 参数中读取分类
    onMounted(() => {
      // 检查URL中是否有category参数
      if (route.query.category) {
        selectedCategory.value = route.query.category
      }
    })

    // 监听分类变化，更新 URL 参数
    watch(selectedCategory, (newCategory) => {
      // 更新 URL 参数，使用替换而不是推送，避免创建新的历史记录
      if (newCategory) {
        router.replace({ query: { ...route.query, category: newCategory } })
      } else {
        // 如果选择了“全部分类”，则移除 category 参数
        const query = { ...route.query }
        delete query.category
        router.replace({ query })
      }
    })

    // 根据当前选中的分类生成面包屑导航项
    const getBreadcrumbItems = () => {
      const items = [
        { name: '首页', path: '/' },
        { name: '文章列表', path: '/articles' }
      ]

      // 如果选中了分类，添加分类导航项
      if (selectedCategory.value) {
        items.push({
          name: selectedCategory.value,
          path: `/articles?category=${encodeURIComponent(selectedCategory.value)}`
        })
      }

      return items
    }

    return {
      selectedCategory,
      getBreadcrumbItems
    }
  }
}
</script>

<style scoped>
/* 使用Tailwind类，无需额外样式 */
</style>