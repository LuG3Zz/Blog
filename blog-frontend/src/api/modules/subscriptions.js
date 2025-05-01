/**
 * 订阅相关 API
 * 封装所有与订阅相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取用户订阅
 * @returns {Promise} 返回用户订阅信息
 */
export const getUserSubscriptions = () => {
  return apiClient.get(API_PATHS.SUBSCRIPTIONS.BASE);
};

/**
 * 订阅分类
 * @param {number} categoryId - 分类ID
 * @returns {Promise} 返回订阅结果
 */
export const subscribeToCategory = (categoryId) => {
  return apiClient.post(API_PATHS.SUBSCRIPTIONS.CATEGORIES, { category_id: categoryId });
};

/**
 * 取消订阅分类
 * @param {number} categoryId - 分类ID
 * @returns {Promise} 返回取消订阅结果
 */
export const unsubscribeFromCategory = (categoryId) => {
  return apiClient.delete(`${API_PATHS.SUBSCRIPTIONS.CATEGORIES}/${categoryId}`);
};

/**
 * 订阅作者
 * @param {number} authorId - 作者ID
 * @returns {Promise} 返回订阅结果
 */
export const subscribeToAuthor = (authorId) => {
  return apiClient.post(API_PATHS.SUBSCRIPTIONS.AUTHORS, { author_id: authorId });
};

/**
 * 取消订阅作者
 * @param {number} authorId - 作者ID
 * @returns {Promise} 返回取消订阅结果
 */
export const unsubscribeFromAuthor = (authorId) => {
  return apiClient.delete(`${API_PATHS.SUBSCRIPTIONS.AUTHORS}/${authorId}`);
};

/**
 * 创建邮件订阅
 * @param {Object} data - 订阅数据
 * @param {string} data.email - 邮箱地址
 * @param {string} data.subscription_type - 订阅类型 (author, category, all)
 * @param {number|null} data.reference_id - 引用ID (作者ID或分类ID，对于all类型为null)
 * @returns {Promise} 返回订阅结果
 */
export const createEmailSubscription = (data) => {
  return apiClient.post(API_PATHS.EMAIL_SUBSCRIPTIONS.BASE, data);
};

/**
 * 通过令牌取消邮件订阅
 * @param {string} token - 订阅令牌
 * @returns {Promise} 返回取消订阅结果
 */
export const unsubscribeByToken = (token) => {
  return apiClient.post(API_PATHS.EMAIL_SUBSCRIPTIONS.UNSUBSCRIBE, { token });
};

/**
 * 通过邮箱取消订阅
 * @param {string} email - 邮箱地址
 * @param {string} [subscription_type] - 订阅类型 (可选)
 * @param {number} [reference_id] - 引用ID (可选)
 * @returns {Promise} 返回取消订阅结果
 */
export const unsubscribeByEmail = (email, subscription_type = null, reference_id = null) => {
  const params = { email };

  if (subscription_type) {
    params.subscription_type = subscription_type;
  }

  if (reference_id !== null) {
    params.reference_id = reference_id;
  }

  return apiClient.post(API_PATHS.EMAIL_SUBSCRIPTIONS.UNSUBSCRIBE_EMAIL, null, { params });
};

/**
 * 获取邮件订阅列表
 * @param {Object} params - 查询参数
 * @param {string} [params.email] - 按邮箱筛选
 * @param {string} [params.subscription_type] - 按订阅类型筛选 (author, category, all)
 * @param {number} [params.reference_id] - 按引用ID筛选
 * @param {boolean} [params.is_active] - 是否只返回活跃订阅
 * @returns {Promise} 返回订阅列表
 */
export const getEmailSubscriptions = (params = {}) => {
  return apiClient.get(API_PATHS.EMAIL_SUBSCRIPTIONS.BASE, { params });
};

/**
 * 更新邮件订阅状态
 * @param {number} id - 订阅ID
 * @param {Object} data - 更新数据
 * @param {boolean} data.is_active - 是否活跃
 * @returns {Promise} 返回更新结果
 */
export const updateEmailSubscription = (id, data) => {
  return apiClient.patch(`${API_PATHS.EMAIL_SUBSCRIPTIONS.BASE}/${id}`, data);
};

export default {
  getUserSubscriptions,
  subscribeToCategory,
  unsubscribeFromCategory,
  subscribeToAuthor,
  unsubscribeFromAuthor,
  createEmailSubscription,
  unsubscribeByToken,
  unsubscribeByEmail,
  getEmailSubscriptions,
  updateEmailSubscription
};
