<template>
  <div class="visitor-management">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-200">访客记录管理</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-1">查看和管理网站访客记录</p>
      <div class="mt-2 p-3 bg-blue-50 dark:bg-blue-900/30 rounded-md text-sm text-blue-700 dark:text-blue-300 flex items-start">
        <i class="fas fa-info-circle mt-0.5 mr-2"></i>
        <div>
          <p>访客记录通过WebSocket连接实时收集，只记录前端页面的访问，不记录管理后台的访问。</p>
          <p class="mt-1">用户每次访问网站时会自动建立WebSocket连接，可在左下角查看连接状态。</p>
          <p class="mt-1">为避免重复记录，同一IP地址的匿名用户在30分钟内只记录一次访问；已登录用户则按IP和用户ID组合在30分钟内只记录一次访问。</p>
        </div>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="mb-6">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex space-x-8">
          <button
            @click="activeTab = 'list'"
            class="py-2 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'list' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'"
          >
            访客列表
          </button>
          <button
            @click="activeTab = 'statistics'"
            class="py-2 px-1 border-b-2 font-medium text-sm"
            :class="activeTab === 'statistics' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'"
          >
            访客统计
          </button>
        </nav>
      </div>
    </div>

    <!-- 内容区域 -->
    <div>
      <VisitorList v-if="activeTab === 'list'" />
      <VisitorStatistics v-else-if="activeTab === 'statistics'" />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import VisitorList from '@/components/admin/VisitorList.vue';
import VisitorStatistics from '@/components/admin/VisitorStatistics.vue';

export default {
  name: 'VisitorManagement',
  components: {
    VisitorList,
    VisitorStatistics
  },
  setup() {
    const activeTab = ref('list');

    return {
      activeTab
    };
  }
};
</script>
