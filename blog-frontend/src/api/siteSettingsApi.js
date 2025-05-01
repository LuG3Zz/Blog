/**
 * 网站设置API服务
 */
import request from '../utils/axios'
import { API_PATHS, API_PREFIX_STR } from './core/apiPaths'

// 网站设置API路径
const SITE_SETTINGS_API = API_PATHS.SITE_SETTINGS.BASE

/**
 * 获取网站设置
 * @returns {Promise} 返回网站设置数据
 */
export const getSiteSettings = () => {
  return request({
    url: SITE_SETTINGS_API,
    method: 'get'
  })
}

/**
 * 更新网站设置
 * @param {Object} data 网站设置数据
 * @returns {Promise} 返回更新后的网站设置数据
 */
export const updateSiteSettings = (data) => {
  return request({
    url: SITE_SETTINGS_API,
    method: 'put',
    data
  })
}

// 导出API服务
export default {
  getSiteSettings,
  updateSiteSettings
}
