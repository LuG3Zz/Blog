import { useRouter } from 'vue-router'

/**
 * 处理页面导航
 * @returns {Object} 包含导航相关方法的对象
 */
export function useNavigation() {
  const router = useRouter()

  /**
   * 返回上一页
   */
  const goBack = () => {
    router.back()
  }

  /**
   * 导航到作者资料页
   * @param {Number|String} authorId 作者ID
   */
  const navigateToAuthorProfile = (authorId) => {
    if (!authorId) return
    router.push(`/user/${authorId}`)
  }

  return {
    goBack,
    navigateToAuthorProfile
  }
}
