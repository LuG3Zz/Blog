<template>
  <div v-if="show" class="fixed inset-0 z-[9999] overflow-y-auto subscription-modal" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="closeModal"></div>

    <div class="flex items-center justify-center min-h-screen">
      <div class="subscribe">
        <p>订阅博客</p>
        <form @submit.prevent="handleSubmit">
          <input
            v-model="email"
            placeholder="请输入您的邮箱"
            class="subscribe-input"
            name="email"
            type="email"
            required
          >
          <br>
          <div
            class="submit-btn"
            @click="handleSubmit"
            :class="{ 'disabled': isSubmitting }"
          >
            {{ isSubmitting ? '提交中...' : '提交' }}
          </div>

          <!-- 登录用户订阅选项 -->
          <div v-if="isLoggedIn && !isSubscribed" class="use-account">
            <a href="#" @click.prevent="handleUserSubscribe">使用当前账号订阅</a>
          </div>

          <!-- 订阅状态消息 -->
          <div v-if="message" class="message" :class="message.type">
            {{ message.text }}
          </div>

          <!-- 已订阅提示 -->
          <div v-if="isSubscribed" class="subscribed">
            <svg xmlns="http://www.w3.org/2000/svg" class="check-icon" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span>您已订阅博客更新</span>
          </div>
        </form>
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

.subscribe {
  position: relative;
  height: 140px;
  width: 240px;
  padding: 20px;
  background-color: #FFF;
  border-radius: 4px;
  color: #333;
  box-shadow: 0px 0px 60px 5px rgba(0, 0, 0, 0.4);
}

.subscribe:after {
  position: absolute;
  content: "";
  right: -10px;
  bottom: 18px;
  width: 0;
  height: 0;
  border-left: 0px solid transparent;
  border-right: 10px solid transparent;
  border-bottom: 10px solid #1a044e;
}

.subscribe p {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 2px;
  line-height: 28px;
}

.subscribe input {
  position: absolute;
  bottom: 30px;
  border: none;
  border-bottom: 1px solid #d4d4d4;
  padding: 10px;
  width: 82%;
  background: transparent;
  transition: all .25s ease;
}

.subscribe input:focus {
  outline: none;
  border-bottom: 1px solid #0d095e;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', 'sans-serif';
}

.subscribe .submit-btn {
  position: absolute;
  border-radius: 30px;
  border-bottom-right-radius: 0;
  border-top-right-radius: 0;
  background-color: #0f0092;
  color: #FFF;
  padding: 12px 25px;
  display: inline-block;
  font-size: 12px;
  font-weight: bold;
  letter-spacing: 2px;
  right: -10px;
  bottom: -20px;
  cursor: pointer;
  transition: all .25s ease;
  box-shadow: -5px 6px 20px 0px rgba(26, 26, 26, 0.4);
}

.subscribe .submit-btn:hover {
  background-color: #07013d;
  box-shadow: -5px 6px 20px 0px rgba(88, 88, 88, 0.569);
}

.subscribe .submit-btn.disabled {
  background-color: #6b6b6b;
  cursor: not-allowed;
}

/* 暗黑模式适配 */
.dark .subscribe {
  background-color: #1f2937;
  color: #e5e7eb;
  box-shadow: 0px 0px 60px 5px rgba(0, 0, 0, 0.6);
}

.dark .subscribe input {
  color: #e5e7eb;
  border-bottom-color: #4b5563;
}

.dark .subscribe input:focus {
  border-bottom-color: #60a5fa;
}

/* 登录用户订阅选项 */
.use-account {
  position: absolute;
  bottom: -45px;
  left: 10px;
  font-size: 12px;
}

.use-account a {
  color: #0f0092;
  text-decoration: none;
}

.dark .use-account a {
  color: #60a5fa;
}

/* 订阅状态消息 */
.message {
  position: absolute;
  bottom: -70px;
  left: 0;
  right: 0;
  text-align: center;
  padding: 8px;
  border-radius: 4px;
  font-size: 12px;
  background-color: rgba(255, 255, 255, 0.9);
}

.message.success {
  color: #047857;
  background-color: #d1fae5;
}

.message.error {
  color: #b91c1c;
  background-color: #fee2e2;
}

.dark .message.success {
  color: #10b981;
  background-color: #064e3b;
}

.dark .message.error {
  color: #f87171;
  background-color: #7f1d1d;
}

/* 已订阅提示 */
.subscribed {
  position: absolute;
  bottom: -45px;
  left: 10px;
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #047857;
}

.check-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
  color: #047857;
}

.dark .subscribed {
  color: #10b981;
}

.dark .check-icon {
  color: #10b981;
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
