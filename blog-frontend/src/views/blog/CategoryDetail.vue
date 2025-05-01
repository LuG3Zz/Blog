<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />

    <main class="flex-grow container mx-auto px-4 py-8">
      <Breadcrumb :items="[
        { name: '首页', path: '/' },
        { name: '分类', path: '/categories' },
        { name: categoryName, path: `/categories/${categoryId}` }
      ]" />

      <div v-if="loading" class="flex justify-center my-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>

      <div v-else-if="error" class="bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100 p-4 rounded-md my-4">
        {{ error }}
      </div>

      <div v-else class="mt-8">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ categoryName }}</h1>
              <p v-if="category && category.description" class="mt-2 text-gray-600 dark:text-gray-400">
                {{ category.description }}
              </p>
            </div>

            <div class="mt-4 md:mt-0 flex items-center">
              <span class="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-1 rounded-full text-sm font-medium">
                {{ articlesCount }} 篇文章
              </span>
            </div>
          </div>

          <!-- 订阅表单 -->
          <SubscriptionForm
            v-if="categoryId"
            type="category"
            :reference-id="categoryId"
            :reference-name="categoryName"
          />
        </div>

        <!-- 文章列表 -->
        <PostsList
          :posts="articles"
          :selected-category="categoryName"
          class="animate__animated animate__fadeIn"
        />
      </div>
    </main>

    <Footer />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { categoryApi, postApi } from '@/api';
import Navbar from '@/components/layout/Navbar.vue';
import Footer from '@/components/layout/Footer.vue';
import PostsList from '@/components/blog/PostsList.vue';
import SubscriptionForm from '@/components/blog/SubscriptionForm.vue';
import { Breadcrumb } from '@/components/ui';

export default {
  name: 'CategoryDetail',
  components: {
    Navbar,
    Footer,
    PostsList,
    Breadcrumb,
    SubscriptionForm
  },

  setup() {
    const route = useRoute();
    const router = useRouter();

    const categoryId = ref(parseInt(route.params.id));
    const categoryName = ref('');
    const category = ref(null);
    const articles = ref([]);
    const articlesCount = ref(0);
    const loading = ref(true);
    const error = ref(null);

    // 分页
    const currentPage = ref(1);
    const pageSize = 9; // 每页显示的文章数
    const totalPages = computed(() => Math.ceil(articlesCount.value / pageSize));

    // 加载分类信息
    const loadCategory = async () => {
      try {
        const categoryData = await categoryApi.getCategoryById(categoryId.value);
        category.value = categoryData;
        categoryName.value = categoryData.name;
      } catch (err) {
        console.error('加载分类信息失败:', err);
        error.value = '加载分类信息失败，请稍后重试';
      }
    };

    // 加载分类下的文章
    const loadArticles = async (page = 1) => {
      try {
        const response = await postApi.getPosts({
          category_id: categoryId.value,
          page,
          page_size: pageSize
        });

        articles.value = response.items || [];
        articlesCount.value = response.total || 0;
      } catch (err) {
        console.error('加载文章失败:', err);
        error.value = '加载文章失败，请稍后重试';
      }
    };

    // 处理页面变化
    const handlePageChange = (page) => {
      currentPage.value = page;
      loadArticles(page);

      // 滚动到顶部
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    };

    // 初始化
    onMounted(async () => {
      loading.value = true;
      error.value = null;

      try {
        await Promise.all([
          loadCategory(),
          loadArticles(currentPage.value)
        ]);
      } catch (err) {
        console.error('初始化失败:', err);
        error.value = '加载数据失败，请稍后重试';
      } finally {
        loading.value = false;
      }
    });

    return {
      categoryId,
      categoryName,
      category,
      articles,
      articlesCount,
      loading,
      error,
      currentPage,
      totalPages,
      handlePageChange
    };
  }
};
</script>
