<template>
  <div>
    <h1 class="text-2xl font-semibold mb-6 text-gray-800 dark:text-white">通知管理</h1>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 通知发送器 -->
      <NotificationSender />

      <!-- 通知历史 -->
      <NotificationHistory />
    </div>
  </div>
</template>

<script>
import NotificationSender from '@/components/admin/NotificationSender.vue';
import NotificationHistory from '@/components/admin/NotificationHistory.vue';

export default {
  name: 'NotificationManage',
  components: {
    NotificationSender,
    NotificationHistory
  }
};
</script>

