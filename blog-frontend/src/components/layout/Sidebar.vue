<template>
  <aside class="w-64 h-full bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <h2 class="text-lg font-bold text-gray-800 dark:text-gray-200">{{ title }}</h2>
    </div>
    
    <div class="flex-1 overflow-y-auto p-4">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="p-4 border-t border-gray-200 dark:border-gray-700">
      <slot name="footer"></slot>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    title: {
      type: String,
      default: '侧边栏'
    }
  }
}
</script>

<style scoped>
/* 使用Tailwind类，无需额外样式 */
</style>
