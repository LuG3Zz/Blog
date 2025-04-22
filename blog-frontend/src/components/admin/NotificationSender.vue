<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">发送系统通知</h2>

    <form @submit.prevent="sendNotification" class="space-y-4">
      <!-- 通知标题 -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          通知标题
        </label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          placeholder="输入通知标题"
          required
        />
      </div>

      <!-- 通知内容 -->
      <div>
        <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          通知内容
        </label>
        <textarea
          id="content"
          v-model="form.content"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          placeholder="输入通知内容"
          required
        ></textarea>
      </div>

      <!-- 通知级别 -->
      <div>
        <label for="level" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          通知级别
        </label>
        <select
          id="level"
          v-model="form.level"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        >
          <option value="info">信息</option>
          <option value="success">成功</option>
          <option value="warning">警告</option>
          <option value="error">错误</option>
        </select>
      </div>

      <!-- 目标用户 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          发送目标
        </label>
        <div class="flex items-center space-x-4">
          <label class="inline-flex items-center">
            <input
              type="radio"
              v-model="targetType"
              value="all"
              class="form-radio text-blue-600"
            />
            <span class="ml-2 text-gray-700 dark:text-gray-300">全站广播</span>
          </label>
          <label class="inline-flex items-center">
            <input
              type="radio"
              v-model="targetType"
              value="specific"
              class="form-radio text-blue-600"
            />
            <span class="ml-2 text-gray-700 dark:text-gray-300">指定用户</span>
          </label>
        </div>
      </div>

      <!-- 指定用户列表 -->
      <div v-if="targetType === 'specific'" class="space-y-2">
        <div class="flex items-center space-x-2">
          <input
            v-model="newUser"
            type="text"
            class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="输入用户名"
          />
          <button
            type="button"
            @click="addUser"
            class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            添加
          </button>
        </div>

        <div v-if="form.target_users && form.target_users.length > 0" class="flex flex-wrap gap-2 mt-2">
          <div
            v-for="(user, index) in form.target_users"
            :key="index"
            class="flex items-center bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-1 rounded-full"
          >
            <span>{{ user }}</span>
            <button
              type="button"
              @click="removeUser(index)"
              class="ml-2 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 focus:outline-none"
            >
              &times;
            </button>
          </div>
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="flex justify-end">
        <button
          type="submit"
          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          :disabled="loading"
        >
          {{ loading ? '发送中...' : '发送通知' }}
        </button>
      </div>
    </form>

    <!-- WebSocket 状态 -->
    <div class="mt-6 border-t border-gray-200 dark:border-gray-700 pt-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">WebSocket 状态</h3>

      <div v-if="wsStatusLoading" class="text-center py-4">
        <div class="inline-block animate-spin rounded-full h-6 w-6 border-2 border-gray-300 border-t-blue-600"></div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">加载中...</p>
      </div>

      <div v-else-if="wsStatusError" class="p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-md">
        {{ wsStatusError }}
      </div>

      <div v-else-if="wsStatus" class="space-y-2">
        <div class="flex justify-between py-2 border-b border-gray-200 dark:border-gray-700">
          <span class="text-gray-600 dark:text-gray-400">当前活跃连接数:</span>
          <span class="font-medium text-gray-900 dark:text-white">{{ wsStatus.active_connections }}</span>
        </div>

        <div class="flex justify-between py-2 border-b border-gray-200 dark:border-gray-700">
          <span class="text-gray-600 dark:text-gray-400">总连接次数:</span>
          <span class="font-medium text-gray-900 dark:text-white">{{ wsStatus.total_connections_ever }}</span>
        </div>

        <div v-if="wsStatus.connected_users" class="py-2">
          <div class="text-gray-600 dark:text-gray-400 mb-2">已连接用户:</div>
          <div class="grid grid-cols-2 gap-2">
            <div
              v-for="(info, userId) in wsStatus.connected_users"
              :key="userId"
              class="flex items-center justify-between p-2 bg-gray-100 dark:bg-gray-700 rounded"
            >
              <span class="text-gray-800 dark:text-gray-200">{{ userId }}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatTime(info.connected_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <button
          @click="fetchWsStatus"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        >
          刷新状态
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { notificationApi } from '@/api';
import message from '@/utils/message';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale/zh-CN';

export default {
  name: 'NotificationSender',

  setup() {
    // 表单数据
    const form = reactive({
      title: '',
      content: '',
      level: 'info',
      target_users: null
    });

    // 目标类型
    const targetType = ref('all');

    // 新用户输入
    const newUser = ref('');

    // 加载状态
    const loading = ref(false);

    // WebSocket 状态
    const wsStatus = ref(null);
    const wsStatusLoading = ref(false);
    const wsStatusError = ref(null);

    // 添加用户
    const addUser = () => {
      if (!newUser.value.trim()) return;

      if (!form.target_users) {
        form.target_users = [];
      }

      if (!form.target_users.includes(newUser.value.trim())) {
        form.target_users.push(newUser.value.trim());
      }

      newUser.value = '';
    };

    // 移除用户
    const removeUser = (index) => {
      form.target_users.splice(index, 1);

      if (form.target_users.length === 0) {
        form.target_users = null;
      }
    };

    // 发送通知
    const sendNotification = async () => {
      try {
        loading.value = true;

        // 如果是全站广播，设置 target_users 为 null
        if (targetType.value === 'all') {
          form.target_users = null;
        }

        // 发送通知
        const response = await notificationApi.sendNotification(form);

        // 显示成功消息
        console.log('发送通知响应:', response);
        let successMsg = '';

        // 检查响应中是否有 success 字段
        if (!response.success) {
          throw new Error(response.message || '发送通知失败');
        }

        // 根据目标类型生成不同的成功消息
        if (response.target_type === 'all_users') {
          successMsg = `通知已成功广播给所有用户（${response.connections_count || 0} 个在线连接）`;
        } else if (response.target_type === 'specific_users') {
          successMsg = `通知已成功发送给指定用户（${response.connections_count || 0} 个在线连接）`;
        } else {
          // 默认消息
          successMsg = response.message || `通知已成功发送（${response.connections_count || 0} 个在线连接）`;
        }

        // 显示成功消息，并设置显示时间为 5 秒
        message.success(successMsg, 5000);

        // 重置表单
        form.title = '';
        form.content = '';
        form.level = 'info';
        form.target_users = null;
        targetType.value = 'all';

        // 刷新 WebSocket 状态
        fetchWsStatus();
      } catch (error) {
        console.error('发送通知失败:', error);
        message.error('发送通知失败: ' + (error.message || '未知错误'));
      } finally {
        loading.value = false;
      }
    };

    // 获取 WebSocket 状态
    const fetchWsStatus = async () => {
      try {
        wsStatusLoading.value = true;
        wsStatusError.value = null;

        const response = await notificationApi.getWebSocketStatus();
        wsStatus.value = response;
      } catch (error) {
        console.error('获取 WebSocket 状态失败:', error);
        wsStatusError.value = '获取 WebSocket 状态失败: ' + (error.message || '未知错误');
      } finally {
        wsStatusLoading.value = false;
      }
    };

    // 格式化时间
    const formatTime = (timestamp) => {
      try {
        return formatDistanceToNow(new Date(timestamp), { addSuffix: true, locale: zhCN });
      } catch (error) {
        return timestamp;
      }
    };

    // 组件挂载时获取 WebSocket 状态
    onMounted(() => {
      fetchWsStatus();
    });

    return {
      form,
      targetType,
      newUser,
      loading,
      wsStatus,
      wsStatusLoading,
      wsStatusError,
      addUser,
      removeUser,
      sendNotification,
      fetchWsStatus,
      formatTime
    };
  }
};
</script>
