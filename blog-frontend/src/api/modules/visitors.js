/**
 * 访客记录相关 API
 * 封装所有与访客记录相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取访客记录列表
 * @param {Object} params - 查询参数
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页条目数
 * @param {string} [params.start_date] - 开始日期
 * @param {string} [params.end_date] - 结束日期
 * @param {string} [params.ip_address] - IP地址筛选
 * @param {string} [params.path] - 访问路径筛选
 * @param {boolean} [params.is_mobile] - 是否为移动设备
 * @param {boolean} [params.is_bot] - 是否为爬虫
 * @returns {Promise} 返回访客记录列表
 */
export const getVisitors = (params = {}) => {
  return apiClient.get(API_PATHS.VISITORS.BASE, {
    params: {
      page: params.page || 1,
      page_size: params.page_size || 10,
      start_date: params.start_date,
      end_date: params.end_date,
      ip_address: params.ip_address,
      path: params.path,
      is_mobile: params.is_mobile,
      is_bot: params.is_bot
    }
  });
};

/**
 * 获取访客统计信息
 * @param {Object} params - 查询参数
 * @param {number} [params.days=30] - 统计天数
 * @returns {Promise} 返回访客统计信息
 */
export const getVisitorStatistics = (params = {}) => {
  return apiClient.get(API_PATHS.VISITORS.STATISTICS, {
    params: {
      days: params.days || 30
    }
  });
};

/**
 * 删除访客记录
 * @param {number} id - 访客记录ID
 * @returns {Promise} 返回删除结果
 */
export const deleteVisitor = (id) => {
  return apiClient.delete(`${API_PATHS.VISITORS.BASE}/${id}`);
};

/**
 * 批量删除访客记录
 * @param {Array<number>} visitorIds - 访客记录ID数组
 * @returns {Promise} 返回删除结果
 */
export const batchDeleteVisitors = (visitorIds) => {
  return apiClient.post(API_PATHS.VISITORS.BATCH_DELETE, {
    visitor_ids: visitorIds
  });
};

export default {
  getVisitors,
  getVisitorStatistics,
  deleteVisitor,
  batchDeleteVisitors
};
