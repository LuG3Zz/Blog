<template>
  <div class="posts-container p-6 w-full dark:bg-gray-900">
    <p class="text-xl font-bold mb-4 dark:text-gray-100">{{ title }}</p>
    <div class="border-t-10 border-secondary dark:border-gray-600 w-full" ref="postsListRef">
      <TerminalLoader v-if="isLoading" />
      <div v-else-if="isLoading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-10 border-secondary dark:border-gray-500"></div>
      </div>
      <div v-else-if="error" class="text-red-500 dark:text-red-400 text-center py-8">
        {{ error }}
      </div>
      <div v-else-if="posts.length === 0" class="empty-state stack">
        <div class="card">
          <div class="card-content">
            <div class="empty-state-content">
              <svg xmlns="http://www.w3.org/2000/svg" class="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
              </svg>
              <h3 class="empty-state-title">暂无文章</h3>
              <p class="empty-state-description">当前分类下还没有任何文章</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="posts-grid">
        <div v-for="(post, index) in posts" :key="post.id" class="stack" :style="{ 'animation-delay': `${index * 0.1}s` }">
          <div class="card" :data-cover-image="post.cover_image || ''">
            <div class="card-content">
              <div class="post-header">
                <div class="title-background" :style="{ backgroundImage: post.cover_image ? `url(${post.cover_image})` : 'none' }">
                  <h2 @click="() => $router.push(`/article/${post.id}`)" class="post-title cursor-pointer hover:text-blue-500 dark:hover:text-blue-400">
                    {{ post.title }}
                  </h2>
                </div>
                <div class="post-category">{{ post.category?.name || '未分类' }}</div>
              </div>

              <div class="post-meta">
                <div class="author-info">
                  <div v-if="post.author" class="flex items-center gap-2">
                    <div class="author-avatar" :data-tooltip="`点击查看 ${post.author.username} 的资料`" @click="navigateToAuthorProfile(post.author.id)" style="cursor: pointer;">
                      <img v-if="post.author.avatar" :src="post.author.avatar" alt="作者头像" class="avatar-image" />
                      <div v-else class="avatar-placeholder">{{ post.author.username.charAt(0).toUpperCase() }}</div>
                    </div>
                    <div class="flex flex-col sm:flex-row sm:items-center">
                      <span class="author-name">{{ post.author.username }}</span>
                      <span class="hidden sm:inline mx-2 text-gray-300 dark:text-gray-600">•</span>
                      <span class="post-role text-xs text-gray-500 dark:text-gray-400">{{ post.author.role || '作者' }}</span>
                    </div>
                  </div>
                  <span class="post-date">{{ formatDate(post.created_at) }}</span>
                </div>

                <div class="post-stats">
                  <div class="stat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stat-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                    <span class="stat-value">{{ post.view_count }}</span>
                    <span class="stat-label">浏览</span>
                  </div>

                  <div class="stat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stat-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                    <span class="stat-value">{{ post.like_count }}</span>
                    <span class="stat-label">喜欢</span>
                  </div>

                  <div v-if="post.is_featured" class="featured-badge">精选</div>
                </div>
              </div>

              <div class="post-excerpt">
                <p>{{ post.excerpt || '暂无摘要' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="pagination">
          <button
            @click="loadPreviousPage"
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            上一页
          </button>
          <span class="page-indicator dark:text-gray-100">第 {{ currentPage }} 页</span>
          <button
            @click="loadNextPage"
            :disabled="!hasMorePosts"
            class="pagination-btn"
          >
            下一页
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="fixed bottom-4 right-4 w-64 h-64 z-50 pointer-events-none" ref="postPreviewRef"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { postApi } from '../../api'
import { usePostAnimation } from '../../hooks/usePostAnimation.js'
import { message } from '../../utils'
import { TerminalLoader } from '../ui'
import { useRouter } from 'vue-router'
// 导入 GSAP 库用于动画效果
import gsap from 'gsap'

export default {
  components: { TerminalLoader },
  name: 'PostsList',
  props: {
    selectedCategory: {
      type: String,
      default: ''
    },
    posts: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    // 使用路由导航到文章详情页和作者资料页
    const router = useRouter()
    const postsListRef = ref(null)
    const postPreviewRef = ref(null)
    const title = ref('精选文章')
    const posts = ref([])
    const isLoading = ref(false)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = 10
    const hasMorePosts = ref(true)

    // 使用动画hook
    const {
      // POSITIONS, // 不使用该变量
      addPostsEventListeners: addPostsEvents,
      setupMouseMoveListener,
      setupScrollListener
    } = usePostAnimation()

    let postsElements = []

    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }

    // 加载文章列表
    const loadPosts = async () => {
      if (!postsListRef.value) return

      isLoading.value = true
      error.value = null

      try {
        const skip = (currentPage.value - 1) * pageSize
        const response = await postApi.getPostsByCategory({
          category: props.selectedCategory,
          skip,
          limit: pageSize
        }).catch(err => {
          message.error('获取文章列表失败');
          throw err;
        })

        // 根据提供的数据格式，文章列表返回的是一个数组，每个元素包含：
        // id, title, slug, excerpt, cover_image, author, category, created_at, view_count, like_count, is_featured
        // author 是一个对象，包含 id, username, avatar
        // category 是一个对象，包含 id, name, description
        console.log('获取到的文章列表数据:', response);
        posts.value = response
        hasMorePosts.value = response.length === pageSize

        // 更新文章元素引用
        setTimeout(() => {
          postsElements = document.querySelectorAll('.post')
          addPostsEvents(postsElements, postPreviewRef.value)
        }, 100)
      } catch (err) {
        error.value = '加载文章失败'
        message.error(error.value)
      } finally {
        isLoading.value = false
      }
    }

    // 加载上一页
    const loadPreviousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        loadPosts()
      }
    }

    // 加载下一页
    const loadNextPage = () => {
      if (hasMorePosts.value) {
        currentPage.value++
        loadPosts()
      }
    }

    // 监听分类变化
    watch(() => props.selectedCategory, (newCategory) => {
      // 更新标题，如果有分类则显示分类名称，否则显示“所有文章”
      title.value = newCategory ? `${newCategory}分类文章` : '所有文章'
      // 切换分类时重置到第一页
      currentPage.value = 1
      // 重新加载文章
      loadPosts()
    }, { immediate: true }) // 添加 immediate: true 确保组件初始化时就执行一次

    // 监听传入的文章列表变化
    watch(() => props.posts, (newPosts) => {
      if (newPosts && newPosts.length > 0) {
        posts.value = newPosts
      }
    })

    onMounted(() => {
      // 如果有传入的文章列表，则使用传入的文章列表
      if (props.posts && props.posts.length > 0) {
        posts.value = props.posts
      } else {
        // 否则初始化文章列表
        loadPosts()
      }

      // 设置延时，确保DOM已经渲染
      setTimeout(() => {
        if (postsListRef.value && postPreviewRef.value) {
          // 获取所有文章卡片元素
          postsElements = postsListRef.value.querySelectorAll('.stack')

          // 为每个卡片添加鼠标悬浮事件，显示封面图片
          postsElements.forEach((post) => {
            post.addEventListener('mouseenter', () => {
              const card = post.querySelector('.card')
              const coverImage = card.dataset.coverImage

              // 如果有封面图片，则显示
              if (coverImage && coverImage !== '' && coverImage !== 'null' && coverImage !== 'undefined' && !coverImage.includes('undefined')) {
                // 创建图片元素
                const img = document.createElement('img')
                img.src = coverImage

                // 添加错误处理，如果图片加载失败，使用默认图片
                img.onerror = () => {
                  img.src = 'https://via.placeholder.com/400x300?text=暂无封面'
                }
                img.className = 'preview-image'
                img.style.position = 'absolute'
                img.style.top = '0'
                img.style.left = '0'
                img.style.width = '100%'
                img.style.height = '100%'
                img.style.objectFit = 'cover'
                img.style.borderRadius = '8px'
                img.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.2)'
                img.style.opacity = '0'
                img.style.transform = 'scale(0.8)'
                // 使用 GSAP 而不是 CSS 过渡
                // img.style.transition = 'opacity 0.3s ease, transform 0.3s ease'
                img.style.zIndex = '100' // 确保图片在最上层

                // 清除之前的图片
                while (postPreviewRef.value.firstChild) {
                  postPreviewRef.value.removeChild(postPreviewRef.value.firstChild)
                }

                // 添加新图片
                postPreviewRef.value.appendChild(img)

                // 更新图片位置跟随鼠标
                const updateImagePosition = (e) => {
                  // 计算鼠标位置，使图片跟随鼠标但保持在视口内
                  const mouseX = e.clientX
                  const mouseY = e.clientY
                  const viewportWidth = window.innerWidth
                  const viewportHeight = window.innerHeight
                  const imgWidth = postPreviewRef.value.offsetWidth
                  const imgHeight = postPreviewRef.value.offsetHeight

                  // 确保图片不会超出视口边界
                  let left = mouseX + 20 // 鼠标右侧20px
                  let top = mouseY - imgHeight / 2 // 鼠标垂直居中

                  if (left + imgWidth > viewportWidth) {
                    left = mouseX - imgWidth - 20 // 如果右侧空间不足，显示在鼠标左侧
                  }

                  if (top < 0) {
                    top = 10 // 顶部边界
                  } else if (top + imgHeight > viewportHeight) {
                    top = viewportHeight - imgHeight - 10 // 底部边界
                  }

                  postPreviewRef.value.style.left = `${left}px`
                  postPreviewRef.value.style.top = `${top}px`
                  postPreviewRef.value.style.transform = 'none' // 移除任何变换
                }

                // 添加鼠标移动事件监听器
                document.addEventListener('mousemove', updateImagePosition)

                // 存储事件监听器引用，以便之后移除
                post._mouseMoveListener = updateImagePosition

                // 使用 GSAP 显示图片
                gsap.to(img, {
                  opacity: 1,
                  scale: 1,
                  duration: 0.3,
                  ease: 'power2.out'
                })
              }
            })

            post.addEventListener('mouseleave', () => {
              // 使用 GSAP 隐藏图片
              const previewImages = postPreviewRef.value.querySelectorAll('img')
              previewImages.forEach(img => {
                gsap.to(img, {
                  opacity: 0,
                  scale: 0.8,
                  duration: 0.3,
                  ease: 'power2.out',
                  onComplete: () => {
                    if (img.parentNode === postPreviewRef.value) {
                      postPreviewRef.value.removeChild(img)
                    }
                  }
                })
              })

              // 移除鼠标移动事件监听器
              if (post._mouseMoveListener) {
                document.removeEventListener('mousemove', post._mouseMoveListener)
                post._mouseMoveListener = null
              }
            })
          })

          // 设置鼠标移动和滚动事件监听
          setupMouseMoveListener(postsListRef.value, postPreviewRef.value)
          setupScrollListener(postsListRef.value, postPreviewRef.value, postsElements)
        }
      }, 500)
    })

    // 导航到作者资料页
    const navigateToAuthorProfile = (authorId) => {
      if (!authorId) {
        message.warning('无法获取作者信息')
        return
      }
      router.push(`/user/${authorId}`)
    }

    return {
      postsListRef,
      postPreviewRef,
      title,
      posts,
      isLoading,
      error,
      currentPage,
      hasMorePosts,
      loadPreviousPage,
      loadNextPage,
      formatDate,
      navigateToAuthorProfile
    }
  }
}
</script>

<style scoped>
.posts-container {
  margin: 0 auto;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

@media (max-width: 640px) {
  .posts-grid {
    grid-template-columns: 1fr;
  }
}

.stack {
  width: 100%;
  transition: 0.25s ease;
  margin: 0 auto;
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.stack:hover {
  transform: rotate(3deg);
}

.stack:hover .card:before {
  transform: translatey(-2%) rotate(-3deg);
}

.stack:hover .card:after {
  transform: translatey(2%) rotate(3deg);
}

.card {
  border: 4px solid;
  background-color: #fff;
  position: relative;
  transition: 0.15s ease;
  cursor: pointer;
  padding: 1rem;
  height: 100%;
}

.dark .card {
  background-color: #1f2937;
  border-color: #374151;
}

.card:before,
.card:after {
  content: "";
  display: block;
  position: absolute;
  height: 100%;
  width: 100%;
  border: 4px solid;
  background-color: #fff;
  transform-origin: center center;
  z-index: -1;
  transition: 0.15s ease;
  top: 0;
  left: 0;
}

.dark .card:before,
.dark .card:after {
  background-color: #1f2937;
  border-color: #374151;
}

.card:before {
  transform: translatey(-2%) rotate(-4deg);
}

.card:after {
  transform: translatey(2%) rotate(4deg);
}

.card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.post-header {
  margin-bottom: 1rem;
}

.title-background {
  background-color: #f3f4f6;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  overflow: hidden;
}

.title-background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.5));
  z-index: 1;
}

.post-title {
  position: relative;
  background-color: transparent;
  z-index: 1;
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.dark .title-background {
  background-color: transparent;
  border-color: #4b5563;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.dark .title-background::before {
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8));
}

.dark .post-title {
  color: #ffffff;
}

.post-category {
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
}

.dark .post-category {
  color: #9ca3af;
}

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px dashed #e5e7eb;
  margin-bottom: 0.5rem;
}

.dark .author-info {
  border-bottom-color: #374151;
}

.author-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.author-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.dark .author-avatar {
  border-color: #4b5563;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark .author-avatar:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.author-avatar:hover .avatar-image {
  transform: scale(1.1);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.dark .avatar-placeholder {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
}

.author-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4b5563;
  transition: color 0.2s ease;
  position: relative;
  padding-bottom: 2px;
}

.author-name:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #6366f1;
  transition: width 0.3s ease;
}

.author-avatar:hover + .author-name:after,
.author-name:hover:after {
  width: 100%;
}

.author-name:hover {
  color: #6366f1;
}

.dark .author-name {
  color: #d1d5db;
}

.dark .author-name:after {
  background-color: #8b5cf6;
}

.dark .author-name:hover {
  color: #8b5cf6;
}

.post-date {
  font-size: 0.75rem;
  color: #6b7280;
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  display: inline-flex;
  align-items: center;
  transition: background-color 0.2s ease;
}

.post-date:before {
  content: '\1F4C5'; /* 日历图标 */
  margin-right: 0.25rem;
  font-size: 0.875rem;
}

.post-date:hover {
  background-color: #e5e7eb;
}

.dark .post-date {
  color: #9ca3af;
  background-color: #374151;
}

.dark .post-date:hover {
  background-color: #4b5563;
}

.post-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #4b5563;
  margin-bottom: 0.25rem;
}

.dark .stat-icon {
  color: #9ca3af;
}

.stat-value {
  font-size: 1rem;
  font-weight: bold;
  color: #2c3e50;
}

.dark .stat-value {
  color: #e5e7eb;
}

.stat-label {
  font-size: 0.625rem;
  color: #6b7280;
}

.dark .stat-label {
  color: #9ca3af;
}

.empty-state {
  width: 100%;
  max-width: 400px;
  margin: 2rem auto;
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

.empty-state-icon {
  width: 4rem;
  height: 4rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.dark .empty-state-icon {
  color: #9ca3af;
}

.empty-state-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.dark .empty-state-title {
  color: #e5e7eb;
}

.empty-state-description {
  font-size: 1rem;
  color: #6b7280;
  line-height: 1.5;
}

.dark .empty-state-description {
  color: #9ca3af;
}

.featured-badge {
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  background-color: #f59e0b;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.post-excerpt {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.dark .post-excerpt {
  border-top: 1px solid #374151;
}

.post-excerpt p {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.5;
}

.dark .post-excerpt p {
  color: #9ca3af;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding: 1rem;
  border: 4px solid;
  background-color: #fff;
  position: relative;
  grid-column: 1 / -1;
}

.dark .pagination {
  background-color: #1f2937;
  border-color: #374151;
}

.pagination:before,
.pagination:after {
  content: "";
  display: block;
  position: absolute;
  height: 100%;
  width: 100%;
  border: 4px solid;
  background-color: #fff;
  transform-origin: center center;
  z-index: -1;
  transition: 0.15s ease;
  top: 0;
  left: 0;
}

.dark .pagination:before,
.dark .pagination:after {
  background-color: #1f2937;
  border-color: #374151;
}

.pagination:before {
  transform: translatey(-2%) rotate(-2deg);
}

.pagination:after {
  transform: translatey(2%) rotate(2deg);
}

.pagination-btn {
  padding: 0.5rem 1rem;
  background-color: #2c3e50;
  color: white;
  border: 2px solid #2c3e50;
  border-radius: 0.25rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #1e293b;
  transform: translateY(-2px);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dark .pagination-btn {
  background-color: #4b5563;
  border-color: #4b5563;
}

.dark .pagination-btn:hover:not(:disabled) {
  background-color: #374151;
}

.page-indicator {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
}

.dark .page-indicator {
  color: #d1d5db;
}
/* 作者角色样式 */
.post-role {
  font-size: 0.7rem;
  font-style: italic;
  transition: color 0.2s ease;
}

/* 头像悬停提示 */
.author-avatar {
  position: relative;
}

.author-avatar:before {
  content: attr(data-tooltip);
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%) scale(0.8);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  pointer-events: none;
  z-index: 10;
}

.author-avatar:hover:before {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) scale(1);
  bottom: -25px;
}

/* 响应式调整 */
@media (max-width: 640px) {
  .author-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .post-date {
    align-self: flex-end;
  }
}
</style>
