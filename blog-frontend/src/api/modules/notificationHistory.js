/**
 * 通知历史相关 API
 * 封装所有与通知历史相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS, API_PREFIX_STR } from '../core/apiPaths';

/**
 * 获取通知历史
 * @param {Object} params - 查询参数
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页条目数
 * @param {string} [params.level] - 通知级别筛选
 * @returns {Promise} 返回通知历史列表
 */
export const getNotificationHistory = (params = {}) => {
  return apiClient.get(API_PATHS.NOTIFICATION_HISTORY.BASE, {
    params: {
      page: params.page || 1,
      page_size: params.page_size || 10,
      level: params.level
    }
  });
};

/**
 * 删除通知
 * @param {number} id - 通知ID
 * @returns {Promise} 返回删除结果
 */
export const deleteNotification = (id) => {
  return apiClient.delete(API_PATHS.NOTIFICATION_HISTORY.BY_ID(id));
};

/**
 * 清空所有通知
 * @returns {Promise} 返回清空结果
 */
export const clearNotifications = () => {
  return apiClient.delete(API_PATHS.NOTIFICATION_HISTORY.CLEAR_ALL);
};

export default {
  getNotificationHistory,
  deleteNotification,
  clearNotifications
};
