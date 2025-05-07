<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-md mx-4 transform transition-all overflow-hidden">
      <!-- Instagram风格的对话框头部 -->
      <div class="bg-gradient-to-r from-purple-500 to-pink-500 p-4 text-white">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            私密内容
          </h3>
          <button
            @click="$emit('close')"
            class="text-white hover:text-gray-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <form @submit.prevent="verifyPassword" class="p-6">
        <div class="mb-6">
          <p class="text-gray-600 dark:text-gray-400 mb-4 text-center">
            此动态已被加密，请输入密码查看内容
          </p>

          <div class="relative">
            <input
              id="password"
              v-model="password"
              type="password"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
              placeholder="输入访问密码"
              required
              ref="passwordInput"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>

          <div v-if="error" class="mt-3 p-3 bg-red-50 dark:bg-red-900/30 rounded-lg">
            <p class="text-sm text-red-600 dark:text-red-400 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              {{ error }}
            </p>
          </div>
        </div>

        <div class="flex justify-center">
          <button
            type="submit"
            :disabled="loading"
            class="w-full px-6 py-3 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              验证中...
            </span>
            <span v-else>查看内容</span>
          </button>
        </div>

        <div class="mt-4 text-center">
          <button
            type="button"
            @click="$emit('close')"
            class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
          >
            取消
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { memoApi } from '@/api';

const props = defineProps({
  memoId: {
    type: Number,
    required: false,
    default: null
  },
  localVerification: {
    type: Boolean,
    default: false
  },
  correctPassword: {
    type: String,
    default: ''
  },
  encryptedContent: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['close', 'verify-success']);

const password = ref('');
const error = ref('');
const loading = ref(false);
const passwordInput = ref(null);

// 验证密码
const verifyPassword = async () => {
  if (!password.value) {
    error.value = '请输入密码';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    // 使用本地验证方式，不需要调用API
    if (props.localVerification && props.correctPassword) {
      // 本地验证密码
      if (password.value === props.correctPassword) {
        emit('verify-success', props.encryptedContent || '');
      } else {
        error.value = '密码错误，请重试';
      }
      loading.value = false;
      return;
    }

    // 使用API验证密码
    try {
      const response = await memoApi.verifyMemoPassword(props.memoId, password.value);

      if (response.success) {
        emit('verify-success', response.content);
      } else {
        error.value = '密码错误，请重试';
      }
    } catch (err) {
      // 如果是403错误，说明用户没有权限或未登录
      if (err.response && err.response.status === 403) {
        error.value = '您没有权限查看此内容，请登录或联系作者';
      } else {
        error.value = err.message || '验证密码失败，请重试';
      }
      console.error('验证密码失败:', err);
    }
  } catch (err) {
    console.error('验证过程出错:', err);
    error.value = '验证过程出错，请重试';
  } finally {
    loading.value = false;
  }
};

// 组件挂载后自动聚焦密码输入框
onMounted(() => {
  if (passwordInput.value) {
    passwordInput.value.focus();
  }
});
</script>

<style scoped>
/* 添加动画效果 */
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

.transform {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
