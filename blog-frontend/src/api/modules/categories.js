/**
 * 分类相关 API
 * 封装所有与分类数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取所有分类数据
 * @returns {Promise} 返回包含分类数据的Promise对象
 */
export const getCategories = () => {
  return apiClient.get(API_PATHS.CATEGORIES.BASE);
};

/**
 * 根据ID获取分类
 * @param {number} id - 分类ID
 * @returns {Promise} 返回包含分类数据的Promise对象
 */
export const getCategoryById = (id) => {
  return apiClient.get(API_PATHS.CATEGORIES.BY_ID(id));
};

/**
 * 创建新分类
 * @param {Object} categoryData - 分类数据
 * @returns {Promise} 返回创建的分类数据
 */
export const createCategory = (categoryData) => {
  return apiClient.post(API_PATHS.CATEGORIES.BASE, categoryData);
};

/**
 * 更新分类
 * @param {number} id - 分类ID
 * @param {Object} categoryData - 分类数据
 * @returns {Promise} 返回更新的分类数据
 */
export const updateCategory = (id, categoryData) => {
  return apiClient.put(API_PATHS.CATEGORIES.BY_ID(id), categoryData);
};

/**
 * 删除分类
 * @param {number} id - 分类ID
 * @returns {Promise} 返回删除结果
 */
export const deleteCategory = (id) => {
  return apiClient.delete(API_PATHS.CATEGORIES.BY_ID(id));
};

export default {
  getCategories,
  getCategoryById,
  createCategory,
  updateCategory,
  deleteCategory
};
