<template>
  <div class="space-y-8">
    <div class="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ isEdit ? '编辑文章' : '添加文章' }}</h1>
      <button
        @click="goBack"
        class="px-5 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-300 flex items-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        返回列表
      </button>
    </div>

    <!-- 文章编辑表单 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden p-6">
      <form @submit.prevent="savePost" class="space-y-6">
        <!-- 显示表单错误信息 -->
        <div v-if="formError" class="p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 rounded-lg text-sm mb-4">
          {{ formError }}
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- 左侧表单 -->
          <div class="space-y-4">
            <div>
              <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <input
                type="text"
                id="title"
                v-model="currentPost.title"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
                required
              />
            </div>

            <div>
              <label for="category" class="block text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
              <select
                id="category"
                v-model="currentPost.category_id"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
                required
              >
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div>
              <div class="flex items-center justify-between">
                  <label for="summary" class="block text-sm font-medium text-gray-700 dark:text-gray-300">摘要</label>
                  <button
                    type="button"
                    @click="handleAIAssist"
                    :disabled="isAILoading"
                    class="px-3 py-1.5 text-sm bg-secondary/20 dark:bg-dark-secondary/20 text-secondary dark:text-dark-secondary rounded-md hover:bg-secondary/30 dark:hover:bg-dark-secondary/30 transition-colors duration-200 flex items-center gap-1.5"
                  >
                    <svg v-if="!isAILoading" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                      <path d="M19.875 6.27a2.225 2.225 0 0 1 1.125 1.948v7.284c0 .809 -.443 1.555 -1.158 1.948l-6.75 4.27a2.269 2.269 0 0 1 -2.184 0l-6.75 -4.27a2.225 2.225 0 0 1 -1.158 -1.948v-7.285c0 -.809 .443 -1.554 1.158 -1.947l6.75 -3.98a2.33 2.33 0 0 1 2.25 0l6.75 3.98h-.033z"/>
                      <path d="M12 8v4" />
                      <path d="M12 16h.01" />
                    </svg>
                    <span class="inline-block h-4 w-4 border-2 border-secondary dark:border-dark-secondary border-t-transparent rounded-full animate-spin" v-else></span>
                    AI总结
                  </button>
                </div>
                <textarea
                  id="summary"
                  v-model="currentPost.summary"
                  rows="3"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
                  required
                ></textarea>
            </div>
          </div>

          <!-- 右侧表单 -->
          <div class="space-y-4">
            <!-- 标签输入组件 -->
            <div>
              <label for="tags" class="block text-sm font-medium text-gray-700 dark:text-gray-300">标签</label>
              <div class="mt-1 flex flex-col space-y-2">
                <div class="flex flex-wrap gap-2 p-2 border border-gray-300 dark:border-gray-600 rounded-md min-h-[42px] bg-white dark:bg-gray-700">
                  <!-- 已添加的标签 -->
                  <div
                    v-for="(tag, index) in tags"
                    :key="index"
                    class="flex items-center bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 px-2 py-1 rounded-md"
                  >
                    <span>{{ tag }}</span>
                    <button
                      type="button"
                      @click="removeTag(index)"
                      class="ml-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                    >
                      &times;
                    </button>
                  </div>
                  <!-- 标签输入框 -->
                  <input
                    type="text"
                    v-model="tagInput"
                    @keydown.enter.prevent="addTag"
                    @keydown.tab.prevent="addTag"
                    @keydown.comma.prevent="addTag"
                    placeholder="输入标签后按 Enter 添加"
                    class="flex-grow min-w-[120px] outline-none border-0 bg-transparent dark:text-white"
                  />
                </div>
                <!-- 标签建议列表 -->
                <div v-if="tagSuggestions.length > 0" class="mt-2 bg-white dark:bg-gray-700 shadow-lg rounded-md p-1 absolute z-10 w-full max-h-40 overflow-y-auto">
                  <div
                    v-for="tag in tagSuggestions"
                    :key="tag.id"
                    @click="selectTagSuggestion(tag.name)"
                    class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer rounded-md"
                  >
                    {{ tag.name }} <span class="text-xs text-gray-500 dark:text-gray-400">({{ tag.article_count || 0 }} 篇文章)</span>
                  </div>
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400">按 Enter、Tab 或输入逗号添加标签</p>
              </div>
            </div>

            <!-- 封面图上传 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">封面图</label>
              <div class="relative">
                <!-- 预览区域 -->
                <div v-if="currentPost.cover_image" class="relative w-full h-48 mb-2 rounded-lg overflow-hidden">
                  <img :src="currentPost.cover_image" alt="封面图预览" class="w-full h-full object-cover" />
                  <button
                    @click="removeCoverImage"
                    type="button"
                    class="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <!-- 上传按钮 -->
                <div v-if="!currentPost.cover_image" class="flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-lg">
                  <div class="space-y-1 text-center">
                    <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <div class="flex text-sm text-gray-600 dark:text-gray-400">
                      <label for="cover-image" class="relative cursor-pointer bg-white dark:bg-gray-700 rounded-md font-medium text-secondary dark:text-dark-secondary hover:text-secondary-dark focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-secondary">
                        <span>上传图片</span>
                        <input
                          id="cover-image"
                          type="file"
                          class="sr-only"
                          accept=".jpg,.jpeg,.png,.gif,.webp"
                          @change="handleCoverImageUpload"
                        />
                      </label>
                    </div>
                    <p class="text-xs text-gray-500 dark:text-gray-400">支持 JPG、PNG、GIF、WEBP 格式</p>
                  </div>
                </div>
                <!-- 上传加载状态 -->
                <div v-if="isUploading" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-lg">
                  <div class="animate-spin rounded-full h-8 w-8 border-4 border-secondary border-t-transparent"></div>
                </div>
              </div>
            </div>

            <!-- 其他可能的元数据字段可以在这里添加 -->
            <div class="flex items-center mt-4">
              <input
                type="checkbox"
                id="featured"
                v-model="currentPost.is_featured"
                class="h-4 w-4 text-secondary focus:ring-secondary border-gray-300 rounded"
              />
              <label for="featured" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                设为精选文章
              </label>
            </div>
          </div>
        </div>

        <!-- 内容编辑器 (占据整行) -->
        <div class="mt-8">
          <label for="content" class="block text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">内容</label>
          <div id="vditor" class="w-full rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden shadow-sm max-h-[600px] overflow-y-auto"></div>
        </div>

        <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          <button
            type="button"
            @click="goBack"
            class="px-6 py-3 border border-gray-300 dark:border-gray-600 shadow-sm rounded-lg bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200 font-medium"
          >
            取消
          </button>
          <button
            type="submit"
            class="px-6 py-3 border border-transparent shadow-sm rounded-lg bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary hover:bg-opacity-90 dark:hover:bg-opacity-90 transition-colors duration-200 font-medium"
          >
            {{ isEdit ? '更新文章' : '保存文章' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { postApi, categoryApi, tagApi } from '@/api'
import message from '@/utils/message.js'  // 添加 message 导入
import Vditor from 'vditor'
import "vditor/dist/index.css"
import { API_BASE_URL } from '@/config'

export default {
  name: 'ArticleEdit',
  setup() {
    const router = useRouter()
    const route = useRoute()

    // 状态数据
    const posts = ref([])
    const categories = ref([])
    const formError = ref('')
    const vditor = ref(null)
    const tagInput = ref('')
    const tags = ref([])
    const allTags = ref([])
    const tagSuggestions = ref([])

    // 当前操作的文章
    const currentPost = ref({
      title: '',
      category_id: '',
      summary: '',
      content: '',
      date: new Date().toISOString().split('T')[0],
      status: 'published',
      is_featured: false
    })

    // AI辅助加载状态
    const isAILoading = ref(false)
    // 图片上传加载状态
    const isUploading = ref(false)

    // 判断是编辑还是新增模式
    const isEdit = computed(() => {
      return route.query.id !== undefined
    })

    // 获取文章数据
    const fetchPosts = async () => {
      try {
        posts.value = await postApi.getPosts()
      } catch (error) {
        console.error('获取文章失败:', error)
      }
    }

    // 获取分类数据
    const fetchCategories = async () => {
      try {
        categories.value = await categoryApi.getCategories()
      } catch (error) {
        console.error('获取分类失败:', error)
        categories.value = []
      }
    }

    // 如果是编辑模式，加载文章数据
    const loadPostData = async () => {
      if (isEdit.value && route.query.id) {
        try {
          // 调用API获取文章详情
          const postId = parseInt(route.query.id)
          // 从API获取文章数据
          const post = await postApi.getPostById(postId)

          if (post) {
            currentPost.value = {
              ...post,
              category_id: post.category_id || '',
              summary: post.excerpt || '',
              content: post.content || '',
              is_featured: post.is_featured || false
            }

            // 处理标签数据
            // 新的API响应中使用 tags_list 字段
            if (post.tags_list && Array.isArray(post.tags_list)) {
              // 从 tags_list 对象数组中提取标签名称
              tags.value = post.tags_list.map(tag => tag.name).filter(Boolean)
            }
            // 兼容旧的API响应格式
            else if (post.tags) {
              // 如果标签是字符串，按逗号分隔
              if (typeof post.tags === 'string') {
                tags.value = post.tags.split(',').map(tag => tag.trim()).filter(tag => tag !== '')
              }
              // 如果标签是数组
              else if (Array.isArray(post.tags)) {
                // 如果标签是对象数组，提取名称
                tags.value = post.tags.map(tag => {
                  if (typeof tag === 'object' && tag !== null) {
                    return tag.name || ''
                  }
                  return tag.trim ? tag.trim() : tag
                }).filter(tag => tag !== '')
              }
            }
          } else {
            formError.value = '未找到文章数据'
          }
        } catch (error) {
          console.error('加载文章数据失败:', error)
          formError.value = '加载文章数据失败'
        }
      } else {
        // 新增模式，初始化默认值
        currentPost.value = {
          title: '',
          category_id: Array.isArray(categories.value) && categories.value.length > 0 ? categories.value[0].id : '',
          summary: '',
          content: '',
          date: new Date().toISOString().split('T')[0],
          status: 'published',
          featured: false
        }
        // 清空标签
        tags.value = []
      }
    }

    // 获取所有标签
    const fetchTags = async () => {
      try {
        const response = await tagApi.getTags()
        allTags.value = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('获取标签失败:', error)
        allTags.value = []
      }
    }

    // 根据输入过滤标签建议
    const updateTagSuggestions = () => {
      if (!tagInput.value.trim()) {
        tagSuggestions.value = []
        return
      }

      const input = tagInput.value.toLowerCase().trim()
      tagSuggestions.value = allTags.value
        .filter(tag => tag.name.toLowerCase().includes(input) && !tags.value.includes(tag.name))
        .slice(0, 5) // 限制建议数量
    }

    // 监听标签输入变化
    watch(tagInput, updateTagSuggestions)

    // 初始化数据
    onMounted(async () => {
      await fetchPosts()
      await fetchCategories()
      await fetchTags()
      await loadPostData()

      // 初始化编辑器
      initVditor()
    })

    // 组件销毁前清理资源
    onBeforeUnmount(() => {
      if (vditor.value) {
        vditor.value.destroy()
        vditor.value = null
      }
    })

    // 初始化Vditor编辑器
    const initVditor = () => {
      // 如果已经存在实例，先销毁
      if (vditor.value) {
        vditor.value.destroy()
      }

      // 创建新实例
      vditor.value = new Vditor('vditor', {
        height: 500, // 增加高度
        mode: 'ir',
        theme: document.documentElement.classList.contains('dark') ? 'dark' : 'classic',
        placeholder: '请输入文章内容...',
        toolbarConfig: {
          pin: true
        },
        cache: {
          enable: false
        },
        preview: {
          maxWidth: 1000, // 预览区域最大宽度
          theme: {
            current: document.documentElement.classList.contains('dark') ? 'dark' : 'light'
          }
        },
        counter: {
          enable: true, // 启用字数统计
          type: 'text' // 统计类型
        },
        upload: {
          accept: 'image/*', // 只接受图片
          multiple: true, // 支持多文件上传
          fieldName: 'file', // 上传字段名称
          url: `${API_BASE_URL}/files/upload-image`, // 上传接口地址
          withCredentials: true, // 跨域请求是否携带 cookie
          headers: {
            // 设置请求头，包括认证信息
            'Authorization': () => {
              const token = localStorage.getItem('token')
              if (!token) return ''

              // 正确处理 token 格式
              const lowerToken = token.toLowerCase()
              let cleanToken = token
              if (lowerToken.includes('bearer')) {
                cleanToken = token.replace(/^\s*bearer\s+/i, '')
              }
              return `Bearer ${cleanToken}`
            }
          },
          format: (files, responseText) => {
            // 格式化服务器返回的数据，使其符合 Vditor 所需格式
            try {
              const res = JSON.parse(responseText)
              if (res.url) {
                return JSON.stringify({
                  msg: '上传成功',
                  code: 0,
                  data: {
                    errFiles: [],
                    succMap: {
                      [files[0].name]: res.url
                    }
                  }
                })
              } else {
                return JSON.stringify({
                  msg: '上传失败',
                  code: 1,
                  data: {}
                })
              }
            } catch (e) {
              console.error('上传响应格式化失败:', e)
              return JSON.stringify({
                msg: '上传失败',
                code: 1,
                data: {}
              })
            }
          }
        },
        after: () => {
          // 编辑模式下，设置编辑器内容
          if (currentPost.value.content) {
            vditor.value.setValue(currentPost.value.content)
          }
        }
      })
    }

    // 添加标签
    const addTag = () => {
      const tag = tagInput.value.trim()
      // 如果标签不为空且不重复，则添加
      if (tag && !tags.value.includes(tag)) {
        tags.value.push(tag)
        tagInput.value = '' // 清空输入框
        tagSuggestions.value = [] // 清空建议
      } else if (tag && tags.value.includes(tag)) {
        // 如果标签重复，提示用户
        message.info('标签已存在')
        tagInput.value = '' // 清空输入框
        tagSuggestions.value = [] // 清空建议
      }
    }

    // 选择标签建议
    const selectTagSuggestion = (tagName) => {
      if (!tags.value.includes(tagName)) {
        tags.value.push(tagName)
        tagInput.value = ''
        tagSuggestions.value = []
      }
    }

    // 删除标签
    const removeTag = (index) => {
      tags.value.splice(index, 1)
    }

    // 保存文章
    const savePost = async () => {
      // 获取Vditor内容
      if (vditor.value) {
        currentPost.value.content = vditor.value.getValue()
      }

      // 表单验证
      if (!currentPost.value.title || !currentPost.value.category_id || !currentPost.value.summary) {
        formError.value = '请填写必填字段（标题、分类和摘要）'
        return
      }

      formError.value = ''

      try {
        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (!token) {
          formError.value = '未登录或登录已过期，请重新登录'
          return
        }

        // 正确处理 token 格式
        // 先将 token 转换为小写进行检查
        const lowerToken = token.toLowerCase();

        // 如果 token 已经包含了 "bearer"，则先删除所有 "bearer" 前缀
        let cleanToken = token;
        if (lowerToken.includes('bearer')) {
          // 删除所有可能的 "bearer" 前缀（包括大小写变体）
          cleanToken = token.replace(/^\s*bearer\s+/i, '');
        }

        // 添加正确的 "Bearer" 前缀
        const formattedToken = `Bearer ${cleanToken}`
        console.log('使用的认证令牌:', formattedToken)

        // 构造文章数据
        const articleData = {
          title: currentPost.value.title,
          content: currentPost.value.content,
          slug: currentPost.value.title.toLowerCase().replace(/\s+/g, '-'),
          excerpt: currentPost.value.summary,
          category_id: currentPost.value.category_id,
          tags: tags.value,  // 使用标签数组，而不是逗号分隔的字符串
          is_featured: currentPost.value.is_featured || false,
          cover_image: currentPost.value.cover_image || '',  // 添加封面图字段
        }

        // 如果标签不存在，则创建新标签
        for (const tagName of tags.value) {
          const existingTag = allTags.value.find(t => t.name === tagName)
          if (!existingTag) {
            try {
              await tagApi.createTag({ name: tagName })
            } catch (error) {
              console.warn(`创建标签 "${tagName}" 失败:`, error)
            }
          }
        }

        let postId;

        if (!isEdit.value) {
          // 创建新文章
          const response = await postApi.createPost(articleData, formattedToken)
          message.success('添加文章成功')
          postId = response.id
        } else {
          // 更新文章
          postId = parseInt(route.query.id)
          await postApi.updatePost(postId, articleData, formattedToken)
          message.success('更新文章成功')
        }

        // 注释: 我们已经在文章数据中包含了标签数组，后端应该能够处理标签的关联
        // 不需要再单独调用标签更新API

        // 返回文章列表页
        goBack()
      } catch (error) {
        console.error('保存文章失败:', error)
        message.error(error.message || '操作失败，请稍后再试')  // 替换 formError
      }
    }

    // 返回文章列表
    const goBack = () => {
      router.push('/admin/articles')
    }

    // AI辅助处理
    const handleAIAssist = async () => {
      isAILoading.value = true
      formError.value = ''

      try {
        const content = vditor.value.getValue()
        if (!content || content.length < 50) {
          formError.value = '文章内容需要至少50字才能生成摘要'
          return
        }

        const token = localStorage.getItem('token')
        if (!token) {
          formError.value = '请先登录后使用AI功能'
          return
        }

        const { excerpt, tags: aiTags } = await postApi.getAIAssist(content, token)

        currentPost.value.summary = excerpt
        if (aiTags?.length > 0) {
          tags.value = aiTags
        }
      } catch (error) {
        console.error('AI辅助失败:', error)
        formError.value = error.message || 'AI摘要生成失败，请稍后重试'
      } finally {
        isAILoading.value = false
      }
    }

    // 删除封面图
    const removeCoverImage = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          message.error('未登录或登录已过期')
          return
        }

        // 从URL中提取文件名
        const imagePath = currentPost.value.cover_image.split('/').pop()
        await postApi.deleteImage(imagePath, token)

        // 清空封面图
        currentPost.value.cover_image = ''
        message.success('封面图删除成功')
      } catch (error) {
        console.error('删除封面图失败:', error)
        message.error(error.message || '删除封面图失败')
      }
    }

    // 处理封面图上传
    const handleCoverImageUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      // 验证文件类型
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
      if (!allowedTypes.includes(file.type)) {
        message.error('请上传正确的图片格式（JPG、PNG、GIF、WEBP）')
        return
      }

      // 验证文件大小（限制为2MB）
      const maxSize = 2 * 1024 * 1024
      if (file.size > maxSize) {
        message.error('图片大小不能超过2MB')
        return
      }

      isUploading.value = true
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          throw new Error('未登录或登录已过期')
        }

        // 创建 FormData 对象
        const formData = new FormData()
        formData.append('file', file)

        // 正确处理 token 格式
        const lowerToken = token.toLowerCase()
        let cleanToken = token
        if (lowerToken.includes('bearer')) {
          cleanToken = token.replace(/^\s*bearer\s+/i, '')
        }
        const formattedToken = `Bearer ${cleanToken}`

        const response = await postApi.uploadImage(formData, formattedToken)
        currentPost.value.cover_image = response.url
        message.success('封面图上传成功')
      } catch (error) {
        console.error('上传封面图失败:', error)
        message.error(error.message || '上传封面图失败')
      } finally {
        isUploading.value = false
        // 清空input的value，确保可以重复上传同一个文件
        event.target.value = ''
      }
    }

    // 删除封面图

    return {
      currentPost,
      categories,
      formError,
      isEdit,
      savePost,
      goBack,
      tags,
      tagInput,
      addTag,
      removeTag,
      tagSuggestions,
      selectTagSuggestion,
      isAILoading,
      handleAIAssist,
      isUploading,
      handleCoverImageUpload,
      removeCoverImage
    }
  }
}
</script>
