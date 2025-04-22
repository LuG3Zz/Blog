<template>
  <div class="loading-spinner-container flex flex-col items-center justify-center p-6">
    <!-- 加载动画 -->
    <div class="loading-spinner mb-4">
      <div class="spinner-ring">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    
    <!-- 加载文本 -->
    <p v-if="message" class="loading-text text-sm text-gray-600 dark:text-gray-400 text-center">
      {{ message }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    message: {
      type: String,
      default: '加载中...'
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  computed: {
    spinnerSize() {
      const sizes = {
        small: 'h-4 w-4',
        medium: 'h-8 w-8',
        large: 'h-12 w-12'
      }
      return sizes[this.size] || sizes.medium
    }
  }
}
</script>

<style scoped>
.loading-spinner-container {
  width: 100%;
  height: 100%;
  min-height: 100px;
}

.spinner-ring {
  display: inline-block;
  position: relative;
  width: 40px;
  height: 40px;
}

.spinner-ring div {
  box-sizing: border-box;
  display: block;
  position: absolute;
  width: 32px;
  height: 32px;
  margin: 4px;
  border: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spinner-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #3b82f6 transparent transparent transparent;
}

.dark .spinner-ring div {
  border-color: #60a5fa transparent transparent transparent;
}

.spinner-ring div:nth-child(1) {
  animation-delay: -0.45s;
}

.spinner-ring div:nth-child(2) {
  animation-delay: -0.3s;
}

.spinner-ring div:nth-child(3) {
  animation-delay: -0.15s;
}

@keyframes spinner-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
</style>
