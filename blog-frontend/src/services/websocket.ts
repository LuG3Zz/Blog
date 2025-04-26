/**
 * WebSocket 服务
 * 处理与后端 WebSocket 连接和消息
 */

import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useUserStore } from '@/stores';
import { API_BASE_URL, WEBSOCKET } from '@/config';

// WebSocket 连接状态
export const enum WebSocketStatus {
  CONNECTING = 0,
  OPEN = 1,
  CLOSING = 2,
  CLOSED = 3,
}

// WebSocket 消息类型
export const enum MessageType {
  USER_ONLINE = 'user_online',
  USER_OFFLINE = 'user_offline',
  NOTIFICATION = 'notification',
  ADMIN_NOTIFICATION = 'admin_notification',
}

// WebSocket 消息接口
export interface WebSocketMessage {
  type: MessageType;
  data: any;
}

// 用户在线消息接口
export interface UserOnlineMessage {
  user_id: string;
  username: string;
  avatar?: string | null;
  is_admin?: boolean;
  timestamp?: string;
}

// 通知消息接口
export interface NotificationMessage {
  title: string;
  content: string;
  level: 'info' | 'success' | 'warning' | 'error';
  timestamp: string;
}

// 管理员通知消息接口
export interface AdminNotificationMessage {
  title: string;
  content: string;
  level: 'info' | 'success' | 'warning' | 'error';
  timestamp: string;
}

// 创建 WebSocket 服务
export function useWebSocket() {
  const socket = ref<WebSocket | null>(null);
  const status = ref<WebSocketStatus>(WebSocketStatus.CLOSED);
  const error = ref<string | null>(null);
  const reconnectAttempts = ref(0);
  const maxReconnectAttempts = WEBSOCKET.MAX_RECONNECT_ATTEMPTS;
  const reconnectInterval = WEBSOCKET.RECONNECT_INTERVAL;

  // 消息处理器
  const messageHandlers = new Map<MessageType, ((data: any) => void)[]>();

  // 添加消息处理器
  const addMessageHandler = (type: MessageType, handler: (data: any) => void) => {
    if (!messageHandlers.has(type)) {
      messageHandlers.set(type, []);
    }
    messageHandlers.get(type)?.push(handler);
  };

  // 移除消息处理器
  const removeMessageHandler = (type: MessageType, handler: (data: any) => void) => {
    const handlers = messageHandlers.get(type);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index !== -1) {
        handlers.splice(index, 1);
      }
    }
  };

  // 连接 WebSocket
  const connect = () => {
    // 检查用户是否已登录
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn('WebSocket: 用户未登录，无法连接 WebSocket');
      return;
    }

    // 关闭现有连接
    if (socket.value && [WebSocketStatus.OPEN, WebSocketStatus.CONNECTING].includes(status.value as WebSocketStatus)) {
      socket.value.close();
    }

    // 创建 WebSocket 连接
    try {
      // 构建 WebSocket URL
      const apiUrl = API_BASE_URL;
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

      // 构建 WebSocket URL
      let wsUrl = apiUrl.replace(/^https?:/, wsProtocol) + WEBSOCKET.PATH;

      // 如果认证方式为 URL，则在 URL 中添加 token
      if (WEBSOCKET.AUTH_METHOD === 'url' && token) {
        // 检查 token 是否已经包含 Bearer 前缀
        let formattedToken = token;
        if (!token.trim().toLowerCase().startsWith('bearer ')) {
          formattedToken = `Bearer ${token}`;
        }

        // 对 token 进行 URL 编码
        const encodedToken = encodeURIComponent(formattedToken);
        wsUrl += `?${WEBSOCKET.AUTH_PARAM_NAME}=${encodedToken}`;
      }

      console.log('WebSocket: 连接到', wsUrl.replace(token || '', '[REDACTED]'));

      socket.value = new WebSocket(wsUrl);
      status.value = WebSocketStatus.CONNECTING;
      error.value = null;

      // 连接打开时
      socket.value.onopen = () => {
        console.log('WebSocket: 连接已建立');
        status.value = WebSocketStatus.OPEN;
        reconnectAttempts.value = 0;

        // 如果认证方式为 message，则发送认证消息
        if (WEBSOCKET.AUTH_METHOD === 'message' && token) {
          // 检查 token 是否已经包含 Bearer 前缀
          let formattedToken = token;
          if (!token.trim().toLowerCase().startsWith('bearer ')) {
            formattedToken = `Bearer ${token}`;
          }

          sendMessage('auth', { token: formattedToken });
        }
      };

      // 接收消息时
      socket.value.onmessage = (event: MessageEvent) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage;
          console.log('WebSocket: 收到消息', message);

          // 调用对应类型的消息处理器
          const handlers = messageHandlers.get(message.type as MessageType);
          if (handlers) {
            handlers.forEach((handler: (data: any) => void) => handler(message.data));
          }
        } catch (err) {
          console.error('WebSocket: 解析消息失败', err);
        }
      };

      // 连接关闭时
      socket.value.onclose = (event) => {
        console.log('WebSocket: 连接已关闭', event.code, event.reason);
        status.value = WebSocketStatus.CLOSED;

        // 尝试重新连接
        if (reconnectAttempts.value < maxReconnectAttempts) {
          reconnectAttempts.value++;
          console.log(`WebSocket: 尝试重新连接 (${reconnectAttempts.value}/${maxReconnectAttempts})...`);
          setTimeout(connect, reconnectInterval);
        } else {
          console.error('WebSocket: 重连次数已达上限，停止重连');
        }
      };

      // 连接错误时
      socket.value.onerror = (event: Event) => {
        console.error('WebSocket: 连接错误', event);
        error.value = '连接错误';
      };
    } catch (err) {
      console.error('WebSocket: 创建连接失败', err);
      error.value = '创建连接失败';
    }
  };

  // 发送消息的通用方法

  // 发送消息
  const sendMessage = (type: string, data: any) => {
    if (socket.value && status.value === WebSocketStatus.OPEN) {
      socket.value.send(JSON.stringify({
        type,
        data
      }));
    } else {
      console.warn('WebSocket: 连接未打开，无法发送消息');
    }
  };

  // 关闭连接
  const disconnect = () => {
    if (socket.value) {
      socket.value.close();
      socket.value = null;
    }
  };

  // 组件挂载时连接 WebSocket
  onMounted(() => {
    // 获取用户状态管理实例
    const userStore = useUserStore();

    // 检查用户是否已登录
    if (userStore.isLoggedIn) {
      connect();
    }

    // 监听用户登录状态变化
    // 使用 watch 函数监听状态变化
    const stopWatch = watch(
      () => userStore.isLoggedIn,
      (isLoggedIn) => {
        if (isLoggedIn && (!socket.value || status.value === WebSocketStatus.CLOSED)) {
          connect();
        } else if (!isLoggedIn && socket.value) {
          disconnect();
        }
      }
    );

    // 组件卸载时取消监听
    onUnmounted(() => {
      stopWatch();
    });
  });

  // 组件卸载时关闭连接
  onUnmounted(() => {
    disconnect();
  });

  return {
    status,
    error,
    connect,
    disconnect,
    sendMessage,
    addMessageHandler,
    removeMessageHandler
  };
}

// 创建全局 WebSocket 实例
export const webSocketService = {
  socket: null as WebSocket | null,
  status: WebSocketStatus.CLOSED,
  messageHandlers: new Map<MessageType, ((data: any) => void)[]>(),

  // 初始化 WebSocket
  init() {
    // 获取用户令牌（如果已登录）
    const token = localStorage.getItem('token');
    // 获取或生成匿名用户标识符
    const anonymousId = this.getOrCreateAnonymousId();

    // 关闭现有连接
    if (this.socket && [WebSocketStatus.OPEN, WebSocketStatus.CONNECTING].includes(this.status)) {
      this.socket.close();
    }

    // 创建 WebSocket 连接
    try {
      // 构建 WebSocket URL
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsHost = window.location.host;

      // 使用相对路径构建 WebSocket URL
      let wsUrl = `${wsProtocol}//${wsHost}${WEBSOCKET.PATH}`;
      let hasQueryParam = false;

      // 如果用户已登录且认证方式为 URL，则在 URL 中添加 token
      if (WEBSOCKET.AUTH_METHOD === 'url' && token) {
        // 检查 token 是否已经包含 Bearer 前缀
        let formattedToken = token;
        if (!token.trim().toLowerCase().startsWith('bearer ')) {
          formattedToken = `Bearer ${token}`;
        }

        // 对 token 进行 URL 编码
        const encodedToken = encodeURIComponent(formattedToken);
        wsUrl += `?${WEBSOCKET.AUTH_PARAM_NAME}=${encodedToken}`;
        hasQueryParam = true;
      }

      // 添加匿名用户标识符
      if (anonymousId) {
        wsUrl += hasQueryParam ? '&' : '?';
        wsUrl += `anonymous_id=${encodeURIComponent(anonymousId)}`;
      }

      console.log('WebSocket: 连接到', wsUrl.replace(token || '', '[REDACTED]'));

      this.socket = new WebSocket(wsUrl);
      this.status = WebSocketStatus.CONNECTING;

      // 连接打开时
      this.socket.onopen = () => {
        console.log('WebSocket: 连接已建立');
        this.status = WebSocketStatus.OPEN;

        // 如果认证方式为 message，则发送认证消息
        if (WEBSOCKET.AUTH_METHOD === 'message' && token) {
          // 检查 token 是否已经包含 Bearer 前缀
          let formattedToken = token;
          if (!token.trim().toLowerCase().startsWith('bearer ')) {
            formattedToken = `Bearer ${token}`;
          }

          this.sendMessage('auth', { token: formattedToken });
        }

        // 发送匿名用户浏览消息
        if (!token && anonymousId) {
          this.sendMessage('anonymous_browsing', {
            anonymous_id: anonymousId,
            url: window.location.href,
            referrer: document.referrer || '',
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
          });
        }
      };

      // 接收消息时
      this.socket.onmessage = (event: MessageEvent) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage;
          console.log('WebSocket: 收到消息', message);

          // 调用对应类型的消息处理器
          const handlers = this.messageHandlers.get(message.type as MessageType);
          if (handlers) {
            handlers.forEach((handler: (data: any) => void) => handler(message.data));
          }
        } catch (err) {
          console.error('WebSocket: 解析消息失败', err);
        }
      };

      // 连接关闭时
      this.socket.onclose = () => {
        console.log('WebSocket: 连接已关闭');
        this.status = WebSocketStatus.CLOSED;
      };

      // 连接错误时
      this.socket.onerror = (event: Event) => {
        console.error('WebSocket: 连接错误', event);
      };
    } catch (err) {
      console.error('WebSocket: 创建连接失败', err);
    }
  },

  // 发送消息的方法已在下面实现

  // 添加消息处理器
  addMessageHandler(type: MessageType, handler: (data: any) => void) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    this.messageHandlers.get(type)?.push(handler);
  },

  // 移除消息处理器
  removeMessageHandler(type: MessageType, handler: (data: any) => void) {
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index !== -1) {
        handlers.splice(index, 1);
      }
    }
  },

  // 发送消息
  sendMessage(type: string, data: any) {
    if (this.socket && this.status === WebSocketStatus.OPEN) {
      this.socket.send(JSON.stringify({
        type,
        data
      }));
    } else {
      console.warn('WebSocket: 连接未打开，无法发送消息');
    }
  },

  // 关闭连接
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  },

  // 获取或创建匿名用户标识符
  getOrCreateAnonymousId() {
    let anonymousId = localStorage.getItem('anonymousId');

    // 如果不存在，创建一个新的匿名 ID
    if (!anonymousId) {
      anonymousId = 'anonymous_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      localStorage.setItem('anonymousId', anonymousId);
    }

    return anonymousId;
  }
};

// 初始化全局 WebSocket 服务
export function initWebSocketService() {
  // 获取用户状态管理实例
  const userStore = useUserStore();

  // 无论用户是否登录，都初始化 WebSocket 连接
  webSocketService.init();

  // 使用 watch 监听用户登录状态变化
  watch(
    () => userStore.isLoggedIn,
    (isLoggedIn) => {
      if (isLoggedIn && (!webSocketService.socket || webSocketService.status === WebSocketStatus.CLOSED)) {
        // 用户登录时，重新连接 WebSocket，使用登录凭证
        webSocketService.init();
      } else if (!isLoggedIn && webSocketService.socket) {
        // 用户登出时，发送登出消息后断开连接
        if (webSocketService.status === WebSocketStatus.OPEN) {
          webSocketService.sendMessage('user_logout', {
            timestamp: new Date().toISOString()
          });
        }
        // 断开连接后重新连接，使用匿名模式
        webSocketService.disconnect();
        setTimeout(() => webSocketService.init(), 500);
      }
    }
  );

  // 监听页面关闭事件，发送用户离开消息
  window.addEventListener('beforeunload', () => {
    if (webSocketService.socket && webSocketService.status === WebSocketStatus.OPEN) {
      const isLoggedIn = userStore.isLoggedIn;
      const anonymousId = webSocketService.getOrCreateAnonymousId();

      if (isLoggedIn) {
        // 已登录用户离开
        webSocketService.sendMessage('user_leave', {
          timestamp: new Date().toISOString()
        });
      } else if (anonymousId) {
        // 匿名用户离开
        webSocketService.sendMessage('anonymous_leave', {
          anonymous_id: anonymousId,
          timestamp: new Date().toISOString()
        });
      }
    }
  });
}
