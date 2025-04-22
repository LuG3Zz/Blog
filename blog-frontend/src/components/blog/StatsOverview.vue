<template>
  <div class="stats-overview bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
    <h2 class="text-xl font-bold mb-4 text-gray-800 dark:text-white">博客统计</h2>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-4">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-700 dark:border-gray-300"></div>
    </div>
    
    <!-- 错误提示 -->
    <div v-else-if="error" class="text-red-500 dark:text-red-400 text-center py-4">
      {{ error }}
    </div>
    
    <!-- 统计数据 -->
    <div v-else class="grid grid-cols-2 gap-4">
      <div class="stat-card bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-blue-600 dark:text-blue-400">{{ stats.total_users || 0 }}</div>
        <div class="text-sm text-gray-600 dark:text-gray-400">用户总数</div>
      </div>
      
      <div class="stat-card bg-green-50 dark:bg-green-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-green-600 dark:text-green-400">{{ stats.total_articles || 0 }}</div>
        <div class="text-sm text-gray-600 dark:text-gray-400">文章总数</div>
      </div>
      
      <div class="stat-card bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">{{ stats.total_comments || 0 }}</div>
        <div class="text-sm text-gray-600 dark:text-gray-400">评论总数</div>
      </div>
      
      <div class="stat-card bg-amber-50 dark:bg-amber-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-amber-600 dark:text-amber-400">{{ stats.total_likes || 0 }}</div>
        <div class="text-sm text-gray-600 dark:text-gray-400">点赞总数</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { statsApi } from '@/api'

export default {
  name: 'StatsOverview',
  setup() {
    const loading = ref(false)
    const error = ref(null)
    const stats = ref({
      total_users: 0,
      total_articles: 0,
      total_comments: 0,
      total_likes: 0
    })
    
    // 获取统计概览数据
    const fetchOverviewStats = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await statsApi.getOverviewStats()
        console.log('获取到的统计概览数据:', response)
        
        // 处理响应数据
        if (response && typeof response === 'object') {
          stats.value = {
            total_users: response.total_users || 0,
            total_articles: response.total_articles || 0,
            total_comments: response.total_comments || 0,
            total_likes: response.total_likes || 0
          }
        }
      } catch (err) {
        console.error('获取统计概览数据失败:', err)
        error.value = '获取统计数据失败'
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      fetchOverviewStats()
    })
    
    return {
      loading,
      error,
      stats
    }
  }
}
</script>

<style scoped>
.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>
