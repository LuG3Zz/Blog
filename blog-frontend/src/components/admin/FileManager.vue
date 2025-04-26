<template>
  <div class="file-manager">
    <!-- 统计信息 -->
    <div class="stats-panel grid grid-cols-4 gap-4 mb-6">
      <div v-for="stat in fileStats" :key="stat.type" 
           class="stat-card p-4 rounded-lg bg-white dark:bg-gray-800 shadow">
        <h3 class="text-lg font-semibold">{{ stat.type }}</h3>
        <p class="text-2xl">{{ stat.count }}</p>
        <p class="text-sm text-gray-500">{{ formatSize(stat.total_size) }}</p>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar flex justify-between items-center mb-4">
      <div class="left-tools flex gap-2">
        <select v-model="fileType" class="form-select">
          <option value="">所有类型</option>
          <option v-for="type in fileTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
        <button @click="refreshList" class="btn">刷新</button>
      </div>
      <div class="right-tools">
        <button @click="showUploader = true" class="btn-primary">
          上传文件
        </button>
      </div>
    </div>

    <!-- 文件列表 -->
    <div class="file-list">
      <table class="w-full">
        <thead>
          <tr>
            <th><input type="checkbox" v-model="selectAll" @change="toggleSelectAll"></th>
            <th>文件名</th>
            <th>类型</th>
            <th>大小</th>
            <th>上传时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in files" :key="file.id">
            <td><input type="checkbox" v-model="selectedFiles" :value="file.id"></td>
            <td>{{ file.original_filename }}</td>
            <td>{{ file.file_type }}</td>
            <td>{{ formatSize(file.file_size) }}</td>
            <td>{{ formatDate(file.created_at) }}</td>
            <td>
              <button @click="downloadFile(file)" class="btn-sm">下载</button>
              <button @click="deleteFile(file.id)" class="btn-sm btn-danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination flex justify-center mt-4">
      <!-- 分页组件 -->
    </div>

    <!-- 上传对话框 -->
    <FileUploader
      v-if="showUploader"
      @close="showUploader = false"
      @upload-success="onUploadSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { filesApi } from '@/api';
import FileUploader from './FileUploader.vue';
import { formatSize, formatDate } from '@/utils/format';
import message from '@/utils/message';

const files = ref([]);
const fileStats = ref([]);
const fileType = ref('');
const selectedFiles = ref([]);
const showUploader = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);

// 获取文件列表
const fetchFiles = async () => {
  try {
    const response = await filesApi.getFileList({
      file_type: fileType.value,
      page: currentPage.value,
      page_size: pageSize.value
    });
    files.value = response.items;
  } catch (error) {
    message.error('获取文件列表失败');
  }
};

// 获取统计信息
const fetchStats = async () => {
  try {
    const stats = await filesApi.getFileStats();
    fileStats.value = stats.type_stats;
  } catch (error) {
    message.error('获取统计信息失败');
  }
};

// 刷新列表
const refreshList = () => {
  fetchFiles();
  fetchStats();
};

onMounted(() => {
  refreshList();
});

// 其他方法实现...
</script>