<template>
  <div class="article-sidebar space-y-6">
    <!-- 作者信息 -->
    <div v-if="post.author" class="author-card bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border border-gray-100 dark:border-gray-700">
      <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">作者信息</h3>
      <div class="flex items-center space-x-3">
        <div class="flex-shrink-0">
          <div
            @click="navigateToAuthorProfile(post.author.id)"
            class="author-avatar w-16 h-16 rounded-full overflow-hidden border-2 border-gray-200 dark:border-gray-600 cursor-pointer hover:border-secondary dark:hover:border-dark-secondary transition-all duration-300 shadow-md"
          >
            <img
              v-if="post.author.avatar"
              :src="post.author.avatar"
              :alt="post.author.username"
              class="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
            />
            <div
              v-else
              class="w-full h-full bg-gradient-to-br from-secondary to-blue-500 dark:from-dark-secondary dark:to-blue-700 text-primary dark:text-dark-primary flex items-center justify-center font-bold text-xl"
            >
              {{ post.author.username.charAt(0).toUpperCase() }}
            </div>
          </div>
        </div>
        <div class="flex-grow">
          <h4
            @click="navigateToAuthorProfile(post.author.id)"
            class="font-medium text-gray-800 dark:text-gray-200 hover:text-secondary dark:hover:text-dark-secondary cursor-pointer transition-colors text-lg"
          >
            {{ post.author.username }}
          </h4>
          <p class="text-sm text-gray-500 dark:text-gray-400 flex items-center">
            <span class="inline-block w-2 h-2 rounded-full bg-green-500 mr-1"></span>
            {{ getRoleName(post.author.role) }}
          </p>
        </div>
      </div>
      <div v-if="post.author.bio" class="mt-4 text-sm text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 p-3 rounded-md border-l-2 border-secondary dark:border-dark-secondary">
        <p class="italic">{{ post.author.bio }}</p>
      </div>
      <div class="mt-4 flex flex-wrap justify-around bg-gray-50 dark:bg-gray-700 p-2 rounded-md">
        <div class="flex flex-col items-center text-sm text-gray-600 dark:text-gray-300 p-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-1 text-secondary dark:text-dark-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <span class="font-medium">{{ post.author.article_count || 0 }}</span>
          <span class="text-xs text-gray-500 dark:text-gray-400">文章</span>
        </div>
        <div class="flex flex-col items-center text-sm text-gray-600 dark:text-gray-300 p-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-1 text-secondary dark:text-dark-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <span class="font-medium">{{ post.author.comment_count || 0 }}</span>
          <span class="text-xs text-gray-500 dark:text-gray-400">评论</span>
        </div>
      </div>
      <button
        @click="navigateToAuthorProfile(post.author.id)"
        class="mt-4 w-full px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary text-sm rounded-md hover:bg-opacity-90 transition-all duration-300 flex items-center justify-center shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        查看作者主页
      </button>
    </div>

    <!-- 文章标签 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
      <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">文章标签</h3>
      <div class="flex flex-wrap gap-2">
        <!-- 处理数组形式的 tags_list -->
        <span
          v-if="post.tags_list && Array.isArray(post.tags_list)"
          v-for="tag in post.tags_list"
          :key="tag.id || tag.name"
          class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-xs hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors cursor-pointer"
        >
          {{ tag.name }}
        </span>

        <!-- 处理数组形式的 tags -->
        <span
          v-else-if="post.tags && Array.isArray(post.tags)"
          v-for="tag in post.tags"
          :key="typeof tag === 'object' ? (tag.id || tag.name) : tag"
          class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-xs hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors cursor-pointer"
        >
          {{ typeof tag === 'object' ? tag.name : tag }}
        </span>
      </div>
    </div>



    <!-- 相关文章 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
      <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">相关文章</h3>
      <div v-if="relatedArticles.length > 0" class="space-y-4">
        <div v-for="article in relatedArticles" :key="article.id" class="group">
          <div class="cursor-pointer" @click="navigateToArticle(article.id)">
            <div class="relative mb-2 overflow-hidden rounded-lg aspect-[16/9] bg-gray-100 dark:bg-gray-700">
              <img
                v-if="article.cover_image && !article.cover_image.includes('undefined')"
                :src="article.cover_image"
                alt="文章封面"
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                @error="handleImageError($event)"
                loading="lazy"
              >
              <img
                v-else
                :src="getArticleImage(article)"
                alt="文章封面"
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                @error="handleImageError($event)"
                loading="lazy"
              >
              <div class="absolute inset-0 flex items-end p-2 bg-gradient-to-t from-black/70 to-transparent">
                <h4 class="text-white font-medium text-sm line-clamp-2 group-hover:text-secondary transition-colors duration-200">
                  {{ article.title }}
                </h4>
              </div>
            </div>
            <h4 class="font-medium text-gray-800 dark:text-gray-200 group-hover:text-secondary dark:group-hover:text-dark-secondary transition-colors duration-200 line-clamp-2">{{ article.title }}</h4>
            <div class="flex items-center justify-between mt-1">
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(article.created_at || article.date) }}</p>
              <span class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-2 py-0.5 rounded-full">
                {{ article.category?.name || article.category }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-6 text-gray-500 dark:text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-3 text-gray-300 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p>暂无相关文章</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '../../api'
import { format, parseISO } from 'date-fns'


export default {
  name: 'ArticleSidebar',

  props: {
    post: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const allPosts = ref([])
    const loading = ref(false)

    // 获取相关文章
    const relatedArticles = computed(() => {
      if (!props.post || allPosts.value.length === 0) return []

      // 获取当前文章的分类
      const currentCategory = props.post.category?.id || props.post.category_id ||
                             (typeof props.post.category === 'object' ? props.post.category.id : props.post.category)

      // 根据分类筛选相关文章
      return allPosts.value
        .filter(post => {
          // 获取文章分类
          const postCategory = post.category?.id || post.category_id ||
                              (typeof post.category === 'object' ? post.category.id : post.category)

          // 确保不显示当前文章
          return postCategory === currentCategory && post.id !== props.post.id
        })
        .slice(0, 3) // 最多显示3篇相关文章
    })

    // 获取文章图片
    const getArticleImage = (article) => {
      if (article.cover_image && !article.cover_image.includes('undefined')) return article.cover_image

      // 根据文章标题生成一个固定的图片索引
      const titleHash = article.title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      const imageIndex = (titleHash % 10) + 1 // 使用模10确保索引在1-10范围内

      return `/images/blog/post-${imageIndex}.jpg`
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(typeof dateString === 'string' ? parseISO(dateString) : new Date(dateString), 'yyyy-MM-dd')
      } catch (e) {
        return dateString
      }
    }

    // 获取角色名称
    const getRoleName = (role) => {
      const roleMap = {
        'admin': '管理员',
        'editor': '编辑',
        'user': '用户'
      }
      return roleMap[role] || '用户'
    }

    // 跳转到作者主页
    const navigateToAuthorProfile = (authorId) => {
      if (!authorId) return
      router.push(`/user/${authorId}`)
    }

    // 获取所有文章数据
    const fetchPosts = async () => {
      if (loading.value) return
      loading.value = true

      try {
        // 获取当前文章的分类
        const currentCategory = props.post.category?.id || props.post.category_id ||
                               (typeof props.post.category === 'object' ? props.post.category.id : props.post.category)

        // 如果有分类，按分类获取文章
        if (currentCategory) {
          allPosts.value = await postApi.getPosts({ category: currentCategory, limit: 10 })
        } else {
          allPosts.value = await postApi.getPosts({ limit: 10 })
        }
      } catch (error) {
        console.error('获取相关文章失败:', error)
        allPosts.value = []
      } finally {
        loading.value = false
      }
    }

    // 监听文章变化，重新获取相关文章
    watch(() => props.post.id, () => {
      fetchPosts()
    }, { immediate: true })

    // 图片错误处理
    const handleImageError = (event) => {
      event.target.src = '/images/default-thumbnail.jpg'
      event.target.onerror = null // 防止循环请求
    }

    // 导航到文章详情页
    const navigateToArticle = (articleId) => {
      if (!articleId) return

      // 使用router.push导航到文章详情页
      router.push(`/article/${articleId}`)

      // 导航后滚动到页面顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })

      // 可选：刷新页面以确保所有内容都重新加载
      // 如果使用这种方法，需要确保不会造成无限刷新循环
      if (router.currentRoute.value.params.id !== articleId.toString()) {
        // 只有当导航到不同的文章时才刷新
        setTimeout(() => {
          window.location.reload()
        }, 100)
      }
    }

    return {
      relatedArticles,
      getArticleImage,
      handleImageError,
      formatDate,
      getRoleName,
      navigateToAuthorProfile,
      navigateToArticle
    }
  }
}
</script>

<style scoped>
/* 添加16:9宽高比容器 */
.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%;
}

.aspect-h-9 {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* 作者卡片样式 */
.author-card {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.author-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(var(--color-secondary-rgb), 0.05), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.author-card:hover::before {
  opacity: 1;
}

/* 作者头像样式 */
.author-avatar {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.author-avatar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.author-avatar:hover::before {
  opacity: 1;
}

.author-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(var(--color-secondary-rgb), 0.3);
}

.author-avatar img {
  transition: transform 0.5s ease;
}

.author-avatar:hover img {
  transform: scale(1.15);
}
</style>
