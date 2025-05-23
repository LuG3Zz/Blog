/**
 * 文章相关 API
 * 封装所有与文章数据相关的网络请求和处理逻辑
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';
// 删除本地模拟数据导入

/**
 * 点赞文章
 * @param {number} id - 文章ID
 * @returns {Promise} 返回点赞结果的Promise对象
 */
export const likePost = (id) => {
  return apiClient.post(API_PATHS.ARTICLES.LIKE(id));
};

/**
 * 获取文章点赞状态
 * @param {number} id - 文章ID
 * @returns {Promise} 返回点赞状态的Promise对象
 */
export const getLikeStatus = async (id) => {
  try {
    return await apiClient.get(API_PATHS.ARTICLES.LIKE_STATUS(id));
  } catch (error) {
    return { liked: false };
  }
};

/**
 * 删除图片
 * @param {string} imagePath - 图片路径
 * @returns {Promise} 返回删除结果的Promise对象
 */
export const deleteImage = (imagePath) => {
  return apiClient.delete(API_PATHS.FILES.DELETE_IMAGE, {
    data: { image_path: imagePath }
  });
};

/**
 * 上传图片
 * @param {FormData} formData - 包含图片的表单数据
 * @param {string} [token] - 认证令牌（可选）
 * @returns {Promise} 返回上传结果的Promise对象
 */
export const uploadImage = (formData, token) => {
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
 * 获取所有文章
 * @param {Object} params - 查询参数
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页数量
 * @param {string} [params.category] - 分类名称
 * @param {string} [params.category_id] - 分类ID
 * @param {string} [params.tag] - 标签
 * @param {boolean} [params.is_featured] - 是否精选
 * @returns {Promise} 返回包含文章列表和分页信息的Promise对象
 */
export const getPosts = (params = {}) => {
  // 计算skip和limit
  const page = params.page || 1;
  const pageSize = params.page_size || 10;
  const skip = (page - 1) * pageSize;

  // 构建查询参数
  const queryParams = {
    skip: skip,
    limit: pageSize,
    tag: params.tag,
    is_featured: params.is_featured
  };

  // 处理分类参数
  if (params.category) {
    queryParams.category = params.category;
  } else if (params.category_id) {
    // 如果提供了分类ID，需要先获取分类名称
    // 后端API只接受分类名称，不接受分类ID
    // 这里我们需要先获取分类名称，然后再使用分类名称查询文章
    // 但为了避免额外的API调用，我们在CategoryDetail.vue中修改逻辑
    console.log('使用分类ID查询文章:', params.category_id);
    queryParams.category_id = params.category_id;
  }

  // 发送请求
  return apiClient.get(API_PATHS.ARTICLES.BASE, {
    params: queryParams
  }).then(response => {
    // 处理响应数据
    if (response && Array.isArray(response)) {
      // 后端返回的是数组，没有分页信息，需要模拟分页信息
      return {
        items: response,
        total: response.length,
        page: page,
        page_size: pageSize,
        pages: Math.ceil(response.length / pageSize)
      };
    } else if (response && response.data && Array.isArray(response.data)) {
      // 后端返回的是包含data字段的对象，没有分页信息，需要模拟分页信息
      return {
        items: response.data,
        total: response.data.length,
        page: page,
        page_size: pageSize,
        pages: Math.ceil(response.data.length / pageSize)
      };
    } else {
      console.warn('返回的文章列表数据格式不符合预期:', response);
      return {
        items: [],
        total: 0,
        page: page,
        page_size: pageSize,
        pages: 0
      };
    }
  });
};

/**
 * 根据分类获取文章
 * @param {Object} params - 查询参数
 * @param {string} [params.category] - 分类名称（可选），如果不提供则获取所有文章
 * @param {number} [params.page=1] - 页码
 * @param {number} [params.page_size=10] - 每页数量
 * @param {boolean} [params.is_featured] - 是否只返回精选文章
 * @param {string} [params.tag] - 标签名称，按标签筛选
 * @returns {Promise} 返回包含文章列表和分页信息的Promise对象
 */
export const getPostsByCategory = (params = {}) => {
  // 计算skip和limit
  const page = params.page || 1;
  const pageSize = params.page_size || 10;
  const skip = (page - 1) * pageSize;

  // 构建查询参数
  const queryParams = {
    skip: skip,
    limit: pageSize
  };

  // 只有当分类不为空时，才添加分类参数
  if (params.category) {
    queryParams.category = params.category;
  }

  // 如果有 is_featured 参数，添加到查询参数中
  if (params.is_featured !== undefined) {
    queryParams.is_featured = params.is_featured;
  }

  // 如果有 tag 参数，添加到查询参数中
  if (params.tag) {
    queryParams.tag = params.tag;
  }

  // 发送请求
  return apiClient.get(API_PATHS.ARTICLES.BASE, {
    params: queryParams
  }).then(response => {
    // 处理响应数据
    if (response && Array.isArray(response)) {
      // 后端返回的是数组，没有分页信息，需要模拟分页信息
      return {
        items: response,
        total: response.length,
        page: page,
        page_size: pageSize,
        pages: Math.ceil(response.length / pageSize)
      };
    } else if (response && response.data && Array.isArray(response.data)) {
      // 后端返回的是包含data字段的对象，没有分页信息，需要模拟分页信息
      return {
        items: response.data,
        total: response.data.length,
        page: page,
        page_size: pageSize,
        pages: Math.ceil(response.data.length / pageSize)
      };
    } else {
      console.warn('返回的文章列表数据格式不符合预期:', response);
      return {
        items: [],
        total: 0,
        page: page,
        page_size: pageSize,
        pages: 0
      };
    }
  });
};

/**
 * 根据ID获取文章
 * @param {number} id - 文章ID
 * @returns {Promise} 返回包含文章数据的Promise对象
 */
export const getPostById = (id) => {
  return apiClient.get(API_PATHS.ARTICLES.BY_ID(id));
};

/**
 * 创建新文章
 * @param {Object} postData - 文章数据
 * @param {string} [token] - 认证令牌（可选）
 * @returns {Promise} 返回创建的文章数据
 */
export const createPost = (postData, token) => {
  const options = {};

  // 如果提供了token，添加到请求头
  if (token) {
    // 正确处理 token 格式
    // 先将 token 转换为小写进行检查
    const lowerToken = token.toLowerCase();

    // 如果 token 已经包含了 "bearer"，则先删除所有 "bearer" 前缀
    let cleanToken = token;
    if (lowerToken.includes('bearer')) {
      // 删除所有可能的 "bearer" 前缀（包括大小写变体）
      cleanToken = token.replace(/^\s*bearer\s+/i, '');
    }

    // 添加正确的 "Bearer" 前缀
    options.headers = {
      Authorization: `Bearer ${cleanToken}`
    };
  }

  return apiClient.post(API_PATHS.ARTICLES.BASE, postData, options);
};

/**
 * 更新文章
 * @param {number} id - 文章ID
 * @param {Object} postData - 文章数据
 * @param {string} [token] - 认证令牌（可选）
 * @returns {Promise} 返回更新的文章数据
 */
export const updatePost = (id, postData, token) => {
  const options = {};

  // 如果提供了token，添加到请求头
  if (token) {
    // 正确处理 token 格式
    // 先将 token 转换为小写进行检查
    const lowerToken = token.toLowerCase();

    // 如果 token 已经包含了 "bearer"，则先删除所有 "bearer" 前缀
    let cleanToken = token;
    if (lowerToken.includes('bearer')) {
      // 删除所有可能的 "bearer" 前缀（包括大小写变体）
      cleanToken = token.replace(/^\s*bearer\s+/i, '');
    }

    // 添加正确的 "Bearer" 前缀
    options.headers = {
      Authorization: `Bearer ${cleanToken}`
    };
  }

  return apiClient.put(API_PATHS.ARTICLES.BY_ID(id), postData, options);
};

/**
 * 删除文章
 * @param {number} id - 文章ID
 * @param {string} [token] - 认证令牌（可选）
 * @returns {Promise} 返回删除结果
 */
export const deletePost = (id, token) => {
  const options = {};

  // 如果提供了token，添加到请求头
  if (token) {
    // 正确处理 token 格式
    // 先将 token 转换为小写进行检查
    const lowerToken = token.toLowerCase();

    // 如果 token 已经包含了 "bearer"，则先删除所有 "bearer" 前缀
    let cleanToken = token;
    if (lowerToken.includes('bearer')) {
      // 删除所有可能的 "bearer" 前缀（包括大小写变体）
      cleanToken = token.replace(/^\s*bearer\s+/i, '');
    }

    // 添加正确的 "Bearer" 前缀
    options.headers = {
      Authorization: `Bearer ${cleanToken}`
    };
  }

  return apiClient.delete(API_PATHS.ARTICLES.BY_ID(id), options);
};

/**
 * 获取AI辅助内容
 * @param {string} prompt - 提示词
 * @returns {Promise} 返回AI生成的内容
 */
export const getAIAssist = (content) => {
  // 根据 API 文档，请求体需要包含 content 字段
  return apiClient.post(API_PATHS.ARTICLES.AI_ASSIST, { content });
};

export default {
  likePost,
  getLikeStatus,
  deleteImage,
  uploadImage,
  getPosts,
  getPostsByCategory,
  getPostById,
  createPost,
  updatePost,
  deletePost,
  getAIAssist
};
