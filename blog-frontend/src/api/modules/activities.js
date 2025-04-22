/**
 * 活动相关 API
 * 封装所有与活动数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取最近活动列表
 * @param {Object} params - 查询参数
 * @param {number} [params.days=30] - 查询天数范围
 * @param {number} [params.user_id] - 筛选特定用户的活动
 * @returns {Promise} 返回包含活动列表的Promise对象
 */
export const getActivities = async (params = {}) => {
  try {
    console.log('开始获取活动列表');

    // 根据提供的API文档，正确的参数格式
    const queryParams = {
      days: params.days || 30,
      user_id: params.user_id
    };

    // 发送请求到活动列表端点
    const response = await apiClient.get(API_PATHS.ACTIVITIES.BASE, {
      params: queryParams
    });

    console.log('获取活动列表成功:', response);
    return response;
  } catch (error) {
    console.error('获取活动列表失败:', error);

    // 如果请求失败，返回空数组
    return [];
  }
};

/**
 * 获取用户活动统计
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @param {number} [params.days=365] - 查询天数范围
 * @returns {Promise} 返回用户活动统计数据
 */
/**
 * 获取用户活动
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的活动数量
 * @param {number} [params.limit=10] - 返回的活动数量
 * @returns {Promise} 返回用户活动列表
 */
export const getUserActivities = (userId, params = {}) => {
  return apiClient.get(API_PATHS.USERS.ACTIVITIES(userId), {
    params: {
      skip: params.skip || 0,
      limit: params.limit || 10
    }
  });
};

/**
 * 获取统计数据
 * @returns {Promise} 返回统计数据
 */
export const getStats = () => {
  return apiClient.get(API_PATHS.STATS.OVERVIEW);
};

/**
 * 获取活动时间线
 * @param {Object} params - 查询参数
 * @param {number} [params.days=30] - 查询天数范围
 * @returns {Promise} 返回活动时间线数据
 */
export const getActivityTimeline = (params = {}) => {
  return apiClient.get(API_PATHS.STATS.ACTIVITY_TIMELINE, {
    params: {
      days: params.days || 30
    }
  });
};

/**
 * 获取公共活动列表
 * @param {Object} params - 查询参数
 * @param {number} [params.days=7] - 查询天数范围，默认为7天，范围为1-30
 * @param {number} [params.limit=10] - 返回的活动数量，默认为10，范围为1-50
 * @returns {Promise} 返回包含公共活动列表的Promise对象
 */
export const getPublicActivities = async (params = {}) => {
  try {
    console.log('开始获取公共活动列表');

    // 根据API文档设置查询参数
    const queryParams = {
      days: params.days || 7,
      limit: params.limit || 10
    };

    // 发送请求到公共活动列表端点
    const response = await apiClient.get(API_PATHS.ACTIVITIES.PUBLIC, {
      params: queryParams
    });

    console.log('获取公共活动列表成功:', response);
    return response;
  } catch (error) {
    console.error('获取公共活动列表失败:', error);

    // 如果请求失败，返回空数组
    return [];
  }
};

/**
 * 获取基本活动列表
 * @param {Object} params - 查询参数
 * @param {number} [params.days=30] - 查询天数范围
 * @param {number} [params.user_id] - 筛选特定用户的活动
 * @returns {Promise} 返回包含基本活动列表的Promise对象
 */
export const getBasicActivities = async (params = {}) => {
  try {
    console.log('开始获取基本活动列表');

    // 根据API文档设置查询参数
    const queryParams = {
      days: params.days || 30,
      user_id: params.user_id
    };

    // 发送请求到基本活动列表端点
    const response = await apiClient.get(API_PATHS.ACTIVITIES.BASIC, {
      params: queryParams
    });

    console.log('获取基本活动列表成功:', response);
    return response;
  } catch (error) {
    console.error('获取基本活动列表失败:', error);

    // 如果请求失败，返回空数组
    return [];
  }
};

export default {
  getActivities,
  getUserActivities,
  getStats,
  getActivityTimeline,
  getPublicActivities,
  getBasicActivities
};
