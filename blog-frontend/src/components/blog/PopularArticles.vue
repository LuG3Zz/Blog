<template>
  <div class="popular-articles bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold text-gray-800 dark:text-white">热门文章</h2>

      <!-- 时间段选择器 -->
      <select
        v-model="selectedPeriod"
        @change="fetchPopularArticles"
        class="text-sm bg-gray-100 dark:bg-gray-700 border-0 rounded-md px-3 py-1 text-gray-700 dark:text-gray-300 focus:ring-2 focus:ring-blue-500"
      >
        <option value="day">今日</option>
        <option value="week">本周</option>
        <option value="month">本月</option>
        <option value="year">今年</option>
        <option value="all">全部</option>
      </select>
    </div>

    <!-- 加载状态 -->
    <LoadingSpinner v-if="loading" message="正在加载热门文章..." />

    <!-- 错误提示 -->
    <ErrorDisplay
      v-else-if="error"
      title="加载热门文章失败"
      :message="error"
      :retry-function="fetchPopularArticles"
    />

    <!-- 文章列表 -->
    <div v-else-if="articles.length > 0" class="space-y-3">
      <div
        v-for="(article, index) in articles"
        :key="article.article_id || index"
        class="flex items-center p-2 rounded-lg transition-all duration-300 hover:bg-gray-50 dark:hover:bg-gray-700/50"
      >
        <!-- 排名 -->
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center mr-3">
          <span class="text-blue-600 dark:text-blue-400 font-bold">{{ index + 1 }}</span>
        </div>

        <!-- 文章信息 -->
        <div class="flex-1 min-w-0">
          <router-link
            :to="`/article/${article.article_id || article.id}`"
            class="text-sm font-medium text-gray-900 dark:text-gray-100 hover:text-blue-600 dark:hover:text-blue-400 line-clamp-1"
          >
            {{ article.title }}
          </router-link>
          <div class="flex items-center text-xs text-gray-500 dark:text-gray-400 mt-1">
            <span class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              {{ article.view_count || 0 }} 次阅读
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 无数据提示 -->
    <EmptyState
      v-else
      title="暂无热门文章"
      description="还没有热门文章数据"
      icon="file"
      actionText="刷新"
      :actionFunction="fetchPopularArticles"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { statsApi } from '@/api'
import { ErrorDisplay, LoadingSpinner, EmptyState } from '@/components/ui'

export default {
  name: 'PopularArticles',
  components: {
    ErrorDisplay,
    LoadingSpinner,
    EmptyState
  },
  props: {
    limit: {
      type: Number,
      default: 5
    }
  },
  setup(props) {
    const loading = ref(false)
    const error = ref(null)
    const articles = ref([])
    const selectedPeriod = ref('week')

    // 获取热门文章
    const fetchPopularArticles = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await statsApi.getPopularArticles({
          limit: props.limit,
          period: selectedPeriod.value
        })
        console.log('获取到的热门文章数据:', response)

        // 处理响应数据
        if (Array.isArray(response)) {
          articles.value = response
        } else if (response && Array.isArray(response.data)) {
          articles.value = response.data
        } else if (response && typeof response === 'object') {
          // 尝试将对象转换为数组
          try {
            articles.value = Object.values(response)
          } catch (e) {
            console.error('无法将响应转换为数组:', e)
            articles.value = []
          }
        } else {
          articles.value = []
        }
      } catch (err) {
        console.error('获取热门文章失败:', err)
        error.value = '获取热门文章失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchPopularArticles()
    })

    return {
      loading,
      error,
      articles,
      selectedPeriod,
      fetchPopularArticles
    }
  }
}
</script>

<style scoped>
/* 添加一些过渡效果 */
.popular-articles a {
  transition: color 0.3s ease;
}

/* 确保文本不会溢出 */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
