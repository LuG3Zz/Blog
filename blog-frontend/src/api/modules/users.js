/**
 * 用户相关 API
 * 封装所有与用户数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import message from '@/utils/message';
import { API_PATHS } from '../core/apiPaths';

/**
 * 用户登录
 * @param {Object} credentials - 登录凭证
 * @param {string} credentials.username - 用户名
 * @param {string} credentials.password - 密码
 * @returns {Promise} 返回包含登录结果的Promise对象
 */
export const login = async (credentials) => {
  try {
    console.log('开始登录请求，用户名:', credentials.username);

    // 根据新的API文档，直接发送JSON格式的登录请求
    const loginData = {
      username: credentials.username,
      password: credentials.password
    };

    console.log('发送登录请求到:', API_PATHS.USERS.LOGIN);

    const response = await apiClient.post(API_PATHS.USERS.LOGIN, loginData);

    // 从响应中提取token信息
    console.log('登录响应:', response);

    // 检查响应中是否包含所需的字段
    if (!response.access_token) {
      throw new Error('服务器响应中缺少 access_token');
    }

    const { access_token, token_type = 'Bearer' } = response;
    // 构造完整的token并存储
    const fullToken = `${token_type} ${access_token}`;

    // 先清除旧的令牌，再存储新的令牌，确保存储成功
    localStorage.removeItem('token');
    localStorage.setItem('token', fullToken);

    // 打印令牌信息以便调试
    console.log('存储的令牌:', fullToken);
    console.log('验证存储:', localStorage.getItem('token'));

    // 获取用户信息并存储用户ID
    try {
      // 设置全局认证头
      apiClient.defaults.headers.common['Authorization'] = fullToken;
      console.log('登录时设置认证头:', fullToken);

      // 请求用户信息
      try {
        const userInfo = await getUserInfo();
        console.log('登录时获取用户信息成功:', userInfo);

        if (userInfo && userInfo.id) {
          localStorage.setItem('userId', userInfo.id);
          localStorage.setItem('userInfo', JSON.stringify(userInfo));
          console.log('用户信息已存储到本地');
        } else {
          console.warn('用户信息不完整:', userInfo);
        }
      } catch (innerError) {
        console.error('登录时获取用户信息失败:', innerError);
      }
    } catch (userError) {
      console.error('获取用户信息外层异常:', userError);
    }

    return response;
  } catch (error) {
    message.error('登录失败: ' + (error.response?.data?.detail || error.message));
    throw error;
  }
};

/**
 * 用户注册
 * @param {Object} userData - 用户数据
 * @param {string} userData.username - 用户名
 * @param {string} userData.email - 邮箱
 * @param {string} userData.password - 密码
 * @param {string} [userData.verification_code] - 邮箱验证码（如果启用了邮箱验证）
 * @returns {Promise} 返回包含注册结果的Promise对象
 */
export const register = (userData) => {
  // 构建注册数据
  const registerData = {
    username: userData.username,
    email: userData.email,
    password: userData.password
  };

  // 如果提供了验证码，添加到请求数据中
  if (userData.verification_code) {
    registerData.verification_code = userData.verification_code;
  }

  return apiClient.post(API_PATHS.USERS.BASE, registerData);
};

/**
 * 用户登出
 * 清除本地存储的token
 */
export const logout = () => {
  // 清除所有用户相关的本地存储
  localStorage.removeItem('token');
  localStorage.removeItem('userId');
  localStorage.removeItem('userInfo');
  return true;
};

/**
 * 获取用户信息
 * @returns {Promise} 返回包含用户信息的Promise对象
 */
export const getUserInfo = async () => {
  try {
    console.log('开始获取用户信息');
    const token = localStorage.getItem('token');
    console.log('当前令牌:', token);

    if (!token) {
      console.error('未找到认证令牌');
      return Promise.reject(new Error('未找到认证令牌'));
    }

    // 使用简单的配置请求用户信息
    // 使用选项参数传递认证信息
    const response = await apiClient.get(API_PATHS.USERS.ME, {}, {
      headers: {
        'Authorization': token
      }
    });

    console.log('获取用户信息成功:', response);
    return response;
  } catch (error) {
    console.error('获取用户信息失败:', error);
    throw error;
  }
};

/**
 * 根据ID获取用户
 * @param {number} userId - 用户ID
 * @returns {Promise} 返回包含用户数据的Promise对象
 */
export const getUserById = async (userId) => {
  try {
    console.log('开始获取用户信息，ID:', userId);

    // 获取用户信息不需要登录，直接请求
    const response = await apiClient.get(API_PATHS.USERS.BY_ID(userId));

    console.log('获取用户信息成功:', response);
    return response;
  } catch (error) {
    console.error('获取用户信息失败:', error);
    throw error;
  }
};

/**
 * 更新用户信息
 * @param {Object} userData - 用户数据
 * @param {string} [userData.email] - 新邮箱，可选
 * @param {string} [userData.password] - 新密码，可选
 * @param {string} [userData.avatar] - 新头像URL，可选
 * @param {string} [userData.bio] - 新个人简介，可选
 * @param {Object} [userData.social_media] - 社交媒体链接，可选
 * @returns {Promise} 返回更新结果
 */
export const updateUserInfo = (userData) => {
  // 需要获取当前用户ID
  const userId = localStorage.getItem('userId');
  if (!userId) {
    return Promise.reject(new Error('用户未登录'));
  }

  // 构造更新数据，只包含有效字段
  const updateData = {};
  if (userData.email) updateData.email = userData.email;
  if (userData.password) updateData.password = userData.password;
  if (userData.avatar) updateData.avatar = userData.avatar;
  if (userData.bio) updateData.bio = userData.bio;
  if (userData.social_media) updateData.social_media = userData.social_media;

  return apiClient.put(API_PATHS.USERS.BY_ID(userId), updateData);
};

/**
 * 更改密码
 * @param {Object} passwordData - 密码数据
 * @param {string} passwordData.old_password - 旧密码
 * @param {string} passwordData.new_password - 新密码
 * @returns {Promise} 返回更改结果
 */
// 根据API文档，没有专门的修改密码接口，使用更新用户接口
export const changePassword = (passwordData) => {
  const userId = localStorage.getItem('userId');
  if (!userId) {
    return Promise.reject(new Error('用户未登录'));
  }
  return apiClient.put(API_PATHS.USERS.BY_ID(userId), { password: passwordData.new_password });
};

/**
 * 检查用户是否已登录
 * @returns {boolean} 返回用户是否已登录
 */
export const isLoggedIn = () => {
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('userId');
  return !!token && !!userId;
};

/**
 * 获取当前用户令牌
 * @returns {string|null} 返回用户令牌或 null
 */
export const getToken = () => {
  return localStorage.getItem('token');
};

/**
 * 获取用户发布的文章列表
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=10] - 返回的最大记录数
 * @returns {Promise} 返回包含文章列表的Promise对象
 */
export const getUserArticles = (userId, params = {}) => {
  return apiClient.get(API_PATHS.USERS.ARTICLES(userId), {
    params: {
      skip: params.skip || 0,
      limit: params.limit || 10
    }
  });
};

/**
 * 获取用户的评论列表
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=10] - 返回的最大记录数
 * @returns {Promise} 返回包含评论列表的Promise对象
 */
export const getUserComments = (userId, params = {}) => {
  return apiClient.get(API_PATHS.USERS.COMMENTS(userId), {
    params: {
      skip: params.skip || 0,
      limit: params.limit || 10
    }
  });
};

/**
 * 获取用户活动记录
 * @param {number} userId - 用户ID
 * @param {Object} params - 查询参数
 * @param {number} [params.skip=0] - 跳过的记录数
 * @param {number} [params.limit=10] - 返回的最大记录数
 * @returns {Promise} 返回包含活动记录的Promise对象
 */
export const getUserActivities = (userId, params = {}) => {
  return apiClient.get(API_PATHS.USERS.ACTIVITIES(userId), {
    params: {
      skip: params.skip || 0,
      limit: params.limit || 10
    }
  });
};

/**
 * 获取管理员信息
 * @returns {Promise} 返回管理员信息
 */
export const getAdminInfo = async () => {
  try {
    console.log('开始获取管理员信息');

    // 使用管理员信息 API 端点
    const response = await apiClient.get(API_PATHS.USERS.ADMIN_INFO);

    console.log('获取管理员信息成功:', response);
    return response;
  } catch (error) {
    console.error('获取管理员信息失败:', error);
    throw error;
  }
};

export default {
  login,
  register,
  logout,
  getUserInfo,
  getUserById,
  updateUserInfo,
  changePassword,
  isLoggedIn,
  getToken,
  getUserArticles,
  getUserComments,
  getUserActivities,
  getAdminInfo
};
