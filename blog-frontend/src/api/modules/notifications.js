/**
 * 通知相关 API
 * 封装所有与通知相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 发送通知
 * @param {Object} data - 通知数据
 * @param {string} data.title - 通知标题
 * @param {string} data.content - 通知内容
 * @param {string} [data.level='info'] - 通知级别，可选值：'info', 'success', 'warning', 'error'
 * @param {Array|null} [data.target_users=null] - 目标用户，null 表示全站广播
 * @returns {Promise} 返回发送结果
 */
export const sendNotification = (data) => {
  return apiClient.post(API_PATHS.WEBSOCKET.ADMIN_NOTIFICATIONS, data);
};

/**
 * 获取 WebSocket 状态
 * @returns {Promise} 返回 WebSocket 状态信息
 */
export const getWebSocketStatus = () => {
  return apiClient.get(API_PATHS.WEBSOCKET.STATUS);
};

export default {
  sendNotification,
  getWebSocketStatus
};
