<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">订阅管理</h1>
      <p class="text-gray-600 dark:text-gray-300">管理博客的邮件订阅</p>
    </div>

    <!-- 搜索和过滤 -->
    <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm mb-6">
      <div class="flex flex-wrap gap-4">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">邮箱搜索</label>
          <input
            v-model="searchEmail"
            type="text"
            placeholder="搜索邮箱..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            @input="debouncedSearch"
          />
        </div>
        <div class="w-40">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">订阅类型</label>
          <select
            v-model="filters.subscription_type"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            @change="fetchSubscriptions"
          >
            <option value="">全部类型</option>
            <option value="all">全站订阅</option>
            <option value="author">作者订阅</option>
            <option value="category">分类订阅</option>
          </select>
        </div>
        <div class="w-40">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">状态</label>
          <select
            v-model="filters.is_active"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            @change="fetchSubscriptions"
          >
            <option value="">全部状态</option>
            <option :value="true">活跃</option>
            <option :value="false">未激活</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="resetFilters"
            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-md transition-colors"
          >
            重置
          </button>
        </div>
      </div>
    </div>

    <!-- 订阅列表 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                ID
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                邮箱
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                订阅类型
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                引用对象
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                状态
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                创建时间
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-if="loading" class="animate-pulse">
              <td colspan="7" class="px-6 py-4">
                <div class="flex justify-center">
                  <div class="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
              </td>
            </tr>
            <tr v-else-if="subscriptions.length === 0">
              <td colspan="7" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                没有找到订阅记录
              </td>
            </tr>
            <tr v-for="subscription in subscriptions" :key="subscription.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ subscription.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ subscription.email }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                <span class="px-2 py-1 text-xs rounded-full" :class="getSubscriptionTypeClass(subscription.subscription_type)">
                  {{ getSubscriptionTypeText(subscription.subscription_type) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ getReferenceName(subscription) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span
                  class="px-2 py-1 text-xs rounded-full"
                  :class="subscription.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'"
                >
                  {{ subscription.is_active ? '活跃' : '未激活' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ formatDate(subscription.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                <div class="flex space-x-2">
                  <button
                    @click="toggleSubscriptionStatus(subscription)"
                    class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                  >
                    {{ subscription.is_active ? '停用' : '激活' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-700 dark:text-gray-300">
            共 <span class="font-medium">{{ total }}</span> 条记录
          </div>
          <div class="flex space-x-2">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 text-sm"
              :class="currentPage === 1 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100 dark:hover:bg-gray-600'"
            >
              上一页
            </button>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage * pageSize >= total"
              class="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 text-sm"
              :class="currentPage * pageSize >= total ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100 dark:hover:bg-gray-600'"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { subscriptionsApi } from '@/api'
import message from '@/utils/message'
import { formatDateTime } from '@/utils/date-utils'
import { debounce } from 'lodash-es'

export default {
  name: 'SubscriptionManage',
  setup() {
    // 状态
    const subscriptions = ref([])
    const loading = ref(false)
    const total = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const searchEmail = ref('')

    // 过滤条件
    const filters = reactive({
      subscription_type: '',
      is_active: '',
    })

    // 获取订阅列表
    const fetchSubscriptions = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          email: searchEmail.value || undefined,
        }

        // 添加可选过滤条件
        if (filters.subscription_type) {
          params.subscription_type = filters.subscription_type
        }

        if (filters.is_active !== '') {
          params.is_active = filters.is_active
        }

        const response = await subscriptionsApi.getEmailSubscriptions(params)
        subscriptions.value = response.items || []
        total.value = response.total || 0
      } catch (error) {
        console.error('获取订阅列表失败:', error)
        message.error('获取订阅列表失败')
      } finally {
        loading.value = false
      }
    }

    // 切换订阅状态
    const toggleSubscriptionStatus = async (subscription) => {
      try {
        const newStatus = !subscription.is_active
        await subscriptionsApi.updateEmailSubscription(subscription.id, {
          is_active: newStatus
        })

        // 更新本地状态
        subscription.is_active = newStatus
        message.success(`订阅已${newStatus ? '激活' : '停用'}`)
      } catch (error) {
        console.error('更新订阅状态失败:', error)
        message.error('更新订阅状态失败')
      }
    }

    // 重置过滤条件
    const resetFilters = () => {
      searchEmail.value = ''
      filters.subscription_type = ''
      filters.is_active = ''
      currentPage.value = 1
      fetchSubscriptions()
    }

    // 切换页码
    const changePage = (page) => {
      if (page < 1 || page > Math.ceil(total.value / pageSize.value)) return
      currentPage.value = page
      fetchSubscriptions()
    }

    // 防抖搜索
    const debouncedSearch = debounce(() => {
      currentPage.value = 1
      fetchSubscriptions()
    }, 500)

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-';

      try {
        // 创建日期对象
        const utcDate = new Date(dateString);

        // 检查日期是否有效
        if (isNaN(utcDate.getTime())) {
          console.error('无效的日期字符串:', dateString);
          return dateString;
        }

        // 手动添加8小时，转换为中国时区(UTC+8)
        const chinaTime = new Date(utcDate.getTime() + 8 * 60 * 60 * 1000);

        // 使用formatDateTime格式化日期时间
        return formatDateTime(chinaTime.toISOString(), 'yyyy-MM-dd HH:mm:ss');
      } catch (error) {
        console.error('日期格式化错误:', error);
        return dateString;
      }
    }

    // 获取订阅类型文本
    const getSubscriptionTypeText = (type) => {
      const types = {
        all: '全站订阅',
        author: '作者订阅',
        category: '分类订阅'
      }
      return types[type] || type
    }

    // 获取订阅类型样式
    const getSubscriptionTypeClass = (type) => {
      const classes = {
        all: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
        author: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        category: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      }
      return classes[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }

    // 获取引用对象名称
    const getReferenceName = (subscription) => {
      if (subscription.subscription_type === 'all') {
        return '全站'
      } else if (subscription.reference_name) {
        return subscription.reference_name
      } else if (subscription.reference_id) {
        return `ID: ${subscription.reference_id}`
      }
      return '-'
    }

    // 组件挂载时获取数据
    onMounted(() => {
      fetchSubscriptions()
    })

    return {
      subscriptions,
      loading,
      total,
      currentPage,
      pageSize,
      searchEmail,
      filters,
      fetchSubscriptions,
      toggleSubscriptionStatus,
      resetFilters,
      changePage,
      debouncedSearch,
      formatDate,
      getSubscriptionTypeText,
      getSubscriptionTypeClass,
      getReferenceName
    }
  }
}
</script>
