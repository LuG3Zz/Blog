<template>
  <div class="min-h-screen flex flex-col">

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
                <strong>{{ articlesCount }}</strong> 篇文章
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
import Footer from '@/components/layout/Footer.vue';
import PostsList from '@/components/blog/PostsList.vue';
import SubscriptionForm from '@/components/blog/SubscriptionForm.vue';
import { Breadcrumb } from '@/components/ui';

export default {
  name: 'CategoryDetail',
  components: {
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
    const totalPages = computed(() => {
      const pages = Math.ceil(articlesCount.value / pageSize);
      console.log('总页数:', pages, '文章数量:', articlesCount.value, '每页大小:', pageSize);
      return pages > 0 ? pages : 1; // 确保至少有一页
    });

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
        // 确保已经加载了分类信息
        if (!categoryName.value && categoryId.value) {
          await loadCategory();
        }

        // 使用分类名称而不是分类ID查询文章
        const response = await postApi.getPosts({
          category: categoryName.value, // 使用分类名称
          page,
          page_size: pageSize
        });

        articles.value = response.items || [];
        articlesCount.value = response.total || 0;

        // 调试信息
        console.log('分类名称:', categoryName.value);
        console.log('文章数量:', articlesCount.value);
        console.log('文章列表:', articles.value);
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
        // 先加载分类信息，然后再加载文章
        await loadCategory();
        await loadArticles(currentPage.value);
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
