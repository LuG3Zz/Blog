/**
 * 日期时间工具函数
 * 处理UTC时间转换为本地时间和格式化
 */

import { formatDistanceToNow, format, parseISO } from 'date-fns';
import { zhCN } from 'date-fns/locale';

/**
 * 将UTC时间字符串转换为本地时间的Date对象
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {Date} 本地时间的Date对象
 */
export const utcToLocalDate = (utcTimeString) => {
  if (!utcTimeString) return null;

  try {
    // 创建Date对象 - JavaScript会自动将UTC时间转换为本地时间
    // 确保时间字符串被解析为UTC时间
    let date;

    // 检查时间字符串格式
    if (utcTimeString.endsWith('Z')) {
      // 已经是ISO格式的UTC时间
      date = new Date(utcTimeString);
    } else if (utcTimeString.includes('T') && utcTimeString.includes('+')) {
      // 带有时区偏移的ISO格式
      date = new Date(utcTimeString);
    } else if (utcTimeString.includes('T')) {
      // ISO格式但没有明确的时区，假定为UTC
      date = new Date(utcTimeString + 'Z');
    } else {
      // 其他格式，尝试直接解析
      date = new Date(utcTimeString);
    }

    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      console.error('无效的UTC时间字符串:', utcTimeString);
      return null;
    }

    return date;
  } catch (error) {
    console.error('UTC时间转换错误:', error, utcTimeString);
    return null;
  }
};

/**
 * 格式化为相对时间（如"3小时前"）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 格式化后的相对时间字符串
 */
export const formatRelativeTime = (utcTimeString) => {
  try {
    if (!utcTimeString) return '未知时间';

    const localDate = utcToLocalDate(utcTimeString);
    if (!localDate) return '无效时间';

    return formatDistanceToNow(localDate, { addSuffix: true, locale: zhCN });
  } catch (error) {
    console.error('格式化相对时间错误:', error, utcTimeString);
    return '无效时间';
  }
};

/**
 * 格式化为标准日期时间格式
 * @param {string} utcTimeString - UTC时间字符串
 * @param {string} formatString - 格式化模板，默认为'yyyy-MM-dd HH:mm:ss'
 * @returns {string} 格式化后的日期时间字符串
 */
export const formatDateTime = (utcTimeString, formatString = 'yyyy-MM-dd HH:mm:ss') => {
  try {
    if (!utcTimeString) return '未知时间';

    const localDate = utcToLocalDate(utcTimeString);
    if (!localDate) return '无效时间';

    return format(localDate, formatString, { locale: zhCN });
  } catch (error) {
    console.error('格式化日期时间错误:', error, utcTimeString);
    return '无效时间';
  }
};

/**
 * 格式化为本地时区的日期时间格式
 * @param {string} utcTimeString - UTC时间字符串
 * @param {boolean} showSeconds - 是否显示秒，默认为true
 * @returns {string} 格式化后的日期时间字符串
 */
export const formatDateTimeWithTimeZone = (utcTimeString, showSeconds = true) => {
  try {
    if (!utcTimeString) return '未知时间';

    const localDate = utcToLocalDate(utcTimeString);
    if (!localDate) return '无效时间';

    const formatStr = showSeconds ? 'yyyy-MM-dd HH:mm:ss' : 'yyyy-MM-dd HH:mm';

    // 直接返回本地时区的时间，不包含时区信息
    return format(localDate, formatStr, { locale: zhCN });
  } catch (error) {
    console.error('格式化本地时区日期时间错误:', error, utcTimeString);
    return '无效时间';
  }
};

/**
 * 格式化为日期（如"2023年01月01日"）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (utcTimeString) => {
  return formatDateTime(utcTimeString, 'yyyy年MM月dd日');
};

/**
 * 格式化为时间（如"12:30:45"）
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 格式化后的时间字符串
 */
export const formatTime = (utcTimeString) => {
  return formatDateTime(utcTimeString, 'HH:mm:ss');
};

/**
 * 获取本地化的完整日期时间字符串
 * @param {string} utcTimeString - UTC时间字符串
 * @returns {string} 本地化的日期时间字符串
 */
export const getLocalizedDateTime = (utcTimeString) => {
  try {
    if (!utcTimeString) return '未知时间';

    const localDate = utcToLocalDate(utcTimeString);
    if (!localDate) return '无效时间';

    // 使用toLocaleString显示本地时区的时间，不显示时区信息
    return localDate.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  } catch (error) {
    console.error('获取本地化日期时间错误:', error, utcTimeString);
    return '无效时间';
  }
};

/**
 * 获取当前时区信息
 * @returns {string} 当前时区信息
 */
export const getCurrentTimeZone = () => {
  try {
    const date = new Date();
    const timeZoneOffset = -date.getTimezoneOffset();
    const hours = Math.floor(Math.abs(timeZoneOffset) / 60);
    const minutes = Math.abs(timeZoneOffset) % 60;
    const sign = timeZoneOffset >= 0 ? '+' : '-';

    return `UTC${sign}${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  } catch (error) {
    console.error('获取时区信息错误:', error);
    return 'UTC+00:00';
  }
};
