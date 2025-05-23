/**
 * 评论相关 API
 * 封装所有与评论数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 创建评论
 * @param {number} articleId - 文章ID
 * @param {string} content - 评论内容
 * @param {number} [parentId] - 父评论ID（用于回复）
 * @param {string} [anonymousName] - 匿名用户的显示名称（只有在未登录时使用）
 * @returns {Promise} 返回创建的评论数据
 */
export const createComment = (articleId, content, parentId = null, anonymousName = null) => {
  // 构造请求体
  const commentData = {
    article_id: articleId,
    content: content,
    ...parentId && { parent_id: parentId }
  };

  // 检查用户是否已登录
  const token = localStorage.getItem('token');
  if (!token) {
    // 如果未登录且提供了匿名名称，添加到请求体
    if (anonymousName) {
      commentData.anonymous_name = anonymousName;
    } else {
      console.error('创建评论失败: 匿名评论需要提供显示名称');
      return Promise.reject(new Error('请提供显示名称或登录后再发表评论'));
    }
  }

  // 添加更详细的日志记录
  console.log(`发送评论请求到 ${API_PATHS.COMMENTS.BASE}`, commentData);
  console.log('评论请求包含认证令牌:', !!token);
  console.log('完整请求URL:', API_PATHS.COMMENTS.BASE);

  // 使用 try-catch 包装请求，以便更好地捕获和记录错误
  try {
    return apiClient.post(API_PATHS.COMMENTS.BASE, commentData)
      .then(response => {
        console.log('评论创建成功:', response);
        return response;
      })
      .catch(error => {
        console.error('评论创建失败:', error);
        console.error('请求URL:', API_PATHS.COMMENTS.BASE);
        console.error('请求数据:', commentData);
        throw error;
      });
  } catch (error) {
    console.error('评论请求异常:', error);
    throw error;
  }
};

/**
 * 获取文章评论
 * @param {number} articleId - 文章ID
 * @param {Object} [options] - 查询选项
 * @param {number} [options.page=1] - 页码
 * @param {number} [options.pageSize=10] - 每页数量
 * @param {string} [options.sortBy='newest'] - 排序方式（newest, oldest, most_liked）
 * @param {boolean} [options.parentOnly=true] - 是否只返回顶层评论
 * @returns {Promise} 返回评论列表
 */
export const fetchComments = (articleId, options = {}) => {
  const params = {
    page: options.page || 1,
    page_size: options.pageSize || 10,
    sort_by: options.sortBy || 'newest',
    parent_only: options.parentOnly !== undefined ? options.parentOnly : true
  };

  console.log(`获取文章 ${articleId} 的评论`, params);
  return apiClient.get(API_PATHS.COMMENTS.BY_ARTICLE_ID(articleId), { params });
};

/**
 * 更新评论
 * @param {number} commentId - 评论ID
 * @param {string} content - 评论内容
 * @returns {Promise} 返回更新的评论数据
 */
export const updateComment = (commentId, content) => {
  return apiClient.put(API_PATHS.COMMENTS.BY_ID(commentId), { content });
};

/**
 * 删除评论
 * @param {number} commentId - 评论ID
 * @returns {Promise} 返回删除结果
 */
export const deleteComment = (commentId) => {
  return apiClient.delete(API_PATHS.COMMENTS.BY_ID(commentId));
};

/**
 * 点赞评论
 * @param {number} commentId - 评论ID
 * @returns {Promise} 返回点赞结果，包含点赞数量和点赞状态
 * @example
 * // 返回结果示例
 * {
 *   like_count: 10,      // 点赞数量
 *   liked_by_me: true,   // 当前用户是否已点赞
 *   message: '点赞成功' // 消息提示
 * }
 */
export const likeComment = (commentId) => {
  // 检查用户是否登录
  const token = localStorage.getItem('token');
  if (!token) {
    console.warn('未登录用户无法点赞');
    return Promise.reject(new Error('请登录后再进行点赞'));
  }

  return apiClient.post(API_PATHS.COMMENTS.LIKE(commentId))
    .then(response => {
      // 确保返回的数据包含点赞状态
      return {
        ...response,
        liked_by_me: response.liked_by_me !== undefined ? response.liked_by_me : true,
        like_count: response.like_count || 0
      };
    });
};

/**
 * 获取待审核评论列表（管理员可查看所有，编辑可查看自己文章的）
 * @param {Object} [options] - 查询选项
 * @param {number} [options.page=1] - 页码
 * @param {number} [options.pageSize=10] - 每页数量
 * @param {number} [options.articleId] - 文章ID（编辑角色筛选自己文章的评论）
 * @param {boolean} [options.parentOnly=false] - 是否只获取父评论
 * @returns {Promise} 返回待审核评论列表
 */
export const fetchPendingComments = (options = {}) => {
  const params = {
    page: options.page || 1,
    page_size: options.pageSize || 10
  };

  // 如果提供了文章ID，添加到查询参数
  if (options.articleId) {
    params.article_id = options.articleId;
  }

  // 如果指定了只获取父评论
  if (options.parentOnly) {
    params.parent_only = true;
  }

  return apiClient.get(API_PATHS.COMMENTS.PENDING, { params });
};

/**
 * 审核通过评论（管理员可审核所有，编辑可审核自己文章的）
 * @param {number} commentId - 评论ID
 * @returns {Promise} 返回审核结果
 */
export const approveComment = (commentId) => {
  return apiClient.post(API_PATHS.COMMENTS.APPROVE(commentId));
};

/**
 * 获取所有评论（需要登录，非管理员只能看到已审核评论）
 * @param {Object} [options] - 查询选项
 * @param {number} [options.page=1] - 页码
 * @param {number} [options.pageSize=10] - 每页数量
 * @param {string} [options.sortBy='newest'] - 排序方式（newest, oldest, most_liked）
 * @param {boolean} [options.approvedOnly=null] - 审核状态筛选（true: 已审核, false: 未审核, null: 所有）
 * @param {number} [options.userId=null] - 按用户ID筛选
 * @param {boolean} [options.parentOnly=false] - 是否只获取父评论
 * @returns {Promise} 返回评论列表
 */
export const fetchAllComments = (options = {}) => {
  const params = {
    page: options.page || 1,
    page_size: options.pageSize || 10,
    sort_by: options.sortBy || 'newest',
    approved_only: options.approvedOnly,
    user_id: options.userId
  };

  // 如果指定了只获取父评论
  if (options.parentOnly) {
    params.parent_only = true;
  }

  return apiClient.get(API_PATHS.COMMENTS.ALL, { params });
};

// 注意：API文档中没有提供拒绝评论的接口
// 实际项目中应该与后端沟通增加这个接口

export default {
  createComment,
  fetchComments,
  updateComment,
  deleteComment,
  likeComment,
  fetchPendingComments,
  approveComment,
  fetchAllComments
};
