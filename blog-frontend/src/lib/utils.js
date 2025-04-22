/**
 * 合并类名
 * @param  {...string} inputs 类名列表
 * @returns {string} 合并后的类名
 */
export function cn(...inputs) {
  return inputs
    .filter(Boolean)
    .join(' ')
    .trim();
}
