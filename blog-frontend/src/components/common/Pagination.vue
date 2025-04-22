<template>
  <div class="px-6 py-4 flex items-center justify-between border-t border-gray-200 dark:border-gray-700">
    <!-- 移动端分页 -->
    <div class="flex-1 flex justify-between sm:hidden">
      <button
        @click="onPageChange(currentPage - 1)"
        :disabled="currentPage === 1"
        class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        上一页
      </button>
      <button
        @click="onPageChange(currentPage + 1)"
        :disabled="currentPage === totalPages || totalPages === 0"
        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        下一页
      </button>
    </div>

    <!-- 桌面端分页 -->
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700 dark:text-gray-300">
          显示
          <span class="font-medium">{{ startItem }}</span>
          至
          <span class="font-medium">{{ endItem }}</span>
          条，共
          <span class="font-medium">{{ total }}</span>
          条
        </p>
      </div>
      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
          <button
            @click="onPageChange(currentPage - 1)"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="sr-only">上一页</span>
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>

          <template v-if="totalPages <= 7">
            <button
              v-for="page in totalPages"
              :key="page"
              @click="onPageChange(page)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                currentPage === page
                  ? 'z-10 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary border-secondary dark:border-dark-secondary'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
              ]"
            >
              {{ page }}
            </button>
          </template>

          <template v-else>
            <button
              @click="onPageChange(1)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                currentPage === 1
                  ? 'z-10 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary border-secondary dark:border-dark-secondary'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
              ]"
            >
              1
            </button>

            <span v-if="showLeftEllipsis" class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300">
              ...
            </span>

            <button
              v-for="page in visiblePages"
              :key="page"
              @click="onPageChange(page)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                currentPage === page
                  ? 'z-10 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary border-secondary dark:border-dark-secondary'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
              ]"
            >
              {{ page }}
            </button>

            <span v-if="showRightEllipsis" class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300">
              ...
            </span>

            <button
              v-if="totalPages > 1"
              @click="onPageChange(totalPages)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                currentPage === totalPages
                  ? 'z-10 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary border-secondary dark:border-dark-secondary'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
              ]"
            >
              {{ totalPages }}
            </button>
          </template>

          <button
            @click="onPageChange(currentPage + 1)"
            :disabled="currentPage === totalPages || totalPages === 0"
            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="sr-only">下一页</span>
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  total: {
    type: Number,
    required: true
  },
  pageSize: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:currentPage'])

// 计算总页数
const totalPages = computed(() => {
  // 确保总数量和每页数量是有效数字
  const total = isNaN(props.total) ? 0 : Math.max(0, props.total)
  const pageSize = isNaN(props.pageSize) ? 10 : Math.max(1, props.pageSize)

  return Math.max(1, Math.ceil(total / pageSize))
})

// 计算当前页显示的起始和结束项
const startItem = computed(() => {
  // 确保总数量和当前页是有效数字
  const total = isNaN(props.total) ? 0 : props.total
  const currentPage = isNaN(props.currentPage) ? 1 : Math.max(1, props.currentPage)
  const pageSize = isNaN(props.pageSize) ? 10 : Math.max(1, props.pageSize)

  return total ? (currentPage - 1) * pageSize + 1 : 0
})

const endItem = computed(() => {
  // 确保总数量和当前页是有效数字
  const total = isNaN(props.total) ? 0 : props.total
  const currentPage = isNaN(props.currentPage) ? 1 : Math.max(1, props.currentPage)
  const pageSize = isNaN(props.pageSize) ? 10 : Math.max(1, props.pageSize)

  return Math.min(currentPage * pageSize, total)
})

// 计算需要显示的页码
const visiblePages = computed(() => {
  // 确保当前页是有效数字
  const currentPage = isNaN(props.currentPage) ? 1 : Math.max(1, props.currentPage)
  const delta = 2 // 当前页前后显示的页码数
  const range = []

  // 计算起始和结束页码
  const start = Math.max(2, currentPage - delta)
  const end = Math.min(totalPages.value - 1, currentPage + delta)

  // 生成页码范围
  for (let i = start; i <= end; i++) {
    range.push(i)
  }

  // 添加附近的页码
  if (range.length > 0) {
    if (range[0] > 2) {
      range.unshift(range[0] - 1)
    }
    if (range[range.length - 1] < totalPages.value - 1) {
      range.push(range[range.length - 1] + 1)
    }
  }

  return range
})

// 是否显示左侧省略号
const showLeftEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 2
})

// 是否显示右侧省略号
const showRightEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1
})

// 页码改变事件处理
const onPageChange = (page) => {
  // 确保页码是有效数字
  const newPage = isNaN(page) ? 1 : parseInt(page, 10)

  // 确保页码在有效范围内
  if (newPage >= 1 && newPage <= totalPages.value) {
    emit('update:currentPage', newPage)
  }
}
</script>