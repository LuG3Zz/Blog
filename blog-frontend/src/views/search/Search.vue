<template>
  <div class="min-h-screen flex flex-col overflow-hidden bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <!-- 搜索框 -->
        <div class="mb-8">
          <div class="flex items-center bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索文章、用户或标签..."
              class="flex-grow px-4 py-3 focus:outline-none dark:bg-gray-800 dark:text-gray-200"
              @keyup.enter="handleSearch"
            />
            <button
              @click="handleSearch"
              class="px-6 py-3 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary hover:bg-opacity-90 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 搜索类型选择 -->
        <div class="mb-6 flex justify-center">
          <div class="inline-flex rounded-md shadow-sm" role="group">
            <button
              v-for="type in searchTypes"
              :key="type.value"
              @click="activeSearchType = type.value"
              :class="[
                'px-4 py-2 text-sm font-medium',
                activeSearchType === type.value
                  ? 'bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              ]"
            >
              {{ type.label }}
            </button>
          </div>
        </div>

        <!-- 搜索结果 -->
        <div v-if="isLoading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary dark:border-dark-secondary"></div>
        </div>

        <div v-else-if="hasSearched && !hasResults" class="text-center py-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">未找到结果</h3>
          <p class="text-gray-500 dark:text-gray-400">
            没有找到与 "{{ searchQuery }}" 相关的{{ getSearchTypeLabel() }}。请尝试其他关键词或搜索类型。
          </p>
        </div>

        <div v-else-if="hasSearched">
          <!-- 文章搜索结果 -->
          <div v-if="activeSearchType === 'articles'">
            <h2 class="text-2xl font-bold mb-4">文章搜索结果</h2>
            <div v-if="articleResults.items && articleResults.items.length > 0" class="space-y-6">
              <ArticleSearchResult
                v-for="article in articleResults.items"
                :key="article.id"
                :article="article"
              />

              <!-- 分页 -->
              <div v-if="articleResults.pages > 1" class="flex justify-center mt-8">
                <Pagination
                  :current-page="articleResults.page"
                  :total-pages="articleResults.pages"
                  @page-change="handlePageChange"
                />
              </div>
            </div>
          </div>

          <!-- 用户搜索结果 -->
          <div v-if="activeSearchType === 'users'">
            <h2 class="text-2xl font-bold mb-4">用户搜索结果</h2>
            <div v-if="userResults.items && userResults.items.length > 0" class="space-y-6">
              <UserSearchResult
                v-for="user in userResults.items"
                :key="user.id"
                :user="user"
              />

              <!-- 分页 -->
              <div v-if="userResults.pages > 1" class="flex justify-center mt-8">
                <Pagination
                  :current-page="userResults.page"
                  :total-pages="userResults.pages"
                  @page-change="handlePageChange"
                />
              </div>
            </div>
          </div>

          <!-- 标签搜索结果 -->
          <div v-if="activeSearchType === 'tags'">
            <h2 class="text-2xl font-bold mb-4">标签搜索结果</h2>
            <div v-if="tagResults && tagResults.length > 0" class="flex flex-wrap gap-2">
              <TagSearchResult
                v-for="(tag, index) in tagResults"
                :key="index"
                :tag="tag"
              />
            </div>
          </div>
        </div>

        <!-- 初始状态 -->
        <div v-else class="text-center py-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">搜索博客内容</h3>
          <p class="text-gray-500 dark:text-gray-400">
            输入关键词搜索文章、用户或标签
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchApi } from '../../api'
import message from '../../utils/message'
import ArticleSearchResult from '../../components/search/ArticleSearchResult.vue'
import UserSearchResult from '../../components/search/UserSearchResult.vue'
import TagSearchResult from '../../components/search/TagSearchResult.vue'
import Pagination from '../../components/ui/Pagination.vue'

export default {
  name: 'Search',
  components: {
    ArticleSearchResult,
    UserSearchResult,
    TagSearchResult,
    Pagination
  },
  setup() {
    const route = useRoute()
    const router = useRouter()

    // 搜索查询
    const searchQuery = ref('')
    const activeSearchType = ref('articles')
    const searchTypes = [
      { value: 'articles', label: '文章' },
      { value: 'users', label: '用户' },
      { value: 'tags', label: '标签' }
    ]

    // 搜索结果
    const articleResults = ref({ items: [], total: 0, page: 1, page_size: 10, pages: 0 })
    const userResults = ref({ items: [], total: 0, page: 1, page_size: 10, pages: 0 })
    const tagResults = ref([])

    // 状态
    const isLoading = ref(false)
    const hasSearched = ref(false)
    const currentPage = ref(1)

    // 计算属性
    const hasResults = computed(() => {
      if (activeSearchType.value === 'articles') {
        return articleResults.value.items && articleResults.value.items.length > 0
      } else if (activeSearchType.value === 'users') {
        return userResults.value.items && userResults.value.items.length > 0
      } else if (activeSearchType.value === 'tags') {
        return tagResults.value && tagResults.value.length > 0
      }
      return false
    })

    // 获取搜索类型标签
    const getSearchTypeLabel = () => {
      const type = searchTypes.find(t => t.value === activeSearchType.value)
      return type ? type.label : '内容'
    }

    // 从URL参数初始化搜索
    const initFromUrlParams = () => {
      const query = route.query.q
      const type = route.query.type
      const page = parseInt(route.query.page) || 1

      if (query) {
        searchQuery.value = query
        if (type && searchTypes.some(t => t.value === type)) {
          activeSearchType.value = type
        }
        currentPage.value = page
        performSearch()
      }
    }

    // 更新URL参数
    const updateUrlParams = () => {
      router.push({
        path: '/search',
        query: {
          q: searchQuery.value,
          type: activeSearchType.value,
          page: currentPage.value
        }
      })
    }

    // 执行搜索
    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
        message.warning('请输入搜索关键词')
        return
      }

      isLoading.value = true
      hasSearched.value = true

      try {
        if (activeSearchType.value === 'articles') {
          const response = await searchApi.searchArticles({
            q: searchQuery.value,
            page: currentPage.value,
            page_size: 10
          })
          articleResults.value = response
        } else if (activeSearchType.value === 'users') {
          const response = await searchApi.searchUsers({
            q: searchQuery.value,
            page: currentPage.value,
            page_size: 10
          })
          userResults.value = response
        } else if (activeSearchType.value === 'tags') {
          const response = await searchApi.searchTags(searchQuery.value, 20)
          tagResults.value = response
        }
      } catch (error) {
        console.error('搜索失败:', error)
        message.error('搜索失败，请稍后重试')
      } finally {
        isLoading.value = false
      }
    }

    // 处理搜索
    const handleSearch = () => {
      currentPage.value = 1
      updateUrlParams()
      performSearch()
    }

    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page
      updateUrlParams()
      performSearch()
    }

    // 监听搜索类型变化
    watch(activeSearchType, () => {
      currentPage.value = 1
      updateUrlParams()
      performSearch()
    })

    // 初始化
    initFromUrlParams()

    return {
      searchQuery,
      activeSearchType,
      searchTypes,
      articleResults,
      userResults,
      tagResults,
      isLoading,
      hasSearched,
      hasResults,
      getSearchTypeLabel,
      handleSearch,
      handlePageChange
    }
  }
}
</script>

<style scoped>
/* 添加任何需要的样式 */
</style>
