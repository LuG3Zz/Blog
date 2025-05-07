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

    <!-- 文件选择器模态框 -->
    <Modal v-if="showFileSelector" @close="showFileSelector = false">
      <div class="w-full max-w-4xl">
        <FileSelector
          file-type="image"
          @close="showFileSelector = false"
          @select="handleFileSelected"
        />
      </div>
    </Modal>

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
                  <div class="space-y-3 text-center">
                    <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <div class="flex flex-col sm:flex-row justify-center gap-2">
                      <button
                        type="button"
                        @click="openFileSelectorForCover"
                        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 font-medium"
                      >
                        从文件管理选择
                      </button>
                      <button
                        type="button"
                        @click="selectRandomCoverImage"
                        class="px-4 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-colors duration-200 font-medium"
                      >
                        随机封面图
                      </button>
                    </div>
                    <p class="text-xs text-gray-500 dark:text-gray-400">请从文件管理中选择图片或使用随机封面图</p>
                  </div>
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
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <label for="content" class="text-lg font-semibold text-gray-900 dark:text-gray-100">内容</label>
              <!-- 导入MD文件按钮 -->
              <button
                type="button"
                @click="triggerImportMdFile"
                class="ml-3 px-3 py-1.5 text-sm bg-blue-500/20 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300 rounded-md hover:bg-blue-500/30 dark:hover:bg-blue-500/30 transition-colors duration-200 flex items-center gap-1.5"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                导入MD文件
              </button>
              <!-- 隐藏的文件输入框 -->
              <input
                type="file"
                ref="mdFileInput"
                class="hidden"
                accept=".md,.markdown"
                @change="handleMdFileImport"
              />
            </div>
            <div class="flex items-center">
              <span class="text-sm text-gray-500 dark:text-gray-400 mr-2">当前模式:</span>
              <span class="px-2 py-1 text-xs font-medium rounded-md"
                    :class="{
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': currentMode === 'ir',
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': currentMode === 'wysiwyg',
                      'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200': currentMode === 'sv'
                    }">
                {{
                  currentMode === 'ir' ? '即时渲染' :
                  currentMode === 'wysiwyg' ? '所见即所得' :
                  currentMode === 'sv' ? '分屏预览' : '未知模式'
                }}
              </span>
            </div>
          </div>
          <div class="relative">
            <div id="vditor" class="w-full rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden shadow-sm" style="height: 600px;"></div>

            <!-- 编辑器加载动画覆盖层 -->
            <div v-if="isLoading" class="absolute inset-0 bg-white dark:bg-gray-800 bg-opacity-90 dark:bg-opacity-90 flex items-center justify-center z-10 rounded-lg">
              <LoadingSpinner message="正在加载编辑器和文章内容..." />
            </div>
          </div>
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
            class="px-6 py-3 border border-transparent shadow-sm rounded-lg bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary hover:bg-opacity-90 dark:hover:bg-opacity-90 transition-colors duration-200 font-medium relative"
            :disabled="isSaving"
          >
            <span v-if="!isSaving">{{ isEdit ? '更新文章' : '保存文章' }}</span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-primary dark:text-dark-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isEdit ? '更新中...' : '保存中...' }}
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch, defineAsyncComponent } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { postApi, categoryApi, tagApi, filesApi } from '@/api'
import message from '@/utils/message.js'  // 添加 message 导入
// 动态导入Vditor
const Vditor = defineAsyncComponent(() => import('vditor').then(module => {
  // 动态导入CSS
  import("vditor/dist/index.css")
  return module.default || module
}))
import { API_BASE_URL } from '@/config'
import Modal from '@/components/common/Modal.vue'
import FileSelector from '@/components/admin/FileSelector.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

export default {
  name: 'ArticleEdit',
  components: {
    Modal,
    FileSelector,
    LoadingSpinner
  },
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

    // 文件选择器相关状态
    const showFileSelector = ref(false)
    const fileSelectorMode = ref('editor') // 'editor' 或 'cover'

    // 编辑器模式 - 默认使用分屏预览模式
    const currentMode = ref('sv')

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
    // 文章保存加载状态
    const isSaving = ref(false)
    // 文章内容加载状态
    const isLoading = ref(false)

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
      // 设置加载状态为true
      isLoading.value = true;

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

      // 延迟一点时间再关闭加载状态，确保编辑器有时间初始化
      // 实际加载状态会在initVditor完成后关闭
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
      console.log('初始化Vditor编辑器...');

      // 确保加载状态为true
      isLoading.value = true;

      // 如果已经存在实例，先销毁
      if (vditor.value) {
        console.log('销毁现有Vditor实例');
        vditor.value.destroy();
        vditor.value = null;
      }

      console.log('设置初始编辑模式:', currentMode.value);

      console.log('创建新实例，当前模式:', currentMode.value);

      // 创建新实例
      vditor.value = new Vditor('vditor', {
        height: 600, // 与容器高度一致
        mode: currentMode.value,
        theme: document.documentElement.classList.contains('dark') ? 'dark' : 'classic',
        placeholder: '请输入文章内容...',
        toolbarConfig: {
          pin: true
        },
        toolbar: [
          'emoji',
          'headings',
          'bold',
          'italic',
          'strike',
          'link',
          '|',
          'list',
          'ordered-list',
          'check',
          'outdent',
          'indent',
          '|',
          'quote',
          'line',
          'code',
          'inline-code',
          'insert-before',
          'insert-after',
          '|',
          {
            name: 'select-image',
            tipPosition: 's',
            tip: '从文件管理选择图片',
            className: 'right',
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M4.502 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/><path d="M14.002 13a2 2 0 0 1-2 2h-10a2 2 0 0 1-2-2V5A2 2 0 0 1 2 3a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v8a2 2 0 0 1-1.998 2zM14 2H4a1 1 0 0 0-1 1h9.002a2 2 0 0 1 2 2v7A1 1 0 0 0 14 11V2zM2.002 4a1 1 0 0 0-1 1v8l2.646-2.354a.5.5 0 0 1 .63-.062l2.66 1.773 3.71-3.71a.5.5 0 0 1 .577-.094l1.777 1.947V5a1 1 0 0 0-1-1h-10z"/></svg>',
            click: () => {
              fileSelectorMode.value = 'editor'
              showFileSelector.value = true
            }
          },
          'table',
          '|',
          {
            name: 'import-md',
            tipPosition: 's',
            tip: '导入MD文件',
            className: 'right',
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.5 11.5a.5.5 0 0 1-1 0V7.707L6.354 8.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 7.707V11.5z"/><path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/></svg>',
            click: () => {
              triggerImportMdFile();
            }
          },
          'undo',
          'redo',
          '|',
          {
            name: 'switch-mode',
            tipPosition: 's',
            tip: '切换编辑模式',
            className: 'right',
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/></svg>',
            click: () => {
              try {
                console.log('切换模式按钮被点击');
                console.log('当前模式:', currentMode.value);

                // 切换编辑模式
                const modes = ['ir', 'wysiwyg', 'sv'];
                const currentIndex = modes.indexOf(currentMode.value);
                console.log('当前模式索引:', currentIndex);

                const nextIndex = (currentIndex + 1) % modes.length;
                const nextMode = modes[nextIndex];
                console.log('下一个模式:', nextMode);

                // 保存当前内容
                const content = vditor.value.getValue();
                console.log('当前内容长度:', content.length);
                console.log('开始切换模式...');

                // 销毁当前实例
                vditor.value.destroy();

                // 更新模式
                currentMode.value = nextMode;
                console.log('模式已更新为:', nextMode);

                // 重新创建实例
                vditor.value = new Vditor('vditor', {
                  height: 600,
                  mode: currentMode.value,
                  theme: document.documentElement.classList.contains('dark') ? 'dark' : 'classic',
                  placeholder: '请输入文章内容...',
                  toolbarConfig: {
                    pin: true
                  },
                  toolbar: [
                    'emoji',
                    'headings',
                    'bold',
                    'italic',
                    'strike',
                    'link',
                    '|',
                    'list',
                    'ordered-list',
                    'check',
                    'outdent',
                    'indent',
                    '|',
                    'quote',
                    'line',
                    'code',
                    'inline-code',
                    'insert-before',
                    'insert-after',
                    '|',
                    {
                      name: 'select-image',
                      tipPosition: 's',
                      tip: '从文件管理选择图片',
                      className: 'right',
                      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M4.502 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/><path d="M14.002 13a2 2 0 0 1-2 2h-10a2 2 0 0 1-2-2V5A2 2 0 0 1 2 3a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v8a2 2 0 0 1-1.998 2zM14 2H4a1 1 0 0 0-1 1h9.002a2 2 0 0 1 2 2v7A1 1 0 0 0 14 11V2zM2.002 4a1 1 0 0 0-1 1v8l2.646-2.354a.5.5 0 0 1 .63-.062l2.66 1.773 3.71-3.71a.5.5 0 0 1 .577-.094l1.777 1.947V5a1 1 0 0 0-1-1h-10z"/></svg>',
                      click: () => {
                        fileSelectorMode.value = 'editor'
                        showFileSelector.value = true
                      }
                    },
                    'table',
                    '|',
                    {
                      name: 'import-md',
                      tipPosition: 's',
                      tip: '导入MD文件',
                      className: 'right',
                      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8.5 11.5a.5.5 0 0 1-1 0V7.707L6.354 8.854a.5.5 0 1 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 7.707V11.5z"/><path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/></svg>',
                      click: () => {
                        triggerImportMdFile();
                      }
                    },
                    'undo',
                    'redo',
                    '|',
                    {
                      name: 'switch-mode',
                      tipPosition: 's',
                      tip: '切换编辑模式',
                      className: 'right',
                      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/></svg>',
                      click: () => {
                        try {
                          console.log('切换模式按钮被点击');
                          console.log('当前模式:', currentMode.value);

                          // 显示加载状态
                          isLoading.value = true;

                          // 切换编辑模式
                          const modes = ['ir', 'wysiwyg', 'sv'];
                          const currentIndex = modes.indexOf(currentMode.value);
                          console.log('当前模式索引:', currentIndex);

                          const nextIndex = (currentIndex + 1) % modes.length;
                          const nextMode = modes[nextIndex];
                          console.log('下一个模式:', nextMode);

                          // 保存当前内容
                          const content = vditor.value.getValue();
                          console.log('当前内容长度:', content.length);

                          // 切换模式
                          console.log('开始切换模式...');

                          // 销毁当前实例
                          vditor.value.destroy();

                          // 更新模式
                          currentMode.value = nextMode;
                          console.log('模式已更新为:', nextMode);

                          // 重新创建实例
                          initVditor();

                          // 设置内容
                          setTimeout(() => {
                            vditor.value.setValue(content);
                          }, 100);

                          // 显示提示消息
                          const modeNames = {
                            'ir': '即时渲染',
                            'wysiwyg': '所见即所得',
                            'sv': '分屏预览'
                          };
                          message.success(`已切换到${modeNames[nextMode]}模式`);
                          console.log('成功消息已显示');
                        } catch (error) {
                          console.error('切换模式时发生错误:', error);
                          message.error(`切换模式失败: ${error.message}`);
                          // 出错时也要关闭加载状态
                          isLoading.value = false;
                        }
                      }
                    },
                    'fullscreen',
                    'preview',
                    'outline',
                    'export',
                    'help'
                  ],
                  cache: {
                    enable: false
                  },
                  preview: {
                    maxWidth: 1000,
                    theme: {
                      current: document.documentElement.classList.contains('dark') ? 'dark' : 'light'
                    }
                    // 不再需要转换URL，因为后端已经返回完整URL
                  },
                  counter: {
                    enable: true,
                    type: 'text'
                  },
                  after: () => {
                    // 设置编辑器内容
                    vditor.value.setValue(content);
                    console.log('编辑器重新创建完成，内容已恢复');
                  }
                });
                console.log('模式已切换为:', nextMode);
              } catch (error) {
                console.error('切换模式时发生错误:', error);
                message.error(`切换模式失败: ${error.message}`);
              }
            }
          },
          'fullscreen',
          'preview',
          'outline',
          'export',
          'help'
        ],
        cache: {
          enable: false
        },
        preview: {
          maxWidth: 1000, // 预览区域最大宽度
          theme: {
            current: document.documentElement.classList.contains('dark') ? 'dark' : 'light'
          }
          // 不再需要转换URL，因为后端已经返回完整URL
        },
        counter: {
          enable: true, // 启用字数统计
          type: 'text' // 统计类型
        },

        after: () => {
          // 编辑模式下，设置编辑器内容
          if (currentPost.value.content) {
            vditor.value.setValue(currentPost.value.content)
          }

          // 内容加载完成后，关闭加载状态
          setTimeout(() => {
            isLoading.value = false;
            console.log('编辑器内容加载完成，关闭加载状态');
          }, 500); // 延迟500ms确保内容渲染完成
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
      // 如果已经在保存中，防止重复提交
      if (isSaving.value) {
        return
      }

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
      isSaving.value = true // 设置保存状态为true

      try {
        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (!token) {
          formError.value = '未登录或登录已过期，请重新登录'
          isSaving.value = false // 重置保存状态
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
      } finally {
        isSaving.value = false // 无论成功或失败，都重置保存状态
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

        // 检查封面图是否是随机封面图（以/images/blog/开头）
        if (currentPost.value.cover_image.startsWith('/images/blog/')) {
          // 如果是随机封面图，直接清空，不需要调用删除API
          console.log('随机封面图，直接清空:', currentPost.value.cover_image);
          currentPost.value.cover_image = '';
          message.success('封面图已移除');
          return;
        }

        // 从URL中提取文件名
        const imagePath = currentPost.value.cover_image.split('/').pop();
        console.log('删除封面图:', imagePath);

        // 正确处理token格式
        const lowerToken = token.toLowerCase();
        let cleanToken = token;
        if (lowerToken.includes('bearer')) {
          cleanToken = token.replace(/^\s*bearer\s+/i, '');
        }
        const formattedToken = `Bearer ${cleanToken}`;

        // 调用API删除图片
        await postApi.deleteImage(imagePath);

        // 清空封面图
        currentPost.value.cover_image = '';
        message.success('封面图删除成功');
      } catch (error) {
        console.error('删除封面图失败:', error);
        message.error(error.message || '删除封面图失败');

        // 即使删除失败，也清空封面图（用户体验考虑）
        currentPost.value.cover_image = '';
      }
    }

    // 封面图上传功能已移除，改为使用文件管理模块

    // 打开文件选择器用于选择封面图
    const openFileSelectorForCover = () => {
      fileSelectorMode.value = 'cover'
      showFileSelector.value = true
    }

    // 打开文件选择器用于编辑器插入图片
    const openFileSelectorForEditor = () => {
      fileSelectorMode.value = 'editor'
      showFileSelector.value = true
    }

    // 处理从文件管理器选择的图片
    const handleFileSelected = (file) => {
      if (!file) return

      console.log('选择的文件:', file);

      // 使用API_BASE_URL拼接完整URL
      let fileUrl = '';

      // 如果file.url已经是完整URL，则直接使用
      if (file.url && (file.url.startsWith('http://') || file.url.startsWith('https://'))) {
        fileUrl = file.url;
      }
      // 如果file.url是相对路径，则使用API_BASE_URL拼接
      else if (file.url) {
        // 确保路径格式正确
        const relativePath = file.url.startsWith('/') ? file.url : `/${file.url}`;
        fileUrl = `${API_BASE_URL}${relativePath}`;
      }
      // 如果没有url，则使用file.id构建下载URL
      else if (file.id) {
        fileUrl = `${API_BASE_URL}/api/v1/files/download/${file.id}`;
      }

      console.log('使用的文件URL:', fileUrl);

      // 根据文件选择器模式处理选择的文件
      if (fileSelectorMode.value === 'cover') {
        // 设置为封面图
        currentPost.value.cover_image = fileUrl
        message.success('封面图设置成功')
      } else {
        // 确保编辑器存在
        if (!vditor.value) return

        // 获取文件名
        const fileName = file.original_filename || `图片${Date.now()}`

        // 构建Markdown格式的图片标记
        const imageMarkdown = `![${fileName}](${fileUrl})`
        console.log('插入的Markdown:', imageMarkdown);

        // 在编辑器当前光标位置插入图片
        vditor.value.insertValue(imageMarkdown)
        message.success('图片插入成功')
      }

      // 关闭文件选择器
      showFileSelector.value = false
    }

    // 触发导入MD文件
    const mdFileInput = ref(null);

    const triggerImportMdFile = () => {
      mdFileInput.value.click();
    };

    // 处理MD文件导入
    const handleMdFileImport = async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      // 验证文件类型
      if (!file.name.toLowerCase().endsWith('.md') && !file.name.toLowerCase().endsWith('.markdown')) {
        message.error('请选择Markdown文件（.md或.markdown格式）');
        return;
      }

      try {
        // 显示加载状态
        isLoading.value = true;

        // 读取文件内容
        const reader = new FileReader();

        reader.onload = (e) => {
          try {
            const content = e.target.result;

            // 设置编辑器内容
            if (vditor.value) {
              vditor.value.setValue(content);
              message.success('Markdown文件导入成功');

              // 尝试从文件内容中提取标题
              const titleMatch = content.match(/^#\s+(.+)$/m);
              if (titleMatch && titleMatch[1] && !currentPost.value.title) {
                currentPost.value.title = titleMatch[1].trim();
              }
            } else {
              message.error('编辑器未初始化，请刷新页面后重试');
            }
          } catch (error) {
            console.error('处理文件内容时出错:', error);
            message.error(`导入失败: ${error.message || '未知错误'}`);
          } finally {
            isLoading.value = false;
            // 清空input的value，确保可以重复上传同一个文件
            event.target.value = '';
          }
        };

        reader.onerror = () => {
          message.error('读取文件失败');
          isLoading.value = false;
          event.target.value = '';
        };

        // 开始读取文件
        reader.readAsText(file);

      } catch (error) {
        console.error('导入MD文件失败:', error);
        message.error(`导入失败: ${error.message || '未知错误'}`);
        isLoading.value = false;
        event.target.value = '';
      }
    };

    // 随机封面图功能
    const selectRandomCoverImage = () => {
      // 从1到35随机选择一个数字（对应post-1.jpg到post-35.jpg）
      const randomNum = Math.floor(Math.random() * 35) + 1;
      const randomImagePath = `/images/blog/post-${randomNum}.jpg`;

      // 设置为封面图
      currentPost.value.cover_image = randomImagePath;
      message.success('已设置随机封面图');
    };

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
      isSaving,
      isLoading,
      removeCoverImage,
      // 文件选择器相关
      showFileSelector,
      handleFileSelected,
      openFileSelectorForCover,
      openFileSelectorForEditor,
      // 编辑器模式
      currentMode,
      // MD文件导入相关
      mdFileInput,
      triggerImportMdFile,
      handleMdFileImport,
      // 随机封面图功能
      selectRandomCoverImage
    }
  }
}
</script>
