<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-800 dark:text-white">选择文件</h3>
      <button
        @click="$emit('close')"
        class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="flex flex-col md:flex-row gap-4 mb-4">
      <div class="flex-1">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索文件名..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
        />
      </div>
      <div>
        <select
          v-model="fileType"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
        >
          <option value="">全部类型</option>
          <option value="image">图片</option>
          <option value="document">文档</option>
          <option value="video">视频</option>
          <option value="audio">音频</option>
          <option value="archive">压缩包</option>
        </select>
      </div>
      <div>
        <button
          @click="showUploader = true"
          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 font-medium"
        >
          上传图片
        </button>
      </div>
    </div>

    <!-- 上传图片区域 -->
    <div v-if="showUploader" class="mb-6 p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800">
      <div class="flex justify-between items-center mb-3">
        <h4 class="text-md font-medium text-gray-800 dark:text-white">上传图片</h4>
        <button
          @click="showUploader = false"
          class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 拖放上传区域 -->
      <div
        class="upload-area p-6 border-2 border-dashed rounded-lg text-center cursor-pointer transition-colors"
        :class="isDragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-600'"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onFileDrop"
        @click="triggerFileInput"
      >
        <input
          type="file"
          ref="fileInput"
          class="hidden"
          @change="onFileChange"
          accept="image/*"
          multiple
        />

        <div v-if="!isUploading">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-500 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <h3 class="text-lg font-medium text-gray-700 dark:text-gray-300 mb-1">拖放图片到此处或点击上传</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            支持的图片格式: JPG, PNG, GIF, WEBP
            <br>
            最大文件大小: 5MB
          </p>
        </div>

        <div v-else class="py-4">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500 mx-auto mb-3"></div>
          <p class="text-sm text-gray-600 dark:text-gray-400">上传中... {{ uploadProgress }}%</p>
          <div class="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: uploadProgress + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- 已选文件列表 -->
      <div v-if="selectedFiles.length > 0 && !isUploading" class="mt-4">
        <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">已选择 {{ selectedFiles.length }} 个文件:</h4>
        <ul class="space-y-2">
          <li v-for="(file, index) in selectedFiles" :key="index" class="flex items-center justify-between bg-gray-50 dark:bg-gray-800 p-2 rounded">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span class="text-sm text-gray-700 dark:text-gray-300">{{ file.name }}</span>
              <span class="ml-2 text-xs text-gray-500 dark:text-gray-400">({{ formatFileSize(file.size) }})</span>
            </div>
            <button @click="removeFile(index)" class="text-red-500 hover:text-red-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </li>
        </ul>
      </div>

      <!-- 错误信息 -->
      <div v-if="error" class="mt-3 text-sm text-red-500">{{ error }}</div>

      <!-- 上传按钮 -->
      <div class="mt-4 flex justify-end">
        <button
          @click="uploadFiles"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          :disabled="isUploading || selectedFiles.length === 0"
        >
          上传文件
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
    </div>

    <!-- 文件列表 -->
    <div v-else class="max-h-[60vh] overflow-y-auto border border-gray-200 dark:border-gray-700 rounded-md">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              预览
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              文件名
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              类型
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              大小
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="file in filteredFiles" :key="file.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="px-6 py-4 whitespace-nowrap">
              <!-- 图片缩略图 -->
              <div v-if="isImage(file)"
                   class="w-20 h-20 overflow-hidden rounded-md border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-lg transition-all duration-200 group relative cursor-pointer"
                   @click="previewImage(file)">
                <img :src="getFileUrl(file)"
                     alt="预览"
                     class="thumbnail-image w-full h-full object-cover hover:scale-110 transition-transform duration-300" />
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 flex items-center justify-center transition-all duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                  </svg>
                </div>
              </div>
              <!-- 非图片文件图标 -->
              <div v-else class="w-16 h-16 flex items-center justify-center overflow-hidden rounded-md border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow duration-200 bg-gray-100 dark:bg-gray-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-gray-100">{{ file.original_filename }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ file.file_type }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ formatSize(file.file_size) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex space-x-2">
                <button
                  @click="selectFile(file)"
                  class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 font-medium"
                >
                  选择此文件
                </button>
                <button
                  @click="confirmDeleteFile(file)"
                  class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200 font-medium"
                >
                  删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="mt-4 flex justify-center">
      <Pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        @update:current-page="handleCurrentChange"
        @update:page-size="handleSizeChange"
      />
    </div>

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

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">确认删除</h3>
        <p class="text-gray-700 dark:text-gray-300 mb-6">
          您确定要删除文件 <span class="font-semibold">{{ fileToDelete?.original_filename }}</span> 吗？此操作无法撤销。
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteConfirm = false"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200"
          >
            取消
          </button>
          <button
            @click="deleteFile"
            class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { filesApi } from '@/api';
import { formatSize } from '@/utils/format.js';
import Pagination from '@/components/common/Pagination.vue';
import message from '@/utils/message.js';
import { API_BASE_URL } from '@/config';

const props = defineProps({
  fileType: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['close', 'select']);

// 状态
const loading = ref(false);
const files = ref([]);
const searchQuery = ref('');
const fileType = ref(props.fileType);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 上传相关状态
const showUploader = ref(false);
const fileInput = ref(null);
const selectedFiles = ref([]);
const isDragging = ref(false);
const isUploading = ref(false);
const uploadProgress = ref(0);
const error = ref('');

// 图片预览相关状态
const previewVisible = ref(false);
const previewImageUrl = ref('');
const previewImageName = ref('');
const previewImageSize = ref(0);

// 删除文件相关状态
const showDeleteConfirm = ref(false);
const fileToDelete = ref(null);
const isDeleting = ref(false);

// 计算属性
const filteredFiles = computed(() => {
  if (!searchQuery.value) return files.value;

  const query = searchQuery.value.toLowerCase();
  return files.value.filter(file =>
    file.original_filename.toLowerCase().includes(query)
  );
});

// 方法
const fetchFiles = async () => {
  loading.value = true;
  try {
    console.log('获取文件列表，参数:', {
      file_type: fileType.value,
      page: currentPage.value,
      page_size: pageSize.value
    });

    // 添加时间戳参数，避免浏览器缓存
    const timestamp = new Date().getTime();
    const response = await filesApi.getFileList({
      file_type: fileType.value,
      page: currentPage.value,
      page_size: pageSize.value,
      _t: timestamp // 添加时间戳参数
    });

    console.log('获取到的文件列表:', response);

    if (response && response.items) {
      files.value = response.items;
      total.value = response.total;
    } else {
      console.error('文件列表响应格式不正确:', response);
      message.error('获取文件列表失败: 响应格式不正确');
    }
  } catch (error) {
    console.error('获取文件列表错误:', error);
    message.error('获取文件列表失败');
  } finally {
    loading.value = false;
  }
};

const handleCurrentChange = (val) => {
  currentPage.value = val;
  fetchFiles();
};

const handleSizeChange = (val) => {
  pageSize.value = val;
  fetchFiles();
};

const isImage = (file) => {
  return file.file_type === 'image';
};

const getFileUrl = (file) => {
  // 使用API_BASE_URL拼接完整URL

  // 如果file.url已经是完整URL，则直接使用
  if (file.url && (file.url.startsWith('http://') || file.url.startsWith('https://'))) {
    console.log('使用完整URL:', file.url);
    return file.url;
  }
  // 如果file.url是相对路径，则使用API_BASE_URL拼接
  else if (file.url) {
    // 确保路径格式正确
    const relativePath = file.url.startsWith('/') ? file.url : `/${file.url}`;
    const fullUrl = `${API_BASE_URL}${relativePath}`;
    console.log('使用API_BASE_URL拼接URL:', fullUrl);
    return fullUrl;
  }
  // 如果没有url，则使用file.id构建下载URL
  else if (file.id) {
    const downloadUrl = `${API_BASE_URL}/api/v1/files/download/${file.id}`;
    console.log('使用ID构建下载URL:', downloadUrl);
    return downloadUrl;
  }

  // 如果都没有，返回空字符串
  return '';
};

const selectFile = (file) => {
  console.log('选择文件:', file);
  emit('select', file);
};

// 预览图片
const previewImage = (file) => {
  previewImageUrl.value = getFileUrl(file);
  previewImageName.value = file.original_filename;
  previewImageSize.value = file.file_size;
  previewVisible.value = true;

  // 防止背景滚动
  document.body.style.overflow = 'hidden';
};

// 关闭预览
const closePreview = () => {
  previewVisible.value = false;

  // 恢复背景滚动
  document.body.style.overflow = '';
};

// 监听文件类型变化
watch(fileType, () => {
  currentPage.value = 1;
  fetchFiles();
});

// 监听props.fileType变化
watch(() => props.fileType, (newValue) => {
  if (newValue !== fileType.value) {
    fileType.value = newValue;
    currentPage.value = 1;
    fetchFiles();
  }
});

// 文件上传相关方法
const triggerFileInput = () => {
  fileInput.value.click();
};

// 文件选择变更
const onFileChange = (event) => {
  const files = Array.from(event.target.files);
  validateAndAddFiles(files);
  // 重置文件输入，以便可以再次选择相同的文件
  event.target.value = '';
};

// 文件拖放处理
const onFileDrop = (event) => {
  isDragging.value = false;
  const files = Array.from(event.dataTransfer.files);
  validateAndAddFiles(files);
};

// 验证并添加文件
const validateAndAddFiles = (files) => {
  error.value = '';

  // 验证文件类型和大小
  const validFiles = files.filter(file => {
    // 检查文件大小
    if (file.size > 5 * 1024 * 1024) { // 5MB
      error.value = '文件大小不能超过5MB';
      return false;
    }

    // 验证文件类型
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      error.value = '只支持JPG、PNG、GIF和WEBP格式的图片';
      return false;
    }

    return true;
  });

  // 添加有效文件到选择列表
  selectedFiles.value = [...selectedFiles.value, ...validFiles];
};

// 移除文件
const removeFile = (index) => {
  selectedFiles.value.splice(index, 1);
};

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// 上传文件
const uploadFiles = async () => {
  if (selectedFiles.value.length === 0) return;

  isUploading.value = true;
  uploadProgress.value = 0;
  error.value = '';

  try {
    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10;
      }
    }, 300);

    // 获取token
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('未登录或登录已过期，请重新登录');
    }

    // 正确处理token格式
    const lowerToken = token.toLowerCase();
    let cleanToken = token;
    if (lowerToken.includes('bearer')) {
      cleanToken = token.replace(/^\s*bearer\s+/i, '');
    }
    const formattedToken = `Bearer ${cleanToken}`;

    // 上传文件
    const results = [];
    for (const file of selectedFiles.value) {
      try {
        // 使用uploadFile API上传图片，确保文件被正确归类为图片类型
        const formData = new FormData();
        formData.append('file', file);

        // 使用通用上传API而不是uploadImage，确保文件被正确归类
        const result = await filesApi.uploadFile(formData, formattedToken);
        console.log('上传结果:', result);

        // 确保结果包含必要的信息
        if (!result || !result.id) {
          throw new Error('上传成功但服务器返回的数据格式不正确');
        }

        results.push(result);
      } catch (err) {
        console.error('文件上传失败:', err);
        error.value = `文件 ${file.name} 上传失败: ${err.message || '未知错误'}`;
        break;
      }
    }

    clearInterval(progressInterval);
    uploadProgress.value = 100;

    // 如果没有错误，则发出成功事件
    if (!error.value) {
      message.success('图片上传成功');
      selectedFiles.value = []; // 清空已选文件
      showUploader.value = false; // 关闭上传区域

      // 刷新文件列表 - 确保显示最新上传的图片
      // 重置到第一页并设置文件类型为"image"以便查看刚上传的图片
      currentPage.value = 1;
      if (props.fileType === 'image') {
        fileType.value = 'image';
      }

      // 延迟一下再刷新，确保服务器已处理完成
      setTimeout(() => {
        fetchFiles();
      }, 300);
    }
  } catch (err) {
    console.error('文件上传过程中发生错误:', err);
    error.value = err.message || '上传过程中发生错误';
  } finally {
    // 延迟重置上传状态，以便用户可以看到100%的进度
    setTimeout(() => {
      isUploading.value = false;
      uploadProgress.value = 0;
    }, 500);
  }
};

// 确认删除文件
const confirmDeleteFile = (file) => {
  fileToDelete.value = file;
  showDeleteConfirm.value = true;
};

// 删除文件
const deleteFile = async () => {
  if (!fileToDelete.value) return;

  isDeleting.value = true;
  try {
    // 根据文件类型选择不同的删除方法
    if (fileToDelete.value.file_type === 'image' && fileToDelete.value.file_path) {
      // 对于图片类型，使用deleteImage方法
      console.log('使用deleteImage方法删除图片:', fileToDelete.value);
      await filesApi.deleteImage(fileToDelete.value.file_path);
    } else {
      // 对于其他类型，使用deleteFile方法
      console.log('使用deleteFile方法删除文件:', fileToDelete.value);
      await filesApi.deleteFile(fileToDelete.value.id);
    }

    message.success('文件删除成功');

    // 关闭确认对话框
    showDeleteConfirm.value = false;
    fileToDelete.value = null;

    // 刷新文件列表
    fetchFiles();
  } catch (error) {
    console.error('删除文件失败:', error);
    message.error('删除文件失败: ' + (error.message || '未知错误'));
  } finally {
    isDeleting.value = false;
  }
};

// 添加键盘事件监听
const handleKeyDown = (e) => {
  if (e.key === 'Escape') {
    if (previewVisible.value) {
      closePreview();
    }
    if (showDeleteConfirm.value) {
      showDeleteConfirm.value = false;
    }
  }
};

// 组件挂载时获取文件列表
onMounted(() => {
  fetchFiles();

  // 添加键盘事件监听
  window.addEventListener('keydown', handleKeyDown);
});

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
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
