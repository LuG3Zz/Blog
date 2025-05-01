<template>
  <div class="subscription-form bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 my-4">
    <h3 class="text-lg font-semibold mb-2">订阅更新</h3>
    <p class="text-sm text-gray-600 dark:text-gray-300 mb-4">
      订阅此{{ subscriptionTypeText }}，当有新文章发布时，我们会通过邮件通知您。
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
        
        <div v-if="isLoggedIn" class="ml-4 text-sm text-gray-600 dark:text-gray-400">
          <span v-if="isSubscribed" class="text-green-600 dark:text-green-400 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            已订阅
          </span>
          <button 
            v-else 
            type="button" 
            @click="handleUserSubscribe" 
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            使用账号订阅
          </button>
        </div>
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
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores';
import { subscriptionApi } from '@/api';

export default {
  name: 'SubscriptionForm',
  props: {
    // 订阅类型: 'author' 或 'category'
    type: {
      type: String,
      required: true,
      validator: (value) => ['author', 'category', 'all'].includes(value)
    },
    // 引用ID (作者ID或分类ID)
    referenceId: {
      type: Number,
      default: null
    },
    // 引用名称 (作者名称或分类名称)
    referenceName: {
      type: String,
      default: ''
    }
  },
  
  setup(props) {
    const userStore = useUserStore();
    const email = ref('');
    const isSubmitting = ref(false);
    const message = ref(null);
    const isSubscribed = ref(false);
    
    // 检查用户是否已登录
    const isLoggedIn = computed(() => userStore.isLoggedIn);
    
    // 订阅类型文本
    const subscriptionTypeText = computed(() => {
      switch (props.type) {
        case 'author':
          return `作者 ${props.referenceName}`;
        case 'category':
          return `分类 ${props.referenceName}`;
        case 'all':
          return '博客';
        default:
          return '';
      }
    });
    
    // 检查用户是否已订阅
    const checkSubscriptionStatus = async () => {
      if (!isLoggedIn.value) return;
      
      try {
        const subscriptions = await subscriptionApi.getUserSubscriptions();
        
        if (props.type === 'author' && subscriptions.author_ids.includes(props.referenceId)) {
          isSubscribed.value = true;
        } else if (props.type === 'category' && subscriptions.category_ids.includes(props.referenceId)) {
          isSubscribed.value = true;
        }
      } catch (error) {
        console.error('获取订阅状态失败:', error);
      }
    };
    
    // 使用账号订阅
    const handleUserSubscribe = async () => {
      if (!isLoggedIn.value) return;
      
      isSubmitting.value = true;
      message.value = null;
      
      try {
        if (props.type === 'author') {
          await subscriptionApi.subscribeToAuthor(props.referenceId);
        } else if (props.type === 'category') {
          await subscriptionApi.subscribeToCategory(props.referenceId);
        }
        
        isSubscribed.value = true;
        message.value = {
          type: 'success',
          text: `成功订阅${subscriptionTypeText.value}`
        };
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
    
    // 提交表单
    const handleSubmit = async () => {
      if (!email.value) return;
      
      isSubmitting.value = true;
      message.value = null;
      
      try {
        await subscriptionApi.createEmailSubscription({
          email: email.value,
          subscription_type: props.type,
          reference_id: props.referenceId
        });
        
        message.value = {
          type: 'success',
          text: `订阅成功！我们会在${subscriptionTypeText.value}有新文章时通知您。`
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
    
    // 初始化时检查订阅状态
    if (isLoggedIn.value) {
      checkSubscriptionStatus();
    }
    
    return {
      email,
      isSubmitting,
      message,
      isLoggedIn,
      isSubscribed,
      subscriptionTypeText,
      handleSubmit,
      handleUserSubscribe
    };
  }
};
</script>
