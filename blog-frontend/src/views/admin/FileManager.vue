
<template>
  <div class="file-manager-page p-6">
    <!-- 页面头部 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 mb-4">
      <div class="flex justify-between items-center">
        <h2 class="text-xl font-bold text-secondary dark:text-dark-secondary">文件管理</h2>
        <GradientButton @click="showUploader = true">
          上传文件
        </GradientButton>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
      <div v-for="stat in fileStats"
           :key="stat.type"
           class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
        <div class="font-bold mb-2 text-secondary dark:text-dark-secondary">
          {{ stat.type || '全部' }}
        </div>
        <div class="text-center">
          <div class="text-2xl mb-2 text-primary dark:text-dark-primary">{{ stat.count }}</div>
          <div class="text-gray-500 dark:text-gray-400">{{ formatSize(stat.total_size) }}</div>
        </div>
      </div>
    </div>

    <!-- 文件列表 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
      <!-- 工具栏 -->
      <div class="flex justify-between items-center mb-4">
        <select v-model="fileType"
                class="px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-secondary dark:text-dark-secondary">
          <option value="">全部类型</option>
          <option v-for="type in fileTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>

        <div class="flex gap-2">
          <GradientButton
            v-if="selectedFiles.length"
            :colors="['#ff4d4d', '#ff1a1a']"
            @click="handleBatchDelete">
            批量删除
          </GradientButton>
          <GradientButton @click="refreshList">
            刷新
          </GradientButton>
        </div>
      </div>

      <!-- 加载状态 -->
      <LoadingSpinner v-if="loading" message="加载中..." />

      <!-- 文件列表表格 -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="p-4">
                <input type="checkbox"
                       :checked="isAllSelected"
                       @change="toggleSelectAll"
                       class="rounded border-gray-300 dark:border-gray-600">
              </th>
              <th class="p-4 text-left">文件名</th>
              <th class="p-4 text-left">类型</th>
              <th class="p-4 text-left">大小</th>
              <th class="p-4 text-left">上传时间</th>
              <th class="p-4 text-left">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file in files"
                :key="file.id"
                class="border-t border-gray-200 dark:border-gray-700">
              <td class="p-4">
                <input type="checkbox"
                       v-model="selectedFiles"
                       :value="file.id"
                       class="rounded border-gray-300 dark:border-gray-600">
              </td>
              <!-- 文件名和预览图 -->
              <td class="p-4">
                <div class="flex items-center gap-3">
                  <!-- 图片缩略图 -->
                  <div v-if="isImage(file)"
                       class="w-16 h-16 overflow-hidden rounded-md border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-lg transition-all duration-200 group relative cursor-pointer"
                       @click="previewImage(file)">
                    <img :src="getFileUrl(file)"
                         alt="预览"
                         class="thumbnail-image w-full h-full object-cover hover:scale-110 transition-transform duration-300" />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 flex items-center justify-center transition-all duration-300">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                      </svg>
                    </div>
                  </div>

                  <!-- 非图片文件图标 -->
                  <div v-else class="w-12 h-12 flex items-center justify-center overflow-hidden rounded-md border border-gray-200 dark:border-gray-700 shadow-sm bg-gray-100 dark:bg-gray-700">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>

                  <!-- 文件名 -->
                  <span class="truncate max-w-xs">{{ file.original_filename }}</span>
                </div>
              </td>
              <td class="p-4">{{ file.file_type }}</td>
              <td class="p-4">{{ formatSize(file.file_size) }}</td>
              <td class="p-4">{{ formatDate(file.created_at) }}</td>
              <td class="p-4">
                <div class="flex gap-2">
                  <GradientButton class="!min-w-0" @click="handleDownload(file)">
                    下载
                  </GradientButton>
                  <GradientButton class="!min-w-0" @click="handleRename(file)">
                    重命名
                  </GradientButton>
                  <GradientButton
                    class="!min-w-0"
                    :colors="['#ff4d4d', '#ff1a1a']"
                    @click="handleDelete(file)">
                    删除
                  </GradientButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div class="flex justify-center mt-4">
          <Pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            @update:current-page="handleCurrentChange"
            @update:page-size="handleSizeChange"
          />
        </div>
      </div>
    </div>

    <!-- 上传对话框 -->
    <Modal v-if="showUploader" @close="showUploader = false">
      <FileUploader
        @success="handleUploadSuccess"
        @close="showUploader = false"
      />
    </Modal>

    <!-- 图片预览模态框 -->
    <div v-if="previewVisible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75" @click="closePreview">
      <div class="relative max-w-4xl max-h-[90vh] p-2 bg-white dark:bg-gray-800 rounded-lg shadow-xl" @click.stop>
        <!-- 关闭按钮 -->
        <button
          @click="closePreview"
          class="absolute top-2 right-2 p-1 bg-gray-200 dark:bg-gray-700 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors z-10"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- 图片容器 -->
        <div class="flex flex-col items-center">
          <div class="overflow-auto max-h-[70vh] flex items-center justify-center p-4">
            <img
              :src="previewImageUrl"
              alt="图片预览"
              class="preview-image max-w-full max-h-[65vh] object-contain"
            />
          </div>

          <!-- 图片信息 -->
          <div class="w-full p-4 bg-gray-100 dark:bg-gray-700 rounded-b-lg">
            <p class="text-sm text-gray-700 dark:text-gray-300 mb-1 truncate">
              <span class="font-semibold">文件名:</span> {{ previewImageName }}
            </p>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              <span class="font-semibold">大小:</span> {{ previewImageSize ? formatSize(previewImageSize) : '未知' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { filesApi } from '@/api'
import { formatSize, formatDate } from '@/utils/format.js'
import FileUploader from '@/components/admin/FileUploader.vue'
import { GradientButton, LoadingSpinner } from '@/components/ui'
import Pagination from '@/components/common/Pagination.vue'
import Modal from '@/components/common/Modal.vue'
import message from '@/utils/message.js'
import { API_BASE_URL } from '@/config'

const loading = ref(false)
const files = ref([])
const fileStats = ref([])
const fileType = ref('')
const selectedFiles = ref([])
const showUploader = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 图片预览相关状态
const previewVisible = ref(false)
const previewImageUrl = ref('')
const previewImageName = ref('')
const previewImageSize = ref(0)

const fileTypes = ref(['image', 'document', 'video', 'audio', 'archive'])

const isAllSelected = computed(() => {
  return files.value.length > 0 && selectedFiles.value.length === files.value.length
})

const toggleSelectAll = (e) => {
  if (e.target.checked) {
    selectedFiles.value = files.value.map(file => file.id)
  } else {
    selectedFiles.value = []
  }
}

// 获取文件列表
const fetchFiles = async () => {
  loading.value = true
  try {
    const response = await filesApi.getFileList({
      file_type: fileType.value,
      page: currentPage.value,
      page_size: pageSize.value
    })
    files.value = response.items
    total.value = response.total
  } catch (error) {
    message.error('获取文件列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计信息
const fetchStats = async () => {
  try {
    const stats = await filesApi.getFileStats()
    fileStats.value = stats.type_stats
  } catch (error) {
    message.error('获取统计信息失败')
  }
}

// 刷新列表
const refreshList = () => {
  fetchFiles()
  fetchStats()
}

// 处理批量删除
const handleBatchDelete = async () => {
  if (!selectedFiles.value.length) return

  if (!confirm('确定要删除选中的文件吗？')) return

  try {
    await filesApi.batchDeleteFiles(selectedFiles.value)
    message.success('批量删除成功')
    refreshList()
  } catch (error) {
    message.error('批量删除失败')
  }
}

// 处理单个文件删除
const handleDelete = async (file) => {
  if (!confirm('确定要删除该文件吗？')) return

  try {
    await filesApi.deleteFile(file.id)
    message.success('删除成功')
    refreshList()
  } catch (error) {
    message.error('删除失败')
  }
}

// 处理文件下载
const handleDownload = async (file) => {
  try {
    const response = await filesApi.downloadFile(file.id)
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.download = file.original_filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    message.error('下载失败')
  }
}

// 处理文件重命名
const handleRename = async (file) => {
  const newName = prompt('请输入新文件名', file.original_filename)
  if (!newName || !newName.trim()) return

  try {
    await filesApi.renameFile(file.id, newName.trim())
    message.success('重命名成功')
    refreshList()
  } catch (error) {
    message.error('重命名失败')
  }
}

// 处理上传成功
const handleUploadSuccess = () => {
  showUploader.value = false
  refreshList()
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchFiles()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchFiles()
}

// 判断文件是否为图片
const isImage = (file) => {
  return file.file_type === 'image'
}

// 获取文件URL
const getFileUrl = (file) => {
  // 使用API_BASE_URL拼接完整URL

  // 如果file.url已经是完整URL，则直接使用
  if (file.url && (file.url.startsWith('http://') || file.url.startsWith('https://'))) {
    return file.url
  }
  // 如果file.url是相对路径，则使用API_BASE_URL拼接
  else if (file.url) {
    // 确保路径格式正确
    const relativePath = file.url.startsWith('/') ? file.url : `/${file.url}`
    return `${API_BASE_URL}${relativePath}`
  }
  // 如果file.file_path存在且是图片类型
  else if (file.file_path && file.file_type === 'image') {
    // 确保路径格式正确
    const filePath = file.file_path.startsWith('/') ? file.file_path : `/${file.file_path}`
    return `${API_BASE_URL}${filePath}`
  }
  // 如果没有url，则使用file.id构建下载URL
  else if (file.id) {
    return `${API_BASE_URL}/api/v1/files/download/${file.id}`
  }

  // 如果都没有，返回空字符串
  return ''
}

// 预览图片
const previewImage = (file) => {
  previewImageUrl.value = getFileUrl(file)
  previewImageName.value = file.original_filename
  previewImageSize.value = file.file_size
  previewVisible.value = true

  // 防止背景滚动
  document.body.style.overflow = 'hidden'
}

// 关闭预览
const closePreview = () => {
  previewVisible.value = false

  // 恢复背景滚动
  document.body.style.overflow = ''
}

// 添加键盘事件监听
const handleKeyDown = (e) => {
  if (e.key === 'Escape' && previewVisible.value) {
    closePreview()
  }
}

onMounted(() => {
  refreshList()

  // 添加键盘事件监听
  window.addEventListener('keydown', handleKeyDown)
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.file-manager-page {
  padding: 20px;
}

/* 缩略图悬停效果 */
.group:hover {
  transform: translateY(-2px);
}

/* 图片预览模态框动画 */
.fixed {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 表格行悬停效果 */
tr:hover td {
  background-color: rgba(0, 0, 0, 0.02);
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 暗色模式滚动条 */
.dark ::-webkit-scrollbar-track {
  background: #2d3748;
}

.dark ::-webkit-scrollbar-thumb {
  background: #4a5568;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #718096;
}

/* 预览图片样式 - 覆盖全局样式 */
.preview-image {
  position: static !important;
  width: auto !important;
  height: auto !important;
  max-width: 100% !important;
  max-height: 65vh !important;
  object-fit: contain !important;
  display: block !important;
  margin: 0 auto !important;
  border-radius: 0.375rem;
}

/* 缩略图样式 - 覆盖全局样式 */
.thumbnail-image {
  position: absolute !important;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  will-change: transform !important;
}
</style>



