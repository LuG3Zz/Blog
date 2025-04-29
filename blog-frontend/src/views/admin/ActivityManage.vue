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
        <button
          v-if="selectedActivities.length > 0"
          @click="confirmBatchDelete"
          class="px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200 text-sm font-medium flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          批量删除 ({{ selectedActivities.length }})
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
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300">
              <div class="flex items-center">
                <input
                  id="select-all"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600"
                  :checked="selectAll"
                  @change="toggleSelectAll"
                />
                <label for="select-all" class="sr-only">全选</label>
              </div>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">活动类型</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">用户</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">描述</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">目标ID</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">时间</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="activity in activities" :key="activity.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <input
                  :id="`select-activity-${activity.id}`"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600"
                  :checked="selectedActivities.includes(activity.id)"
                  @change="toggleActivitySelection(activity.id)"
                />
                <label :for="`select-activity-${activity.id}`" class="sr-only">选择活动</label>
              </div>
            </td>
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
            <td class="px-6 py-4 whitespace-nowrap">
              <button
                @click="confirmDelete(activity)"
                class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300 transition-colors"
                title="删除活动"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 无数据提示 -->
    <div v-if="!loading && !error && activities.length === 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
      <p class="text-gray-500 dark:text-gray-400">暂无活动记录</p>
    </div>

    <!-- 单个删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">确认删除</h3>
        <p class="text-gray-700 dark:text-gray-300 mb-6">
          您确定要删除此活动记录吗？此操作无法撤销。
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="cancelDelete"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200"
          >
            取消
          </button>
          <button
            @click="deleteActivity"
            class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 批量删除确认对话框 -->
    <div v-if="showBatchDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">确认批量删除</h3>
        <p class="text-gray-700 dark:text-gray-300 mb-6">
          您确定要删除选中的 {{ selectedActivities.length }} 条活动记录吗？此操作无法撤销。
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="cancelBatchDelete"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200"
          >
            取消
          </button>
          <button
            @click="batchDeleteActivities"
            class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200"
            :disabled="isBatchDeleting"
          >
            <span v-if="isBatchDeleting">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { activityApi, userApi } from '@/api'
import message from '@/utils/message'
import { formatDateTimeWithTimeZone } from '@/utils/date-utils'

export default {
  name: 'ActivityManage',
  setup() {
    // 状态变量
    const activities = ref([])
    const loading = ref(true)
    const error = ref(null)
    const filterDays = ref('30')
    const users = ref({}) // 缓存用户信息

    // 删除相关状态
    const showDeleteConfirm = ref(false)
    const activityToDelete = ref(null)
    const isDeleting = ref(false)

    // 批量删除相关状态
    const selectedActivities = ref([])
    const selectAll = ref(false)
    const showBatchDeleteConfirm = ref(false)
    const isBatchDeleting = ref(false)

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
        // 使用自定义日期工具函数，将UTC时间转换为本地时间
        return formatDateTimeWithTimeZone(dateString)
      } catch (error) {
        console.error('日期格式化错误:', error)
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

    // 确认删除对话框
    const confirmDelete = (activity) => {
      activityToDelete.value = activity
      showDeleteConfirm.value = true
    }

    // 取消删除
    const cancelDelete = () => {
      showDeleteConfirm.value = false
      activityToDelete.value = null
    }

    // 删除活动
    const deleteActivity = async () => {
      if (!activityToDelete.value) return

      isDeleting.value = true
      try {
        const activityId = activityToDelete.value.id
        await activityApi.deleteActivity(activityId)
        message.success('活动记录删除成功')

        // 如果该活动在选中列表中，也要移除
        if (selectedActivities.value.includes(activityId)) {
          selectedActivities.value = selectedActivities.value.filter(id => id !== activityId)
        }

        // 关闭确认对话框
        showDeleteConfirm.value = false
        activityToDelete.value = null

        // 刷新活动列表
        fetchActivities()
      } catch (error) {
        console.error('删除活动记录失败:', error)
        message.error('删除活动记录失败: ' + (error.message || '未知错误'))
      } finally {
        isDeleting.value = false
      }
    }

    // 切换活动选择状态
    const toggleActivitySelection = (activityId) => {
      if (selectedActivities.value.includes(activityId)) {
        // 如果已选中，则取消选中
        selectedActivities.value = selectedActivities.value.filter(id => id !== activityId)
        // 如果取消选中某个活动，全选状态也要取消
        selectAll.value = false
      } else {
        // 如果未选中，则选中
        selectedActivities.value.push(activityId)
        // 检查是否所有活动都被选中
        selectAll.value = selectedActivities.value.length === activities.value.length
      }
    }

    // 切换全选状态
    const toggleSelectAll = () => {
      selectAll.value = !selectAll.value

      if (selectAll.value) {
        // 全选：将所有活动ID添加到选中列表
        selectedActivities.value = activities.value.map(activity => activity.id)
      } else {
        // 取消全选：清空选中列表
        selectedActivities.value = []
      }
    }

    // 确认批量删除
    const confirmBatchDelete = () => {
      if (selectedActivities.value.length === 0) return
      showBatchDeleteConfirm.value = true
    }

    // 取消批量删除
    const cancelBatchDelete = () => {
      showBatchDeleteConfirm.value = false
    }

    // 批量删除活动
    const batchDeleteActivities = async () => {
      if (selectedActivities.value.length === 0) return

      isBatchDeleting.value = true
      try {
        const response = await activityApi.batchDeleteActivities(selectedActivities.value)
        message.success(response.message || `成功删除 ${response.deleted_count} 条活动记录`)

        // 关闭确认对话框
        showBatchDeleteConfirm.value = false

        // 清空选中列表
        selectedActivities.value = []
        selectAll.value = false

        // 刷新活动列表
        fetchActivities()
      } catch (error) {
        console.error('批量删除活动记录失败:', error)
        message.error('批量删除活动记录失败: ' + (error.message || '未知错误'))
      } finally {
        isBatchDeleting.value = false
      }
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
      getActionTypeClass,
      // 删除相关
      showDeleteConfirm,
      isDeleting,
      confirmDelete,
      cancelDelete,
      deleteActivity,
      // 批量删除相关
      selectedActivities,
      selectAll,
      toggleActivitySelection,
      toggleSelectAll,
      showBatchDeleteConfirm,
      isBatchDeleting,
      confirmBatchDelete,
      cancelBatchDelete,
      batchDeleteActivities
    }
  }
}
</script>
