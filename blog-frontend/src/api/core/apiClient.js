/**
 * API 客户端
 * 提供统一的 API 请求方法和错误处理
 */

import axios from '@/utils/axios';
import message from '@/utils/message';

/**
 * 通用 API 错误处理
 * @param {Error} error - 错误对象
 * @param {string} customMessage - 自定义错误消息
 * @returns {Promise} 返回被拒绝的 Promise
 */
export const handleApiError = (error, customMessage = '操作失败') => {
  console.error('请求错误详情:', error);

  // 输出详细的错误信息以便调试
  if (error.response) {
    console.error('响应状态:', error.response.status);
    console.error('响应头:', error.response.headers);
    console.error('响应数据:', error.response.data);

    // 如果有详细的错误信息，显示出来
    if (error.response.data && error.response.data.detail) {
      console.error('错误详情:', JSON.stringify(error.response.data.detail, null, 2));
    }
  } else if (error.request) {
    console.error('请求已发送但没有收到响应:', error.request);
  } else {
    console.error('请求设置错误:', error.message);
  }

  const errorMessage = error.response?.data?.message || error.message || customMessage;
  message.error(errorMessage);
  return Promise.reject(error);
};

/**
 * 创建 API 请求方法
 * @param {Function} apiCall - API 调用函数
 * @param {string} errorMessage - 错误消息
 * @returns {Function} 包装后的 API 调用函数
 */
export const createApiMethod = (apiCall, errorMessage) => {
  return async (...args) => {
    try {
      return await apiCall(...args);
    } catch (error) {
      return handleApiError(error, errorMessage);
    }
  };
};

/**
 * 获取认证头信息
 * @returns {Object} 包含认证信息的对象
 */
export const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  if (!token) return {};

  // 确保 token 格式正确
  // 先将 token 转换为小写进行检查，防止大小写不一致导致的重复
  const lowerToken = token.toLowerCase();

  // 如果 token 已经包含了 "bearer"，则先删除所有 "bearer" 前缀
  let cleanToken = token;
  if (lowerToken.includes('bearer')) {
    // 删除所有可能的 "bearer" 前缀（包括大小写变体）
    cleanToken = token.replace(/^\s*bearer\s+/i, '');
  }

  // 添加正确的 "Bearer" 前缀
  const formattedToken = `Bearer ${cleanToken}`;
  console.log('格式化后的 token:', formattedToken);
  return { Authorization: formattedToken };
};

/**
 * API 客户端
 * 提供统一的 API 请求方法
 */
const apiClient = {
  /**
   * GET 请求
   * @param {string} url - 请求 URL
   * @param {Object} params - 查询参数
   * @param {Object} options - 请求选项
   * @returns {Promise} 返回请求结果
   */
  get: createApiMethod(
    async (url, params = {}, options = {}) => {
      // 添加更详细的日志记录
      console.log('发送 GET 请求:', {
        url,
        params: params.params || params,
        options
      });

      // 确保参数直接传递，而不是嵌套在params对象中
      const requestParams = params.params || params;

      // 记录完整的请求信息
      console.log('完整请求URL:', url);
      console.log('请求参数:', requestParams);

      try {
        const response = await axios.get(url, {
          params: requestParams,
          ...options,
          headers: {
            ...getAuthHeaders(),
            ...options.headers
          }
        });

        console.log('收到 GET 响应:', response);
        return response;
      } catch (error) {
        console.error('GET 请求失败:', error);
        console.error('请求URL:', url);
        console.error('请求参数:', requestParams);
        throw error;
      }
    },
    '获取数据失败'
  ),

  /**
   * POST 请求
   * @param {string} url - 请求 URL
   * @param {Object} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise} 返回请求结果
   */
  post: createApiMethod(
    async (url, data = {}, options = {}) => {
      // 添加更详细的日志记录
      console.log('发送 POST 请求:', {
        url,
        data: data instanceof FormData ? '[FormData]' : data,
        options
      });

      // 如果是 FormData，不要尝试将其转换为 JSON
      const requestData = data instanceof FormData ? data :
                         (typeof data === 'string' ? JSON.parse(data) : data);

      // 如果是 FormData，不要设置 Content-Type，让浏览器自动设置包含 boundary
      const headers = {
        ...getAuthHeaders(),
        ...options.headers
      };

      // 只有当不是 FormData 时才设置 Content-Type
      if (!(data instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
      }

      // 记录完整的请求信息
      console.log('完整请求URL:', url);
      console.log('请求头:', headers);
      console.log('请求数据:', data instanceof FormData ? '[FormData]' : JSON.stringify(data, null, 2));

      try {
        const response = await axios.post(url, requestData, {
          ...options,
          headers
        });

        console.log('收到 POST 响应:', response);
        return response;
      } catch (error) {
        console.error('POST 请求失败:', error);
        console.error('请求URL:', url);
        console.error('请求数据:', data instanceof FormData ? '[FormData]' : JSON.stringify(data, null, 2));
        throw error;
      }
    },
    '提交数据失败'
  ),

  /**
   * PUT 请求
   * @param {string} url - 请求 URL
   * @param {Object} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise} 返回请求结果
   */
  put: createApiMethod(
    async (url, data = {}, options = {}) => {
      const response = await axios.put(url, data, {
        ...options,
        headers: {
          ...getAuthHeaders(),
          ...options.headers
        }
      });
      return response;
    },
    '更新数据失败'
  ),

  /**
   * DELETE 请求
   * @param {string} url - 请求 URL
   * @param {Object} options - 请求选项
   * @returns {Promise} 返回请求结果
   */
  delete: createApiMethod(
    async (url, options = {}) => {
      const response = await axios.delete(url, {
        ...options,
        headers: {
          ...getAuthHeaders(),
          ...options.headers
        }
      });
      return response;
    },
    '删除数据失败'
  ),

  /**
   * PATCH 请求
   * @param {string} url - 请求 URL
   * @param {Object} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise} 返回请求结果
   */
  patch: createApiMethod(
    async (url, data = {}, options = {}) => {
      const response = await axios.patch(url, data, {
        ...options,
        headers: {
          ...getAuthHeaders(),
          ...options.headers
        }
      });
      return response;
    },
    '更新数据失败'
  )
};

export default apiClient;
