<template>
  <div class="min-h-screen flex flex-col overflow-hidden bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <ScrollIsland v-if="post" title="Reading Progress" :headings="articleHeadings" class="animate__animated animate__fadeInRight animate__delay-1s">
      <!-- 添加调试信息 -->
      <div v-if="articleHeadings.length === 0" class="text-xs text-red-500">没有标题列表</div>
    </ScrollIsland>
    <div class="container mx-auto px-4 py-8">
      <!-- 返回按钮 - 固定在左侧 -->
      <button
        @click="goBack"
        class="fixed left-4 top-20 z-40 flex items-center bg-white dark:bg-gray-800 text-secondary dark:text-dark-secondary hover:bg-gray-100 dark:hover:bg-gray-700 px-3 py-2 rounded-lg shadow-md transition-all duration-300 animate__animated animate__fadeInLeft animate__delay-1s"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
        返回
      </button>

      <!-- 面包屑导航 -->
      <Breadcrumb v-if="post" :category="post.category" :title="post.title" class="animate__animated animate__fadeInDown animate__delay-1s" />

      <!-- 文章头部 -->
      <div v-if="post" class="mb-8 animate__animated animate__fadeIn animate__delay-1s">
        <div class="relative rounded-lg overflow-hidden">
          <div class="w-full h-48 md:h-64 lg:h-96 bg-gray-300 dark:bg-gray-700 overflow-hidden relative aspect-video">
            <img
              :src="getPostImage()"
              alt="文章封面"
              class="w-full h-full object-cover md:object-contain lg:object-cover object-center"
            >
            <!-- AI总结组件 -->
            <AiSummary :summary="generateAiSummary()" />
          </div>
          <div class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/70 to-transparent p-6">
            <div class="px-2 py-1 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary text-sm font-medium rounded-md inline-block mb-2">
              {{ post.category }}
            </div>
            <div v-if="getPostTags().length > 0" class="flex flex-wrap gap-2 mt-2">
              <span v-for="tag in getPostTags()" :key="tag" class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-xs">
                {{ tag }}
              </span>
            </div>
            <div class="flex items-center justify-between mb-2 animate__animated animate__fadeInUp animate__delay-1s">
              <h1 class="text-3xl font-bold text-white">{{ post.title }}</h1>
              <!-- 编辑按钮 - 只有有权限的用户才能看到 -->
              <button
                v-if="canEditArticle"
                @click="editArticle"
                class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-md shadow-md transition-all duration-300 flex items-center gap-1 transform hover:scale-105"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                编辑文章
              </button>
            </div>
            <div class="flex items-center gap-2 mb-2 animate__animated animate__fadeInUp animate__delay-1s">
              <!-- 作者头像 -->
              <div
                @click="navigateToAuthorProfile(post.author?.id)"
                class="w-10 h-10 rounded-full overflow-hidden border-2 border-white cursor-pointer hover:border-secondary transition-all duration-300 transform hover:scale-105 shadow-md author-avatar"
              >
                <img
                  v-if="post.author?.avatar"
                  :src="post.author.avatar"
                  :alt="post.author?.username || '作者头像'"
                  class="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
                />
                <div
                  v-else
                  class="w-full h-full bg-gradient-to-br from-secondary to-blue-500 text-primary flex items-center justify-center font-bold text-sm"
                >
                  {{ (post.author?.username || 'A').charAt(0).toUpperCase() }}
                </div>
              </div>
              <!-- 作者信息 -->
              <div>
                <div class="flex items-center">
                  <p
                    @click="navigateToAuthorProfile(post.author?.id)"
                    class="text-white font-medium cursor-pointer hover:text-secondary transition-colors"
                  >
                    {{ post.author?.username || '匿名作者' }}
                  </p>
                  <span
                    v-if="post.author?.role"
                    class="ml-2 px-1.5 py-0.5 text-xs rounded-full bg-black bg-opacity-30 border border-white border-opacity-30"
                  >
                    {{ getRoleName(post.author?.role) }}
                  </span>
                </div>
                <p class="text-gray-200 text-xs flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ post.date }}
                </p>
              </div>
            </div>
            <div class="flex items-center gap-4 mt-2 text-gray-200 text-sm animate__animated animate__fadeInUp animate__delay-1s">
              <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                {{ post.view_count }} 浏览
              </span>
              <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ readingTime }} 分钟阅读
              </span>
              <button
                @click="handleLike"
                class="flex items-center hover:text-red-500 transition-colors duration-300 animate__animated"
                :class="{ 'text-red-500': isLiked, 'animate__rubberBand': isLiked }"
              >
                <svg xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 mr-1 transition-transform duration-300"
                  :class="{ 'scale-125': isLiked }"
                  :fill="isLiked ? 'currentColor' : 'none'"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
                {{ post.like_count }} 点赞
              </button>
              <span v-if="post.is_featured" class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="#FFD700" viewBox="0 0 24 24" stroke="#F59E0B">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                </svg>
                <span class="text-yellow-500 dark:text-yellow-400 font-medium">精选</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 三栏布局：文章内容 + 侧边栏 -->
      <div v-if="post" class="flex flex-col lg:flex-row gap-6 animate__animated animate__fadeIn animate__delay-2s">
        <!-- 左侧：文章目录 -->
        <div class="lg:w-1/5 order-3 lg:order-1 animate__animated animate__fadeInLeft animate__delay-2s">
          <ArticleToc :content="renderedContent" />
        </div>

        <!-- 中间：文章主体 -->
        <div class="lg:w-3/5 order-1 lg:order-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden animate__animated animate__fadeInUp animate__delay-2s">
          <div class="p-6">
            <p class="text-xl text-gray-700 dark:text-gray-300 font-medium mb-6">{{ post.summary }}</p>

            <!-- Markdown渲染的文章内容 -->
            <div class="prose prose-lg max-w-none dark:prose-invert text-gray-800 dark:text-gray-200 article-content markdown-body animate__animated animate__fadeIn animate__delay-2s" v-html="renderedContent">
</div>

            <!-- 文章底部信息 -->
            <div class="mt-10 pt-6 border-t border-gray-200 dark:border-gray-700">
              <!-- 作者信息卡片 -->
              <div v-if="post.author" class="mb-6 p-6 bg-gray-50 dark:bg-gray-700 rounded-lg shadow-md border border-gray-100 dark:border-gray-600 flex flex-col md:flex-row items-center md:items-start gap-4 author-card animate__animated animate__fadeIn animate__delay-3s">
                <div
                  @click="navigateToAuthorProfile(post.author.id)"
                  class="w-24 h-24 rounded-full overflow-hidden border-3 border-gray-200 dark:border-gray-600 cursor-pointer hover:border-secondary dark:hover:border-dark-secondary transition-all duration-300 transform hover:scale-105 shadow-lg author-avatar"
                >
                  <img
                    v-if="post.author.avatar && !post.author.avatar.includes('undefined')"
                    :src="post.author.avatar"
                    :alt="post.author.username"
                    class="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                    @error="handleImageError"
                  />
                  <div
                    v-else
                    class="w-full h-full bg-gradient-to-br from-secondary to-blue-500 dark:from-dark-secondary dark:to-blue-700 text-primary dark:text-dark-primary flex items-center justify-center font-bold text-3xl"
                  >
                    {{ post.author.username.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <div class="flex-1 md:ml-4">
                  <div class="flex flex-wrap items-center gap-2 mb-2">
                    <h3
                      @click="navigateToAuthorProfile(post.author.id)"
                      class="text-xl font-bold text-gray-800 dark:text-gray-200 hover:text-secondary dark:hover:text-dark-secondary cursor-pointer transition-colors"
                    >
                      {{ post.author.username }}
                    </h3>
                    <span
                      v-if="post.author.role"
                      class="px-2 py-0.5 text-xs rounded-full"
                      :class="{
                        'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': post.author.role === 'admin',
                        'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': post.author.role === 'editor',
                        'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': post.author.role === 'user'
                      }"
                    >
                      {{ getRoleName(post.author.role) }}
                    </span>
                  </div>
                  <p v-if="post.author.bio" class="text-gray-600 dark:text-gray-400 mt-2 mb-3 text-sm leading-relaxed max-w-2xl">{{ post.author.bio }}</p>

                  <!-- 作者统计信息 -->
                  <div class="flex flex-wrap gap-4 mb-3 text-sm text-gray-500 dark:text-gray-400">
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      文章数：{{ post.author.article_count || 0 }}
                    </div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                      </svg>
                      评论数：{{ post.author.comment_count || 0 }}
                    </div>
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      加入时间：{{ formatDate(post.author.created_at) }}
                    </div>
                  </div>

                </div>
              </div>

              <!-- 文章底部信息和操作按钮 -->
              <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-4">
                <div class="flex items-center">
                  <span class="text-gray-600 dark:text-gray-400">分类：</span>
                  <span class="ml-2 px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-sm">
                    {{ post.category }}
                  </span>
                </div>
                <div class="text-gray-600 dark:text-gray-400">
                  发布日期：{{ post.date }}
                </div>
              </div>

              <!-- 分享和下载按钮 -->
              <div class="flex flex-wrap items-center gap-3 mt-6 mb-2 animate__animated animate__fadeIn animate__delay-3s">
                <!-- 分享按钮 -->
                <button
                  @click="shareArticle"
                  class="flex items-center gap-2 px-4 py-2 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-800/40 transition-colors duration-300"
                  title="分享文章"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                  分享文章
                </button>

                <!-- 下载MD按钮 -->
                <button
                  @click="downloadMarkdown"
                  class="flex items-center gap-2 px-4 py-2 bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-300 rounded-lg hover:bg-green-100 dark:hover:bg-green-800/40 transition-colors duration-300"
                  title="下载Markdown文件"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  下载Markdown
                </button>
              </div>

              <!-- 订阅表单 -->
              <div class="mt-8 animate__animated animate__fadeIn animate__delay-3s">
                <SubscriptionForm
                  v-if="post && post.author"
                  type="author"
                  :reference-id="post.author.id"
                  :reference-name="post.author.username"
                />
              </div>
            </div>

            <!-- 评论区分隔 -->
            <div class="my-12 border-t-2 border-gray-100 dark:border-gray-700"></div>

            <!-- 评论区 -->
            <CommentSection :post-id="post.id" class="animate__animated animate__fadeIn animate__delay-3s" />
          </div>
        </div>

        <!-- 右侧：作者信息和相关文章 -->
        <div class="lg:w-1/5 order-2 lg:order-3 animate__animated animate__fadeInRight animate__delay-2s">
          <ArticleSidebar :post="post" />
        </div>
      </div>

      <!-- 加载中状态 -->
      <div v-else-if="loading" class="flex justify-center items-center h-64 animate__animated animate__fadeIn">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary dark:border-dark-secondary"></div>
      </div>

      <!-- 文章不存在 -->
      <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 text-center animate__animated animate__fadeIn animate__delay-1s">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-300 mt-4">文章不存在或已被删除</h2>
        <button
          @click="goBack"
          class="mt-4 px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-lg hover:bg-gray-800 dark:hover:bg-gray-300 transition-colors duration-300"
        >
          返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi, usersApi } from '@/api'
import { CommentSection, ArticleToc, ArticleSidebar, AiSummary } from '@/components/blog'
import { Breadcrumb, ScrollIsland, CodeBlock } from '@/components/ui'
import SubscriptionForm from '@/components/blog/SubscriptionForm.vue'
import 'katex/dist/katex.min.css' // 导入 KaTeX 样式
import { useUserStore } from '@/stores'
import { isAdmin, hasRole } from '@/utils/permission'
import message from '@/utils/message'


// 导入组合式函数
import {
  useMarkdownRenderer,
  useArticleHeadings,
  useCodeBlockProcessor,
  useArticleLike,
  useArticleData,
  useDomObserver,
  useNavigation
} from '@/composables'

export default {
  name: 'ArticleDetail',
  components: {
    CommentSection,
    ArticleToc,
    ArticleSidebar,
    AiSummary,
    Breadcrumb,
    ScrollIsland,
    SubscriptionForm
  },
  setup() {
    const route = useRoute()
    const router = useRouter()

    // 添加取消标记
    const isComponentMounted = ref(true)

    // 使用Markdown渲染器
    const { renderMarkdown, calculateReadingTime } = useMarkdownRenderer()

    // 获取用户状态
    const userStore = useUserStore()

    // 判断当前用户是否有权限编辑文章
    const canEditArticle = computed(() => {
      // 检查用户是否已登录
      if (!userStore.isLoggedIn || !userStore.userInfo) {
        return false
      }

      const currentUser = userStore.userInfo

      // 如果用户是管理员或编辑，可以编辑任何文章
      if (isAdmin(currentUser) || hasRole(currentUser, ['editor'])) {
        return true
      }

      // 如果用户是文章作者，也可以编辑
      if (post.value && post.value.author_id === currentUser.id) {
        return true
      }

      return false
    })

    // 使用文章数据
    const {
      post,
      loading,
      markdownContent,
      readingTime,
      getPostImage,
      getPostTags,
      getRoleName,
      formatDate,
      fetchPost,
      generateAiSummary
    } = useArticleData({
      postApi,
      usersApi,
      isComponentMounted,
      calculateReadingTime
    })

    // 使用文章标题和目录
    const {
      articleHeadings,
      extractArticleHeadings,
      setupHeadingClickHandlers
    } = useArticleHeadings()

    // 使用代码块处理器
    const { processCodeBlocks } = useCodeBlockProcessor({
      CodeBlock,
      isComponentMounted
    })

    // 使用文章点赞
    const {
      isLiked,
      fetchLikeStatus,
      handleLike
    } = useArticleLike({
      postApi,
      isComponentMounted
    })

    // 使用导航
    const {
      goBack,
      navigateToAuthorProfile
    } = useNavigation()

    // 使用DOM观察器
    const { setupObserver } = useDomObserver({
      isComponentMounted,
      setupHeadingClickHandlers,
      processCodeBlocks,
      extractArticleHeadings
    })


    // 渲染Markdown内容的计算属性
    const renderedContent = computed(() => {
      if (!markdownContent.value) return ''
      return renderMarkdown(markdownContent.value)
    })

    onMounted(async () => {
      isComponentMounted.value = true

      // 获取文章数据
      await fetchPost(route.params.id)

      // 只有在组件仍然挂载时才继续执行
      if (isComponentMounted.value) {
        // 获取点赞状态
        await fetchLikeStatus(post.value.id)
      }

      // 内容加载后设置标题点击处理器
      setupHeadingClickHandlers()

      // 处理代码块
      processCodeBlocks()

      // 提取文章标题
      // 使用多次尝试，确保标题元素已经渲染
      setTimeout(() => {
        if (isComponentMounted.value) {
          extractArticleHeadings()

          // 再次尝试，以确保标题元素已经渲染
          setTimeout(() => {
            if (isComponentMounted.value && articleHeadings.value.length === 0) {
              extractArticleHeadings()
            }
          }, 500)
        }
      }, 500) // 延迟执行，确保标题元素已经渲染

      // 设置Dom观察器
      setupObserver()
    })

    // 添加组件卸载钩子
    onUnmounted(() => {
      console.log('组件卸载，清理资源')

      // 设置挂载状态为 false
      isComponentMounted.value = false

      // 清理标题相关资源
      cleanup()
    })

    // 处理文章点赞的包装函数
    const handleArticleLike = () => {
      if (post.value) {
        handleLike(post.value)
      }
    }

    // 跳转到编辑页面
    const editArticle = () => {
      if (post.value && post.value.id) {
        router.push({
          path: '/admin/articles/edit',
          query: { id: post.value.id }
        })
      }
    }

    // 分享文章
    const shareArticle = () => {
      if (!post.value) return

      try {
        // 获取当前页面URL
        const url = window.location.href

        // 尝试使用现代API复制到剪贴板
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(() => {
            message.success('文章链接已复制到剪贴板')
          }).catch(err => {
            console.error('复制失败:', err)
            // 回退到传统方法
            fallbackCopyToClipboard(url)
          })
        } else {
          // 回退到传统方法
          fallbackCopyToClipboard(url)
        }
      } catch (error) {
        console.error('分享文章失败:', error)
        message.error('分享失败，请手动复制链接')
      }
    }

    // 传统的复制到剪贴板方法
    const fallbackCopyToClipboard = (text) => {
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()

      try {
        const successful = document.execCommand('copy')
        if (successful) {
          message.success('文章链接已复制到剪贴板')
        } else {
          message.error('复制失败，请手动复制链接')
        }
      } catch (err) {
        console.error('复制失败:', err)
        message.error('复制失败，请手动复制链接')
      }

      document.body.removeChild(textArea)
    }

    // 下载Markdown文件
    const downloadMarkdown = () => {
      if (!post.value || !markdownContent.value) return

      try {
        // 创建文件内容
        let mdContent = `# ${post.value.title}\n\n`

        // 添加文章元数据
        mdContent += `> 作者: ${post.value.author?.username || '匿名作者'}\n`
        mdContent += `> 分类: ${post.value.category || '未分类'}\n`
        mdContent += `> 发布时间: ${post.value.date}\n`

        // 添加标签
        const tags = getPostTags()
        if (tags.length > 0) {
          mdContent += `> 标签: ${tags.join(', ')}\n`
        }

        mdContent += '\n---\n\n'

        // 添加文章摘要
        if (post.value.excerpt) {
          mdContent += `**摘要**: ${post.value.excerpt}\n\n---\n\n`
        }

        // 添加文章正文内容
        mdContent += markdownContent.value

        // 添加文章来源
        mdContent += `\n\n---\n\n> 本文来自: [${window.location.hostname}](${window.location.href})`

        // 创建Blob对象
        const blob = new Blob([mdContent], { type: 'text/markdown;charset=utf-8' })

        // 创建下载链接
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url

        // 设置文件名 - 使用文章标题，并移除不合法的文件名字符
        const fileName = `${post.value.title.replace(/[\\/:*?"<>|]/g, '_')}.md`
        link.download = fileName

        // 触发下载
        document.body.appendChild(link)
        link.click()

        // 清理
        document.body.removeChild(link)
        URL.revokeObjectURL(url)

        message.success('Markdown文件下载成功')
      } catch (error) {
        console.error('下载Markdown文件失败:', error)
        message.error('下载失败，请稍后重试')
      }
    }

    return {
      post,
      loading,
      markdownContent,
      renderedContent,
      getPostImage,
      getPostTags,
      goBack,
      generateAiSummary,
      readingTime,
      handleLike: handleArticleLike,
      isLiked,
      getRoleName,
      navigateToAuthorProfile,
      formatDate,
      articleHeadings,
      canEditArticle,
      editArticle,
      shareArticle,
      downloadMarkdown
    }
  }
}
</script>

<style>
:root {
  --color-secondary-rgb: 59, 130, 246; /* 蓝色的RGB值 */
  --color-secondary: #3b82f6;
}

/* 强制覆盖KaTeX样式 */
.article-content .katex-html .base {
  position: relative !important;
}

/* 标题高亮效果 */
.heading-highlight {
  position: relative;
  animation: headingHighlight 2s ease;
}

.dark .heading-highlight {
  animation: darkHeadingHighlight 2s ease;
}

@keyframes headingHighlight {
  0% {
    background-color: rgba(var(--color-secondary-rgb), 0.2);
    padding-left: 8px;
    border-left: 3px solid var(--color-secondary);
  }
  70% {
    background-color: rgba(var(--color-secondary-rgb), 0.1);
    padding-left: 8px;
    border-left: 3px solid var(--color-secondary);
  }
  100% {
    background-color: transparent;
    padding-left: 0;
    border-left: none;
  }
}

/* 暗黑模式下的标题高亮动画 */
@keyframes darkHeadingHighlight {
  0% {
    background-color: rgba(96, 165, 250, 0.25);
    padding-left: 8px;
    border-left: 3px solid var(--color-dark-secondary, #60a5fa);
    box-shadow: 0 0 15px rgba(96, 165, 250, 0.2);
  }
  70% {
    background-color: rgba(96, 165, 250, 0.15);
    padding-left: 8px;
    border-left: 3px solid var(--color-dark-secondary, #60a5fa);
    box-shadow: 0 0 10px rgba(96, 165, 250, 0.1);
  }
  100% {
    background-color: transparent;
    padding-left: 0;
    border-left: none;
    box-shadow: none;
  }
}

/* 确保标题有足够的上边距，避免被导航栏遮挡 */
.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
  scroll-margin-top: 80px;
  padding-top: 0.5rem;
}

/* 文章内容容器样式 */
.article-content {
  line-height: 1.8;
  font-size: 1.1rem;
}

/* 暗黑模式下的文章内容容器样式 */
.dark .article-content {
  color: #e2e8f0; /* 使用浅色文本，提高可读性 */
  letter-spacing: 0.01em; /* 增加字间距，提高可读性 */
}

/* 暗黑模式下的文章内容链接样式 */
.dark .article-content a {
  color: var(--color-dark-secondary, #60a5fa);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
  transition: all 0.2s ease;
}

.dark .article-content a:hover {
  color: #93c5fd; /* 浅蓝色，悬停时更亮 */
  text-decoration-thickness: 2px;
  text-shadow: 0 0 8px rgba(147, 197, 253, 0.3);
}

/* 代码块包装器样式 */
.code-block-wrapper {
  margin: 1.5rem 0;
  overflow: hidden;
}

/* 暗黑模式下的代码块样式 */
.dark .article-content .code-block-container {
  background-color: #282c34 !important;
  border: 1px solid #4b5563 !important;
}

/* 确保文章内容中的代码块正确显示 */
.prose pre {
  margin: 0 !important;
  padding: 0 !important;
  overflow: visible !important;
  background-color: transparent !important;
}

.prose .code-block-wrapper pre {
  border-radius: 0 !important;
}

/* 文章内容中的代码块容器 */
.prose .code-block-container {
  display: flex;
  overflow-x: auto;
  border: 1px solid #e5e7eb;
}

.dark .prose .code-block-container {
  border: 1px solid #4b5563;
}

/* 确保行号正确显示 */
.prose .line-numbers-wrapper {
  padding: 0.5rem 0;
  display: flex;
  align-items: stretch;
}

.prose .line-numbers {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  padding: 0.5rem 0.5rem;
}

.prose .line-number {
  display: flex;
  align-items: flex-start; /* 与代码对齐上边缘 */
  justify-content: flex-end; /* 右对齐 */
  height: 1.5rem;
  min-width: 2rem;
  user-select: none;
  padding: 0;
  margin: 0;
  line-height: 1.5;
}

/* 确保代码行高与行号行高一致 */
.prose .code-wrapper {
  display: flex;
  align-items: stretch;
}

.prose .code-wrapper pre {
  padding: 0.5rem;
  margin: 0;
  width: 100%;
}

.prose pre code {
  display: block;
  line-height: 1.5;
  padding: 0;
  margin: 0;
}

/* 确保代码内容中的每一行与行号对齐 */
.prose .hljs-line {
  display: flex;
  align-items: flex-start; /* 与行号对齐上边缘 */
  min-height: 1.5rem;
  line-height: 1.5;
}

/* 如果没有行元素，确保行高一致 */
.prose pre code span {
  line-height: 1.5;
}

/* 暗黑模式下的行内代码样式 */
.dark .article-content code:not(pre code) {
  background-color: #334155 !important; /* 深蓝色背景，增强对比度 */
  color: #e2e8f0 !important; /* 浅色文本，提高可读性 */
  padding: 0.2em 0.4em !important;
  border-radius: 0.25rem !important;
  font-weight: 500 !important;
  font-size: 0.9em !important;
}

/* 暗黑模式下的引用块样式 */
.dark .article-content blockquote {
  background-color: #1e293b !important; /* 深蓝色背景，增强对比度 */
  border-left: 4px solid var(--color-dark-secondary, #60a5fa) !important; /* 使用暗色主题的强调色 */
  color: #e2e8f0 !important; /* 浅色文本，提高可读性 */
  padding: 1em 1.5em !important;
  margin: 1.5em 0 !important;
  border-radius: 0 0.25rem 0.25rem 0 !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important; /* 添加阴影，增强立体感 */
  font-style: italic !important;
}

/* 暗黑模式下的引用块内文本样式 */
.dark .article-content blockquote p {
  color: #cbd5e1 !important; /* 浅色文本，提高可读性 */
  line-height: 1.7 !important;
}

/* 暗黑模式下的表格样式 */
.dark .article-content table {
  border-collapse: separate !important;
  border-spacing: 0 !important;
  border-radius: 0.5rem !important;
  overflow: hidden !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1) !important;
  margin: 2em 0 !important;
  border: 1px solid #334155 !important;
}

/* 暗黑模式下的表头样式 */
.dark .article-content thead {
  background-color: #1e293b !important; /* 深蓝色背景，增强对比度 */
}

.dark .article-content th {
  color: #e2e8f0 !important; /* 浅色文本，提高可读性 */
  font-weight: 600 !important;
  padding: 0.75em 1em !important;
  border-bottom: 2px solid #334155 !important;
  text-align: left !important;
}

/* 暗黑模式下的表格单元格样式 */
.dark .article-content td {
  padding: 0.75em 1em !important;
  border-bottom: 1px solid #334155 !important;
  color: #cbd5e1 !important; /* 浅色文本，提高可读性 */
}

/* 暗黑模式下的表格行悬停效果 */
.dark .article-content tbody tr:hover {
  background-color: rgba(96, 165, 250, 0.05) !important; /* 使用暗色主题的强调色，非常淡 */
  transition: background-color 0.2s ease !important;
}

/* 数学公式容器样式增强 */
.article-content .katex-display {
  margin: 1.5em 0 !important;
  overflow-x: auto !important;
}

/* 确保数学公式在暗黑模式下可见 */
.dark .article-content .katex {
  color: #e2e8f0 !important;
}

/* 直接在组件中添加上下标样式 - 根据实际DOM结构调整 */
.article-content .katex-html .vlist > span.reset-textstyle.scriptstyle {
  font-size: 0.75em !important;
  position: relative !important;
  top: -0.5em !important;
  color: #3b82f6 !important;
}

.article-content .katex-html .vlist > span.reset-textstyle.scriptstyle.cramped {
  font-size: 0.75em !important;
  position: relative !important;
  top: 0.3em !important;
  color: #3b82f6 !important;
}

/* 调整strut元素 */
.article-content .katex-html .strut {
  display: inline-block !important;
}

.article-content .katex-html .strut.bottom {
  vertical-align: -0.25em !important;
}

/* 调整fontsize-ensurer */
.article-content .katex-html .fontsize-ensurer {
  display: inline-block !important;
}

/* 调整baseline-fix */
.article-content .katex-html .baseline-fix {
  display: inline-block !important;
  position: relative !important;
}

/* 添加更多特定的选择器，确保样式能够应用 */
.article-content span.katex-html .vlist span.reset-textstyle.scriptstyle {
  font-size: 0.75em !important;
  position: relative !important;
  top: -0.5em !important;
  color: #3b82f6 !important;
}

.article-content span.katex-html .vlist span.reset-textstyle.scriptstyle.cramped {
  font-size: 0.75em !important;
  position: relative !important;
  top: 0.3em !important;
  color: #3b82f6 !important;
}
/* 作者头像样式 */
.author-avatar {
  position: relative;
  overflow: hidden;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.author-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(var(--color-secondary-rgb), 0.5);
}

.author-avatar img {
  transition: transform 0.5s ease;
}

.author-avatar:hover img {
  transform: scale(1.1);
}

/* 作者信息卡片样式 */
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
  background: linear-gradient(135deg, rgba(var(--color-secondary-rgb), 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.author-card:hover::before {
  opacity: 1;
}

/* 文章标题样式 */
.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
  scroll-margin-top: 100px; /* 滚动偏移量，确保标题不被导航栏遮挡 */
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  padding-top: 0.5em; /* 添加上方空间，确保标题可见性 */
  margin-top: 0.5em; /* 添加上方边距 */
}

/* 暗黑模式下的标题颜色 */
.dark .prose h1, .dark .prose h2, .dark .prose h3, .dark .prose h4, .dark .prose h5, .dark .prose h6 {
  color: #e2e8f0; /* 浅色的文本，提高可读性 */
}

/* 标题悬停效果 */
.prose h1:hover, .prose h2:hover, .prose h3:hover, .prose h4:hover, .prose h5:hover, .prose h6:hover {
  color: var(--color-secondary);
}

/* 暗黑模式下的标题悬停效果 */
.dark .prose h1:hover, .dark .prose h2:hover, .dark .prose h3:hover,
.dark .prose h4:hover, .dark .prose h5:hover, .dark .prose h6:hover {
  color: var(--color-dark-secondary, #60a5fa); /* 使用暗色主题的强调色 */
  text-shadow: 0 0 8px rgba(96, 165, 250, 0.3); /* 添加文本阴影增强可见性 */
}

/* 添加锚点图标 */
.prose h1:hover::before, .prose h2:hover::before, .prose h3:hover::before,
.prose h4:hover::before, .prose h5:hover::before, .prose h6:hover::before {
  content: '#';
  position: absolute;
  left: -1em;
  opacity: 0.5;
  font-weight: normal;
}

/* 暗黑模式下的锚点图标 */
.dark .prose h1:hover::before, .dark .prose h2:hover::before, .dark .prose h3:hover::before,
.dark .prose h4:hover::before, .dark .prose h5:hover::before, .dark .prose h6:hover::before {
  opacity: 0.7; /* 增加不透明度，提高可见性 */
  color: var(--color-dark-secondary, #60a5fa); /* 使用暗色主题的强调色 */
}

/* 标题锚点特殊样式 */
.heading-anchor {
  position: relative;
  z-index: 1;
}

/* 添加可见性样式，确保标题在滚动时可见 */
.prose h1, .prose h2 {
  border-bottom: 1px solid rgba(var(--color-secondary-rgb), 0.2);
  padding-bottom: 0.3em;
}

/* 暗黑模式下的标题分隔线 */
.dark .prose h1, .dark .prose h2 {
  border-bottom: 1px solid rgba(96, 165, 250, 0.2); /* 使用暗色主题的强调色 */
}

/* 标题高亮效果 */
@keyframes highlight-pulse {
  0% {
    background-color: rgba(var(--color-secondary-rgb), 0.1);
  }
  50% {
    background-color: rgba(var(--color-secondary-rgb), 0.2);
  }
  100% {
    background-color: rgba(var(--color-secondary-rgb), 0.1);
  }
}

/* 标题高亮效果增强 - 使用不同的类名避免冲突 */
.prose .heading-highlight,
.prose .highlight-heading {
  animation: highlight-pulse 1s ease-in-out 2;
  background-color: rgba(var(--color-secondary-rgb), 0.1);
  border-left: 3px solid var(--color-secondary);
  padding-left: 0.5em;
  transition: all 0.5s ease;
}

/* 暗黑模式下的标题高亮效果 */
.dark .prose .heading-highlight,
.dark .prose .highlight-heading {
  background-color: rgba(96, 165, 250, 0.15); /* 使用暗色主题的强调色，增加不透明度 */
  border-left: 3px solid var(--color-dark-secondary, #60a5fa);
  box-shadow: 0 0 10px rgba(96, 165, 250, 0.1); /* 添加阴影增强可见性 */
}

/* 文章内容元素动画效果 */
.prose p, .prose ul, .prose ol, .prose blockquote, .prose pre, .prose table {
  animation-duration: 0.5s;
  animation-fill-mode: both;
}

/* 添加滑入动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translate3d(0, 20px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

/* 添加滑入动画效果类 */
.animate-fadeInUp {
  animation-name: fadeInUp;
}

/* 为文章内容中的元素添加动画效果 */
.prose p {
  animation-name: fadeInUp;
  animation-delay: 0.2s;
}

.prose ul, .prose ol {
  animation-name: fadeInUp;
  animation-delay: 0.3s;
}

.prose blockquote {
  animation-name: fadeInUp;
  animation-delay: 0.4s;
}

.prose pre {
  animation-name: fadeInUp;
  animation-delay: 0.5s;
}

.prose table {
  animation-name: fadeInUp;
  animation-delay: 0.6s;
}

/* 添加悬停动画效果 */
@keyframes pulse {
  from {
    transform: scale3d(1, 1, 1);
  }
  50% {
    transform: scale3d(1.05, 1.05, 1.05);
  }
  to {
    transform: scale3d(1, 1, 1);
  }
}

.animate-pulse {
  animation-name: pulse;
  animation-duration: 1s;
  animation-fill-mode: both;
  animation-iteration-count: infinite;
}
</style>

<style scoped>
/* 使用深度选择器确保样式能够应用到KaTeX渲染的元素上 - 根据实际DOM结构调整 */
:deep(.katex-html) {
  font-size: 1.1em !important;
  color: #3b82f6 !important;
}

/* 基础样式 */
:deep(.katex-html .base) {
  position: relative !important;
}

/* 上标样式 - 根据实际DOM结构调整 */
:deep(.katex-html .vlist > span.reset-textstyle.scriptstyle),
:deep(span.katex-html .vlist span.reset-textstyle.scriptstyle) {
  font-size: 0.6em !important;
  position: relative !important;
  margin-left: 0.2em !important;
  top: 0.5em !important; /* 修改为负值，使上标向上移动 */
  color: #3b82f6 !important;
}

/* 下标样式 - 根据实际DOM结构调整 */
:deep(.katex-html .vlist > span.reset-textstyle.scriptstyle.cramped),
:deep(span.katex-html .vlist span.reset-textstyle.scriptstyle.cramped) {
  font-size: 0.7em !important;
  position: relative !important;
  margin-left: 0.1em !important;
  top: 0.6em !important;
  color: #3b82f6 !important;
}

/* 调整strut元素 */
:deep(.katex-html .strut) {
  display: inline-block !important;
}

:deep(.katex-html .strut.bottom) {
  vertical-align: -0.25em !important;
}

/* 调整fontsize-ensurer */
:deep(.katex-html .fontsize-ensurer) {
  display: inline-block !important;
}

/* 调整baseline-fix */
:deep(.katex-html .baseline-fix) {
  display: inline-block !important;
  position: relative !important;
}
</style>