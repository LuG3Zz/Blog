<template>
  <div class="subscription-card bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 my-4">
    <h3 class="text-lg font-semibold mb-2">订阅博客更新</h3>
    <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
      订阅博客，当有新文章发布时，我们会通过邮件通知您。
    </p>
    
    <form @submit.prevent="handleSubmit" class="space-y-3">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          邮箱地址
        </label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          placeholder="your@email.com"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        />
      </div>
      
      <div class="flex items-center">
        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isSubmitting ? '订阅中...' : '订阅' }}
        </button>
      </div>
    </form>
    
    <div v-if="message" :class="[
      'mt-3 p-2 text-sm rounded',
      message.type === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100' : 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
    ]">
      {{ message.text }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { subscriptionApi } from '@/api';

export default {
  name: 'SiteSubscription',
  
  setup() {
    const email = ref('');
    const isSubmitting = ref(false);
    const message = ref(null);
    
    // 提交表单
    const handleSubmit = async () => {
      if (!email.value) return;
      
      isSubmitting.value = true;
      message.value = null;
      
      try {
        await subscriptionApi.createEmailSubscription({
          email: email.value,
          subscription_type: 'all',
          reference_id: null
        });
        
        message.value = {
          type: 'success',
          text: '订阅成功！我们会在有新文章发布时通知您。'
        };
        
        // 清空表单
        email.value = '';
      } catch (error) {
        console.error('订阅失败:', error);
        message.value = {
          type: 'error',
          text: '订阅失败，请稍后重试'
        };
      } finally {
        isSubmitting.value = false;
      }
    };
    
    return {
      email,
      isSubmitting,
      message,
      handleSubmit
    };
  }
};
</script>
