<template>
  <div class="min-h-screen flex flex-col overflow-hidden bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <div class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-200 mb-4">标签: {{ tagName }}</h1>
        <p class="text-gray-600 dark:text-gray-400">
          共找到 {{ totalArticles }} 篇相关文章
        </p>
      </div>

      <!-- 文章列表 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- 加载状态 -->
        <LoadingSpinner v-if="loading" message="正在加载文章..." />

        <!-- 错误提示 -->
        <ErrorDisplay
          v-else-if="error"
          title="加载文章失败"
          :message="error"
          :retry-function="fetchArticles"
        />

        <!-- 无数据状态 -->
        <EmptyState
          v-else-if="!articles.length"
          title="暂无文章"
          description="该标签下还没有任何文章"
          icon="file"
        />

        <!-- 文章卡片 -->
        <div v-else v-for="article in articles" :key="article.id" class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
          <router-link :to="`/article/${article.id}`" class="block">
            <div class="relative h-48 overflow-hidden">
              <img
                :src="article.cover_image || getDefaultImage(article)"
                :alt="article.title"
                class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
              >
              <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/70 to-transparent p-4">
                <h2 class="text-white text-xl font-bold line-clamp-2">{{ article.title }}</h2>
              </div>
            </div>
            <div class="p-4">
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-2">
                {{ formatDate(article.created_at || article.date) }} · {{ article.author?.username || '匿名作者' }}
              </p>
              <p class="text-gray-700 dark:text-gray-300 line-clamp-3 mb-4">{{ article.excerpt || article.summary }}</p>
              <div class="flex items-center justify-between">
                <span class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-xs">
                  {{ article.category?.name || article.category }}
                </span>
                <div class="flex items-center text-gray-500 dark:text-gray-400 text-sm">
                  <span class="flex items-center mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    {{ article.view_count || 0 }}
                  </span>
                  <span class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    {{ article.comment_count || 0 }}
                  </span>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="flex justify-center mt-8">
        <div class="flex space-x-2">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-4 py-2 rounded-md bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50"
          >
            上一页
          </button>
          <button
            v-for="page in paginationRange"
            :key="page"
            @click="changePage(page)"
            class="px-4 py-2 rounded-md"
            :class="page === currentPage ? 'bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'"
          >
            {{ page }}
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-4 py-2 rounded-md bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50"
          >
            下一页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { tagApi } from '@/api'
import { ErrorDisplay, LoadingSpinner, EmptyState } from '@/components/ui'
import { format, parseISO } from 'date-fns'

export default {
  name: 'TagList',
  components: {
    ErrorDisplay,
    LoadingSpinner,
    EmptyState
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const articles = ref([])
    const loading = ref(true)
    const error = ref(null)
    const tagName = ref('')
    const tagId = ref(null)
    const totalArticles = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalPages = ref(1)

    // 计算分页范围
    const paginationRange = computed(() => {
      const range = []
      const start = Math.max(1, currentPage.value - 2)
      const end = Math.min(totalPages.value, start + 4)

      for (let i = start; i <= end; i++) {
        range.push(i)
      }

      return range
    })

    // 获取标签信息
    const fetchTagInfo = async () => {
      try {
        const id = route.params.id
        tagId.value = id
        const tagInfo = await tagApi.getTagById(id)
        tagName.value = tagInfo.name
      } catch (err) {
        console.error('获取标签信息失败:', err)
        tagName.value = '未知标签'
      }
    }

    // 获取文章列表
    const fetchArticles = async () => {
      loading.value = true
      error.value = null

      try {
        const id = route.params.id
        const skip = (currentPage.value - 1) * pageSize.value

        const response = await tagApi.getArticlesByTag(id, {
          skip,
          limit: pageSize.value
        })

        articles.value = response.articles || response
        totalArticles.value = response.total || articles.value.length
        totalPages.value = Math.ceil(totalArticles.value / pageSize.value)
      } catch (err) {
        console.error('获取文章失败:', err)
        error.value = '获取文章失败，请稍后再试'
        articles.value = []
      } finally {
        loading.value = false
      }
    }

    // 切换页码
    const changePage = (page) => {
      if (page < 1 || page > totalPages.value) return
      currentPage.value = page
      fetchArticles()

      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    // 获取默认图片
    const getDefaultImage = (article) => {
      const titleHash = article.title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      const imageIndex = (titleHash % 35) + 1 // 使用模35确保索引在1-35范围内
      return `/images/img${imageIndex}.jpg`
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(typeof dateString === 'string' ? parseISO(dateString) : new Date(dateString), 'yyyy-MM-dd')
      } catch (e) {
        return dateString
      }
    }

    // 监听路由参数变化
    watch(() => route.params.id, () => {
      fetchTagInfo()
      currentPage.value = 1
      fetchArticles()
    })

    onMounted(() => {
      fetchTagInfo()
      fetchArticles()
    })

    return {
      articles,
      loading,
      error,
      tagName,
      totalArticles,
      currentPage,
      totalPages,
      paginationRange,
      fetchArticles,
      changePage,
      getDefaultImage,
      formatDate
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
