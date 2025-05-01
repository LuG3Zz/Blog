/**
 * 统计相关 API
 * 封装所有与统计数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取概览统计数据
 * @returns {Promise} 返回包含概览统计数据的Promise对象
 */
export const getOverviewStats = () => {
  return apiClient.get(API_PATHS.STATS.OVERVIEW);
};

/**
 * 获取热门文章
 * @param {Object} params - 查询参数
 * @param {number} [params.limit=5] - 返回的文章数量，范围1-20
 * @param {string} [params.period='all'] - 时间段，可选值：day, week, month, year, all
 * @returns {Promise} 返回热门文章列表
 */
export const getPopularArticles = (params = {}) => {
  return apiClient.get(API_PATHS.STATS.POPULAR_ARTICLES, {
    params: {
      limit: params.limit || 5,
      period: params.period || 'all'
    }
  });
};

/**
 * 获取活动时间线
 * @param {Object} params - 查询参数
 * @param {number} [params.days=30] - 查询天数范围，范围1-365
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
 * 获取分类分布
 * @returns {Promise} 返回分类分布数据
 */
export const getCategoryDistribution = () => {
  return apiClient.get(API_PATHS.STATS.CATEGORY_DISTRIBUTION);
};

/**
 * 获取用户活动统计
 * @param {Object} params - 查询参数
 * @param {number} [params.limit=10] - 返回的用户数量，范围1-50
 * @returns {Promise} 返回用户活动统计数据
 */
export const getUserActivity = (params = {}) => {
  return apiClient.get(API_PATHS.STATS.USER_ACTIVITY, {
    params: {
      limit: params.limit || 10
    }
  });
};

/**
 * 获取活动热力图数据
 * @param {Object} params - 查询参数
 * @param {number} [params.days=365] - 查询天数范围，范围1-730
 * @param {string} [params.action_type] - 活动类型过滤，例如 'article', 'comment', 'like'
 * @param {number} [params.user_id] - 用户ID过滤
 * @returns {Promise} 返回热力图数据
 */
export const getActivityHeatmap = (params = {}) => {
  return apiClient.get(API_PATHS.STATS.ACTIVITY_HEATMAP, {
    params: {
      days: params.days || 365,
      action_type: params.action_type || null,
      user_id: params.user_id || null
    }
  });
};

/**
 * 获取订阅统计数据
 * @returns {Promise} 返回订阅统计数据
 */
export const getSubscriptionStats = () => {
  return apiClient.get(API_PATHS.STATS.SUBSCRIPTIONS);
};

export default {
  getOverviewStats,
  getPopularArticles,
  getActivityTimeline,
  getCategoryDistribution,
  getUserActivity,
  getActivityHeatmap,
  getSubscriptionStats
};
