<template>
  <div class="pagination flex items-center justify-center space-x-1">
    <!-- 上一页按钮 -->
    <button
      @click="handlePageChange(currentPage - 1)"
      :disabled="currentPage === 1"
      :class="[
        'px-3 py-1 rounded-md',
        currentPage === 1
          ? 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-gray-700 dark:text-gray-500'
          : 'bg-white text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
      ]"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
    </button>

    <!-- 页码按钮 -->
    <template v-for="page in displayedPages" :key="page">
      <!-- 省略号 -->
      <span
        v-if="page === '...'"
        class="px-3 py-1 text-gray-500 dark:text-gray-400"
      >
        ...
      </span>
      
      <!-- 页码 -->
      <button
        v-else
        @click="handlePageChange(page)"
        :class="[
          'px-3 py-1 rounded-md',
          currentPage === page
            ? 'bg-secondary text-primary dark:bg-dark-secondary dark:text-dark-primary'
            : 'bg-white text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
        ]"
      >
        {{ page }}
      </button>
    </template>

    <!-- 下一页按钮 -->
    <button
      @click="handlePageChange(currentPage + 1)"
      :disabled="currentPage === totalPages"
      :class="[
        'px-3 py-1 rounded-md',
        currentPage === totalPages
          ? 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-gray-700 dark:text-gray-500'
          : 'bg-white text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
      ]"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'Pagination',
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    },
    maxDisplayedPages: {
      type: Number,
      default: 5
    }
  },
  setup(props, { emit }) {
    // 计算要显示的页码
    const displayedPages = computed(() => {
      const { currentPage, totalPages, maxDisplayedPages } = props
      
      // 如果总页数小于等于最大显示页数，则显示所有页码
      if (totalPages <= maxDisplayedPages) {
        return Array.from({ length: totalPages }, (_, i) => i + 1)
      }
      
      // 否则，显示部分页码，并在中间使用省略号
      const pages = []
      
      // 始终显示第一页
      pages.push(1)
      
      // 计算中间页码的起始和结束
      let startPage = Math.max(2, currentPage - Math.floor(maxDisplayedPages / 2))
      let endPage = Math.min(totalPages - 1, startPage + maxDisplayedPages - 3)
      
      // 调整起始页，确保显示足够的页码
      if (endPage - startPage < maxDisplayedPages - 3) {
        startPage = Math.max(2, endPage - (maxDisplayedPages - 3))
      }
      
      // 添加省略号和中间页码
      if (startPage > 2) {
        pages.push('...')
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }
      
      if (endPage < totalPages - 1) {
        pages.push('...')
      }
      
      // 始终显示最后一页
      if (totalPages > 1) {
        pages.push(totalPages)
      }
      
      return pages
    })
    
    // 处理页码变化
    const handlePageChange = (page) => {
      if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
        emit('page-change', page)
      }
    }
    
    return {
      displayedPages,
      handlePageChange
    }
  }
}
</script>

<style scoped>
/* 添加任何需要的样式 */
</style>
