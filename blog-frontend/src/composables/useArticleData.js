import { ref } from 'vue'
import message from '@/utils/message'

/**
 * 处理文章数据获取和处理
 * @param {Object} options 配置选项
 * @returns {Object} 包含文章数据相关方法和状态的对象
 */
export function useArticleData(options = {}) {
  const { postApi, usersApi, isComponentMounted, calculateReadingTime } = options
  const post = ref(null)
  const loading = ref(true)
  const markdownContent = ref('')
  const readingTime = ref(0)

  /**
   * 获取文章图片
   * @returns {String} 文章图片URL
   */
  const getPostImage = () => {
    if (!post.value) return ''

    // 优先使用文章的自定义封面图
    if (post.value.cover_image) {
      return post.value.cover_image
    }

    // 如果没有自定义封面，使用随机图片
    const titleHash = post.value.title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
    const imageIndex = (titleHash % 35) + 1 // 使用模35确保索引在1-35范围内

    return `/images/img${imageIndex}.jpg`
  }

  /**
   * 获取文章标签
   * @returns {Array} 文章标签数组
   */
  const getPostTags = () => {
    if (!post.value) return []

    // 如果有 tags_list 字段，使用新格式
    if (post.value.tags_list && Array.isArray(post.value.tags_list)) {
      return post.value.tags_list.map(tag => tag.name)
    }
    // 兼容旧格式
    else if (post.value.tags) {
      if (typeof post.value.tags === 'string') {
        return post.value.tags.split(',').map(tag => tag.trim()).filter(tag => tag !== '')
      } else if (Array.isArray(post.value.tags)) {
        return post.value.tags.map(tag => {
          if (typeof tag === 'object' && tag !== null) {
            return tag.name || ''
          }
          return tag
        }).filter(tag => tag !== '')
      }
    }
    return []
  }

  /**
   * 获取角色名称
   * @param {String} role 角色代码
   * @returns {String} 角色名称
   */
  const getRoleName = (role) => {
    const roleMap = {
      'admin': '管理员',
      'editor': '编辑',
      'user': '用户'
    }
    return roleMap[role] || role
  }

  /**
   * 格式化日期
   * @param {String} dateString 日期字符串
   * @returns {String} 格式化后的日期
   */
  const formatDate = (dateString) => {
    if (!dateString) return '-'
    try {
      return new Date(dateString).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    } catch (error) {
      console.error('日期格式化错误:', error)
      return dateString
    }
  }

  /**
   * 处理图片加载错误
   * @param {Event} event 事件对象
   */
  const handleImageError = (event) => {
    // 设置默认图片
    event.target.src = '/images/default-avatar.jpg'
    // 防止循环触发错误事件
    event.target.onerror = null
  }

  /**
   * 获取文章数据
   * @param {Number|String} postId 文章ID
   */
  const fetchPost = async (postId) => {
    if (!isComponentMounted.value) return

    loading.value = true
    try {
      const response = await postApi.getPostById(postId)
      if (!isComponentMounted.value) return

      // 如果有作者ID，获取作者信息
      let authorData = null
      if (response.author_id) {
        try {
          authorData = await usersApi.getUserById(response.author_id)
        } catch (authorError) {
          console.error('获取作者信息失败:', authorError)
        }
      }

      post.value = {
        id: response.id,
        title: response.title,
        slug: response.slug,
        content: response.content,
        category: response.category?.name || response.category_name,
        category_id: response.category?.id || response.category_id,
        tags: response.tags_list || response.tags,
        cover_image: response.cover_image,
        excerpt: response.excerpt,
        author_id: response.author_id,
        // 如果响应中已包含作者信息，使用响应中的作者信息
        author: response.author || authorData,
        view_count: response.view_count,
        like_count: response.like_count,
        is_featured: response.is_featured,
        created_at: response.created_at,
        updated_at: response.updated_at,
        date: new Date(response.created_at).toLocaleDateString('zh-CN')
      }

      markdownContent.value = response.content
      readingTime.value = calculateReadingTime(response.content)
    } catch (error) {
      console.error('获取文章失败:', error)
      message.error('获取文章详情失败')
      post.value = null
    } finally {
      loading.value = false
    }
  }

  /**
   * 生成AI摘要内容
   * @returns {String} AI摘要内容
   */
  const generateAiSummary = () => {
    if (!post.value) return ''
    if (post.value.excerpt) return post.value.excerpt

    // 这里可以根据文章内容生成一个更智能的摘要
    return `这是一篇关于${post.value.category}的精彩文章，主要探讨了${post.value.title}的核心观点。文章从多个角度分析了这一主题的重要性和应用价值，值得深入阅读。`
  }

  return {
    post,
    loading,
    markdownContent,
    readingTime,
    getPostImage,
    getPostTags,
    getRoleName,
    formatDate,
    handleImageError,
    fetchPost,
    generateAiSummary
  }
}
