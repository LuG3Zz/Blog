/**
 * 工具函数
 */

import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * 合并类名工具函数
 * 用于合并多个类名，并过滤掉假值（如 null、undefined、false）
 *
 * @param {...ClassValue} inputs - 要合并的类名
 * @returns {string} - 合并后的类名字符串
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * 生成唯一ID
 * @returns 唯一ID字符串
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

/**
 * 格式化日期
 * @param date 日期对象或日期字符串
 * @param format 格式化字符串
 * @returns 格式化后的日期字符串
 */
export function formatDate(date: Date | string, format: string = 'yyyy-MM-dd HH:mm:ss'): string {
  const d = typeof date === 'string' ? new Date(date) : date;

  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');

  return format
    .replace('yyyy', String(year))
    .replace('MM', month)
    .replace('dd', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}
