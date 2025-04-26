<template>
  <div class="file-uploader">
    <!-- 文件上传区域 -->
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
        :accept="acceptedFileTypes"
        :multiple="allowMultiple"
      />
      
      <div v-if="!isUploading">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-500 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <h3 class="text-lg font-medium text-gray-700 dark:text-gray-300 mb-1">拖放文件到此处或点击上传</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          支持的文件类型: {{ displayAcceptedTypes }}
          <br>
          最大文件大小: {{ maxFileSizeMB }}MB
        </p>
      </div>
      
      <div v-else class="py-4">
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mb-2">
          <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${uploadProgress}%` }"></div>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400">上传中... {{ uploadProgress }}%</p>
      </div>
    </div>
    
    <!-- 错误提示 -->
    <div v-if="error" class="mt-2 text-red-500 text-sm">
      {{ error }}
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
            <span class="text-sm text-gray-700 dark:text-gray-300 truncate max-w-xs">{{ file.name }}</span>
            <span class="text-xs text-gray-500 ml-2">({{ formatFileSize(file.size) }})</span>
          </div>
          <button @click="removeFile(index)" class="text-red-500 hover:text-red-700 dark:hover:text-red-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </li>
      </ul>
      
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
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { filesApi } from '@/api';
import message from '@/utils/message';

export default {
  name: 'FileUploader',
  props: {
    // 允许的文件类型，例如 '.jpg,.png,.pdf'
    acceptedTypes: {
      type: String,
      default: '*'
    },
    // 是否允许多文件上传
    allowMultiple: {
      type: Boolean,
      default: true
    },
    // 最大文件大小（MB）
    maxFileSizeMB: {
      type: Number,
      default: 50
    }
  },
  emits: ['upload-success', 'upload-error'],
  setup(props, { emit }) {
    const fileInput = ref(null);
    const selectedFiles = ref([]);
    const isDragging = ref(false);
    const isUploading = ref(false);
    const uploadProgress = ref(0);
    const error = ref('');

    // 计算接受的文件类型显示文本
    const displayAcceptedTypes = computed(() => {
      if (props.acceptedTypes === '*') return '所有文件';
      return props.acceptedTypes.split(',').join(', ');
    });

    // 计算接受的文件类型
    const acceptedFileTypes = computed(() => {
      return props.acceptedTypes;
    });

    // 触发文件选择
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

    // 文件拖放
    const onFileDrop = (event) => {
      isDragging.value = false;
      const files = Array.from(event.dataTransfer.files);
      validateAndAddFiles(files);
    };

    // 验证并添加文件
    const validateAndAddFiles = (files) => {
      error.value = '';
      
      // 检查文件数量
      if (!props.allowMultiple && files.length > 1) {
        error.value = '只能上传一个文件';
        return;
      }
      
      // 验证文件类型和大小
      const validFiles = files.filter(file => {
        // 检查文件大小
        if (file.size > props.maxFileSizeMB * 1024 * 1024) {
          error.value = `文件大小不能超过 ${props.maxFileSizeMB}MB`;
          return false;
        }
        
        // 如果接受所有文件类型，则不需要验证
        if (props.acceptedTypes === '*') return true;
        
        // 验证文件类型
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        const isValidType = props.acceptedTypes.split(',').some(type => {
          return type.trim().toLowerCase() === fileExtension;
        });
        
        if (!isValidType) {
          error.value = `不支持的文件类型，请上传 ${displayAcceptedTypes.value} 格式的文件`;
          return false;
        }
        
        return true;
      });
      
      // 添加有效文件到选择列表
      if (props.allowMultiple) {
        selectedFiles.value = [...selectedFiles.value, ...validFiles];
      } else {
        selectedFiles.value = validFiles.slice(0, 1);
      }
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
        
        // 上传文件
        const results = [];
        for (const file of selectedFiles.value) {
          try {
            const result = await filesApi.uploadFile(file);
            results.push(result);
          } catch (err) {
            console.error('文件上传失败:', err);
            error.value = `文件 ${file.name} 上传失败: ${err.message || '未知错误'}`;
            emit('upload-error', err);
            break;
          }
        }
        
        clearInterval(progressInterval);
        uploadProgress.value = 100;
        
        // 如果没有错误，则发出成功事件
        if (!error.value) {
          message.success('文件上传成功');
          emit('upload-success', results);
          selectedFiles.value = []; // 清空已选文件
        }
      } catch (err) {
        console.error('文件上传过程中发生错误:', err);
        error.value = err.message || '上传过程中发生错误';
        emit('upload-error', err);
      } finally {
        // 延迟重置上传状态，以便用户可以看到100%的进度
        setTimeout(() => {
          isUploading.value = false;
          uploadProgress.value = 0;
        }, 500);
      }
    };

    return {
      fileInput,
      selectedFiles,
      isDragging,
      isUploading,
      uploadProgress,
      error,
      displayAcceptedTypes,
      acceptedFileTypes,
      triggerFileInput,
      onFileChange,
      onFileDrop,
      removeFile,
      uploadFiles,
      formatFileSize
    };
  }
};
</script>

