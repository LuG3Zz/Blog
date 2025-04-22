/**
 * axios配置文件
 * 配置请求拦截器和响应拦截器
 */

import axios from 'axios'
import { API_BASE_URL, IS_DEV } from '@/config'

// 创建axios实例
const instance = axios.create({
  baseURL: API_BASE_URL,  // 使用配置文件中的 API 基础 URL
  timeout: 15000,   // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
  },
  // 添加调试信息
  validateStatus: function (status) {
    if (IS_DEV) {
      console.log('响应状态码:', status);
    }
    return status >= 200 && status < 300; // 默认的验证逻辑
  }
})

// 请求拦截器
instance.interceptors.request.use(
  async config => {
    // 在开发模式下输出详细日志
    if (IS_DEV) {
      console.log('发送请求:', config.method.toUpperCase(), config.url);
      console.log('请求头:', config.headers);
      if (config.data) {
        console.log('请求体:',
          typeof config.data === 'string' ? config.data : JSON.stringify(config.data));
      }
      if (config.params) {
        console.log('请求参数:', config.params);
      }
    }

    // 如果请求头中已经有 Authorization，则优先使用请求头中的
    if (!config.headers.Authorization && !config.headers.get('Authorization')) {
      const token = localStorage.getItem('token')
      if (token) {
        // 根据 OAuth2 规范设置 Authorization 头
        const lowerToken = token.toLowerCase();
        let cleanToken = token;
        if (lowerToken.includes('bearer')) {
          cleanToken = token.replace(/^\s*bearer\s+/i, '');
        }
        config.headers.Authorization = `Bearer ${cleanToken}`
        console.log('拦截器中的token:', config.headers.Authorization)
      } else if (!config.url.includes('/auth/login')) {
        console.warn('未找到认证令牌，请先登录')
      }
    } else {
      console.log('使用请求中提供的 Authorization 头:', config.headers.Authorization || config.headers.get('Authorization'))
    }

    // 确保内容类型正确设置
    if (!config.headers['Content-Type'] && !config.headers.get('Content-Type')) {
      config.headers['Content-Type'] = 'application/json'
    }

    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  response => {
    if (IS_DEV) {
      console.log('响应成功:', response.status, response.config.url);
      console.log('响应数据:', response.data);
    }
    return response.data
  },
  async error => {
    const originalRequest = error.config;

    // 如果是认证错误且不是登录请求本身
    if (error.response && error.response.status === 401 &&
        !originalRequest._retry &&
        !originalRequest.url.includes('/auth/login')) {

      console.warn('认证失败，请重新登录');

      // 清除本地存储的认证信息
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      localStorage.removeItem('userInfo');

      // 跳转到登录页面
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }

    if (error.response) {
      switch (error.response.status) {
        case 401:
          console.error('未授权，请先登录');
          break;
        case 403:
          console.error('没有权限访问该资源');
          break;
        case 404:
          console.error('请求的资源不存在');
          break;
        case 500:
          console.error('服务器错误');
          break;
        default:
          console.error(`未知错误: ${error.response.status}`);
      }

      // 打印详细错误信息以便调试
      if (error.response.data) {
        console.error('错误详情:', error.response.data);
      }
    } else {
      console.error('网络错误:', error.message);
    }

    return Promise.reject(error);
  }
)

export default instance
