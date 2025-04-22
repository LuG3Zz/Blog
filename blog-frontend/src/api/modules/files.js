/**
 * 文件相关 API
 * 封装所有与文件上传和管理相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 上传图片
 * @param {File|FormData} file - 文件对象或已经准备好的 FormData
 * @param {string} [token] - 认证令牌（可选）
 * @returns {Promise} 返回上传结果
 */
export const uploadImage = (file, token) => {
  let formData;

  // 如果传入的是 FormData 对象，直接使用
  if (file instanceof FormData) {
    formData = file;
  } else {
    // 否则创建新的 FormData 并添加文件
    formData = new FormData();
    formData.append('file', file);
  }

  const options = {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  };

  // 如果提供了token，添加到请求头
  if (token) {
    options.headers['Authorization'] = token;
  }

  return apiClient.post(API_PATHS.FILES.UPLOAD_IMAGE, formData, options);
};

/**
 * 删除图片
 * @param {string} imagePath - 图片路径
 * @returns {Promise} 返回删除结果
 */
export const deleteImage = (imagePath) => {
  return apiClient.delete(API_PATHS.FILES.DELETE_IMAGE, {
    data: { image_path: imagePath }
  });
};

export default {
  uploadImage,
  deleteImage
};
