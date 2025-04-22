<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6 text-gray-800 dark:text-white">通知管理</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 通知发送器 -->
      <NotificationSender />
      
      <!-- 通知历史 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">通知历史</h2>
        
        <div class="text-center py-8 text-gray-500 dark:text-gray-400">
          <p>通知历史功能即将上线</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NotificationSender from '@/components/admin/NotificationSender.vue';

export default {
  name: 'NotificationManage',
  components: {
    NotificationSender
  }
};
</script>
