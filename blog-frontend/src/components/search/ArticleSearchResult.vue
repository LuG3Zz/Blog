<template>
  <div class="article-search-result bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
    <div class="flex flex-col md:flex-row">
      <!-- 文章封面图 -->
      <div class="md:w-1/4 h-48 md:h-auto relative overflow-hidden bg-gray-100 dark:bg-gray-700">
        <img
          v-if="article.cover_image"
          :src="article.cover_image"
          :alt="article.title"
          class="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
          @error="handleImageError"
        />
        <div v-else class="w-full h-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>

      <!-- 文章内容 -->
      <div class="md:w-3/4 p-4 md:p-6 flex flex-col justify-between">
        <div class="flex items-center mb-2">
          <!-- 作者头像 -->
          <div v-if="article.author" class="flex-shrink-0 mr-3">
            <router-link :to="`/user/${article.author.id}`" class="block">
              <div class="author-avatar w-8 h-8 rounded-full overflow-hidden border border-gray-200 dark:border-gray-600 hover:border-secondary dark:hover:border-dark-secondary transition-all duration-300 shadow-sm">
                <template v-if="article.author.avatar">
                  <img
                    :src="article.author.avatar"
                    :alt="article.author.username"
                    class="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
                    @error="handleAvatarError"
                  />
                </template>
                <div
                  v-else
                  class="w-full h-full bg-gradient-to-br from-secondary to-blue-500 dark:from-dark-secondary dark:to-blue-700 text-primary dark:text-dark-primary flex items-center justify-center font-bold text-sm"
                >
                  {{ article.author.username.charAt(0).toUpperCase() }}
                </div>
              </div>
            </router-link>
          </div>

          <!-- 作者名称和日期 -->
          <div class="flex-grow">
            <router-link
              v-if="article.author"
              :to="`/user/${article.author.id}`"
              class="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-secondary dark:hover:text-dark-secondary"
            >
              {{ article.author.username }}
            </router-link>
            <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">
              {{ formatDate(article.created_at) }}
            </span>
          </div>

          <!-- 文章统计 -->
          <div class="flex items-center space-x-3 text-sm text-gray-500 dark:text-gray-400">
            <span class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              {{ article.view_count || 0 }}
            </span>
            <span class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              {{ article.like_count || 0 }}
            </span>
          </div>
        </div>

        <!-- 文章标题和摘要 -->
        <router-link :to="`/article/${article.id}`" class="block">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2 hover:text-secondary dark:hover:text-dark-secondary transition-colors">
            {{ article.title }}
          </h3>
          <p class="text-gray-600 dark:text-gray-300 mb-4 line-clamp-2">
            {{ article.excerpt || '暂无摘要' }}
          </p>
        </router-link>

        <!-- 分类和标签 -->
        <div class="flex flex-wrap items-center gap-2">
          <router-link
            v-if="article.category"
            :to="`/articles?category=${article.category.id}`"
            class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
          >
            {{ article.category.name }}
          </router-link>

          <router-link
            v-for="tag in article.tags_list"
            :key="tag.id"
            :to="`/articles?tag=${tag.name}`"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            #{{ tag.name }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { format, parseISO } from 'date-fns'

export default {
  name: 'ArticleSearchResult',
  props: {
    article: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    // 图片加载状态
    const imageLoaded = ref(false)
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(parseISO(dateString), 'yyyy-MM-dd')
      } catch (e) {
        console.error('日期格式化错误:', e)
        return dateString
      }
    }

    // 获取默认封面图
    const getDefaultCoverImage = () => {
      // 根据文章标题生成一个固定的图片索引
      const titleHash = props.article.title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      const imageIndex = (titleHash % 10) + 1 // 使用模10确保索引在1-10范围内

      return `/images/blog/post-${imageIndex}.jpg`
    }

    // 处理图片加载错误
    const handleImageError = (event) => {
      // 设置默认图片
      event.target.src = '/images/default-thumbnail.jpg'
      // 防止循环触发错误事件
      event.target.onerror = null
    }

    // 处理头像加载错误
    const handleAvatarError = (event) => {
      // 移除图片，显示默认头像
      const parent = event.target.parentNode
      if (parent) {
        parent.removeChild(event.target)
      }
    }

    return {
      formatDate,
      handleImageError,
      handleAvatarError,
      getDefaultCoverImage,
      imageLoaded
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 文章封面图样式 */
@media (min-width: 768px) {
  .article-search-result {
    height: 200px;
  }
}

/* 移动端样式调整 */
@media (max-width: 768px) {
  .article-search-result {
    height: auto;
  }
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
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.author-avatar img {
  transition: transform 0.5s ease;
}

.author-avatar:hover img {
  transform: scale(1.15);
}
</style>
