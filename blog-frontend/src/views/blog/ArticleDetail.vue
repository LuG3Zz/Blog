<template>
  <div class="min-h-screen flex flex-col overflow-hidden bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <Navbar class="animate__animated animate__fadeInDown" />
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
            <h1 class="text-3xl font-bold text-white mb-2 animate__animated animate__fadeInUp animate__delay-1s">{{ post.title }}</h1>
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
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                </svg>
                精选
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
            <div class="prose prose-lg max-w-none dark:prose-invert text-gray-800 dark:text-gray-200 article-content markdown-body animate__animated animate__fadeIn animate__delay-2s" v-html="renderedContent"></div>

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

              <div class="flex items-center justify-between">
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
import { ref, onMounted, onUnmounted, computed, h, createApp } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi, usersApi } from '@/api'
import { Navbar } from '@/components/layout'
import { CommentSection, ArticleToc, ArticleSidebar, AiSummary } from '@/components/blog'
import { Breadcrumb, ScrollIsland, CodeBlock } from '@/components/ui'
import MarkdownIt from 'markdown-it'
import markdownItKatex from 'markdown-it-katex'
import 'katex/dist/katex.min.css' // 导入 KaTeX 样式
import message from '@/utils/message'
import confetti from 'canvas-confetti'

export default {
  name: 'ArticleDetail',
  components: {
    Navbar,
    CommentSection,
    ArticleToc,
    ArticleSidebar,
    AiSummary,
    Breadcrumb,
    ScrollIsland
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const post = ref(null)
    const loading = ref(true)
    const markdownContent = ref('')
    const isLiked = ref(false)
    const readingTime = ref(0)
    const articleHeadings = ref([])

    // 添加取消标记
    const isComponentMounted = ref(true)

    // 添加 requestAnimationFrame IDs 数组，用于清理
    const rafIds = []


    // 获取文章图片
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

    // 获取文章标签
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

    // 创建markdown-it实例
    const md = new MarkdownIt({
      html: true,
      linkify: true,
      typographer: true,
      highlight: function (str, lang) {
        // 返回空字符串，因为我们将使用自定义的代码块组件
        return '';
      }
    })

    // 使用 KaTeX 插件渲染数学公式
    md.use(markdownItKatex, {
      throwOnError: false,
      errorColor: '#cc0000'
    })

    // 添加自动生成标题ID的功能
    md.use(function(md) {
      // 创建一个映射来跟踪标题文本和计数器
      const headingCounters = {};

      const originalHeadingOpen = md.renderer.rules.heading_open || function(tokens, idx, options, env, self) {
        return self.renderToken(tokens, idx, options);
      };

      md.renderer.rules.heading_open = function(tokens, idx, options, env, self) {
        const token = tokens[idx];
        const nextToken = tokens[idx + 1];
        if (nextToken && nextToken.type === 'inline' && nextToken.content) {
          // 生成基本ID：将标题文本转换为小写，替换空格为连字符，移除非单词字符
          const text = nextToken.content;
          let baseId = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '');

          // 如果 baseId 为空，使用备用的 ID
          if (!baseId) {
            const headingLevel = token.tag.substring(1); // 例如，从 'h1' 中提取 '1'
            baseId = `heading-${headingLevel}-${idx}`;
            console.log(`标题文本生成的 ID 为空，使用备用 ID: ${baseId}`);
          }

          // 检查是否已经有相同文本的标题，如果有，增加计数器
          if (!headingCounters[text]) {
            headingCounters[text] = 0;
          }
          headingCounters[text]++;

          // 如果是第一个出现的标题，使用基本ID，否则添加计数器
          let uniqueId;
          if (headingCounters[text] === 1) {
            uniqueId = baseId;
          } else {
            uniqueId = `${baseId}-${headingCounters[text]}`;
          }

          console.log(`渲染标题: 文本="${text}", ID="${uniqueId}"`);

          // 确保 ID 不为空
          if (!uniqueId) {
            uniqueId = `heading-${idx}-${Date.now()}`;
            console.log(`生成的 ID 仍然为空，使用备用 ID: ${uniqueId}`);
          }

          // 设置标题ID和数据属性
          token.attrSet('id', uniqueId);
          token.attrSet('data-heading-text', text);
          token.attrSet('data-heading-index', headingCounters[text].toString());

          console.log(`标题生成ID: ${text} -> ${uniqueId} (索引: ${headingCounters[text]})`);
        }
        return originalHeadingOpen(tokens, idx, options, env, self);
      };
    })

    // 添加标题点击跳转功能
    md.use(function(md) {
      const originalHeadingRender = md.renderer.rules.heading_close || function(tokens, idx, options, env, self) {
        return self.renderToken(tokens, idx, options);
      };

      md.renderer.rules.heading_close = function(tokens, idx, options, env, self) {
        // 不使用内联脚本，而是添加一个特殊的类
        const token = tokens[idx - 2]; // heading_open token
        if (token && token.tag && token.tag.match(/^h[1-6]$/)) {
          const id = token.attrs && token.attrs.find(attr => attr[0] === 'id');
          if (id && id[1]) {
            // 在标题开始标签上添加类，用于样式和脚本选择
            token.attrSet('class', (token.attrGet('class') || '') + ' heading-anchor');
            token.attrSet('data-id', id[1]);
          }
        }
        return originalHeadingRender(tokens, idx, options, env, self);
      };
    })

    // 渲染Markdown内容的计算属性
    const renderedContent = computed(() => {
      if (!markdownContent.value) return ''

      // 使用 markdown-it 渲染内容
      return md.render(markdownContent.value)
    })

    // 处理渲染后的内容，替换代码块
    const processCodeBlocks = () => {
      // 如果组件已经卸载，不执行操作
      if (!isComponentMounted.value) return

      setTimeout(() => {
        try {
          // 查找所有代码块
          const codeBlocks = document.querySelectorAll('.prose pre code')

          if (codeBlocks.length === 0) return

          // 遍历每个代码块
          codeBlocks.forEach(codeBlock => {
            // 获取代码块父元素
            const preElement = codeBlock.parentElement
            if (!preElement) return

            // 获取语言
            const classNames = codeBlock.className.split(' ')
            let language = 'none'
            for (const className of classNames) {
              if (className.startsWith('language-')) {
                language = className.replace('language-', '')
                break
              }
            }

            // 获取代码内容
            const code = codeBlock.textContent

            // 创建新的代码块元素
            const codeBlockElement = document.createElement('div')
            codeBlockElement.className = 'custom-code-block'
            codeBlockElement.setAttribute('data-language', language)
            codeBlockElement.setAttribute('data-code', code)

            // 替换原来的代码块
            preElement.parentElement.replaceChild(codeBlockElement, preElement)
          })

          // 将自定义代码块替换为 Vue 组件
          const customCodeBlocks = document.querySelectorAll('.custom-code-block')
          customCodeBlocks.forEach(element => {
            const language = element.getAttribute('data-language') || 'none'
            const code = element.getAttribute('data-code') || ''

            // 创建 CodeBlock 组件实例
            const codeBlockInstance = h(CodeBlock, {
              language,
              code,
              lineNumbers: true
            })

            // 渲染组件
            const app = createApp({
              render() {
                return codeBlockInstance
              }
            })

            // 创建容器并挂载组件
            const container = document.createElement('div')
            element.parentElement.replaceChild(container, element)
            app.mount(container)
          })
        } catch (error) {
          console.error('处理代码块时出错:', error)
        }
      }, 100) // 等待内容渲染完成
    }

    // 计算阅读时间
    const calculateReadingTime = (content) => {
      const wordsPerMinute = 200 // 假设平均阅读速度为每分钟200字
      const wordCount = content.length
      return Math.ceil(wordCount / wordsPerMinute)
    }


    // 处理点赞
    const handleLike = async () => {
      // 如果组件已经卸载，不执行操作
      if (!isComponentMounted.value) {
        console.log('组件已卸载，取消点赞操作')
        return
      }

      const token = localStorage.getItem('token')
      if (!token) {
        message.warning('请先登录后再点赞')
        router.push('/login')
        return
      }

      try {
        await postApi.likePost(post.value.id)

        // 再次检查组件是否已卸载
        if (!isComponentMounted.value) {
          console.log('点赞操作后，组件已卸载，取消后续操作')
          return
        }

        const wasLiked = isLiked.value
        isLiked.value = !wasLiked
        post.value.like_count += isLiked.value ? 1 : -1
        message.success(isLiked.value ? '点赞成功' : '已取消点赞')

        // 如果是点赞操作（不是取消点赞），触发彩带效果
        if (isLiked.value) {
          triggerConfetti()
        }
      } catch (error) {
        console.error('点赞失败:', error)
        message.error('点赞失败，请稍后重试')
      }
    }

    // 触发彩带效果
    const triggerConfetti = () => {
      const end = Date.now() + 2 * 1000; // 2秒
      const colors = ['#ff0000', '#ff4d94', '#ff9999', '#ffcccc']; // 红色系列
      let rafId = null; // 存储 requestAnimationFrame 的 ID

      // 帧函数，触发彩带炮
      function frame() {
        if (Date.now() > end || !isComponentMounted.value) {
          // 如果时间到了或组件已卸载，停止动画
          return;
        }

        // 左侧彩带炮
        confetti({
          particleCount: 2,
          angle: 60,
          spread: 55,
          startVelocity: 60,
          origin: { x: 0, y: 0.5 },
          colors: colors,
        });

        // 右侧彩带炮
        confetti({
          particleCount: 2,
          angle: 120,
          spread: 55,
          startVelocity: 60,
          origin: { x: 1, y: 0.5 },
          colors: colors,
        });

        // 继续调用帧函数，并存储 ID 以便清理
        rafId = requestAnimationFrame(frame);
      }

      // 开始动画
      rafId = requestAnimationFrame(frame);

      // 添加到 rafIds 数组中，以便在组件卸载时清理
      if (rafId) {
        rafIds.push(rafId);
      }
    }

    // 获取点赞状态
    const fetchLikeStatus = async () => {
      // 如果组件已经卸载，不执行操作
      if (!isComponentMounted.value) {
        console.log('组件已卸载，取消获取点赞状态')
        return
      }

      const token = localStorage.getItem('token')
      if (!token || !post.value) return

      try {
        const response = await postApi.getLikeStatus(post.value.id)

        // 再次检查组件是否已卸载
        if (!isComponentMounted.value) {
          console.log('获取点赞状态后，组件已卸载，取消后续操作')
          return
        }

        isLiked.value = response.is_liked
      } catch (error) {
        console.error('获取点赞状态失败:', error)
      }
    }

    // 获取角色名称
    const getRoleName = (role) => {
      const roleMap = {
        'admin': '管理员',
        'editor': '编辑',
        'user': '用户'
      }
      return roleMap[role] || role
    }

    // 导航到作者资料页
    const navigateToAuthorProfile = (authorId) => {
      if (!authorId) return
      router.push(`/user/${authorId}`)
    }

    // 格式化日期
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

    // 处理图片加载错误
    const handleImageError = (event) => {
      console.log('图片加载失败:', event.target.src)
      // 设置默认图片
      event.target.src = '/images/default-avatar.jpg'
      // 防止循环触发错误事件
      event.target.onerror = null
    }

    // 获取文章数据
    const fetchPost = async () => {
      // 如果组件已经卸载，不执行操作
      if (!isComponentMounted.value) {
        console.log('组件已卸载，取消获取文章数据')
        return
      }

      loading.value = true
      try {
        const response = await postApi.getPostById(route.params.id)

        // 再次检查组件是否已卸载
        if (!isComponentMounted.value) {
          console.log('获取文章数据后，组件已卸载，取消后续操作')
          return
        }

        // 如果有作者ID，获取作者信息
        let authorData = null
        if (response.author_id) {
          try {
            authorData = await usersApi.getUserById(response.author_id)
            console.log('获取到作者信息:', authorData)
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

        // 获取点赞状态
        fetchLikeStatus()
      } catch (error) {
        console.error('获取文章失败:', error)
        message.error('获取文章详情失败')
        post.value = null
      } finally {
        loading.value = false
      }
    }

    // 返回上一页
    const goBack = () => {
      router.back()
    }

    // 添加标题点击事件处理
    const setupHeadingClickHandlers = () => {
      // 如果组件已经卸载，不执行操作
      if (!isComponentMounted.value) {
        console.log('组件已卸载，取消设置标题点击处理器')
        return
      }

      // console.log('设置标题点击处理器')

      // 使用局部变量保存当前的挂载状态
      const isMounted = isComponentMounted.value

      // 使用 requestAnimationFrame 确保在下一帧渲染时执行
      // 将 requestAnimationFrame ID 保存到 rafIds 数组，以便清理
      const id = requestAnimationFrame(() => {
        // 再次检查组件是否已卸载，使用局部变量而不是响应式对象
        if (!isMounted) {
          console.log('requestAnimationFrame 回调中，组件已卸载，取消操作')
          return
        }
        try {
          // 查找所有标题元素
          const headings = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')

          if (headings.length === 0) {
            // console.log('没有找到标题元素')
            return
          }

          // console.log(`找到 ${headings.length} 个标题元素`)

          // 为每个标题处理 ID 和类
          headings.forEach((heading, idx) => {
            // 添加 heading-anchor 类
            if (!heading.classList.contains('heading-anchor')) {
              heading.classList.add('heading-anchor')
            }

            // 处理 ID
            if (!heading.id) {
              const text = heading.textContent.trim()
              if (text) {
                // 获取标题索引
                const index = parseInt(heading.getAttribute('data-heading-index') || '0')

                // 生成基本ID
                let baseId = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '')

                // 如果 baseId 为空，使用备用的 ID
                if (!baseId) {
                  baseId = `heading-${idx + 1}`
                  console.log(`标题文本生成的 ID 为空，使用备用 ID: ${baseId}`)
                }

                // 如果有索引，使用索引生成ID
                let id = index > 1 ? `${baseId}-${index}` : baseId

                // 检查是否已存在相同ID的元素
                let counter = index || 1
                while (document.getElementById(id)) {
                  counter++
                  id = `${baseId}-${counter}`
                }

                console.log(`设置标题 ${idx + 1} 的 ID: "${id}", 文本="${text}"`)

                // 确保 ID 不为空
                if (!id) {
                  id = `heading-${idx + 1}-${Date.now()}`
                  console.log(`生成的 ID 仍然为空，使用备用 ID: ${id}`)
                }


                heading.id = id
                heading.setAttribute('data-id', id)

                // 确保标题有索引属性
                if (!heading.hasAttribute('data-heading-index')) {
                  heading.setAttribute('data-heading-index', counter.toString())
                }
              }
            } else if (!heading.hasAttribute('data-id')) {
              heading.setAttribute('data-id', heading.id)
            }

            // 检查是否已添加点击事件
            if (heading.getAttribute('data-click-handler') !== 'true') {
              const id = heading.getAttribute('data-id') || heading.id
              if (id) {
                // 创建命名的点击处理函数，便于移除
                const clickHandler = function(event) {
                  // console.log(`标题点击: ${id}`)

                  // 更新 URL 但不触发页面滚动
                  history.pushState(null, null, `#${id}`)

                  // 计算元素的位置
                  const rect = heading.getBoundingClientRect()
                  const absoluteElementTop = rect.top + window.pageYOffset

                  // 计算偏移量，使标题位于页面中间位置
                  const viewportHeight = window.innerHeight
                  const offset = viewportHeight * 0.2 // 视口高度的20%

                  // 滚动到元素位置减去偏移量
                  window.scrollTo({
                    top: absoluteElementTop - offset,
                    behavior: 'smooth'
                  })

                  // 添加高亮效果
                  heading.classList.add('highlight-heading')
                  setTimeout(() => {
                    if (document.body.contains(heading)) {
                      heading.classList.remove('highlight-heading')
                    }
                  }, 2000)

                  // 阻止事件冒泡
                  event.stopPropagation()
                }

                // 存储处理函数引用
                heading._clickHandler = clickHandler

                // 添加点击事件
                heading.addEventListener('click', clickHandler)

                // 标记已添加点击事件
                heading.setAttribute('data-click-handler', 'true')
              }
            }
          })
        } catch (error) {
          console.error('设置标题点击处理器时出错:', error)
        }
      })

      // 将 ID 添加到 rafIds 数组中
      if (id) {
        rafIds.push(id)
      }
    }

    // 提取文章中的标题
    const extractArticleHeadings = () => {
      // 如果组件已经卸载，不执行操作
      if (!isComponentMounted.value) {
        console.log('组件已卸载，取消提取文章标题')
        return
      }

      try {
        // 查找所有标题元素
        const headingElements = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')

        if (headingElements.length === 0) {
          console.log('没有找到标题元素')

          // 如果没有找到标题元素，尝试手动创建一些标题数据用于测试
          const testHeadings = [
            { id: 'heading-1', level: 1, text: '文章标题' },
            { id: 'heading-2', level: 2, text: '第一部分' },
            { id: 'heading-3', level: 3, text: '小节一' },
            { id: 'heading-4', level: 2, text: '第二部分' },
            { id: 'heading-5', level: 3, text: '小节二' }
          ];

          console.log('使用测试标题数据:', testHeadings);
          articleHeadings.value = testHeadings;
          return;
        }

        console.log(`找到 ${headingElements.length} 个标题元素`)

        // 清空现有标题列表
        articleHeadings.value = []

        // 提取标题信息
        headingElements.forEach((heading) => {
          const id = heading.id || heading.getAttribute('data-id')
          if (!id) return

          const level = parseInt(heading.tagName.substring(1)) // 从 'H1', 'H2' 等提取数字
          const text = heading.textContent.trim()

          articleHeadings.value.push({
            id,
            level,
            text
          })
        })

        console.log('提取的标题列表:', articleHeadings.value)

        // 强制触发响应式更新，确保 ScrollIsland 组件能接收到最新的标题列表
        // 这是解决问题的关键，通过创建一个新数组来触发响应式更新
        const newHeadings = [...articleHeadings.value];
        console.log('强制更新标题列表，新数组:', newHeadings);
        articleHeadings.value = newHeadings;

        // 在下一帧再次检查标题列表
        setTimeout(() => {
          console.log('更新后的标题列表:', articleHeadings.value);
        }, 0);
      } catch (error) {
        console.error('提取文章标题时出错:', error)
      }
    }

    onMounted(async () => {
      isComponentMounted.value = true
      await fetchPost()

      // 只有在组件仍然挂载时才继续执行
      if (isComponentMounted.value) {
        await fetchLikeStatus()
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
              console.log('第一次提取标题失败，再次尝试')
              extractArticleHeadings()

              // 第三次尝试
              setTimeout(() => {
                if (isComponentMounted.value && articleHeadings.value.length === 0) {
                  console.log('第二次提取标题失败，再次尝试')
                  extractArticleHeadings()
                }
              }, 1000)
            }
          }, 500)
        }
      }, 500) // 延迟执行，确保标题元素已经渲染

      // 使用防抖处理的 MutationObserver
      let debounceTimer = null
      // 注意：我们已经在外部声明了 rafIds 数组，这里不需要再声明
      const observer = new MutationObserver((mutations) => {
        // 如果组件已经卸载，不执行操作
        if (!isComponentMounted.value) {
          console.log('MutationObserver 回调中，组件已卸载，取消操作')
          return
        }

        // 使用局部变量保存当前的挂载状态
        // 注意：我们在定时器回调中使用了局部变量，这里不需要再使用
        // 检查是否有相关的变化
        const hasRelevantChanges = mutations.some(mutation => {
          // 只处理添加标题元素的变化
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            for (const node of mutation.addedNodes) {
              if (node.nodeType === Node.ELEMENT_NODE) {
                // 检查是否是标题元素或包含标题元素
                if (node.tagName && /^H[1-6]$/.test(node.tagName) ||
                    node.querySelector && node.querySelector('h1, h2, h3, h4, h5, h6')) {
                  return true
                }
              }
            }
          }
          return false
        })

        // 如果有相关变化，使用防抖处理
        if (hasRelevantChanges) {
          // console.log('检测到标题元素变化，准备更新点击处理器')

          // 清除之前的定时器
          if (debounceTimer) {
            clearTimeout(debounceTimer)
          }

          // 设置新的定时器，延迟执行
          // 使用局部变量保存当前的挂载状态
          const currentIsMounted = isComponentMounted.value

          debounceTimer = setTimeout(() => {
            // 在定时器回调中再次检查组件是否已卸载
            if (!currentIsMounted) {
              console.log('定时器回调中，组件已卸载，取消标题点击处理器更新')
              return
            }

            // console.log('执行延迟的标题点击处理器更新')
            setupHeadingClickHandlers()

            // 处理代码块
            processCodeBlocks()

            // 同时更新标题列表
            extractArticleHeadings()
          }, 500)
        }
      })

      // 监听文章内容容器
      const contentContainer = document.querySelector('.prose')
      if (contentContainer) {
        // 使用更精细的配置，减少不必要的触发
        observer.observe(contentContainer, {
          childList: true,  // 监听子元素的添加和删除
          subtree: true,    // 监听所有后代元素
          attributes: false, // 不监听属性变化
          characterData: false // 不监听文本变化
        })
      }

      // 组件卸载时清理所有资源
      return () => {
        // 断开观察者连接
        observer.disconnect()

        // 清除定时器
        if (debounceTimer) {
          clearTimeout(debounceTimer)
          debounceTimer = null
        }

        // 清除 requestAnimationFrame
        rafIds.forEach(id => {
          cancelAnimationFrame(id)
        })
        rafIds.length = 0; // 清空数组
      }
    })

    // 添加组件卸载钩子
    onUnmounted(() => {
      console.log('组件卸载，清理资源')

      // 首先设置挂载状态为 false，确保所有异步操作都会检查这个状态
      isComponentMounted.value = false

      try {
        // 清除所有标题元素的点击事件
        const headings = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')
        headings.forEach(heading => {
          // 移除所有事件监听器
          heading.replaceWith(heading.cloneNode(true))
        })

        // 清理所有 requestAnimationFrame
        rafIds.forEach(id => {
          cancelAnimationFrame(id)
        })
      } catch (error) {
        console.error('清除资源时出错:', error)
      } finally {
        // 清除引用，避免内存泄漏
        post.value = null
        markdownContent.value = ''
      }
    })

    // 生成AI摘要内容
    const generateAiSummary = () => {
      if (post.value.excerpt) return post.value.excerpt

      // 这里可以根据文章内容生成一个更智能的摘要
      // 实际应用中可以调用AI服务来生成
      return `这是一篇关于${post.value.category}的精彩文章，主要探讨了${post.value.title}的核心观点。文章从多个角度分析了这一主题的重要性和应用价值，值得深入阅读。`
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
      handleLike,
      isLiked,
      getRoleName,
      navigateToAuthorProfile,
      formatDate,
      articleHeadings,
      processCodeBlocks
    }
  }
}
</script>

<style>
:root {
  --color-secondary-rgb: 59, 130, 246; /* 蓝色的RGB值 */
  --color-secondary: #3b82f6;
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

/* 自定义代码块样式 */
.custom-code-block {
  margin: 1.5rem 0;
}

/* 暗黑模式下的代码块样式 */
.dark .article-content pre {
  background-color: #1e293b !important; /* 深蓝色背景，增强对比度 */
  border: 1px solid #334155 !important; /* 添加边框，增强边界 */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.1) !important; /* 添加阴影，增强立体感 */
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