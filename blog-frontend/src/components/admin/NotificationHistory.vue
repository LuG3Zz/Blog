<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white">通知历史</h2>
      <button
        @click="clearAllNotifications"
        class="px-3 py-1 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md"
      >
        清空历史
      </button>
    </div>

    <!-- 筛选器 -->
    <div class="mb-4 flex gap-2">
      <select
        v-model="filter.level"
        class="px-3 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-sm"
      >
        <option value="">所有级别</option>
        <option value="info">信息</option>
        <option value="success">成功</option>
        <option value="warning">警告</option>
        <option value="error">错误</option>
      </select>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white mx-auto"></div>
      <p class="mt-2 text-gray-600 dark:text-gray-400">加载中...</p>
    </div>

    <!-- 通知列表 -->
    <div v-else-if="notifications.length" class="space-y-4">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-2">
            <span
              class="w-2 h-2 rounded-full"
              :class="{
                'bg-blue-500': notification.level === 'info',
                'bg-green-500': notification.level === 'success',
                'bg-yellow-500': notification.level === 'warning',
                'bg-red-500': notification.level === 'error'
              }"
            ></span>
            <h3 class="font-medium text-gray-900 dark:text-white">{{ notification.title }}</h3>
          </div>
          <button
            @click="deleteNotification(notification.id)"
            class="text-gray-400 hover:text-red-500 dark:hover:text-red-400"
          >
            <span class="sr-only">删除</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <p class="mt-1 text-gray-600 dark:text-gray-400">{{ notification.content }}</p>
        <div class="mt-2 text-sm text-gray-500 dark:text-gray-500">
          {{ formatTime(notification.created_at) }}
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
      <p>暂无通知历史</p>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="mt-6 flex justify-between items-center">
      <div class="text-sm text-gray-600 dark:text-gray-400">
        共 {{ total }} 条记录
      </div>
      <div class="flex gap-2">
        <button
          v-for="p in pages"
          :key="p"
          @click="page = p"
          class="px-3 py-1 rounded-md"
          :class="{
            'bg-blue-500 text-white': page === p,
            'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700': page !== p
          }"
        >
          {{ p }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import { notificationHistoryApi } from '@/api';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import message from '@/utils/message';

export default {
  name: 'NotificationHistory',

  setup() {
    const notifications = ref([]);
    const loading = ref(false);
    const page = ref(1);
    const pageSize = ref(10);
    const total = ref(0);
    const pages = ref(1);
    const filter = ref({
      level: ''
    });

    // 获取通知列表
    const fetchNotifications = async () => {
      loading.value = true;
      try {
        const response = await notificationHistoryApi.getNotificationHistory({
          page: page.value,
          page_size: pageSize.value,
          level: filter.value.level || undefined
        });
        notifications.value = response.items;
        total.value = response.total;
        pages.value = response.pages;
      } catch (error) {
        message.error('获取通知历史失败');
        console.error('获取通知历史失败:', error);
      } finally {
        loading.value = false;
      }
    };

    // 删除单个通知
    const deleteNotification = async (id) => {
      try {
        await notificationHistoryApi.deleteNotification(id);
        message.success('删除成功');
        fetchNotifications();
      } catch (error) {
        message.error('删除失败');
        console.error('删除通知失败:', error);
      }
    };

    // 清空所有通知
    const clearAllNotifications = async () => {
      if (!confirm('确定要清空所有通知历史吗？')) return;

      try {
        await notificationHistoryApi.clearNotifications();
        message.success('清空成功');
        fetchNotifications();
      } catch (error) {
        message.error('清空失败');
        console.error('清空通知历史失败:', error);
      }
    };

    // 格式化时间
    const formatTime = (timestamp) => {
      try {
        if (!timestamp) return '未知时间';
        return formatDistanceToNow(new Date(timestamp), { addSuffix: true, locale: zhCN });
      } catch (error) {
        console.error('格式化时间错误:', error, timestamp);
        return '无效时间';
      }
    };

    // 监听筛选条件变化
    watch([() => page.value, () => filter.value.level], () => {
      fetchNotifications();
    });

    // 初始加载
    fetchNotifications();

    return {
      notifications,
      loading,
      page,
      total,
      pages,
      filter,
      deleteNotification,
      clearAllNotifications,
      formatTime
    };
  }
};
</script>