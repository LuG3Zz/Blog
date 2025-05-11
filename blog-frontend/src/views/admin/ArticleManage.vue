<template>
  <div class="space-y-6">
    <!-- 头部区域 -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-gray-800 dark:text-white">文章管理</h1>
      <button
        @click="navigateToAddArticle"
        class="px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-lg hover:bg-gray-800 dark:hover:bg-gray-300 transition-colors duration-300"
      >
        添加文章
      </button>
    </div>

    <!-- 文章列表 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <!-- 搜索和筛选 -->
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="relative flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索文章标题或内容"
              class="w-full px-4 py-2 pr-10 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200"
            />
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <select
            v-model="categoryFilter"
            class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200"
          >
            <option value="">全部分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.name || (category.category ? category.category.name : '')">
              {{ category.name || (category.category ? category.category.name : '') }}
            </option>
          </select>
        </div>
      </div>

      <!-- 表格 -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700 table-fixed">
          <thead class="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-1/3">
                标题
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-1/6">
                分类
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-1/8">
                创建日期
              </th>

              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-1/12">
                是否精选
              </th>
              <th scope="col" class="px-6 py-3 text-md text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-1/6">
                操作
              </th>
            </tr>
          </thead>

          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="(post, index) in paginatedPosts" :key="index" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <div class="w-full">
                    <div
                      class="text-1xl font-medium text-gray-900 dark:text-white truncate max-w-xs cursor-pointer hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                      :title="post.title"
                      @click="viewArticle(post)"
                    >
                      {{ post.title }}
                      <span class="ml-1 text-xs text-blue-500 opacity-70">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </span>
                    </div>
                    <div class="text-sm text-gray-400 dark:text-gray-400 truncate max-w-xs" :title="getTagsDisplay(post)">
                      {{ getTagsDisplay(post) }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">
                  {{ post.category ? (typeof post.category === 'object' ? post.category.name : post.category) : post.category_name || '' }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(post.created_at) }}</div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <!-- 开关按钮 - 只有管理员和编辑可以设置精选 -->
                  <template v-if="canToggleFeatured(post)">
                    <label class="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        :checked="post.is_featured"
                        class="sr-only peer"
                        @change="toggleFeatured(post)"
                      >
                      <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                    </label>
                  </template>
                  <!-- 状态文本 - 所有人都可以看到 -->
                  <span
                    :class="post.is_featured ? 'ml-3 text-xs font-medium text-green-600 dark:text-green-400' : 'ml-3 text-xs font-medium text-gray-500 dark:text-gray-400'"
                  >
                    {{ post.is_featured ? '已精选' : '未精选' }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <!-- 编辑按钮 - 管理员、编辑和作者可以编辑 -->
                <button
                  v-if="canEditArticle(post)"
                  @click="navigateToEditArticle(post)"
                  class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-200 mr-3"
                >
                  编辑
                </button>
                <!-- 评论按钮 - 所有人都可以查看评论 -->
                <button
                  @click="viewArticleComments(post)"
                  class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-200 mr-3"
                  title="查看评论"
                >
                  评论
                </button>
                <!-- 删除按钮 - 管理员可以删除任何文章，编辑和作者只能删除自己的文章 -->
                <button
                  v-if="canDeleteArticle(post)"
                  @click="confirmDelete(post, index)"
                  class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-200"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
              <!-- 加载状态 -->

        </table>
      </div>
      <LoadingSpinner
      v-if="isLoading"
      message="正在加载文章数据..."
      class="py-8"
    />

    <!-- 错误提示 -->
    <ErrorDisplay
      v-else-if="error"
      :message="error"
      @retry="loadData"
      class="p-4"
    />

      <!-- 空状态 -->
      <EmptyState
        v-if="!isLoading && !error && filteredPosts.total === 0"
        message="没有找到匹配的文章"
        description="请尝试修改搜索条件或清除分类筛选"
        class="py-8"
      />

      <!-- 分页 -->
      <Pagination
        v-if="!isLoading && !error && filteredPosts.total > 0"
        v-model:currentPage="currentPage"
        :total="filteredPosts.total"
        :pageSize="itemsPerPage"
      />
    </div>
    <!-- 删除确认对话框 -->
    <DeleteConfirmDialog
      v-model:show="showDeleteModal"
      title="确认删除"
      :message="deleteConfirmMessage"
      @confirm="deletePost"
      @cancel="closeModals"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { postApi, categoryApi } from '@/api'
import message from '@/utils/message.js'
// 使用自定义日期工具函数
import { formatDateTimeWithTimeZone } from '@/utils/date-utils'
import DeleteConfirmDialog from '@/components/common/DeleteConfirmDialog.vue'
import Pagination from '@/components/common/Pagination.vue'
import { ErrorDisplay, LoadingSpinner, EmptyState } from '@/components/ui'
import { useUserStore } from '@/stores'
import { isSuperAdmin, isEditor } from '@/utils/permission'

export default {
  name: 'ArticleManage',
  components: {
    DeleteConfirmDialog,
    Pagination,
    ErrorDisplay,
    LoadingSpinner,
    EmptyState
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()

    // 状态数据
    const posts = ref([])
    const categories = ref([])
    const searchQuery = ref('')
    const categoryFilter = ref('')
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    const totalItems = ref(0) // 添加总条目数变量
    // 删除模态框相关状态变量，仅保留必要的变量
    const showDeleteModal = ref(false) // 保留删除确认对话框状态
    const editIndex = ref(-1) // 保留编辑索引变量，用于删除操作
    // 删除 vditor 相关状态变量
    const isLoading = ref(false)
    const error = ref('')

    // 用户角色相关计算属性
    const isUserSuperAdmin = computed(() => isSuperAdmin(userStore.userInfo))
    const isUserEditor = computed(() => isEditor(userStore.userInfo))

    // 检查当前用户是否是文章的作者
    const isArticleAuthor = (post) => {
      if (!post || !userStore.userInfo) return false
      return post.author_id === userStore.userInfo.id
    }

    // 当前操作的文章
    const currentPost = ref({
      title: '',
      category: '',
      category_id: null,
      summary: '',
      excerpt: '',
      content: '',
      date: '',
      is_featured: false,
      cover_image: '',
      tags: [],
      status: 'published'
    })

    // 删除未使用的错误信息变量

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        // 使用自定义日期工具函数，将UTC时间转换为本地时间
        return formatDateTimeWithTimeZone(dateString)
      } catch (error) {
        console.error('日期格式化错误:', error)
        return dateString
      }
    }

    // 使用 axios 全局拦截器添加 token，不再需要手动处理 token

    // 获取文章数据
    const fetchPosts = async () => {
      try {
        error.value = ''
        isLoading.value = true

        // 构建查询参数，使用 API 的分页功能
        const params = {
          skip: (currentPage.value - 1) * itemsPerPage.value,
          limit: itemsPerPage.value
        }

        // 添加分类筛选
        if (categoryFilter.value) {
          params.category = categoryFilter.value
        }

        // 获取文章数据
        const response = await postApi.getPosts(params)

        // 添加调试日志
        console.log('API返回的文章数据格式:', response)

        // 处理文章数据，确保数据结构一致
        // 检查response是否是对象且包含items字段
        const articlesArray = Array.isArray(response) ? response :
                             (response && response.items ? response.items : [])

        // 处理文章数据，确保数据结构一致
        posts.value = articlesArray.map(post => ({
          ...post,
          category_name: post.category ?
            (typeof post.category === 'object' ? post.category.name : post.category) :
            post.category_name || '',
          tags: post.tags || '',
          author_name: post.author ?
            (typeof post.author === 'object' ? post.author.username : post.author) :
            post.author_name || ''
        }))

        // 获取总数据量，用于分页
        // 如果 API 返回总数量，使用 API 返回的值
        if (response && response.total !== undefined && !isNaN(response.total)) {
          // API 返回了有效的总数量
          totalItems.value = response.total
          console.log('使用API返回的总数量:', totalItems.value)
        } else if (response && response.count !== undefined && !isNaN(response.count)) {
          // 有些 API 可能使用 count 字段
          totalItems.value = response.count
          console.log('使用API返回的count字段:', totalItems.value)
        } else {
          // API 没有返回总数量，使用估算值
          // 如果当前页数据少于每页数量，说明这是最后一页
          if (posts.value.length < itemsPerPage.value) {
            totalItems.value = Math.max(0, (currentPage.value - 1) * itemsPerPage.value) + posts.value.length
          } else {
            // 否则，至少还有一页
            totalItems.value = currentPage.value * itemsPerPage.value + 1
          }

          // 确保总数量至少等于当前显示的数量
          totalItems.value = Math.max(totalItems.value, posts.value.length)
          console.log('使用估算的总数量:', totalItems.value)
        }

        // 计算最大页数
        const maxPage = Math.max(1, Math.ceil(totalItems.value / itemsPerPage.value))

        // 确保当前页不超出范围
        if (currentPage.value > maxPage) {
          currentPage.value = maxPage
        }
      } catch (err) {
        console.error('获取文章失败:', err)
        error.value = err.message || '获取文章失败，请稍后重试'
        posts.value = []
      } finally {
        isLoading.value = false
      }
    }

    // 获取分类数据
    const fetchCategories = async () => {
      try {
        // 使用 API 获取分类数据
        const response = await categoryApi.getCategories()

        // 处理分类数据，确保数据结构一致
        categories.value = Array.isArray(response) ? response : []

        // 如果分类为空，显示提示
        if (categories.value.length === 0) {
          console.warn('未找到分类数据')
        }
      } catch (err) {
        console.error('获取分类失败:', err)
        message.error('获取分类失败，将使用空列表')
        categories.value = []
      }
    }

    // 初始化数据
    onMounted(() => {
      fetchPosts()
      fetchCategories()
    })

    // 筛选文章（仅在前端进行搜索筛选）
    const filteredPosts = computed(() => {
      // 确保 totalItems 是有效数字
      const safeTotal = isNaN(totalItems.value) || totalItems.value === undefined ? posts.value.length : totalItems.value

      // 如果没有搜索关键词，直接返回所有文章
      if (!searchQuery.value) {
        return {
          data: posts.value,
          total: safeTotal
        }
      }

      // 按搜索关键词筛选
      const query = searchQuery.value.toLowerCase()
      const filtered = posts.value.filter(post =>
        (post.title && post.title.toLowerCase().includes(query)) ||
        (post.excerpt && post.excerpt.toLowerCase().includes(query)) ||
        (post.content && post.content.toLowerCase().includes(query)) ||
        (post.category_name && post.category_name.toLowerCase().includes(query))
      )

      return {
        data: filtered,
        total: filtered.length
      }
    })

    // 分页数据（使用已经分页的数据）
    const paginatedPosts = computed(() => {
      // 如果有搜索关键词，则使用前端筛选的结果
      if (searchQuery.value) {
        // 确保数据存在
        if (!filteredPosts.value.data || filteredPosts.value.data.length === 0) {
          return []
        }

        // 计算当前页的数据
        const page = Math.max(1, currentPage.value) // 确保页码至少为 1
        const pageSize = Math.max(1, itemsPerPage.value) // 确保每页至少显示 1 条
        const startIndex = (page - 1) * pageSize

        // 返回当前页的数据
        return filteredPosts.value.data.slice(startIndex, startIndex + pageSize)
      }

      // 如果没有搜索，直接返回 API 分页的结果
      return posts.value
    })

    // 总页数
    const totalPages = computed(() => {
      // 确保总条目数是有效数字
      const total = filteredPosts.value.total || 0
      // 确保每页条目数是有效数字
      const pageSize = itemsPerPage.value || 10
      // 计算总页数，至少为 1 页
      return Math.max(1, Math.ceil(total / pageSize))
    })



    // 删除确认消息
    const deleteConfirmMessage = computed(() => {
      return `您确定要删除文章 "${currentPost.value.title}" 吗？此操作无法撤销。`
    })

    // 删除添加和编辑文章的模态框相关代码

    // 确认删除
    const confirmDelete = (post, index) => {
      currentPost.value = { ...post }
      // 计算在原数组中的实际索引
      const actualIndex = posts.value.findIndex(p => p.title === post.title && p.date === post.date)
      editIndex.value = actualIndex !== -1 ? actualIndex : index
      showDeleteModal.value = true
    }

    // 删除保存文章的方法，因为我们不再使用模态框进行编辑

    // 删除文章
    const deletePost = async () => {
      if (editIndex.value > -1 && currentPost.value.id) {
        try {
          // 使用 axios 全局拦截器添加 token，不再需要手动处理 token

          // 调用API删除文章
          await postApi.deletePost(currentPost.value.id)

          // 从本地列表中移除
          posts.value.splice(editIndex.value, 1)
          message.success('删除文章成功')
          closeModals()
        } catch (error) {
          console.error('删除文章失败:', error)
          message.error(error.message || '删除文章失败，请稍后再试')
        }
      }
    }

    // 关闭删除确认对话框
    const closeModals = () => {
      showDeleteModal.value = false
      currentPost.value = {
        title: '',
        category: '',
        category_id: null,
        summary: '',
        excerpt: '',
        content: '',
        date: '',
        is_featured: false,
        cover_image: '',
        tags: [],
        status: 'published'
      }
      editIndex.value = -1
    }

    // 删除重复的 watch 函数



    // 删除 Vditor 编辑器相关代码

    // 删除监听暗黑模式变化的代码

    // 监听分类筛选条件变化，重新获取数据
    watch(categoryFilter, () => {
      currentPage.value = 1
      fetchPosts()
    })

    // 监听搜索条件变化，重置到第一页（前端搜索）
    watch(searchQuery, () => {
      currentPage.value = 1
    })

    // 监听当前页变化
    watch(currentPage, (newPage, oldPage) => {
      // 滚动到页面顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })

      // 如果没有搜索关键词且页码变化，则重新获取数据
      if (!searchQuery.value && newPage !== oldPage) {
        fetchPosts()
      }
    })

    // 导航到添加文章页面
    const navigateToAddArticle = () => {
      router.push('/admin/articles/edit')
    }



    // 导航到编辑文章页面
    const navigateToEditArticle = (post) => {
      router.push({
        path: '/admin/articles/edit',
        query: { id: post.id }
      })
    }

    // 查看文章评论
    const viewArticleComments = (post) => {
      // 跳转到评论管理页面，并传递文章ID作为查询参数
      router.push({
        path: '/admin/comments',
        query: { articleId: post.id, articleTitle: post.title }
      })
    }

    // 查看文章详情
    const viewArticle = (post) => {
      // 在新标签页中打开文章详情页面
      const url = `/article/${post.id}`
      window.open(url, '_blank')
    }

    // 切换文章精选状态
    const toggleFeatured = async (post) => {
      try {
        // 切换状态
        const newFeaturedStatus = !post.is_featured

        // 调用API更新文章
        await postApi.updatePost(post.id, {
          is_featured: newFeaturedStatus
        })

        // 更新本地状态
        post.is_featured = newFeaturedStatus

        // 显示成功消息
        message.success(`文章已${newFeaturedStatus ? '设为精选' : '取消精选'}`)
      } catch (error) {
        console.error('更新文章精选状态失败:', error)
        message.error('更新文章精选状态失败，请稍后重试')

        // 恢复原状态（UI回滚）
        post.is_featured = !post.is_featured
      }
    }

    // 获取文章标签显示文本
    const getTagsDisplay = (post) => {
      // 如果有 tags_list 字段，使用新格式
      if (post.tags_list && Array.isArray(post.tags_list)) {
        return post.tags_list.map(tag => tag.name).join(' ')
      }

      // 兼容旧格式
      if (!post.tags) return ''

      if (typeof post.tags === 'string') {
        return post.tags.split(',').join(' ')
      }

      if (Array.isArray(post.tags)) {
        return post.tags.map(tag => {
          return (typeof tag === 'object' && tag !== null) ? (tag.name || '') : tag
        }).join(' ')
      }

      return ''
    }

    // 权限检查函数
    const canEditArticle = (post) => {
      // 管理员可以编辑任何文章
      if (isUserSuperAdmin.value) return true

      // 编辑可以编辑任何文章
      if (isUserEditor.value) return true

      // 作者可以编辑自己的文章
      return isArticleAuthor(post)
    }

    const canDeleteArticle = (post) => {
      // 管理员可以删除任何文章
      if (isUserSuperAdmin.value) return true

      // 编辑只能删除自己的文章
      if (isUserEditor.value) return isArticleAuthor(post)

      // 作者可以删除自己的文章
      return isArticleAuthor(post)
    }

    const canToggleFeatured = (post) => {
      // 只有管理员和编辑可以设置精选
      return isUserSuperAdmin.value || isUserEditor.value
    }

    return {
      posts,
      categories,
      searchQuery,
      categoryFilter,
      currentPage,
      paginatedPosts,
      filteredPosts,
      totalPages,
      showDeleteModal,
      currentPost,
      isLoading,
      error,
      totalItems,
      formatDate,
      getTagsDisplay,
      deletePost,
      confirmDelete,
      closeModals,
      navigateToAddArticle,
      navigateToEditArticle,
      viewArticleComments,
      viewArticle,
      toggleFeatured,
      loadData: fetchPosts,
      deleteConfirmMessage,
      // 权限检查函数
      canEditArticle,
      canDeleteArticle,
      canToggleFeatured,
      isUserSuperAdmin,
      isUserEditor,
      isArticleAuthor
    }
  }
}
</script>