<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-gray-800 dark:text-white">控制面板</h1>
      <div class="text-sm text-gray-500 dark:text-gray-400">
        <span>今天是 {{ currentDate }}</span>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500 dark:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 uppercase">文章总数</p>
            <p class="text-2xl font-semibold text-gray-800 dark:text-white">{{ stats.totalArticles }}</p>
          </div>
        </div>
      </div>

      <!-- 用户总数 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-500 dark:text-purple-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 uppercase">用户总数</p>
            <p class="text-2xl font-semibold text-gray-800 dark:text-white">{{ stats.totalUsers }}</p>
          </div>
        </div>
      </div>

      <!-- 评论总数 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-100 dark:bg-yellow-900 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500 dark:text-yellow-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 uppercase">评论总数</p>
            <p class="text-2xl font-semibold text-gray-800 dark:text-white">{{ stats.totalComments }}</p>
          </div>
        </div>
      </div>

      <!-- 点赞总数 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-red-100 dark:bg-red-900 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500 dark:text-red-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 uppercase">点赞总数</p>
            <p class="text-2xl font-semibold text-gray-800 dark:text-white">{{ stats.totalLikes }}</p>
          </div>
        </div>
      </div>

      <!-- 待审核评论 -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-amber-100 dark:bg-amber-900 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-500 dark:text-amber-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400 uppercase">待审核评论</p>
            <p class="text-2xl font-semibold text-gray-800 dark:text-white">{{ stats.pendingComments || 0 }}</p>
            <div class="flex items-center mt-1 space-x-2">
              <router-link to="/admin/comments" class="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">管理评论</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据统计和活动时间线 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <!-- 活动时间线 -->
      <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white">活动时间线</h2>
          <select
            v-model="timelineDays"
            @change="fetchActivityTimeline"
            class="text-sm bg-gray-100 dark:bg-gray-700 border-0 rounded-md px-3 py-1 text-gray-700 dark:text-gray-300 focus:ring-2 focus:ring-blue-500"
          >
            <option value="7">最近7天</option>
            <option value="30">最近30天</option>
            <option value="90">最近90天</option>
          </select>
        </div>

        <!-- 加载状态 -->
        <div v-if="timelineLoading" class="flex justify-center items-center py-16">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-700 dark:border-gray-300"></div>
        </div>

        <!-- 错误提示 -->
        <div v-else-if="timelineError" class="text-center py-16 text-red-500 dark:text-red-400">
          {{ timelineError }}
          <button @click="fetchActivityTimeline" class="ml-2 text-sm text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300">
            重试
          </button>
        </div>

        <!-- 时间线图表 -->
        <div v-else-if="activityTimeline.length > 0" class="h-64">
          <canvas ref="timelineChartCanvas"></canvas>
        </div>

        <!-- 无数据提示 -->
        <div v-else class="flex flex-col items-center justify-center py-16 text-gray-500 dark:text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p>暂无活动数据</p>
        </div>
      </div>

      <!-- 热门文章 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white">热门文章</h2>
          <select
            v-model="popularPeriod"
            @change="fetchPopularArticles"
            class="text-sm bg-gray-100 dark:bg-gray-700 border-0 rounded-md px-3 py-1 text-gray-700 dark:text-gray-300 focus:ring-2 focus:ring-blue-500"
          >
            <option value="week">本周</option>
            <option value="month">本月</option>
            <option value="year">今年</option>
            <option value="all">全部</option>
          </select>
        </div>

        <!-- 文章列表 -->
        <div v-if="popularArticles.length > 0" class="space-y-3">
          <div
            v-for="(article, index) in popularArticles"
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
                :to="`/admin/articles/edit/${article.article_id || article.id}`"
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
        <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
          暂无热门文章数据
        </div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <h2 class="text-lg font-semibold mb-4 text-gray-800 dark:text-white">最近活动</h2>
      <div class="relative">
        <!-- 加载状态 -->
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 dark:bg-gray-800 dark:bg-opacity-75 rounded-lg">
          <TerminalLoader />
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="text-center py-4 text-red-500 dark:text-red-400">
          {{ error }}
          <button @click="fetchActivities" class="ml-2 text-sm text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300">
            重试
          </button>
        </div>

        <!-- 活动列表 -->
        <div class="space-y-4 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 dark:hover:scrollbar-thumb-gray-500 pr-2">
          <div v-for="(activity, index) in recentActivities" :key="activity.id || index" class="flex items-start pb-4 border-b border-gray-200 dark:border-gray-700 last:border-0 last:pb-0 transition-all duration-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg p-2">
            <div class="flex-shrink-0 mr-4">
              <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                <span class="text-gray-600 dark:text-gray-300 text-sm font-semibold">{{ activity.user.slice(0, 2).toUpperCase() }}</span>
              </div>
            </div>
            <div class="flex-1">
              <p class="text-sm text-gray-800 dark:text-gray-200">{{ activity.action }}</p>
              <div class="flex items-center space-x-2 mt-1">
                <span class="px-2 py-0.5 text-xs rounded-full"
                  :class="{
                    'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300': activity.actionType === 'login',
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': activity.actionType === 'article_create',
                    'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300': activity.actionType === 'profile_update',
                    'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300': activity.actionType === 'system' || !activity.actionType
                  }">
                  {{ activity.actionType || '未知类型' }}
                </span>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 无数据提示 -->
        <div v-if="!loading && !error && recentActivities.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400">
          暂无活动记录
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { TerminalLoader } from '@/components/ui'
import { activityApi, commentApi, statsApi } from '@/api'
import { formatDistanceToNow, format, subDays } from 'date-fns'
import { zhCN } from 'date-fns/locale/zh-CN'
import { userStore } from '@/store'
import message from '@/utils/message'
import { Chart, registerables } from 'chart.js'

// 注册所有 Chart.js 组件
Chart.register(...registerables)

export default {
  name: 'Dashboard',
  components: {
    TerminalLoader
  },
  setup() {
    // 统计数据
    const stats = ref({
      totalArticles: 0,
      totalCategories: 0,
      totalUsers: 0,
      totalComments: 0,
      totalLikes: 0,
      pendingComments: 0
    })

    // 热门文章
    const popularArticles = ref([])

    // 获取统计数据
    const fetchStats = async () => {
      try {
        // 并行请求多个统计数据
        const [overviewResponse, pendingCommentsResponse, popularArticlesResponse] = await Promise.all([
          statsApi.getOverviewStats(),
          commentApi.fetchPendingComments({ pageSize: 1 }),
          statsApi.getPopularArticles({ limit: 5, period: 'month' })
        ])

        // 处理概览统计数据
        if (overviewResponse) {
          console.log('获取到的统计概览数据:', overviewResponse)
          stats.value = {
            ...stats.value,
            totalArticles: overviewResponse.total_articles || 0,
            totalUsers: overviewResponse.total_users || 0,
            totalComments: overviewResponse.total_comments || 0,
            totalLikes: overviewResponse.total_likes || 0
          }
        }

        // 处理待审核评论数据
        stats.value.pendingComments = pendingCommentsResponse?.total || 0

        // 处理热门文章数据
        if (Array.isArray(popularArticlesResponse)) {
          popularArticles.value = popularArticlesResponse
        }

        // 获取分类总数
        try {
          const categoryDistribution = await statsApi.getCategoryDistribution()
          if (Array.isArray(categoryDistribution)) {
            stats.value.totalCategories = categoryDistribution.length
          }
        } catch (err) {
          console.error('获取分类总数失败:', err)
          stats.value.totalCategories = 0
        }
      } catch (err) {
        console.error('获取统计数据失败:', err)
        message.error('获取统计数据失败')
      }
    }

    // 活动时间线数据
    const timelineChart = ref(null)
    const timelineDays = ref(30)
    const activityTimeline = ref([])
    const timelineLoading = ref(false)
    const timelineError = ref(null)

    // 热门文章数据参数
    const popularPeriod = ref('week')
    const popularLoading = ref(false)
    const popularError = ref(null)

    // 活动列表数据
    const recentActivities = ref([])
    const loading = ref(false)
    const error = ref(null)

    // 获取活动列表
    const fetchActivities = async () => {
      loading.value = true
      error.value = null
      try {
        console.log('开始获取活动列表');

        // 不需要手动设置认证头，因为 activityApi 已经处理了这个问题

        // 获取活动列表
        const data = await activityApi.getActivities({ days: 30 })
        console.log('获取到的活动数据:', data);

        // 处理活动数据
        if (Array.isArray(data) && data.length > 0) {
          // 根据 API 文档，活动数据包含: action_type, user_id, target_id, description, id, created_at
          recentActivities.value = data.map(activity => ({
            id: activity.id,
            user: activity.user_id ? '管理员' : '系统',  // 这里可以根据user_id获取具体用户信息
            action: activity.description,
            actionType: activity.action_type,
            targetId: activity.target_id,
            time: formatDistanceToNow(new Date(activity.created_at), { addSuffix: true, locale: zhCN })
          }));
        } else {
          // 如果没有数据，显示空列表
          recentActivities.value = [];
        }
      } catch (e) {
        console.error('获取活动列表异常:', e);
        error.value = e.message || '获取活动列表失败';
        recentActivities.value = [];
      } finally {
        loading.value = false
      }
    }

    // 当前日期格式化
    const currentDate = computed(() => {
      const now = new Date()
      const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
      return now.toLocaleDateString('zh-CN', options)
    })

    // 获取活动时间线数据
    const fetchActivityTimeline = async () => {
      timelineLoading.value = true
      timelineError.value = null

      console.log('开始获取活动时间线数据, 天数:', timelineDays.value)

      try {
        // 使用 statsApi 的 getActivityTimeline 方法
        const response = await statsApi.getActivityTimeline({ days: parseInt(timelineDays.value) })
        const responseData = response.data || response
        console.log('获取到的活动时间线数据:', responseData)
        console.log('数据类型:', typeof responseData)

        if (responseData && typeof responseData === 'object') {
          console.log('数据结构:', Object.keys(responseData))
        }

        // 处理响应数据
        if (Array.isArray(responseData)) {
          console.log('数据是数组格式, 长度:', responseData.length)
          activityTimeline.value = responseData

          // 检查数据是否有效
          if (responseData.length > 0) {
            console.log('第一条数据示例:', responseData[0])

            // 检查非零数据
            const nonZeroData = responseData.filter(item =>
              (item.articles && item.articles > 0) || (item.comments && item.comments > 0)
            )
            console.log('非零数据条数:', nonZeroData.length)

            // 即使没有非零数据也继续渲染
            setTimeout(() => renderTimelineChart(), 100)
          } else {
            console.warn('数组为空')
          }
        } else if (responseData && Array.isArray(responseData.data)) {
          console.log('数据在 data 属性中, 长度:', responseData.data.length)
          activityTimeline.value = responseData.data
          setTimeout(() => renderTimelineChart(), 100)
        } else {
          console.error('无法解析活动时间线数据')
          activityTimeline.value = []
          timelineError.value = '无效的活动时间线数据'

          // 创建测试数据以调试图表渲染
          console.log('创建测试数据以调试图表渲染')
          const testData = []
          const today = new Date()

          for (let i = 0; i < 30; i++) {
            const date = new Date(today)
            date.setDate(date.getDate() - i)
            testData.unshift({
              date: format(date, 'yyyy-MM-dd'),
              articles: Math.floor(Math.random() * 5),
              comments: Math.floor(Math.random() * 10)
            })
          }

          activityTimeline.value = testData
          setTimeout(() => renderTimelineChart(), 100)
        }
      } catch (err) {
        console.error('获取活动时间线数据失败:', err)
        timelineError.value = '获取活动时间线数据失败: ' + (err.message || err)
      } finally {
        timelineLoading.value = false
      }
    }

    // 渲染活动时间线图表
    const timelineChartCanvas = ref(null)

    const renderTimelineChart = () => {
      console.log('开始渲染时间线图表, 数据长度:', activityTimeline.value.length)

      if (!activityTimeline.value.length) {
        console.warn('无活动时间线数据可渲染')
        return
      }

      // 销毁现有图表
      if (timelineChart.value) {
        console.log('销毁现有图表')
        timelineChart.value.destroy()
      }

      const canvas = timelineChartCanvas.value
      if (!canvas) {
        console.error('无法获取时间线图表画布元素')
        return
      }

      console.log('获取到画布元素:', canvas)
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('无法获取画布上下文')
        return
      }

      // 准备数据
      const dates = []
      const articlesData = []
      const commentsData = []

      activityTimeline.value.forEach((item, index) => {
        if (!item.date) {
          console.warn(`第 ${index} 项数据缺少日期:`, item)
          return
        }

        dates.push(item.date)

        // 处理文章数据
        const articleCount = item.articles || item.articles_created || 0
        articlesData.push(articleCount)

        // 处理评论数据
        const commentCount = item.comments || item.comments_posted || 0
        commentsData.push(commentCount)

        // 记录非零数据
        if (articleCount > 0 || commentCount > 0) {
          console.log(`非零数据: 日期=${item.date}, 文章=${articleCount}, 评论=${commentCount}`)
        }
      })

      console.log('处理后的数据:', {
        dates: dates.length > 10 ? [...dates.slice(0, 5), '...', ...dates.slice(-5)] : dates,
        articlesData: articlesData.length > 10 ? [...articlesData.slice(0, 5), '...', ...articlesData.slice(-5)] : articlesData,
        commentsData: commentsData.length > 10 ? [...commentsData.slice(0, 5), '...', ...commentsData.slice(-5)] : commentsData
      })

      // 创建图表
      timelineChart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [
            {
              label: '文章',
              data: articlesData,
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true
            },
            {
              label: '评论',
              data: commentsData,
              borderColor: '#f59e0b',
              backgroundColor: 'rgba(245, 158, 11, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                usePointStyle: true,
                color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#4b5563'
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280'
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                color: document.documentElement.classList.contains('dark') ? 'rgba(75, 85, 99, 0.2)' : 'rgba(209, 213, 219, 0.5)'
              },
              ticks: {
                precision: 0,
                color: document.documentElement.classList.contains('dark') ? '#9ca3af' : '#6b7280'
              }
            }
          }
        }
      })
    }

    // 获取热门文章
    const fetchPopularArticles = async () => {
      popularLoading.value = true
      popularError.value = null

      try {
        const response = await statsApi.getPopularArticles({
          limit: 5,
          period: popularPeriod.value
        })
        console.log('获取到的热门文章数据:', response)

        // 处理响应数据
        if (Array.isArray(response)) {
          popularArticles.value = response
        } else if (response && Array.isArray(response.data)) {
          popularArticles.value = response.data
        } else if (response && typeof response === 'object') {
          // 尝试将对象转换为数组
          try {
            popularArticles.value = Object.values(response)
          } catch (e) {
            console.error('无法将响应转换为数组:', e)
            popularArticles.value = []
          }
        } else {
          popularArticles.value = []
        }
      } catch (err) {
        console.error('获取热门文章失败:', err)
        popularError.value = '获取热门文章失败'
      } finally {
        popularLoading.value = false
      }
    }

    onMounted(() => {
      // 检查登录状态
      console.log('仪表盘组件挂载，检查登录状态:', userStore.state.isLoggedIn);

      // 获取统计数据
      fetchStats()

      // 获取活动时间线数据
      fetchActivityTimeline()

      // 获取热门文章
      fetchPopularArticles()

      // 延迟加载活动列表，确保用户信息已加载
      setTimeout(async () => {
        // 如果没有登录状态，尝试检查登录状态
        if (!userStore.state.isLoggedIn) {
          try {
            console.log('尝试检查登录状态');
            await userStore.checkLoginStatus();
          } catch (error) {
            console.error('检查登录状态失败:', error);
          }
        }

        // 直接获取活动列表，不需要手动设置认证头
        // activityApi 会自动处理认证
        fetchActivities();
      }, 1000);
    })

    // 清理图表资源
    onUnmounted(() => {
      if (timelineChart.value) {
        timelineChart.value.destroy()
      }
    })

    return {
      stats,
      popularArticles,
      recentActivities,
      currentDate,
      loading,
      error,

      // 活动时间线相关
      timelineDays,
      activityTimeline,
      timelineLoading,
      timelineError,
      fetchActivityTimeline,
      timelineChartCanvas,

      // 热门文章相关
      popularPeriod,
      popularLoading,
      popularError,
      fetchPopularArticles
    }
  }
}</script>