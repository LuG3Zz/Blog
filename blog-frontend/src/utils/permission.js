/**
 * 权限检查工具
 * 提供检查用户权限的函数
 */

/**
 * 检查用户是否为管理员
 * @param {Object} userInfo - 用户信息对象
 * @returns {boolean} 是否为管理员
 */
export const isAdmin = (userInfo) => {
  if (!userInfo) return false;
  
  // 检查 is_admin 属性
  if (userInfo.is_admin === true) {
    return true;
  }
  
  // 检查 role 属性
  if (userInfo.role) {
    return ['admin', 'administrator'].includes(userInfo.role.toLowerCase());
  }
  
  return false;
};

/**
 * 检查用户是否有特定角色
 * @param {Object} userInfo - 用户信息对象
 * @param {string|Array} roles - 角色或角色数组
 * @returns {boolean} 是否有指定角色
 */
export const hasRole = (userInfo, roles) => {
  if (!userInfo || !userInfo.role) return false;
  
  const userRole = userInfo.role.toLowerCase();
  
  if (Array.isArray(roles)) {
    return roles.some(role => role.toLowerCase() === userRole);
  }
  
  return roles.toLowerCase() === userRole;
};

export default {
  isAdmin,
  hasRole
};
