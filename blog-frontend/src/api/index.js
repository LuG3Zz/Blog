/**
 * API 模块导出
 * 集中导出所有 API 模块，方便统一导入
 */

// 核心 API 客户端
import apiClient from './core/apiClient';

// API 模块
import * as postsApi from './modules/posts';
import * as usersApi from './modules/users';
import * as categoriesApi from './modules/categories';
import * as commentsApi from './modules/comments';
import * as homeApi from './modules/home';
import * as activitiesApi from './modules/activities';
import * as adminApi from './modules/admin';
import * as filesApi from './modules/files';
import * as tagsApi from './modules/tags';
import * as searchApi from './modules/search';
import * as statsApi from './modules/stats';
import * as notificationsApi from './modules/notifications';
import * as notificationHistoryApi from './modules/notificationHistory';
import * as aboutApi from './modules/about';
import * as visitorsApi from './modules/visitors';
import * as siteSettingsApi from './modules/siteSettings';
import * as emailApi from './modules/email';
import * as subscriptionsApi from './modules/subscriptions';
import * as memosApi from './modules/memos';

// 导出所有 API 模块
export {
  apiClient,
  postsApi,
  usersApi,
  categoriesApi,
  commentsApi,
  homeApi,
  activitiesApi,
  adminApi,
  filesApi,
  tagsApi,
  searchApi,
  statsApi,
  notificationsApi,
  notificationHistoryApi,
  aboutApi,
  visitorsApi,
  siteSettingsApi,
  emailApi,
  subscriptionsApi,
  memosApi
};

// 为了向后兼容，保留原来的导出名称
export const postApi = postsApi;
export const userApi = usersApi;
export const categoryApi = categoriesApi;
export const commentApi = commentsApi;
export const activityApi = activitiesApi;
export const userManageApi = adminApi;
export const fileApi = filesApi;
export const tagApi = tagsApi;
export const search = searchApi;
export const notificationApi = notificationsApi;
// notificationHistoryApi 已经在上面导出，这里不需要重复导出
export const aboutPageApi = aboutApi;
// statsApi 已经在上面导出，这里不需要重复导出
export const visitorApi = visitorsApi;
export const emailVerificationApi = emailApi;
export const subscriptionApi = subscriptionsApi;
export const memoApi = memosApi;

// 默认导出所有 API
export default {
  client: apiClient,
  posts: postsApi,
  users: usersApi,
  categories: categoriesApi,
  comments: commentsApi,
  home: homeApi,
  activities: activitiesApi,
  admin: adminApi,
  files: filesApi,
  tags: tagsApi,
  search: searchApi,
  stats: statsApi,
  notifications: notificationsApi,
  notificationHistory: notificationHistoryApi,
  about: aboutApi,
  visitors: visitorsApi,
  siteSettings: siteSettingsApi,
  email: emailApi,
  subscriptions: subscriptionsApi,
  memos: memosApi
};
