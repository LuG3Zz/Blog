<template>
  <router-link
    :to="`/articles?tag=${tag}`"
    class="tag-search-result inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200 hover:bg-secondary hover:text-primary dark:hover:bg-dark-secondary dark:hover:text-dark-primary transition-colors duration-300"
  >
    #{{ tag }}
  </router-link>
</template>

<script>
export default {
  name: 'TagSearchResult',
  props: {
    tag: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.tag-search-result {
  transition: transform 0.2s ease;
}

.tag-search-result:hover {
  transform: translateY(-2px);
}
</style>
