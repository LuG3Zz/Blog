/**
 * 状态管理入口文件
 * 导出所有状态管理模块
 */

import userStore from './userStore';
import { themeStore } from './themeStore';

export {
  userStore,
  themeStore
};

export default {
  user: userStore,
  theme: themeStore
};
