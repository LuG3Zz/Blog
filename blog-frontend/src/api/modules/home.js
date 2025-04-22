/**
 * 首页相关 API
 * 封装所有与首页数据相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 获取首页数据
 * @returns {Promise} 返回包含首页所需数据的Promise对象
 */
export const getHomeData = async () => {
  try {
    // 并行请求多个接口，提高效率
    // 使用 Promise.allSettled 而不是 Promise.all，这样即使某个请求失败也不会影响其他请求
    const results = await Promise.allSettled([
      getFeaturedPosts(5),
      getLatestPosts(10),
      apiClient.get(API_PATHS.CATEGORIES.BASE),
      apiClient.get(API_PATHS.STATS.ACTIVITY_HEATMAP),
      getUserData()
    ]);

    // 处理结果，如果请求失败则提供默认数据
    const featuredPosts = results[0].status === 'fulfilled' ? results[0].value : [];
    const latestPosts = results[1].status === 'fulfilled' ? results[1].value : [];
    const categories = results[2].status === 'fulfilled' ? results[2].value : [];
    const activityData = results[3].status === 'fulfilled' ? results[3].value : [];
    const userData = results[4].status === 'fulfilled' ? results[4].value : getDefaultUserData();

    // 打印失败的请求
    results.forEach((result, index) => {
      if (result.status === 'rejected') {
        console.error(`请求 ${index} 失败:`, result.reason);
      }
    });

    // 构造首页数据
    return {
      featuredPosts,
      posts: latestPosts,
      categories,
      activityData,
      userData
    };
  } catch (error) {
    console.error('获取首页数据失败:', error);

    // 返回默认数据而不是抛出异常
    return {
      featuredPosts: [],
      posts: [],
      categories: [],
      activityData: [],
      userData: getDefaultUserData()
    };
  }
};

/**
 * 获取默认用户数据
 * @returns {Object} 返回默认用户数据
 */
const getDefaultUserData = () => {
  return {
    username: 'BrownLu',
    bio: '欢迎来到我的博客！',
    avatar: null,
    social: {
      github: 'https://github.com',
      twitter: 'https://twitter.com',
      linkedin: 'https://linkedin.com'
    }
  };
};

/**
 * 获取用户数据
 * @returns {Promise} 返回用户数据
 */
const getUserData = async () => {
  try {
    // 尝试获取管理员信息
    try {
      console.log('尝试使用 /users/admin/info 获取管理员信息');
      const adminInfo = await apiClient.get(API_PATHS.USERS.ADMIN_INFO);
      if (adminInfo) {
        console.log('成功获取管理员信息:', adminInfo);
        return adminInfo;
      }
    } catch (adminError) {
      console.warn('获取管理员信息失败，尝试备用方法:', adminError);
    }

    // 如果获取管理员信息失败，尝试获取当前登录用户的信息
    const token = localStorage.getItem('token');
    if (token) {
      try {
        console.log('尝试获取当前登录用户信息');
        const userInfo = await apiClient.get(API_PATHS.USERS.ME, {}, {
          headers: {
            'Authorization': token
          }
        });
        console.log('成功获取当前用户信息:', userInfo);
        return userInfo;
      } catch (e) {
        console.warn('获取用户信息失败，使用默认数据:', e);
      }
    }

    // 如果上述方法都失败，返回默认数据
    console.log('使用默认用户数据');
    return getDefaultUserData();
  } catch (error) {
    console.error('获取用户数据失败:', error);
    return getDefaultUserData();
  }
};

/**
 * 获取精选文章
 * @param {number} limit - 返回的文章数量
 * @returns {Promise} 返回精选文章列表
 */
/**
 * 获取热门文章
 * @param {number} limit - 返回的文章数量
 * @param {string} period - 时间范围（day/week/month/year/all）
 * @returns {Promise} 返回热门文章列表
 */
export const getPopularPosts = (limit = 5, period = 'all') => {
  return apiClient.get(API_PATHS.STATS.POPULAR_ARTICLES, {
    params: {
      limit,
      period
    }
  });
};

/**
 * 获取最新文章
 * @param {number} limit - 返回的文章数量
 * @returns {Promise} 返回最新文章列表
 */
export const getLatestPosts = async (limit = 5) => {
  try {
    // 使用文章列表接口，按创建时间排序
    const response = await apiClient.get(API_PATHS.ARTICLES.BASE, {
      params: {
        limit: limit,
        skip: 0,
        sort: 'created_at:desc'
      }
    });

    return Array.isArray(response) ? response : [];
  } catch (error) {
    console.error('获取最新文章失败:', error);
    return [];
  }
};

/**
 * 获取精选文章
 * @param {number} limit - 返回的文章数量
 * @returns {Promise} 返回精选文章列表
 */
export const getFeaturedPosts = async (limit = 5) => {
  try {
    // 使用文章列表接口，并过滤精选文章
    const response = await apiClient.get(API_PATHS.ARTICLES.BASE, {
      params: {
        limit: limit,
        skip: 0,
        is_featured: true
      }
    });

    return Array.isArray(response) ? response : [];
  } catch (error) {
    console.error('获取精选文章失败:', error);
    return [];
  }
};

export default {
  getHomeData,
  getFeaturedPosts,
  getLatestPosts,
  getPopularPosts
};
