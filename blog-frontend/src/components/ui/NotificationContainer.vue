<template>
  <div class="fixed inset-x-0 top-20 z-40 flex flex-col items-center gap-2 pointer-events-none">
    <TransitionGroup name="notification">
      <div v-for="notification in activeNotifications" :key="notification.id" class="notification-item pointer-events-auto">
        <UserStatusNotification
          :name="getNotificationTitle(notification)"
          :description="notification.content"
          :time="formatTime(notification.timestamp)"
          :icon="getNotificationIcon(notification)"
          :color="getNotificationColor(notification)"
          :avatar="getNotificationAvatar(notification)"
          :first-letter="getFirstLetter(notification)"
          @click="markAsRead(notification.id)"
          @close="closeNotification(notification.id)"
        />
      </div>
    </TransitionGroup>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue';
import UserStatusNotification from './UserStatusNotification.vue';
import { notificationService, initNotificationService, Notification, NotificationType, NotificationLevel } from '@/services/notification';
import { initWebSocketService } from '@/services/websocket-new';

// 获取活跃通知
const activeNotifications = computed(() => {
  console.log('当前通知列表:', notificationService.notifications);
  return notificationService.notifications.filter((n: Notification) => !n.read).slice(0, 3);
});

// 获取通知标题
const getNotificationTitle = (notification: Notification): string => {
  switch (notification.type) {
    case NotificationType.USER_ONLINE:
      return notification.data?.username || '用户上线';
    case NotificationType.USER_OFFLINE:
      return notification.data?.username || '用户下线';
    case NotificationType.SYSTEM:
      return notification.title;
    default:
      return notification.title;
  }
};

// 获取通知图标
const getNotificationIcon = (notification: Notification): string => {
  return notificationService.getNotificationIcon(notification.type, notification.level);
};

// 获取通知颜色
const getNotificationColor = (notification: Notification): string => {
  // 如果是用户上线或下线通知，且没有头像，使用基于用户名的颜色
  if (
    (notification.type === NotificationType.USER_ONLINE ||
     notification.type === NotificationType.USER_OFFLINE) &&
    !getNotificationAvatar(notification)
  ) {
    const username = notification.data?.username || '';
    if (username) {
      return getUserColor(username);
    }
  }
  // 否则使用默认颜色
  return notificationService.getNotificationColor(notification.type, notification.level);
};

// 生成用户名的首字母
const getFirstLetter = (notification: Notification): string => {
  if (
    notification.type === NotificationType.USER_ONLINE ||
    notification.type === NotificationType.USER_OFFLINE
  ) {
    const username = notification.data?.username || '';
    if (username) {
      // 获取用户名的第一个字符，并转为大写
      return username.charAt(0).toUpperCase();
    }
  }
  return '';
};

// 根据用户名生成随机颜色
const getUserColor = (username: string): string => {
  // 预定义的颜色数组，这些颜色都比较适合作为背景色
  const colors = [
    '#4f46e5', // indigo-600
    '#0891b2', // cyan-600
    '#0d9488', // teal-600
    '#7c3aed', // violet-600
    '#c026d3', // fuchsia-600
    '#db2777', // pink-600
    '#e11d48', // rose-600
    '#ea580c', // orange-600
    '#65a30d', // lime-600
    '#16a34a', // green-600
  ];

  // 使用用户名的字符码之和作为随机数生成器的种子
  let sum = 0;
  for (let i = 0; i < username.length; i++) {
    sum += username.charCodeAt(i);
  }

  // 使用这个和来选择颜色
  return colors[sum % colors.length];
};

// 获取通知头像
const getNotificationAvatar = (notification: Notification): string | null => {
  // 如果是用户上线或下线通知，尝试获取用户头像
  if (
    notification.type === NotificationType.USER_ONLINE ||
    notification.type === NotificationType.USER_OFFLINE
  ) {
    // 检查头像是否为 null 或空字符串
    const avatar = notification.data?.avatar;

    if (avatar && typeof avatar === 'string' && avatar.trim() !== '') {
      // 如果头像是相对路径，添加基础 URL
      if (avatar.startsWith('/')) {
        return `${window.location.origin}${avatar}`;
      }
      return avatar;
    }
  }
  return null; // 返回 null，让组件显示首字母
};

// 格式化时间
const formatTime = (timestamp: Date): string => {
  return notificationService.formatTime(timestamp);
};

// 标记通知为已读
const markAsRead = (id: string): void => {
  notificationService.markAsRead(id);
};

// 关闭通知
const closeNotification = (id: string): void => {
  // 如果是当前显示的通知，则关闭它
  if (notificationService.currentNotification.value?.id === id) {
    notificationService.closeCurrentNotification();
  } else {
    // 否则只标记为已读
    notificationService.markAsRead(id);
  }
};

// 组件挂载时初始化服务
onMounted(() => {
  initWebSocketService();
  initNotificationService();

//   // 测试通知（开发环境）
//   const isDev = process.env.NODE_ENV === 'development';
//   if (isDev) {
//     setTimeout(() => {
//       notificationService.addNotification({
//         type: NotificationType.USER_ONLINE,
//         title: '用户上线',
//         content: '张三 已上线',
//         level: NotificationLevel.INFO,
//         timestamp: new Date(),
//         data: { username: '张三', user_id: '123', timestamp: new Date().toISOString() },
//       });
//     }, 1000);

//     setTimeout(() => {
//       notificationService.addNotification({
//         type: NotificationType.SYSTEM,
//         title: '系统通知',
//         content: '系统将于今晚23:00进行维护，预计持续1小时。',
//         level: NotificationLevel.WARNING,
//         timestamp: new Date(),
//       });
//     }, 1000);
//   }
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
