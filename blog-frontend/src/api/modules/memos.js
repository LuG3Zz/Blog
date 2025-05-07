/**
 * 备忘录相关 API
 * 封装所有与备忘录数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取备忘录列表
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=100] - 返回的记录数
 * @returns {Promise} 返回包含备忘录列表的Promise对象
 */
export const getMemos = async (params = {}) => {
  try {
    console.log('开始获取备忘录列表');

    // 设置查询参数
    const queryParams = {
      skip: params.skip || 0,
      limit: params.limit || 100
    };

    // 发送请求到备忘录列表端点
    const response = await apiClient.get(API_PATHS.MEMOS.BASE, {
      params: queryParams
    });

    console.log('获取备忘录列表成功:', response);
    return response;
  } catch (error) {
    console.error('获取备忘录列表失败:', error);
    throw error;
  }
};

/**
 * 获取指定ID的备忘录
 * @param {number} memoId - 备忘录ID
 * @returns {Promise} 返回包含备忘录信息的Promise对象
 */
export const getMemo = async (memoId) => {
  try {
    console.log(`开始获取备忘录 ${memoId}`);

    // 发送请求到备忘录详情端点
    const response = await apiClient.get(API_PATHS.MEMOS.BY_ID(memoId));

    console.log(`获取备忘录 ${memoId} 成功:`, response);
    return response;
  } catch (error) {
    console.error(`获取备忘录 ${memoId} 失败:`, error);
    throw error;
  }
};

/**
 * 创建新备忘录
 * @param {Object} memoData - 备忘录数据
 * @param {string} memoData.title - 备忘录标题
 * @param {string} memoData.content - 备忘录内容
 * @param {boolean} [memoData.is_encrypted=false] - 是否加密
 * @param {string} [memoData.password] - 如果加密，提供密码
 * @returns {Promise} 返回包含创建的备忘录信息的Promise对象
 */
export const createMemo = async (memoData) => {
  try {
    console.log('开始创建备忘录，发送的数据:', JSON.stringify(memoData, null, 2));

    // 发送请求到创建备忘录端点
    const response = await apiClient.post(API_PATHS.MEMOS.BASE, memoData);

    console.log('创建备忘录成功，服务器响应:', response);
    return response;
  } catch (error) {
    console.error('创建备忘录失败:', error);
    console.error('错误详情:', error.response ? error.response.data : '无详细信息');
    throw error;
  }
};

/**
 * 更新备忘录
 * @param {number} memoId - 备忘录ID
 * @param {Object} memoData - 备忘录数据
 * @param {string} [memoData.title] - 备忘录标题
 * @param {string} [memoData.content] - 备忘录内容
 * @param {boolean} [memoData.is_encrypted] - 是否加密
 * @param {string} [memoData.password] - 如果加密，提供密码
 * @returns {Promise} 返回包含更新后的备忘录信息的Promise对象
 */
export const updateMemo = async (memoId, memoData) => {
  try {
    console.log(`开始更新备忘录 ${memoId}`);

    // 发送请求到更新备忘录端点
    const response = await apiClient.put(API_PATHS.MEMOS.BY_ID(memoId), memoData);

    console.log(`更新备忘录 ${memoId} 成功:`, response);
    return response;
  } catch (error) {
    console.error(`更新备忘录 ${memoId} 失败:`, error);
    throw error;
  }
};

/**
 * 删除备忘录
 * @param {number} memoId - 备忘录ID
 * @returns {Promise} 返回删除结果
 */
export const deleteMemo = async (memoId) => {
  try {
    console.log(`开始删除备忘录 ${memoId}`);

    // 发送请求到删除备忘录端点
    // 使用正确的API路径
    const url = API_PATHS.MEMOS.BY_ID(memoId);
    console.log(`删除备忘录的URL: ${url}`);
    const response = await apiClient.delete(url);

    console.log(`删除备忘录 ${memoId} 成功:`, response);
    return response;
  } catch (error) {
    console.error(`删除备忘录 ${memoId} 失败:`, error);
    throw error;
  }
};

/**
 * 验证备忘录密码
 * @param {number} memoId - 备忘录ID
 * @param {string} password - 密码
 * @returns {Promise} 返回验证结果和备忘录内容（如果验证成功）
 */
export const verifyMemoPassword = async (memoId, password) => {
  try {
    console.log(`开始验证备忘录 ${memoId} 的密码`);

    // 发送请求到验证密码端点
    const response = await apiClient.post(API_PATHS.MEMOS.VERIFY(memoId), {
      password
    });

    console.log(`验证备忘录 ${memoId} 的密码成功:`, response);
    return response;
  } catch (error) {
    console.error(`验证备忘录 ${memoId} 的密码失败:`, error);
    throw error;
  }
};

/**
 * 获取公开备忘录列表，无需登录
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=100] - 返回的记录数
 * @returns {Promise} 返回包含公开备忘录列表的Promise对象
 */
export const getPublicMemos = async (params = {}) => {
  try {
    console.log('开始获取公开备忘录列表');

    // 设置查询参数
    const queryParams = {
      skip: params.skip || 0,
      limit: params.limit || 100
    };

    // 发送请求到公开备忘录列表端点
    const response = await apiClient.get(`${API_PATHS.MEMOS.BASE}public`, {
      params: queryParams
    });

    console.log('获取公开备忘录列表成功:', response);
    return response;
  } catch (error) {
    console.error('获取公开备忘录列表失败:', error);
    throw error;
  }
};

/**
 * 获取所有备忘录列表（包括加密的），无需登录
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=100] - 返回的记录数
 * @returns {Promise} 返回包含所有备忘录列表的Promise对象
 */
export const getAllMemos = async (params = {}) => {
  try {
    console.log('开始获取所有备忘录列表（包括加密的）');

    // 设置查询参数
    const queryParams = {
      skip: params.skip || 0,
      limit: params.limit || 100
    };

    // 发送请求到所有备忘录列表端点
    const response = await apiClient.get(`${API_PATHS.MEMOS.BASE}all`, {
      params: queryParams
    });

    console.log('获取所有备忘录列表成功:', response);
    return response;
  } catch (error) {
    console.error('获取所有备忘录列表失败:', error);
    throw error;
  }
};



/**
 * 获取指定ID的公开备忘录，无需登录
 * @param {number} memoId - 备忘录ID
 * @returns {Promise} 返回包含公开备忘录信息的Promise对象
 */
export const getPublicMemo = async (memoId) => {
  try {
    console.log(`开始获取公开备忘录 ${memoId}`);

    // 发送请求到公开备忘录详情端点
    const response = await apiClient.get(`${API_PATHS.MEMOS.BASE}public/${memoId}`);

    console.log(`获取公开备忘录 ${memoId} 成功:`, response);
    return response;
  } catch (error) {
    console.error(`获取公开备忘录 ${memoId} 失败:`, error);
    throw error;
  }
};

/**
 * 搜索备忘录
 * @param {Object} params - 搜索参数
 * @param {string} params.q - 搜索关键词
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=100] - 返回的记录数
 * @returns {Promise} 返回包含搜索结果的Promise对象
 */
export const searchMemos = async (params) => {
  try {
    if (!params.q) {
      throw new Error('搜索关键词不能为空');
    }

    console.log('开始搜索备忘录，关键词:', params.q);

    // 设置查询参数
    const queryParams = {
      q: params.q,
      skip: params.skip || 0,
      limit: params.limit || 100
    };

    // 发送请求到搜索端点
    const response = await apiClient.get(API_PATHS.MEMOS.SEARCH, {
      params: queryParams
    });

    console.log('搜索备忘录成功:', response);
    return response;
  } catch (error) {
    console.error('搜索备忘录失败:', error);
    throw error;
  }
};

export default {
  getMemos,
  getMemo,
  createMemo,
  updateMemo,
  deleteMemo,
  verifyMemoPassword,
  getPublicMemos,
  getAllMemos,
  getPublicMemo,
  searchMemos
};
