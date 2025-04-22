<template>
  <nav class="breadcrumb-container py-2 px-4 mb-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
    <ol class="flex flex-wrap items-center text-sm">
      <li class="flex items-center">
        <router-link to="/" class="flex items-center text-gray-600 dark:text-gray-400 hover:text-secondary dark:hover:text-dark-secondary transition-colors duration-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span class="ml-1">首页</span>
        </router-link>
      </li>
      
      <li v-if="category" class="flex items-center">
        <span class="mx-2 text-gray-500 dark:text-gray-500">/</span>
        <router-link 
          :to="`/?category=${encodeURIComponent(category)}`" 
          class="flex items-center text-gray-600 dark:text-gray-400 hover:text-secondary dark:hover:text-dark-secondary transition-colors duration-200"
        >
          {{ category }}
        </router-link>
      </li>
      
      <li v-if="title" class="flex items-center">
        <span class="mx-2 text-gray-500 dark:text-gray-500">/</span>
        <span class="text-secondary dark:text-dark-secondary font-medium truncate max-w-xs">{{ title }}</span>
      </li>
    </ol>
  </nav>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Breadcrumb',
  props: {
    category: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    }
  }
})
</script>

<style scoped>
.breadcrumb-container {
  transition: all 0.3s ease;
}

.breadcrumb-container:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>
