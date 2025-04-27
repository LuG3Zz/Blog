/**
 * 标签相关 API
 * 封装所有与标签数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';
import { getAuthHeaders } from '../core/apiClient';

/**
 * 获取所有标签及关联文章数量
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的标签数量
 * @param {number} [params.limit=100] - 返回的标签数量
 * @returns {Promise} 返回包含标签列表的Promise对象
 */
export const getTags = (params = {}) => {
  return apiClient.get(API_PATHS.TAGS.BASE, {
    params: {
      skip: params.skip || 0,
      limit: params.limit || 100
    }
  });
};

/**
 * 根据ID获取标签
 * @param {number} id - 标签ID
 * @returns {Promise} 返回包含标签数据的Promise对象
 */
export const getTagById = (id) => {
  return apiClient.get(API_PATHS.TAGS.BY_ID(id));
};

/**
 * 根据名称获取标签
 * @param {string} name - 标签名称
 * @returns {Promise} 返回包含标签数据的Promise对象
 */
export const getTagByName = (name) => {
  return apiClient.get(API_PATHS.TAGS.BY_NAME(name));
};

/**
 * 创建新标签
 * @param {Object} tagData - 标签数据
 * @param {string} tagData.name - 标签名称
 * @returns {Promise} 返回创建的标签数据
 */
export const createTag = (tagData) => {
  return apiClient.post(API_PATHS.TAGS.BASE, tagData, {
    headers: getAuthHeaders()
  });
};

/**
 * 更新标签
 * @param {number} id - 标签ID
 * @param {Object} tagData - 标签数据
 * @param {string} tagData.name - 标签名称
 * @returns {Promise} 返回更新的标签数据
 */
export const updateTag = (id, tagData) => {
  return apiClient.put(API_PATHS.TAGS.BY_ID(id), tagData, {
    headers: getAuthHeaders()
  });
};

/**
 * 删除标签
 * @param {number} id - 标签ID
 * @returns {Promise} 返回删除结果
 */
export const deleteTag = (id) => {
  return apiClient.delete(API_PATHS.TAGS.BY_ID(id), {
    headers: getAuthHeaders()
  });
};

/**
 * 批量删除标签
 * @param {Array<number>} tagIds - 标签ID数组
 * @returns {Promise} 返回删除结果
 */
export const batchDeleteTags = (tagIds) => {
  return apiClient.post(API_PATHS.TAGS.BATCH_DELETE, {
    tag_ids: tagIds
  }, {
    headers: getAuthHeaders()
  });
};

/**
 * 获取具有特定标签的所有文章
 * @param {number} tagId - 标签ID
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的文章数量
 * @param {number} [params.limit=10] - 返回的文章数量
 * @returns {Promise} 返回包含文章列表的Promise对象
 */
export const getArticlesByTag = (tagId, params = {}) => {
  return apiClient.get(API_PATHS.TAGS.ARTICLES(tagId), {
    params: {
      skip: params.skip || 0,
      limit: params.limit || 10
    }
  });
};

/**
 * 给文章添加标签
 * @param {number} articleId - 文章ID
 * @param {number} tagId - 标签ID
 * @returns {Promise} 返回添加结果
 */
export const addTagToArticle = (articleId, tagId) => {
  return apiClient.post(API_PATHS.TAGS.ADD_TO_ARTICLE(articleId), null, {
    params: { tag_id: tagId },
    headers: getAuthHeaders()
  });
};

/**
 * 更新文章的所有标签
 * @param {number} articleId - 文章ID
 * @param {Array<number>} tagIds - 标签ID数组
 * @returns {Promise} 返回更新结果
 */
export const updateArticleTags = (articleId, tagIds) => {
  return apiClient.put(API_PATHS.TAGS.UPDATE_ARTICLE_TAGS(articleId), null, {
    params: { tag_ids: tagIds },
    headers: getAuthHeaders()
  });
};

/**
 * 从文章中删除标签
 * @param {number} articleId - 文章ID
 * @param {number} tagId - 标签ID
 * @returns {Promise} 返回删除结果
 */
export const removeTagFromArticle = (articleId, tagId) => {
  return apiClient.delete(API_PATHS.TAGS.REMOVE_FROM_ARTICLE(articleId, tagId), {
    headers: getAuthHeaders()
  });
};

/**
 * 搜索标签
 * @param {string} query - 搜索关键词
 * @param {number} [limit=10] - 返回的标签数量
 * @returns {Promise} 返回搜索结果
 */
export const searchTags = (query, limit = 10) => {
  return apiClient.get(API_PATHS.SEARCH.TAGS, {
    params: {
      q: query,
      limit
    }
  });
};

export default {
  getTags,
  getTagById,
  getTagByName,
  createTag,
  updateTag,
  deleteTag,
  batchDeleteTags,
  getArticlesByTag,
  addTagToArticle,
  updateArticleTags,
  removeTagFromArticle,
  searchTags
};
