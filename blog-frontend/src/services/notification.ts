/**
 * 通知服务
 * 处理系统通知和用户状态通知
 */

import { ref, reactive } from 'vue';
import { MessageType, UserOnlineMessage, NotificationMessage, AdminNotificationMessage, webSocketService } from './websocket';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale/zh-CN';

// 通知显示时间配置（毫秒）
const NOTIFICATION_DISPLAY_DURATION = {
  // 用户上线通知显示 3 秒
  USER_ONLINE: 3000,
  // 用户下线通知显示 3 秒
  USER_OFFLINE: 3000,
  // 系统通知显示 10 秒
  SYSTEM: 10000,
  // 管理员通知显示 10 秒
  ADMIN: 10000,
  // 默认显示 5 秒
  DEFAULT: 5000
};

// 通知类型
export enum NotificationType {
  USER_ONLINE = 'user_online',
  USER_OFFLINE = 'user_offline',
  SYSTEM = 'system',
  ADMIN = 'admin',
}

// 通知级别
export enum NotificationLevel {
  INFO = 'info',
  SUCCESS = 'success',
  WARNING = 'warning',
  ERROR = 'error',
}

// 通知接口
export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  content: string;
  level: NotificationLevel;
  timestamp: Date;
  read: boolean;
  data?: any;
}

// 通知状态
const notifications = reactive<Notification[]>([]);
const showNotification = ref(false);
const currentNotification = ref<Notification | null>(null);

// 获取通知图标
const getNotificationIcon = (type: NotificationType, level: NotificationLevel): string => {
  switch (type) {
    case NotificationType.USER_ONLINE:
      return '👋';
    case NotificationType.USER_OFFLINE:
      return '👋';
    case NotificationType.ADMIN:
      return '💬'; // 对话气泡图标
    case NotificationType.SYSTEM:
      switch (level) {
        case NotificationLevel.INFO:
          return 'ℹ️';
        case NotificationLevel.SUCCESS:
          return '✅';
        case NotificationLevel.WARNING:
          return '⚠️';
        case NotificationLevel.ERROR:
          return '❌';
        default:
          return 'ℹ️';
      }
    default:
      return 'ℹ️';
  }
};

// 获取通知颜色
const getNotificationColor = (type: NotificationType, level: NotificationLevel): string => {
  switch (type) {
    case NotificationType.USER_ONLINE:
      return '#4ade80'; // 绿色
    case NotificationType.USER_OFFLINE:
      return '#94a3b8'; // 灰色
    case NotificationType.ADMIN:
      switch (level) {
        case NotificationLevel.INFO:
          return '#8b5cf6'; // 紫色
        case NotificationLevel.SUCCESS:
          return '#4ade80'; // 绿色
        case NotificationLevel.WARNING:
          return '#fbbf24'; // 黄色
        case NotificationLevel.ERROR:
          return '#f87171'; // 红色
        default:
          return '#8b5cf6'; // 紫色
      }
    case NotificationType.SYSTEM:
      switch (level) {
        case NotificationLevel.INFO:
          return '#60a5fa'; // 蓝色
        case NotificationLevel.SUCCESS:
          return '#4ade80'; // 绿色
        case NotificationLevel.WARNING:
          return '#fbbf24'; // 黄色
        case NotificationLevel.ERROR:
          return '#f87171'; // 红色
        default:
          return '#60a5fa'; // 蓝色
      }
    default:
      return '#60a5fa'; // 蓝色
  }
};

// 格式化时间
const formatTime = (date: Date): string => {
  try {
    // 检查时间是否有效
    if (!(date instanceof Date) || isNaN(date.getTime())) {
      console.error('无效的时间值:', date);
      return '刚刚'; // 返回默认值
    }
    return formatDistanceToNow(date, { addSuffix: true, locale: zhCN });
  } catch (error) {
    console.error('格式化时间出错:', error);
    return '刚刚'; // 返回默认值
  }
};

// 添加通知
const addNotification = (notification: Omit<Notification, 'id' | 'read'>): void => {
  const id = Date.now().toString();
  const newNotification: Notification = {
    ...notification,
    id,
    read: false,
  };

  // 添加到通知列表
  notifications.unshift(newNotification);

  // 限制通知数量
  if (notifications.length > 50) {
    notifications.pop();
  }

  // 显示通知
  showCurrentNotification(newNotification);
};

// 显示当前通知
const showCurrentNotification = (notification: Notification): void => {
  currentNotification.value = notification;
  showNotification.value = true;

  // 获取通知类型对应的显示时间
  let duration = NOTIFICATION_DISPLAY_DURATION.DEFAULT;

  switch (notification.type) {
    case NotificationType.USER_ONLINE:
      duration = NOTIFICATION_DISPLAY_DURATION.USER_ONLINE;
      break;
    case NotificationType.USER_OFFLINE:
      duration = NOTIFICATION_DISPLAY_DURATION.USER_OFFLINE;
      break;
    case NotificationType.SYSTEM:
      duration = NOTIFICATION_DISPLAY_DURATION.SYSTEM;
      break;
    case NotificationType.ADMIN:
      duration = NOTIFICATION_DISPLAY_DURATION.ADMIN;
      break;
  }

  // 设置定时器，在指定时间后自动关闭通知
  const timer = setTimeout(() => {
    if (currentNotification.value?.id === notification.id) {
      showNotification.value = false;
      currentNotification.value = null;
    }
    // 标记为已读
    markAsRead(notification.id);
  }, duration);

  // 将定时器 ID 存储在通知对象上，以便需要时可以清除
  (notification as any)._timer = timer;
};

// 关闭当前通知
const closeCurrentNotification = (): void => {
  if (currentNotification.value) {
    // 清除定时器
    const timer = (currentNotification.value as any)._timer;
    if (timer) {
      clearTimeout(timer);
    }

    // 标记为已读
    markAsRead(currentNotification.value.id);

    // 关闭通知
    showNotification.value = false;
    currentNotification.value = null;
  }
};

// 标记通知为已读
const markAsRead = (id: string): void => {
  const notification = notifications.find(n => n.id === id);
  if (notification) {
    notification.read = true;
  }
};

// 标记所有通知为已读
const markAllAsRead = (): void => {
  notifications.forEach(notification => {
    notification.read = true;
  });
};

// 清除通知
const clearNotification = (id: string): void => {
  const index = notifications.findIndex(n => n.id === id);
  if (index !== -1) {
    notifications.splice(index, 1);
  }
};

// 清除所有通知
const clearAllNotifications = (): void => {
  notifications.splice(0, notifications.length);
};

// 处理用户上线消息
const handleUserOnlineMessage = (data: UserOnlineMessage): void => {
  console.log('处理用户上线消息:', data);
  addNotification({
    type: NotificationType.USER_ONLINE,
    title: '用户上线',
    content: `${data.username} 已上线`,
    level: NotificationLevel.INFO,
    timestamp: new Date(data.timestamp || new Date().toISOString()),
    data,
  });
};

// 处理用户下线消息
const handleUserOfflineMessage = (data: UserOnlineMessage): void => {
  console.log('处理用户下线消息:', data);
  addNotification({
    type: NotificationType.USER_OFFLINE,
    title: '用户下线',
    content: `${data.username} 已下线`,
    level: NotificationLevel.INFO,
    timestamp: new Date(data.timestamp || new Date().toISOString()),
    data,
  });
};

// 处理系统通知消息
const handleNotificationMessage = (data: NotificationMessage): void => {
  // 验证时间戳
  let timestamp: Date;
  try {
    // 如果时间戳不存在或无效，使用当前时间
    if (!data.timestamp || isNaN(new Date(data.timestamp).getTime())) {
      console.warn('系统通知消息的时间戳无效，使用当前时间:', data.timestamp);
      timestamp = new Date();
    } else {
      timestamp = new Date(data.timestamp);
    }
  } catch (error) {
    console.error('解析系统通知消息的时间戳出错:', error);
    timestamp = new Date();
  }

  addNotification({
    type: NotificationType.SYSTEM,
    title: data.title || '系统通知',
    content: data.content || '',
    level: (data.level as NotificationLevel) || NotificationLevel.INFO,
    timestamp,
    data,
  });
};

// 处理管理员通知消息
const handleAdminNotificationMessage = (data: AdminNotificationMessage): void => {
  console.log('处理管理员通知消息:', data);

  // 验证时间戳
  let timestamp: Date;
  try {
    // 如果时间戳不存在或无效，使用当前时间
    if (!data.timestamp || isNaN(new Date(data.timestamp).getTime())) {
      console.warn('管理员通知消息的时间戳无效，使用当前时间:', data.timestamp);
      timestamp = new Date();
    } else {
      timestamp = new Date(data.timestamp);
    }
  } catch (error) {
    console.error('解析管理员通知消息的时间戳出错:', error);
    timestamp = new Date();
  }

  addNotification({
    type: NotificationType.ADMIN,
    title: data.title || '管理员通知',
    content: data.content || '',
    level: (data.level as NotificationLevel) || NotificationLevel.INFO,
    timestamp,
    data,
  });
};

// 初始化通知服务
export function initNotificationService(): void {
  // 添加 WebSocket 消息处理器
  webSocketService.addMessageHandler(MessageType.USER_ONLINE, handleUserOnlineMessage);
  webSocketService.addMessageHandler(MessageType.USER_OFFLINE, handleUserOfflineMessage);
  webSocketService.addMessageHandler(MessageType.NOTIFICATION, handleNotificationMessage);
  webSocketService.addMessageHandler(MessageType.ADMIN_NOTIFICATION, handleAdminNotificationMessage);
}

// 导出通知服务
export const notificationService = {
  notifications,
  showNotification,
  currentNotification,
  getNotificationIcon,
  getNotificationColor,
  formatTime,
  addNotification,
  markAsRead,
  markAllAsRead,
  clearNotification,
  clearAllNotifications,
  closeCurrentNotification,
};
