<template>
  <div class="error-display flex flex-col items-center justify-center p-6 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
    <!-- 错误图标 -->
    <div class="error-icon mb-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-red-500 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    </div>
    
    <!-- 错误标题 -->
    <h3 class="error-title text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
      {{ title || '加载失败' }}
    </h3>
    
    <!-- 错误信息 -->
    <p class="error-message text-sm text-gray-600 dark:text-gray-400 text-center mb-4">
      {{ message || '无法加载数据，请稍后再试' }}
    </p>
    
    <!-- 重试按钮 -->
    <button 
      v-if="retryFunction" 
      @click="retryFunction" 
      class="retry-button px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-300 flex items-center"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      重试
    </button>
  </div>
</template>

<script>
export default {
  name: 'ErrorDisplay',
  props: {
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      default: ''
    },
    retryFunction: {
      type: Function,
      default: null
    }
  }
}
</script>

<style scoped>
.error-display {
  width: 100%;
  height: 100%;
  min-height: 200px;
}

.error-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.retry-button:hover svg {
  animation: spin 1s ease-in-out;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
