/**
 * About页面相关 API
 * 封装所有与About页面相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取About页面内容
 * @returns {Promise} 返回About页面内容
 */
export const getAboutPage = () => {
  return apiClient.get(API_PATHS.ABOUT.BASE);
};

/**
 * 更新About页面内容
 * @param {Object} content - 页面内容
 * @returns {Promise} 返回更新后的About页面内容
 */
export const updateAboutPage = (content) => {
  console.log('发送更新请求，内容:', content);
  return apiClient.put(API_PATHS.ABOUT.BASE, { content });
};

export default {
  getAboutPage,
  updateAboutPage
};
