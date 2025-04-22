<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6 dark:text-white">分类管理</h1>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold dark:text-gray-200">分类列表</h2>
        <button
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          @click="showAddModal = true"
        >
          添加分类
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">分类名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">描述</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-if="isLoading">
              <td colspan="4" class="px-6 py-4 text-center text-gray-500 dark:text-gray-300">加载中...</td>
            </tr>
            <tr v-else-if="error">
              <td colspan="4" class="px-6 py-4 text-center text-red-500">{{ error }}</td>
            </tr>
            <tr v-else v-for="category in categories" :key="category.id">
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
      saveCategory
    }
  }
}
</script>

<style scoped>
/* 可以添加一些自定义样式 */
</style>