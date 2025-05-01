<template>
  <div v-if="show" class="fixed inset-0 z-[9999] overflow-y-auto subscription-modal" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- 背景遮罩 -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="closeModal"></div>

      <!-- 居中对齐 -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <!-- 模态框内容 -->
      <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900 sm:mx-0 sm:h-10 sm:w-10">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600 dark:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100" id="modal-title">
                订阅博客更新
              </h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  订阅博客，当有新文章发布时，我们会通过邮件通知您。
                </p>
              </div>

              <!-- 订阅表单 -->
              <div class="mt-4">
                <form @submit.prevent="handleSubmit" class="space-y-4">
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

                  <div v-if="isLoggedIn" class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <span v-if="isSubscribed" class="text-green-600 dark:text-green-400 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      您已订阅博客更新
                    </span>
                    <button
                      v-else
                      type="button"
                      @click="handleUserSubscribe"
                      class="text-blue-600 dark:text-blue-400 hover:underline"
                    >
                      使用当前账号订阅
                    </button>
                  </div>

                  <div v-if="message" :class="[
                    'p-2 text-sm rounded',
                    message.type === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100' : 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
                  ]">
                    {{ message.text }}
                  </div>

                  <div class="flex justify-end gap-3 mt-5">
                    <button
                      type="button"
                      @click="$emit('close')"
                      class="px-4 py-2 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500"
                    >
                      取消
                    </button>
                    <button
                      type="submit"
                      :disabled="isSubmitting"
                      class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {{ isSubmitting ? '订阅中...' : '订阅' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores';
import { subscriptionApi } from '@/api';

export default {
  name: 'SubscriptionModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'subscribed'],

  setup(props, { emit }) {
    const userStore = useUserStore();
    const email = ref('');
    const isSubmitting = ref(false);
    const message = ref(null);
    const isSubscribed = ref(false);

    // 关闭模态框
    const closeModal = () => {
      console.log('关闭订阅模态框');
      emit('close');
    };

    // 检查用户是否已登录
    const isLoggedIn = computed(() => userStore.isLoggedIn);

    // 检查用户是否已订阅
    const checkSubscriptionStatus = async () => {
      if (!isLoggedIn.value) return;

      try {
        const subscriptions = await subscriptionApi.getUserSubscriptions();
        isSubscribed.value = true; // 如果能获取到订阅信息，说明用户已订阅
      } catch (error) {
        console.error('获取订阅状态失败:', error);
        isSubscribed.value = false;
      }
    };

    // 使用账号订阅
    const handleUserSubscribe = async () => {
      if (!isLoggedIn.value) return;

      isSubmitting.value = true;
      message.value = null;

      try {
        await subscriptionApi.createEmailSubscription({
          email: userStore.user.email,
          subscription_type: 'all',
          reference_id: null
        });

        isSubscribed.value = true;
        message.value = {
          type: 'success',
          text: '成功订阅博客更新'
        };

        // 通知父组件订阅成功
        emit('subscribed');
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
          subscription_type: 'all',
          reference_id: null
        });

        message.value = {
          type: 'success',
          text: '订阅成功！我们会在有新文章发布时通知您。'
        };

        // 清空表单
        email.value = '';

        // 通知父组件订阅成功
        emit('subscribed');

        // 3秒后关闭弹窗
        setTimeout(() => {
          if (message.value && message.value.type === 'success') {
            emit('close');
          }
        }, 3000);
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
      handleSubmit,
      handleUserSubscribe,
      closeModal
    };
  }
};
</script>

<style scoped>
.subscription-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
