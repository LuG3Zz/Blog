/**
 * WebSocket服务
 * 提供WebSocket连接、消息发送和接收功能
 */
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { WEBSOCKET } from '@/config';

// WebSocket连接状态枚举
export enum WebSocketStatus {
  CONNECTING = 0,
  OPEN = 1,
  CLOSING = 2,
  CLOSED = 3
}

// WebSocket连接状态描述
export const WebSocketStatusText = {
  [WebSocketStatus.CONNECTING]: '正在连接',
  [WebSocketStatus.OPEN]: '已连接',
  [WebSocketStatus.CLOSING]: '正在关闭',
  [WebSocketStatus.CLOSED]: '未连接'
}

// 消息类型
export enum MessageType {
  NOTIFICATION = 'notification',
  SYSTEM = 'system',
  AUTH = 'auth',
  ANONYMOUS_BROWSING = 'anonymous_browsing',
  USER_LOGOUT = 'user_logout',
  USER_LEAVE = 'user_leave',
  ANONYMOUS_LEAVE = 'anonymous_leave',
  USER_ONLINE = 'user_online',
  USER_OFFLINE = 'user_offline',
  ADMIN_NOTIFICATION = 'admin_notification'
}

// WebSocket消息接口
export interface WebSocketMessage {
  type: string;
  data: any;
}

// 用户上线/下线消息接口
export interface UserOnlineMessage {
  user_id: string;
  username: string;
  avatar?: string;
  timestamp?: string;
}

// 系统通知消息接口
export interface NotificationMessage {
  title?: string;
  content: string;
  level?: string;
  timestamp?: string;
}

// 管理员通知消息接口
export interface AdminNotificationMessage {
  title?: string;
  content: string;
  level?: string;
  admin_id?: string;
  admin_name?: string;
  timestamp?: string;
}

/**
 * 使用WebSocket的Hook
 * @param token 用户令牌
 * @param maxReconnectAttempts 最大重连次数
 * @param reconnectInterval 重连间隔（毫秒）
 * @returns WebSocket相关方法和状态
 */
export function useWebSocket(
  token?: string,
  maxReconnectAttempts = WEBSOCKET.MAX_RECONNECT_ATTEMPTS,
  reconnectInterval = WEBSOCKET.RECONNECT_INTERVAL
) {
  // WebSocket实例
  const socket = ref<WebSocket | null>(null);
  // 连接状态
  const status = ref<WebSocketStatus>(WebSocketStatus.CLOSED);
  // 错误信息
  const error = ref<string | null>(null);
  // 重连尝试次数
  const reconnectAttempts = ref<number>(0);
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

  // 连接WebSocket
  const connect = () => {
    // 如果已经连接，则不再重复连接
    if (socket.value && [WebSocketStatus.OPEN, WebSocketStatus.CONNECTING].includes(status.value)) {
      return;
    }

    // 创建WebSocket连接
    try {
      // 构建WebSocket URL
      // 使用完整的URL，包括协议、主机和路径
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsHost = window.location.hostname + (window.location.port ? ':' + window.location.port : '');
      let wsUrl = `${wsProtocol}//${wsHost}/api/v1${WEBSOCKET.PATH}`;

      // 获取或创建匿名用户标识符
      const anonymousId = getOrCreateAnonymousId();
      let hasQueryParam = false;

      // 如果认证方式为URL，则在URL中添加token
      if (WEBSOCKET.AUTH_METHOD === 'url' && token) {
        // 检查token是否已经包含Bearer前缀
        let formattedToken = token;
        if (!token.trim().toLowerCase().startsWith('bearer ')) {
          formattedToken = `Bearer ${token}`;
        }

        // 对token进行URL编码
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

      socket.value = new WebSocket(wsUrl);
      status.value = WebSocketStatus.CONNECTING;
      error.value = null;

      // 连接打开时
      socket.value.onopen = () => {
        console.log('WebSocket: 连接已建立');
        status.value = WebSocketStatus.OPEN;
        reconnectAttempts.value = 0;

        // 如果认证方式为message，则发送认证消息
        if (WEBSOCKET.AUTH_METHOD === 'message' && token) {
          // 检查token是否已经包含Bearer前缀
          let formattedToken = token;
          if (!token.trim().toLowerCase().startsWith('bearer ')) {
            formattedToken = `Bearer ${token}`;
          }

          sendMessage('auth', { token: formattedToken });
        }

        // 发送匿名用户浏览消息
        if (!token && anonymousId) {
          sendMessage('anonymous_browsing', {
            anonymous_id: anonymousId,
            url: window.location.href,
            referrer: document.referrer || '',
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
          });
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

  // 获取或创建匿名用户标识符
  const getOrCreateAnonymousId = () => {
    let anonymousId = localStorage.getItem('anonymousId');

    // 如果不存在，创建一个新的匿名ID
    if (!anonymousId) {
      anonymousId = 'anonymous_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      localStorage.setItem('anonymousId', anonymousId);
    }

    return anonymousId;
  };

  // 组件挂载时连接WebSocket
  onMounted(() => {
    // 获取用户状态管理实例
    const userStore = useUserStore();

    // 检查用户是否已登录
    if (userStore.isLoggedIn) {
      connect();
    }

    // 监听用户登录状态变化
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

// 创建全局WebSocket实例
export const webSocketService = {
  socket: null as WebSocket | null,
  status: WebSocketStatus.CLOSED,
  messageHandlers: new Map<MessageType, ((data: any) => void)[]>(),

  // 初始化WebSocket
  init() {
    // 获取用户令牌（如果已登录）
    const token = localStorage.getItem('token');
    // 获取或生成匿名用户标识符
    const anonymousId = this.getOrCreateAnonymousId();

    // 关闭现有连接
    if (this.socket && [WebSocketStatus.OPEN, WebSocketStatus.CONNECTING].includes(this.status)) {
      this.socket.close();
    }

    // 创建WebSocket连接
    try {
      // 构建WebSocket URL
      // 使用完整的URL，包括协议、主机和路径
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsHost = window.location.hostname + (window.location.port ? ':' + window.location.port : '');
      let wsUrl = `${wsProtocol}//${wsHost}/api/v1${WEBSOCKET.PATH}`;
      let hasQueryParam = false;

      // 如果用户已登录且认证方式为URL，则在URL中添加token
      if (WEBSOCKET.AUTH_METHOD === 'url' && token) {
        // 检查token是否已经包含Bearer前缀
        let formattedToken = token;
        if (!token.trim().toLowerCase().startsWith('bearer ')) {
          formattedToken = `Bearer ${token}`;
        }

        // 对token进行URL编码
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

        // 如果认证方式为message，则发送认证消息
        if (WEBSOCKET.AUTH_METHOD === 'message' && token) {
          // 检查token是否已经包含Bearer前缀
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

    // 如果不存在，创建一个新的匿名ID
    if (!anonymousId) {
      anonymousId = 'anonymous_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      localStorage.setItem('anonymousId', anonymousId);
    }

    return anonymousId;
  }
};

// 初始化全局WebSocket服务
export function initWebSocketService() {
  // 获取用户状态管理实例
  const userStore = useUserStore();

  // 无论用户是否登录，都初始化WebSocket连接
  webSocketService.init();

  // 使用watch监听用户登录状态变化
  watch(
    () => userStore.isLoggedIn,
    (isLoggedIn) => {
      if (isLoggedIn && (!webSocketService.socket || webSocketService.status === WebSocketStatus.CLOSED)) {
        // 用户登录时，重新连接WebSocket，使用登录凭证
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
