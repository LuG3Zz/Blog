/**
 * 邮箱验证相关 API
 * 封装所有与邮箱验证相关的网络请求
 */

import apiClient from '../core/apiClient';
import { API_PATHS } from '../core/apiPaths';

/**
 * 发送邮箱验证码
 * @param {string} email - 邮箱地址
 * @returns {Promise} 返回发送结果
 */
export const sendVerificationCode = (email) => {
  return apiClient.post(API_PATHS.EMAIL.SEND_VERIFICATION, { email });
};

/**
 * 验证邮箱验证码
 * @param {string} email - 邮箱地址
 * @param {string} code - 验证码
 * @returns {Promise} 返回验证结果
 */
export const verifyEmailCode = (email, code) => {
  return apiClient.post(API_PATHS.EMAIL.VERIFY_CODE, { email, code });
};

export default {
  sendVerificationCode,
  verifyEmailCode
};
