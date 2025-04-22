/**
 * 搜索相关 API
 * 封装所有与搜索功能相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 搜索文章
 * @param {Object} params - 搜索参数
 * @param {string} params.q - 搜索关键词
 * @param {number} [params.category_id] - 分类ID
 * @param {string} [params.tag] - 标签
 * @param {number} [params.author_id] - 作者ID
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页数量
 * @returns {Promise} 返回搜索结果
 */
export const searchArticles = (params) => {
  if (!params.q) {
    return Promise.reject(new Error('搜索关键词不能为空'));
  }

  // 根据 OpenAPI 文档，正确的参数格式
  return apiClient.get(API_PATHS.SEARCH.ARTICLES, {
    params: {
      q: params.q,
      category_id: params.category_id,
      tag: params.tag,
      author_id: params.author_id,
      page: params.page || 1,
      page_size: params.page_size || 10
    }
  });
};

/**
 * 搜索用户
 * @param {Object} params - 搜索参数
 * @param {string} params.q - 搜索关键词
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页数量
 * @returns {Promise} 返回搜索结果
 */
export const searchUsers = (params) => {
  if (!params.q) {
    return Promise.reject(new Error('搜索关键词不能为空'));
  }

  // 根据 OpenAPI 文档，正确的参数格式
  return apiClient.get(API_PATHS.SEARCH.USERS, {
    params: {
      q: params.q,
      page: params.page || 1,
      page_size: params.page_size || 10
    }
  });
};

/**
 * 搜索标签
 * @param {string} query - 搜索关键词
 * @param {number} [limit=10] - 返回的标签数量
 * @returns {Promise} 返回搜索结果
 */
export const searchTags = (query, limit = 10) => {
  if (!query) {
    return Promise.reject(new Error('搜索关键词不能为空'));
  }

  return apiClient.get(API_PATHS.SEARCH.TAGS, {
    params: {
      q: query,
      limit
    }
  });
};

export default {
  searchArticles,
  searchUsers,
  searchTags
};
