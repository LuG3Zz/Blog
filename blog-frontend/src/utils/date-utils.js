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
 * 格式化为中国时区(UTC+8)的日期时间格式
 * @param {string} utcTimeString - UTC时间字符串
 * @param {boolean} showSeconds - 是否显示秒，默认为true
 * @param {boolean} showTimeZone - 是否显示时区信息，默认为false
 * @returns {string} 格式化后的日期时间字符串
 */
export const formatDateTimeChinaTimeZone = (utcTimeString, showSeconds = true, showTimeZone = false) => {
  try {
    if (!utcTimeString) return '未知时间';

    // 创建日期对象
    const utcDate = new Date(utcTimeString);

    // 检查日期是否有效
    if (isNaN(utcDate.getTime())) {
      console.error('无效的UTC时间字符串:', utcTimeString);
      return '无效时间';
    }

    // 手动添加8小时，转换为中国时区(UTC+8)
    const chinaTime = new Date(utcDate.getTime() + 8 * 60 * 60 * 1000);

    // 获取时区信息（仅在需要显示时区时使用）
    let timeZoneString = '';
    if (showTimeZone) {
      timeZoneString = ' +08:00'; // 中国标准时间 UTC+8
    }

    // 格式化日期部分
    const year = chinaTime.getUTCFullYear();
    const month = (chinaTime.getUTCMonth() + 1).toString().padStart(2, '0');
    const day = chinaTime.getUTCDate().toString().padStart(2, '0');

    // 基本日期格式
    let formattedDate = `${year}-${month}-${day}`;

    // 如果需要包含时间
    const hours = chinaTime.getUTCHours().toString().padStart(2, '0');
    const minutes = chinaTime.getUTCMinutes().toString().padStart(2, '0');

    if (showSeconds) {
      const seconds = chinaTime.getUTCSeconds().toString().padStart(2, '0');
      formattedDate += ` ${hours}:${minutes}:${seconds}`;
    } else {
      formattedDate += ` ${hours}:${minutes}`;
    }

    // 添加时区信息（如果需要）
    if (showTimeZone) {
      formattedDate += timeZoneString;
    }

    return formattedDate;
  } catch (error) {
    console.error('格式化中国时区日期时间错误:', error, utcTimeString);
    return '无效时间';
  }
};

// formatDate 函数已删除，请使用 formatDateTime 或 formatDateTimeChinaTimeZone 函数

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
