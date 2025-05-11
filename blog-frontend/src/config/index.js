/**
 * 全局配置文件
 * 集中管理所有配置项，方便统一修改
 */

// 运行模式
export const MODE = import.meta.env.VITE_MODE || 'development';

// API 基础 URL
// 在开发模式下，使用空字符串，这样请求会使用相对路径，通过Vite代理转发
// 在生产模式下，使用环境变量中配置的完整URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

// 判断是否为开发模式
export const IS_DEV = MODE === 'development';

// WebSocket 配置
export const WEBSOCKET = {
  // WebSocket 路径
  PATH: import.meta.env.VITE_WS_PATH || '/ws',
  // 重连尝试次数
  MAX_RECONNECT_ATTEMPTS: 5,
  // 重连间隔（毫秒）
  RECONNECT_INTERVAL: 3000,
  // 认证方式：'url' 表示在 URL 中添加 token，'message' 表示连接后发送认证消息
  AUTH_METHOD: 'url',
  // 认证参数名
  AUTH_PARAM_NAME: 'token'
};

// 默认头像
export const DEFAULT_AVATAR = '/images/default-avatar.jpg';

// 默认封面图
export const DEFAULT_COVER = '/images/default-thumbnail.jpg';

// 分页配置
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  DEFAULT_PAGE: 1
};

// 导出所有配置
export default {
  MODE,
  IS_DEV,
  API_BASE_URL,
  WEBSOCKET,
  DEFAULT_AVATAR,
  DEFAULT_COVER,
  PAGINATION
};
