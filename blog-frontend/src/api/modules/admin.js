/**
 * 管理员相关 API
 * 封装所有与管理员操作相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取所有用户（仅管理员可用）
 * @param {Object} params - 查询参数
 * @param {string} [params.role] - 用户角色，可选
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页条目数
 * @returns {Promise} 返回包含用户列表的Promise对象
 */
export const getUsers = (params = {}) => {
  // 使用后端API获取用户列表
  // 根据新的API文档，正确的参数格式
  return apiClient.get(API_PATHS.USERS.ADMIN, {
    params: {
      role: params.role,
      page: params.page || 1,
      page_size: params.page_size || 10
    }
  });
};

/**
 * 根据ID获取用户
 * @param {number} id - 用户ID
 * @returns {Promise} 返回包含用户数据的Promise对象
 */
export const getUserById = (id) => {
  // 使用后端API获取用户信息
  return apiClient.get(API_PATHS.USERS.BY_ID(id));
};

/**
 * 创建新用户
 * @param {Object} userData - 用户数据
 * @returns {Promise} 返回创建的用户数据
 */
export const createUser = (userData) => {
  // 使用后端API创建用户
  return apiClient.post(API_PATHS.USERS.BASE, userData);
};

/**
 * 更新用户
 * @param {number} id - 用户ID
 * @param {Object} userData - 用户数据
 * @returns {Promise} 返回更新的用户数据
 */
export const updateUser = (id, userData) => {
  // 使用后端API更新用户
  return apiClient.put(API_PATHS.USERS.BY_ID(id), userData);
};

/**
 * 删除用户
 * @param {number} id - 用户ID
 * @returns {Promise} 返回删除结果
 */
export const deleteUser = (id) => {
  // 使用后端API删除用户
  return apiClient.delete(API_PATHS.USERS.BY_ID(id));
};

/**
 * 获取系统统计数据
 * @returns {Promise} 返回系统统计数据
 */
export const getSystemStats = () => {
  // 使用统计概览接口
  return apiClient.get(API_PATHS.STATS.OVERVIEW);
};

/**
 * 获取用户活动统计
 * @param {Object} params - 查询参数
 * @param {number} [params.limit=10] - 返回的用户数量
 * @returns {Promise} 返回用户活动统计数据
 */
export const getUserActivity = (params = {}) => {
  // 根据 OpenAPI 文档，正确的参数格式
  return apiClient.get(API_PATHS.STATS.USER_ACTIVITY, {
    params: {
      limit: params.limit || 10
    }
  });
};

/**
 * 获取分类分布
 * @returns {Promise} 返回分类分布数据
 */
export const getCategoryDistribution = () => {
  return apiClient.get(API_PATHS.STATS.CATEGORY_DISTRIBUTION);
};

/**
 * 更新用户角色
 * @param {number} userId - 用户ID
 * @param {string} role - 新角色 (admin, editor, author, user)
 * @returns {Promise} 返回包含更新后用户信息的Promise对象
 */
export const updateUserRole = (userId, role) => {
  console.log('API调用 updateUserRole:', userId, role);
  // 使用 JSON 格式发送请求体，而不是查询参数
  return apiClient.patch(`${API_PATHS.USERS.ADMIN}/${userId}/role`, { role });
};

export default {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
  getSystemStats,
  getUserActivity,
  getCategoryDistribution,
  updateUserRole
};
