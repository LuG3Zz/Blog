/**
 * API 路径配置
 * 集中管理所有 API 路径，方便统一修改
 */

// API 路径前缀
const API_PREFIX = '/api/v1';  // 使用后端定义的API前缀

// API 路径
export const API_PATHS = {
  // 认证相关
  AUTH: {
    LOGIN: `${API_PREFIX}/auth/login`,
  },

  // 用户相关
  USERS: {
    BASE: `${API_PREFIX}/users`,
    ME: `${API_PREFIX}/users/me`,
    BY_ID: (id) => `${API_PREFIX}/users/${id}`,
    ARTICLES: (id) => `${API_PREFIX}/users/${id}/articles`,
    COMMENTS: (id) => `${API_PREFIX}/users/${id}/comments`,
    ACTIVITIES: (id) => `${API_PREFIX}/users/${id}/activities`,
    LOGIN: `${API_PREFIX}/users/login`,
    ADMIN: `${API_PREFIX}/admin/users`,
    ADMIN_INFO: `${API_PREFIX}/users/admin/info`,
  },

  // 文章相关
  ARTICLES: {
    BASE: `${API_PREFIX}/articles`,
    BY_ID: (id) => `${API_PREFIX}/articles/${id}`,
    LIKE: (id) => `${API_PREFIX}/articles/${id}/like`,
    LIKE_STATUS: (id) => `${API_PREFIX}/articles/${id}/like-status`,
    BY_SLUG: (slug) => `${API_PREFIX}/articles/by-slug/${slug}`,
    HOME: `${API_PREFIX}/articles/home`,
    AI_ASSIST: `${API_PREFIX}/articles/ai-assist`,
  },

  // 评论相关
  COMMENTS: {
    BASE: `${API_PREFIX}/comments`,
    BY_ARTICLE_ID: (id) => `${API_PREFIX}/comments/${id}`, // 获取指定文章的评论
    BY_ID: (id) => `${API_PREFIX}/comments/${id}`, // 更新或删除评论
    LIKE: (id) => `${API_PREFIX}/comments/${id}/like`, // 点赞评论
    PENDING: `${API_PREFIX}/comments/pending`, // 获取待审核评论
    APPROVE: (id) => `${API_PREFIX}/comments/approve/${id}`, // 审核通过评论
    ALL: `${API_PREFIX}/comments/all`, // 获取所有评论
  },

  // 分类相关
  CATEGORIES: {
    BASE: `${API_PREFIX}/categories/`,
    BY_ID: (id) => `${API_PREFIX}/categories/${id}`,
  },

  // 标签相关
  TAGS: {
    BASE: `${API_PREFIX}/tags`,
    BY_ID: (id) => `${API_PREFIX}/tags/${id}`,
    BY_NAME: (name) => `${API_PREFIX}/tags/by-name/${name}`,
    ARTICLES: (id) => `${API_PREFIX}/tags/${id}/articles`,
    ADD_TO_ARTICLE: (articleId) => `${API_PREFIX}/tags/articles/${articleId}/tags`,
    UPDATE_ARTICLE_TAGS: (articleId) => `${API_PREFIX}/tags/articles/${articleId}/tags`,
    REMOVE_FROM_ARTICLE: (articleId, tagId) => `${API_PREFIX}/tags/articles/${articleId}/tags/${tagId}`,
  },

  // 搜索相关
  SEARCH: {
    ARTICLES: `${API_PREFIX}/search/articles`,
    USERS: `${API_PREFIX}/search/users`,
    TAGS: `${API_PREFIX}/search/tags`,
  },

  // 统计相关
  STATS: {
    OVERVIEW: `${API_PREFIX}/stats/overview`,
    POPULAR_ARTICLES: `${API_PREFIX}/stats/popular-articles`,
    ACTIVITY_TIMELINE: `${API_PREFIX}/stats/activity-timeline`,
    CATEGORY_DISTRIBUTION: `${API_PREFIX}/stats/category-distribution`,
    USER_ACTIVITY: `${API_PREFIX}/stats/user-activity`,
    ACTIVITY_HEATMAP: `${API_PREFIX}/stats/activity-heatmap`,
  },

  // 文件相关
  FILES: {
    UPLOAD_IMAGE: `${API_PREFIX}/files/upload-image`,
    DELETE_IMAGE: `${API_PREFIX}/files/delete-image`,
    UPLOAD: `${API_PREFIX}/files/upload`,
    LIST: `${API_PREFIX}/files/list`,
    DOWNLOAD: (id) => `${API_PREFIX}/files/download/${id}`,
    DELETE: (id) => `${API_PREFIX}/files/${id}`,
    RENAME: (id) => `${API_PREFIX}/files/rename/${id}`,
    STATS: `${API_PREFIX}/files/stats`,
    BATCH_DELETE: `${API_PREFIX}/files/batch-delete`,
  },

  // 活动相关
  ACTIVITIES: {
    BASE: `${API_PREFIX}/activities/`,
    BASIC: `${API_PREFIX}/activities/basic`,
    PUBLIC: `${API_PREFIX}/activities/public`,
  },

  // About页面相关
  ABOUT: {
    BASE: `${API_PREFIX}/about`,
  },
};

export default API_PATHS;
