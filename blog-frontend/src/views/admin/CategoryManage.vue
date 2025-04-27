<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6 dark:text-white">分类管理</h1>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold dark:text-gray-200">分类列表</h2>
        <div class="flex space-x-2">
          <button
            v-if="selectedCategories.length > 0"
            @click="confirmBatchDelete"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            批量删除 ({{ selectedCategories.length }})
          </button>
          <button
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            @click="showAddModal = true"
          >
            添加分类
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
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
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">分类名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">描述</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-if="isLoading">
              <td colspan="5" class="px-6 py-4 text-center text-gray-500 dark:text-gray-300">加载中...</td>
            </tr>
            <tr v-else-if="error">
              <td colspan="5" class="px-6 py-4 text-center text-red-500">{{ error }}</td>
            </tr>
            <tr v-else v-for="category in categories" :key="category.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                <div class="flex items-center">
                  <input
                    :id="`select-category-${category.id}`"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600"
                    :checked="selectedCategories.includes(category.id)"
                    @change="toggleCategorySelection(category.id)"
                  />
                  <label :for="`select-category-${category.id}`" class="sr-only">选择分类</label>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ category.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ category.name }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-300">{{ category.description }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                <button
                  class="text-blue-500 hover:text-blue-700 mr-3"
                  @click="editCategory(category)"
                >
                  编辑
                </button>
                <button
                  class="text-red-500 hover:text-red-700"
                  @click="deleteCategory(category.id)"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加/编辑分类模态框 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAddModal = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4 dark:text-white">{{ isEditing ? '编辑分类' : '添加分类' }}</h3>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">分类名称</label>
          <input
            v-model="currentCategory.name"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="输入分类名称"
            required
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">描述</label>
          <textarea
            v-model="currentCategory.description"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="输入分类描述"
            rows="3"
            required
          ></textarea>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            class="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
            @click="showAddModal = false"
          >
            取消
          </button>
          <button
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            @click="saveCategory"
          >
            保存
          </button>
        </div>
      </div>
    </div>

    <!-- 批量删除确认对话框 -->
    <div
      v-if="showBatchDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showBatchDeleteModal = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4 dark:text-white">确认批量删除</h3>
        <p class="mb-6 text-gray-700 dark:text-gray-300">
          确定要删除选中的 {{ selectedCategories.length }} 个分类吗？此操作不可撤销。
          <span v-if="hasArticlesWarning" class="block mt-2 text-yellow-600 dark:text-yellow-400">
            注意：如果分类下有文章，将无法删除该分类。
          </span>
        </p>
        <div class="flex justify-end space-x-3">
          <button
            class="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
            @click="showBatchDeleteModal = false"
          >
            取消
          </button>
          <button
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
            @click="batchDeleteCategories"
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
import { ref, onMounted } from 'vue'
import { categoryApi } from '@/api'
import message from '@/utils/message'

export default {
  name: 'CategoryManage',
  setup() {
    const categories = ref([])
    const isLoading = ref(false)
    const error = ref(null)
    const showAddModal = ref(false)
    const isEditing = ref(false)
    const currentCategory = ref({ id: null, name: '', description: '' })

    // 批量删除相关状态
    const selectedCategories = ref([])
    const selectAll = ref(false)
    const showBatchDeleteModal = ref(false)
    const isBatchDeleting = ref(false)
    const hasArticlesWarning = ref(true) // 默认显示警告

    // 加载分类数据
    const loadCategories = async () => {
      isLoading.value = true
      error.value = null
      try {
        categories.value = await categoryApi.getCategories()
      } catch (err) {
        error.value = err.message
        message.error('加载分类数据失败')
      } finally {
        isLoading.value = false
      }
    }

    const editCategory = (category) => {
      currentCategory.value = { ...category }
      isEditing.value = true
      showAddModal.value = true
    }

    const handleDeleteCategory = async (id) => {
      if (confirm('确定要删除这个分类吗？')) {
        try {
          await categoryApi.deleteCategory(id)
          await loadCategories()
          message.success('删除分类成功')
        } catch (err) {
          message.error('删除分类失败')
        }
      }
    }

    const saveCategory = async () => {
      try {
        // 获取token
        const token = localStorage.getItem('token')
        if (!token) {
          message.error('未登录或登录已过期，请重新登录')
          return
        }

        if (isEditing.value) {
          await categoryApi.updateCategory(currentCategory.value.id, {
            name: currentCategory.value.name,
            description: currentCategory.value.description
          })
          message.success('更新分类成功')
        } else {
          await categoryApi.createCategory({
            name: currentCategory.value.name,
            description: currentCategory.value.description
          }, token)
          message.success('创建分类成功')
        }

        showAddModal.value = false
        currentCategory.value = { id: null, name: '', description: '' }
        isEditing.value = false
        await loadCategories()
      } catch (err) {
        message.error(isEditing.value ? '更新分类失败' : '创建分类失败')
      }
    }

    // 切换分类选择状态
    const toggleCategorySelection = (categoryId) => {
      if (selectedCategories.value.includes(categoryId)) {
        // 如果已选中，则取消选中
        selectedCategories.value = selectedCategories.value.filter(id => id !== categoryId)
        // 如果取消选中某个分类，全选状态也要取消
        selectAll.value = false
      } else {
        // 如果未选中，则选中
        selectedCategories.value.push(categoryId)
        // 检查是否所有分类都被选中
        selectAll.value = selectedCategories.value.length === categories.value.length
      }
    }

    // 切换全选状态
    const toggleSelectAll = () => {
      selectAll.value = !selectAll.value

      if (selectAll.value) {
        // 全选：将所有分类ID添加到选中列表
        selectedCategories.value = categories.value.map(category => category.id)
      } else {
        // 取消全选：清空选中列表
        selectedCategories.value = []
      }
    }

    // 确认批量删除
    const confirmBatchDelete = () => {
      if (selectedCategories.value.length === 0) return
      showBatchDeleteModal.value = true
    }

    // 批量删除分类
    const batchDeleteCategories = async () => {
      if (selectedCategories.value.length === 0) return

      isBatchDeleting.value = true
      try {
        // 从localStorage获取token
        const token = localStorage.getItem('token')
        if (!token) {
          message.error('未登录或登录已过期，请重新登录')
          return
        }

        // 调用API批量删除分类
        const response = await categoryApi.batchDeleteCategories(selectedCategories.value)

        // 显示结果消息
        if (response.not_deleted && response.not_deleted.length > 0) {
          const notDeletedCount = response.not_deleted.length
          const deletedCount = response.deleted_count

          if (deletedCount > 0) {
            message.success(`成功删除 ${deletedCount} 个分类，${notDeletedCount} 个分类无法删除`)
          } else {
            message.warning(`所选分类无法删除，可能是因为分类下有文章`)
          }
        } else {
          message.success(response.message || `成功删除 ${response.deleted_count} 个分类`)
        }

        // 关闭确认对话框
        showBatchDeleteModal.value = false

        // 清空选中列表
        selectedCategories.value = []
        selectAll.value = false

        // 刷新分类列表
        await loadCategories()
      } catch (error) {
        console.error('批量删除分类失败:', error)
        message.error('批量删除分类失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      } finally {
        isBatchDeleting.value = false
      }
    }

    onMounted(() => {
      loadCategories()
    })

    return {
      categories,
      isLoading,
      error,
      showAddModal,
      isEditing,
      currentCategory,
      editCategory,
      deleteCategory: handleDeleteCategory,
      saveCategory,
      // 批量删除相关
      selectedCategories,
      selectAll,
      toggleCategorySelection,
      toggleSelectAll,
      showBatchDeleteModal,
      isBatchDeleting,
      hasArticlesWarning,
      confirmBatchDelete,
      batchDeleteCategories
    }
  }
}
</script>

<style scoped>
/* 可以添加一些自定义样式 */
</style>