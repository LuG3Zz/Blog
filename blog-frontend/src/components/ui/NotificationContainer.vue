<template>
  <div class="fixed inset-x-0 top-20 z-40 flex flex-col items-center gap-2 pointer-events-none">
    <TransitionGroup name="notification">
      <div v-for="notification in notifications" :key="notification.id" class="notification-item pointer-events-auto">
        <UserStatusNotification
          :name="notification.name"
          :description="notification.description"
          :time="formatTime(notification.timestamp)"
          :icon="notification.icon"
          :color="notification.color"
          :avatar="notification.avatar"
          :first-letter="getFirstLetter(notification)"
          @click="removeNotification(notification.id)"
          @close="removeNotification(notification.id)"
        />
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale/zh-CN';
import UserStatusNotification from './UserStatusNotification.vue';
import { initWebSocketService } from '@/services/websocket-new';
import { eventBus } from '@/utils/eventBus';

// 通知列表
const notifications = ref([]);

// 格式化时间
const formatTime = (timestamp) => {
  try {
    return formatDistanceToNow(new Date(timestamp), { addSuffix: true, locale: zhCN });
  } catch (error) {
    console.error('格式化时间出错:', error);
    return '刚刚';
  }
};

// 生成用户名的首字母
const getFirstLetter = (notification) => {
  if (notification.type === 'user_online' || notification.type === 'anonymous_online' ||
      notification.type === 'user_offline' || notification.type === 'user_welcome') {
    const username = notification.name || '';
    if (username) {
      // 获取用户名的第一个字符，并转为大写
      return username.charAt(0).toUpperCase();
    }
  }
  return '';
};

// 添加通知
const addNotification = (notification) => {
  console.log('添加通知:', notification);

  const id = Date.now().toString();
  notifications.value.unshift({
    id,
    ...notification
  });

  // 限制通知数量
  if (notifications.value.length > 3) {
    notifications.value = notifications.value.slice(0, 3);
  }

  // 5秒后自动移除通知
  setTimeout(() => {
    removeNotification(id);
  }, 5000);

  // 打印当前通知列表
  console.log('当前通知列表:', notifications.value);
};

// 移除通知
const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id);
  if (index !== -1) {
    notifications.value.splice(index, 1);
  }
};

// 监听通知事件
const handleNotification = (notification) => {
  console.log('NotificationContainer: 收到通知事件', notification);
  addNotification(notification);
};

// 组件挂载时初始化
onMounted(() => {
  // 检查页面是否已经加载完成
  if (document.readyState === 'complete') {
    // 页面已加载完成，直接初始化
    initWebSocketAndListeners();
  } else {
    // 页面尚未加载完成，等待页面加载完成后再初始化
    window.addEventListener('load', initWebSocketAndListeners);
  }
});

// 初始化WebSocket服务和事件监听器
const initWebSocketAndListeners = () => {
  console.log('页面加载完成，初始化WebSocket服务和通知监听器');

  // 先监听通知事件，确保在WebSocket连接之前注册
  console.log('NotificationContainer: 注册通知事件监听器');
  eventBus.on('notification', handleNotification);

  // 然后初始化WebSocket服务
  console.log('NotificationContainer: 初始化WebSocket服务');
  initWebSocketService();
};

// 组件卸载时清理
onUnmounted(() => {
  // 移除事件监听
  eventBus.off('notification', handleNotification);

  // 移除页面加载完成的事件监听器
  window.removeEventListener('load', initWebSocketAndListeners);
});
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.notification-move {
  transition: transform 0.3s ease;
}

.notification-item {
  width: 350px;
  max-width: 90vw;
  margin-bottom: 8px;
  animation: fadeIn 0.3s ease-in-out;
  position: relative;
  z-index: 1;
  isolation: isolate; /* 创建新的层叠上下文 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
