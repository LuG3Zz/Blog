/**
 * WebSocket服务
 * 提供WebSocket连接、消息发送和接收功能
 */
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { WEBSOCKET } from '@/config';
import { eventBus } from '@/utils/eventBus';

// 扩展Window接口，添加webSocketInitialized属性
declare global {
  interface Window {
    webSocketInitialized?: boolean;
  }
}

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
  SYSTEM_NOTIFICATION = 'system_notification',
  AUTH = 'auth',
  ANONYMOUS_BROWSING = 'anonymous_browsing',
  USER_LOGOUT = 'user_logout',
  USER_LEAVE = 'user_leave',
  ANONYMOUS_LEAVE = 'anonymous_leave',
  USER_ONLINE = 'user_online',
  USER_OFFLINE = 'user_offline',
  ADMIN_NOTIFICATION = 'admin_notification',
  WELCOME = 'welcome',
  PING = 'ping',
  PONG = 'pong'
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

// 欢迎消息接口
export interface WelcomeMessage {
  title?: string;
  content: string;
  ip_location?: string;
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
    // 如果全局WebSocket已初始化，则不再创建新的连接
    if (window.webSocketInitialized) {
      console.log('全局WebSocket已初始化，组件不再创建新的连接');
      return;
    }

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

    console.log('初始化WebSocket连接，用户状态:', token ? '已登录' : '匿名用户');

    // 关闭现有连接
    if (this.socket && [WebSocketStatus.OPEN, WebSocketStatus.CONNECTING].includes(this.status)) {
      console.log('关闭现有WebSocket连接');
      this.socket.close();
      // 等待一段时间，确保连接完全关闭
      setTimeout(() => this._createConnection(token, anonymousId), 500);
      return;
    }

    // 创建新连接
    this._createConnection(token, anonymousId);
  },

  // 创建WebSocket连接
  _createConnection(token: string | null, anonymousId: string) {

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

        // 触发一个自定义事件，通知其他组件WebSocket已连接
        window.dispatchEvent(new CustomEvent('websocket-connected'));

        // 如果认证方式为message，则发送认证消息
        if (WEBSOCKET.AUTH_METHOD === 'message' && token) {
          // 检查token是否已经包含Bearer前缀
          let formattedToken = token;
          if (!token.trim().toLowerCase().startsWith('bearer ')) {
            formattedToken = `Bearer ${token}`;
          }

          this.sendMessage('auth', { token: formattedToken });
          console.log('已发送认证消息');
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
          console.log('已发送匿名用户浏览消息');
        }

        // 发送ping消息，确保连接活跃
        this.sendMessage('ping', { timestamp: new Date().toISOString() });
        console.log('已发送ping消息');

        // 设置定时ping，保持连接活跃
        setInterval(() => {
          if (this.status === WebSocketStatus.OPEN) {
            this.sendMessage('ping', { timestamp: new Date().toISOString() });
          }
        }, 30000); // 每30秒发送一次ping
      };

      // 接收消息时
      this.socket.onmessage = (event: MessageEvent) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage;
          console.log('WebSocket: 收到消息', message);

          // 调用对应类型的消息处理器
          const handlers = this.messageHandlers.get(message.type as MessageType);
          if (handlers) {
            console.log(`WebSocket: 找到 ${handlers.length} 个处理器，类型: ${message.type}`);
            handlers.forEach((handler: (data: any) => void) => {
              try {
                handler(message.data);
              } catch (handlerErr) {
                console.error(`WebSocket: 处理器执行失败，类型: ${message.type}`, handlerErr);
              }
            });
          } else {
            console.warn(`WebSocket: 未找到处理器，类型: ${message.type}`);
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
  // 检查是否已经初始化
  if (window.webSocketInitialized) {
    console.log('WebSocket服务已经初始化，跳过重复初始化');
    // 即使已初始化，也检查连接状态，如果未连接则重新连接
    if (webSocketService.status === WebSocketStatus.CLOSED) {
      console.log('WebSocket连接已关闭，尝试重新连接');
      webSocketService.init();
    }
    return;
  }

  // 设置初始化标志，防止重复初始化
  window.webSocketInitialized = true;

  // 获取用户状态管理实例
  const userStore = useUserStore();

  // 注册消息处理器
  webSocketService.addMessageHandler(MessageType.WELCOME, (data) => {
    console.log('收到欢迎消息:', data);

    // 存储欢迎消息，等待页面加载完成后显示
    const showWelcomeMessage = () => {
      // 检查是否有用户信息
      if (data.user_id && data.username) {
        // 已登录用户，使用用户头像
        const description = data.content || '欢迎回来！';

        eventBus.emit('notification', {
          type: 'user_welcome',
          name: data.username,
          description: description,
          icon: '👋',
          color: '#4f46e5', // indigo-600
          timestamp: new Date(data.timestamp || new Date().toISOString()),
          avatar: data.avatar,
          data,
        });
      } else {
        // 匿名用户，使用系统图标
        const description = data.content || '欢迎访问我的博客！';

        eventBus.emit('notification', {
          type: 'system',
          name: data.title || '欢迎',
          description: description,
          icon: '✅',
          color: '#16a34a', // green-600
          timestamp: new Date(data.timestamp || new Date().toISOString()),
          data,
        });
      }
    };

    // 检查页面是否已经加载完成
    if (document.readyState === 'complete') {
      // 页面已加载完成，延迟一小段时间再显示欢迎消息，确保所有组件都已渲染
      setTimeout(showWelcomeMessage, 1000);
    } else {
      // 页面尚未加载完成，等待页面加载完成后再显示欢迎消息
      window.addEventListener('load', () => {
        // 页面加载完成后，延迟一小段时间再显示欢迎消息
        setTimeout(showWelcomeMessage, 1000);
      });
    }
  });

  webSocketService.addMessageHandler(MessageType.SYSTEM_NOTIFICATION, (data) => {
    console.log('收到系统通知:', data);

    // 忽略WebSocket连接相关的系统通知
    if (data.message && (
        data.message.includes('WebSocket连接已初始化') ||
        data.message.includes('WebSocket连接已建立') ||
        data.message.includes('正在处理')
    )) {
      console.log('忽略WebSocket连接相关的系统通知');
      return;
    }

    // 处理其他系统通知
    eventBus.emit('notification', {
      type: 'system',
      name: '系统通知',
      description: data.message || data.content || '系统通知',
      icon: 'ℹ️',
      color: '#0891b2', // cyan-600
      timestamp: new Date(data.timestamp || new Date().toISOString()),
      data,
    });
  });

  webSocketService.addMessageHandler(MessageType.NOTIFICATION, (data) => {
    console.log('收到通知:', data);
    eventBus.emit('notification', {
      type: 'system',
      name: data.title || '通知',
      description: data.content,
      icon: data.level === 'error' ? '❌' : data.level === 'warning' ? '⚠️' : data.level === 'success' ? '✅' : 'ℹ️',
      color: data.level === 'error' ? '#e11d48' : data.level === 'warning' ? '#ea580c' : data.level === 'success' ? '#16a34a' : '#0891b2',
      timestamp: new Date(data.timestamp || new Date().toISOString()),
      data,
    });
  });

  webSocketService.addMessageHandler(MessageType.ADMIN_NOTIFICATION, (data) => {
    console.log('收到管理员通知:', data);
    eventBus.emit('notification', {
      type: 'admin',
      name: data.title || '管理员通知',
      description: data.content,
      icon: '💬',
      color: '#0891b2', // cyan-600
      timestamp: new Date(data.timestamp || new Date().toISOString()),
      data,
    });
  });

  webSocketService.addMessageHandler(MessageType.USER_ONLINE, (data) => {
    console.log('收到用户上线消息:', data);
    console.log('用户上线消息类型:', typeof data);
    console.log('用户上线消息是否为匿名用户:', data.is_anonymous);

    // 提取IP属地信息
    const ipLocation = data.ip_location || '';
    const username = data.original_username || data.username || '用户';
    const isAnonymous = data.is_anonymous === true;

    // 构建带有IP属地的描述
    let description = `${username} 已上线`;
    if (ipLocation) {
      description = `${username} 已上线 (${ipLocation})`;
    }

    console.log(`准备显示用户上线通知: ${description}, 是否为匿名用户: ${isAnonymous}`);

    // 创建显示通知的函数
    const showNotification = () => {
      console.log(`显示用户上线通知: ${description}, 是否为匿名用户: ${isAnonymous}`);

      // 发送通知
      const notification = {
        type: isAnonymous ? 'anonymous_online' : 'user_online',
        name: username,
        description: description,
        icon: '👋',
        color: isAnonymous ? '#0891b2' : '#4f46e5', // 匿名用户使用青色，已登录用户使用靛蓝色
        timestamp: new Date(data.timestamp || new Date().toISOString()),
        avatar: data.avatar,
        data,
      };

      console.log('发送用户上线通知到事件总线:', notification);
      eventBus.emit('notification', notification);
    };

    // 检查页面是否已经加载完成
    console.log(`当前页面加载状态: ${document.readyState}`);
    if (document.readyState === 'complete') {
      // 页面已加载完成，直接显示通知
      console.log('页面已加载完成，直接显示通知');
      showNotification();
    } else {
      // 页面尚未加载完成，等待页面加载完成后再显示通知
      console.log('页面尚未加载完成，等待页面加载完成后再显示通知');
      window.addEventListener('load', () => {
        console.log('页面加载完成事件触发，显示通知');
        showNotification();
      });
    }
  });

  webSocketService.addMessageHandler(MessageType.USER_OFFLINE, (data) => {
    console.log('用户下线:', data);

    // 提取IP属地信息
    const ipLocation = data.ip_location || '';
    const username = data.original_username || data.username || '用户';

    // 构建带有IP属地的描述
    let description = `${username} 已下线`;
    if (ipLocation) {
      description = `${username} 已下线 (${ipLocation})`;
    }

    // 创建显示通知的函数
    const showNotification = () => {
      // 发送通知
      eventBus.emit('notification', {
        type: 'user_offline',
        name: username,
        description: description,
        icon: '👋',
        color: '#7c3aed', // violet-600
        timestamp: new Date(data.timestamp || new Date().toISOString()),
        avatar: data.avatar,
        data,
      });
    };

    // 检查页面是否已经加载完成
    if (document.readyState === 'complete') {
      // 页面已加载完成，直接显示通知
      showNotification();
    } else {
      // 页面尚未加载完成，等待页面加载完成后再显示通知
      window.addEventListener('load', showNotification);
    }
  });

  // 无论用户是否登录，都初始化WebSocket连接
  webSocketService.init();

  console.log('WebSocket服务初始化完成');

  // 使用watch监听用户登录状态变化
  watch(
    () => userStore.isLoggedIn,
    (isLoggedIn) => {
      if (isLoggedIn && (!webSocketService.socket || webSocketService.status === WebSocketStatus.CLOSED)) {
        // 用户登录时，重新连接WebSocket，使用登录凭证
        webSocketService.init();
        console.log('用户登录，重新连接WebSocket');
      } else if (!isLoggedIn && webSocketService.socket) {
        // 用户登出时，发送登出消息后断开连接
        if (webSocketService.status === WebSocketStatus.OPEN) {
          webSocketService.sendMessage('user_logout', {
            timestamp: new Date().toISOString()
          });
          console.log('用户登出，发送登出消息');
        }
        // 断开连接后重新连接，使用匿名模式
        webSocketService.disconnect();
        setTimeout(() => webSocketService.init(), 500);
        console.log('用户登出，断开连接后重新连接');
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
