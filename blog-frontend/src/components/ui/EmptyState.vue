<template>
  <div class="empty-state flex flex-col items-center justify-center p-6 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
    <!-- 空状态图标 -->
    <div class="empty-icon mb-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
    </div>
    
    <!-- 空状态标题 -->
    <h3 class="empty-title text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">
      {{ title || '暂无数据' }}
    </h3>
    
    <!-- 空状态描述 -->
    <p class="empty-description text-sm text-gray-500 dark:text-gray-400 text-center mb-4">
      {{ description || '没有找到任何数据' }}
    </p>
    
    <!-- 操作按钮 -->
    <button 
      v-if="actionText && actionFunction" 
      @click="actionFunction" 
      class="action-button px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-300"
    >
      {{ actionText }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    actionText: {
      type: String,
      default: ''
    },
    actionFunction: {
      type: Function,
      default: null
    },
    icon: {
      type: String,
      default: 'inbox' // inbox, search, file, data
    }
  },
  computed: {
    iconPath() {
      const icons = {
        inbox: 'M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4',
        search: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
        file: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
        data: 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4'
      }
      return icons[this.icon] || icons.inbox
    }
  }
}
</script>

<style scoped>
.empty-state {
  width: 100%;
  height: 100%;
  min-height: 200px;
}

.empty-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

.action-button {
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
</style>
