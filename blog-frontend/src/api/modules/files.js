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

/**
 * 上传文件
 * @param {File|FormData} file - 文件对象或已经准备好的 FormData
 * @param {string} [token] - 认证令牌（可选）
 * @returns {Promise} 返回上传结果
 */
export const uploadFile = (file, token) => {
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

  return apiClient.post(API_PATHS.FILES.UPLOAD, formData, options);
};

/**
 * 获取文件列表
 * @param {Object} params - 查询参数
 * @param {string} [params.file_type] - 文件类型筛选
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=20] - 每页条目数
 * @returns {Promise} 返回文件列表
 */
export const getFileList = (params = {}) => {
  return apiClient.get(API_PATHS.FILES.LIST, { params });
};

/**
 * 下载文件
 * @param {number} fileId - 文件ID
 * @returns {Promise} 返回文件内容
 */
export const downloadFile = (fileId) => {
  return apiClient.get(API_PATHS.FILES.DOWNLOAD(fileId), {
    responseType: 'blob'
  });
};

/**
 * 删除文件
 * @param {number} fileId - 文件ID
 * @returns {Promise} 返回删除结果
 */
export const deleteFile = (fileId) => {
  return apiClient.delete(API_PATHS.FILES.DELETE(fileId));
};

/**
 * 重命名文件
 * @param {number} fileId - 文件ID
 * @param {string} newFilename - 新文件名
 * @returns {Promise} 返回重命名结果
 */
export const renameFile = (fileId, newFilename) => {
  return apiClient.put(API_PATHS.FILES.RENAME(fileId), {
    new_filename: newFilename
  });
};

/**
 * 获取文件统计信息
 * @returns {Promise} 返回统计信息
 */
export const getFileStats = () => {
  return apiClient.get(API_PATHS.FILES.STATS);
};

/**
 * 批量删除文件
 * @param {number[]} fileIds - 文件ID数组
 * @returns {Promise} 返回删除结果
 */
export const batchDeleteFiles = (fileIds) => {
  return apiClient.post(API_PATHS.FILES.BATCH_DELETE, { file_ids: fileIds });
};

export default {
  uploadImage,
  deleteImage,
  uploadFile,
  getFileList,
  downloadFile,
  deleteFile,
  renameFile,
  getFileStats,
  batchDeleteFiles
};


