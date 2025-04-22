<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-gray-800 dark:text-white">活动管理</h1>
      <div class="flex items-center space-x-2">
        <select
          v-model="filterDays"
          class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
        >
          <option value="7">最近7天</option>
          <option value="30">最近30天</option>
          <option value="90">最近90天</option>
          <option value="365">最近一年</option>
        </select>
        <button
          @click="refreshActivities"
          class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          title="刷新"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 p-4 rounded-md">
      {{ error }}
      <button @click="refreshActivities" class="ml-2 underline">重试</button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-700 dark:border-gray-300"></div>
    </div>

    <!-- 活动列表 -->
    <div v-if="!loading && activities.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">活动类型</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">用户</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">描述</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">目标ID</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">时间</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="activity in activities" :key="activity.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full" 
                :class="getActionTypeClass(activity.action_type)">
                {{ formatActionType(activity.action_type) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                  <span v-if="!getUserAvatar(activity.user_id)" class="text-xs font-medium text-gray-700 dark:text-gray-300">{{ getUserInitial(activity.user_id) }}</span>
                  <img v-else :src="getUserAvatar(activity.user_id)" alt="" class="h-8 w-8 rounded-full">
                </div>
                <div class="ml-3">
                  <div class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ getUserName(activity.user_id) }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-normal">
              <div class="text-sm text-gray-900 dark:text-gray-100 line-clamp-2">{{ activity.description }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ activity.target_id }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(activity.created_at) }}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 无数据提示 -->
    <div v-if="!loading && !error && activities.length === 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
      <p class="text-gray-500 dark:text-gray-400">暂无活动记录</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { activityApi, userApi } from '@/api'
import message from '@/utils/message'

export default {
  name: 'ActivityManage',
  setup() {
    // 状态变量
    const activities = ref([])
    const loading = ref(true)
    const error = ref(null)
    const filterDays = ref('30')
    const users = ref({}) // 缓存用户信息

    // 获取活动列表
    const fetchActivities = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await activityApi.getActivities({
          days: parseInt(filterDays.value)
        })

        activities.value = Array.isArray(response) ? response : []
        
        // 获取活动中涉及的用户信息
        await fetchUserInfo()
      } catch (err) {
        console.error('获取活动列表失败:', err)
        error.value = err.message || '获取活动列表失败'
        message.error('获取活动列表失败')
      } finally {
        loading.value = false
      }
    }

    // 获取用户信息
    const fetchUserInfo = async () => {
      const userIds = [...new Set(activities.value
        .filter(activity => activity.user_id)
        .map(activity => activity.user_id))]
      
      for (const userId of userIds) {
        if (!users.value[userId]) {
          try {
            const userInfo = await userApi.getUserById(userId)
            users.value[userId] = userInfo
          } catch (error) {
            console.error(`获取用户 ${userId} 信息失败:`, error)
          }
        }
      }
    }

    // 刷新活动列表
    const refreshActivities = () => {
      fetchActivities()
    }

    // 获取用户名
    const getUserName = (userId) => {
      if (!userId) return '系统'
      return users.value[userId]?.username || `用户 #${userId}`
    }

    // 获取用户头像
    const getUserAvatar = (userId) => {
      if (!userId) return null
      return users.value[userId]?.avatar || null
    }

    // 获取用户首字母
    const getUserInitial = (userId) => {
      if (!userId) return 'S'
      const username = getUserName(userId)
      return username.charAt(0).toUpperCase()
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知时间'
      try {
        const date = new Date(dateString)
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        return '日期格式错误'
      }
    }

    // 格式化活动类型
    const formatActionType = (actionType) => {
      const typeMap = {
        'CREATE_ARTICLE': '创建文章',
        'UPDATE_ARTICLE': '更新文章',
        'DELETE_ARTICLE': '删除文章',
        'CREATE_COMMENT': '发表评论',
        'UPDATE_COMMENT': '更新评论',
        'DELETE_COMMENT': '删除评论',
        'LIKE_ARTICLE': '点赞文章',
        'LIKE_COMMENT': '点赞评论',
        'LOGIN': '登录',
        'LOGOUT': '登出',
        'REGISTER': '注册',
        'UPDATE_PROFILE': '更新资料'
      }
      return typeMap[actionType] || actionType
    }

    // 获取活动类型样式
    const getActionTypeClass = (actionType) => {
      const typeClasses = {
        'CREATE_ARTICLE': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'UPDATE_ARTICLE': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'DELETE_ARTICLE': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
        'CREATE_COMMENT': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
        'UPDATE_COMMENT': 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200',
        'DELETE_COMMENT': 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
        'LIKE_ARTICLE': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'LIKE_COMMENT': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
        'LOGIN': 'bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200',
        'LOGOUT': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-200',
        'REGISTER': 'bg-lime-100 text-lime-800 dark:bg-lime-900 dark:text-lime-200',
        'UPDATE_PROFILE': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200'
      }
      return typeClasses[actionType] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }

    // 监听筛选条件变化
    watch(filterDays, () => {
      fetchActivities()
    })

    // 组件挂载时获取活动列表
    onMounted(() => {
      fetchActivities()
    })

    return {
      activities,
      loading,
      error,
      filterDays,
      refreshActivities,
      getUserName,
      getUserAvatar,
      getUserInitial,
      formatDate,
      formatActionType,
      getActionTypeClass
    }
  }
}
</script>
