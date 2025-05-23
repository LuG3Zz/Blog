<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">标签管理</h1>
      <div class="flex space-x-2">
        <button
          v-if="selectedTags.length > 0"
          @click="confirmBatchDelete"
          class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          批量删除 ({{ selectedTags.length }})
        </button>
        <button
          @click="showAddModal = true"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          添加标签
        </button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="mb-6">
      <div class="flex gap-4">
        <div class="flex-1">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索标签..."
            class="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          />
        </div>
      </div>
    </div>

    <!-- 标签列表 -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
      <div v-if="isLoading" class="p-4 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">加载中...</p>
      </div>
      <div v-else-if="filteredTags.length === 0" class="p-8 text-center">
        <p class="text-gray-600 dark:text-gray-400">没有找到标签</p>
      </div>
      <table v-else class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300">
              <div class="flex items-center">
                <input
                  id="select-all"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600"
                  :checked="selectAll"
                  @change="toggleSelectAll"
                />
                <label for="select-all" class="sr-only">全选</label>
              </div>
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              ID
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              标签名称
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              文章数量
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="tag in paginatedTags" :key="tag.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <input
                  :id="`select-tag-${tag.id}`"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600"
                  :checked="selectedTags.includes(tag.id)"
                  @change="toggleTagSelection(tag.id)"
                />
                <label :for="`select-tag-${tag.id}`" class="sr-only">选择标签</label>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-white">{{ tag.id }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-white">{{ tag.name }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-white">{{ tag.article_count || 0 }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                @click="editTag(tag)"
                class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 mr-3"
              >
                编辑
              </button>
              <button
                @click="confirmDelete(tag)"
                class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="mt-6 flex justify-center">
      <nav class="flex items-center">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded-l border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 disabled:opacity-50"
        >
          上一页
        </button>
        <div v-for="page in pagesAroundCurrent" :key="page">
          <button
            @click="goToPage(page)"
            :class="[
              'px-3 py-1 border-t border-b border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800',
              currentPage === page
                ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-300 font-medium'
                : 'text-gray-600 dark:text-gray-300'
            ]"
          >
            {{ page }}
          </button>
        </div>
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded-r border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 disabled:opacity-50"
        >
          下一页
        </button>
      </nav>
    </div>

    <!-- 添加标签模态框 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">添加标签</h2>
        <div class="mb-4">
          <label class="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2" for="tag-name">
            标签名称
          </label>
          <input
            id="tag-name"
            v-model="currentTag.name"
            type="text"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            placeholder="输入标签名称"
          />
          <p v-if="formError" class="mt-1 text-red-500 text-xs">{{ formError }}</p>
        </div>
        <div class="flex justify-end gap-2">
          <button
            @click="closeModals"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition"
          >
            取消
          </button>
          <button
            @click="saveTag"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            保存
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑标签模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">编辑标签</h2>
        <div class="mb-4">
          <label class="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2" for="edit-tag-name">
            标签名称
          </label>
          <input
            id="edit-tag-name"
            v-model="currentTag.name"
            type="text"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            placeholder="输入标签名称"
          />
          <p v-if="formError" class="mt-1 text-red-500 text-xs">{{ formError }}</p>
        </div>
        <div class="flex justify-end gap-2">
          <button
            @click="closeModals"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition"
          >
            取消
          </button>
          <button
            @click="saveTag"
            class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            保存
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认模态框 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">确认删除</h2>
        <p class="mb-6 text-gray-700 dark:text-gray-300">
          确定要删除标签 "{{ currentTag.name }}" 吗？此操作不可撤销。
        </p>
        <div class="flex justify-end gap-2">
          <button
            @click="closeModals"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition"
          >
            取消
          </button>
          <button
            @click="deleteTag"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          >
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- 批量删除确认模态框 -->
    <div v-if="showBatchDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">确认批量删除</h2>
        <p class="mb-6 text-gray-700 dark:text-gray-300">
          确定要删除选中的 {{ selectedTags.length }} 个标签吗？此操作不可撤销。
        </p>
        <div class="flex justify-end gap-2">
          <button
            @click="closeModals"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition"
          >
            取消
          </button>
          <button
            @click="batchDeleteTags"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
            :disabled="isBatchDeleting"
          >
            <span v-if="isBatchDeleting">删除中...</span>
            <span v-else>删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { tagApi } from '@/api'
import message from '@/utils/message.js'

export default {
  name: 'TagManage',
  setup() {
    // 状态数据
    const tags = ref([])
    const searchQuery = ref('')
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    const showAddModal = ref(false)
    const showEditModal = ref(false)
    const showDeleteModal = ref(false)
    const showBatchDeleteModal = ref(false)
    const currentTag = ref({ name: '' })
    const formError = ref('')
    const isLoading = ref(false)

    // 批量删除相关状态
    const selectedTags = ref([])
    const selectAll = ref(false)
    const isBatchDeleting = ref(false)

    // 获取标签数据
    const fetchTags = async () => {
      try {
        isLoading.value = true
        const response = await tagApi.getTags()
        tags.value = Array.isArray(response) ? response : []
      } catch (error) {
        console.error('获取标签失败:', error)
        message.error('获取标签失败')
        tags.value = []
      } finally {
        isLoading.value = false
      }
    }

    // 过滤标签
    const filteredTags = computed(() => {
      if (!searchQuery.value) return tags.value

      const query = searchQuery.value.toLowerCase()
      return tags.value.filter(tag =>
        tag.name.toLowerCase().includes(query)
      )
    })

    // 分页
    const totalPages = computed(() => {
      return Math.ceil(filteredTags.value.length / itemsPerPage.value)
    })

    const paginatedTags = computed(() => {
      const startIndex = (currentPage.value - 1) * itemsPerPage.value
      const endIndex = startIndex + itemsPerPage.value
      return filteredTags.value.slice(startIndex, endIndex)
    })

    const pagesAroundCurrent = computed(() => {
      const delta = 2
      const range = []
      const rangeWithDots = []
      let l

      for (let i = 1; i <= totalPages.value; i++) {
        if (
          i === 1 ||
          i === totalPages.value ||
          (i >= currentPage.value - delta && i <= currentPage.value + delta)
        ) {
          range.push(i)
        }
      }

      range.forEach(i => {
        if (l) {
          if (i - l === 2) {
            rangeWithDots.push(l + 1)
          } else if (i - l !== 1) {
            rangeWithDots.push('...')
          }
        }
        rangeWithDots.push(i)
        l = i
      })

      return rangeWithDots
    })

    const goToPage = (page) => {
      if (page < 1 || page > totalPages.value) return
      currentPage.value = page
    }

    // 添加标签
    const addTag = () => {
      currentTag.value = { name: '' }
      showAddModal.value = true
      formError.value = ''
    }

    // 编辑标签
    const editTag = (tag) => {
      currentTag.value = { ...tag }
      showEditModal.value = true
      formError.value = ''
    }

    // 保存标签
    const saveTag = async () => {
      try {
        // 验证表单
        if (!currentTag.value.name.trim()) {
          formError.value = '标签名称不能为空'
          return
        }

        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (!token) {
          formError.value = '未登录或登录已过期，请重新登录'
          return
        }

        if (showAddModal.value) {
          // 创建新标签
          await tagApi.createTag({ name: currentTag.value.name.trim() })
          message.success('添加标签成功')
        } else {
          // 更新标签
          await tagApi.updateTag(currentTag.value.id, { name: currentTag.value.name.trim() })
          message.success('更新标签成功')
        }

        // 关闭模态框并刷新数据
        closeModals()
        fetchTags()
      } catch (error) {
        console.error('保存标签失败:', error)
        formError.value = '保存标签失败: ' + (error.response?.data?.detail || error.message || '未知错误')
      }
    }

    // 确认删除
    const confirmDelete = (tag) => {
      currentTag.value = { ...tag }
      showDeleteModal.value = true
    }

    // 删除标签
    const deleteTag = async () => {
      try {
        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (!token) {
          message.error('未登录或登录已过期，请重新登录')
          return
        }

        // 调用API删除标签
        await tagApi.deleteTag(currentTag.value.id)
        message.success('删除标签成功')

        // 关闭模态框并刷新数据
        closeModals()
        fetchTags()
      } catch (error) {
        console.error('删除标签失败:', error)
        message.error('删除标签失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      }
    }

    // 切换标签选择状态
    const toggleTagSelection = (tagId) => {
      if (selectedTags.value.includes(tagId)) {
        // 如果已选中，则取消选中
        selectedTags.value = selectedTags.value.filter(id => id !== tagId)
        // 如果取消选中某个标签，全选状态也要取消
        selectAll.value = false
      } else {
        // 如果未选中，则选中
        selectedTags.value.push(tagId)
        // 检查是否所有标签都被选中
        selectAll.value = selectedTags.value.length === paginatedTags.value.length
      }
    }

    // 切换全选状态
    const toggleSelectAll = () => {
      selectAll.value = !selectAll.value

      if (selectAll.value) {
        // 全选：将当前页的所有标签ID添加到选中列表
        selectedTags.value = paginatedTags.value.map(tag => tag.id)
      } else {
        // 取消全选：清空选中列表
        selectedTags.value = []
      }
    }

    // 确认批量删除
    const confirmBatchDelete = () => {
      if (selectedTags.value.length === 0) return
      showBatchDeleteModal.value = true
    }

    // 批量删除标签
    const batchDeleteTags = async () => {
      if (selectedTags.value.length === 0) return

      isBatchDeleting.value = true
      try {
        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (!token) {
          message.error('未登录或登录已过期，请重新登录')
          return
        }

        // 调用API批量删除标签
        const response = await tagApi.batchDeleteTags(selectedTags.value)
        message.success(response.message || `成功删除 ${response.deleted_count} 个标签`)

        // 关闭确认对话框
        closeModals()

        // 清空选中列表
        selectedTags.value = []
        selectAll.value = false

        // 刷新标签列表
        fetchTags()
      } catch (error) {
        console.error('批量删除标签失败:', error)
        message.error('批量删除标签失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        isBatchDeleting.value = false
      }
    }

    // 关闭所有模态框
    const closeModals = () => {
      showAddModal.value = false
      showEditModal.value = false
      showDeleteModal.value = false
      showBatchDeleteModal.value = false
      currentTag.value = { name: '' }
      formError.value = ''
    }

    // 监听搜索查询变化，重置页码
    watch(searchQuery, () => {
      currentPage.value = 1
    })

    // 组件挂载时获取数据
    onMounted(() => {
      fetchTags()
    })

    return {
      tags,
      searchQuery,
      currentPage,
      filteredTags,
      paginatedTags,
      totalPages,
      showAddModal,
      showEditModal,
      showDeleteModal,
      showBatchDeleteModal,
      currentTag,
      formError,
      isLoading,
      addTag,
      editTag,
      saveTag,
      deleteTag,
      confirmDelete,
      closeModals,
      goToPage,
      pagesAroundCurrent,
      // 批量删除相关
      selectedTags,
      selectAll,
      toggleTagSelection,
      toggleSelectAll,
      confirmBatchDelete,
      batchDeleteTags,
      isBatchDeleting
    }
  }
}
</script>
