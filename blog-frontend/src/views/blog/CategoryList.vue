<template>
  <div class="container mx-auto px-4 py-8">
    <Breadcrumb :items="[{ name: '首页', path: '/' }, { name: '分类', path: '/categories' }]" />

    <div class="my-8">
      <h1 class="text-3xl font-bold mb-6">所有分类</h1>

      <TerminalLoader v-if="isLoading" />
      <div v-else-if="error" class="py-5 text-center text-red-500">{{ error }}</div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="category in categories"
          :key="category.id"
          class="stack"
          @click="viewCategoryArticles(category.name)"
        >
          <div class="card">
            <div class="content-box">
              <h2 class="card-title text-xl font-bold uppercase">{{ category.name }}</h2>
              <p class="card-content text-sm mt-2">{{ category.description }}</p>
              <div class="card-content text-sm font-medium mt-4">
                文章数量: {{ category.articleCount }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { categoryApi, postApi } from '../../api'
import { Breadcrumb, TerminalLoader } from '../../components/ui'

export default {
  name: 'CategoryList',
  components: {
    Breadcrumb,
    TerminalLoader
  },
  setup() {
    const router = useRouter()
    const categories = ref([])
    const count = ref(0)
    const posts = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    // 获取分类数据
    const loadData = async () => {
      isLoading.value = true
      error.value = null

      try {
        // 并行获取分类和文章数据
        const [categoriesData, postsData] = await Promise.all([
          categoryApi.getCategories(),
          postApi.getPosts()
        ])

        categories.value = categoriesData
        posts.value = postsData
      } catch (err) {
        console.error('加载数据失败:', err)
        error.value = `加载数据失败: ${err.message}`
      } finally {
        isLoading.value = false
      }
    }

    // 获取每个分类的文章数量
    const getCategoryPostCount = (categoryName) => {
      return articleCount.value
    }

    // 查看分类下的文章
    const viewCategoryArticles = (categoryName) => {
      // 根据分类名称查找分类ID
      const category = categories.value.find(c => c.name === categoryName);
      if (category && category.id) {
        // 如果找到分类ID，跳转到分类详情页
        router.push({
          path: `/categories/${category.id}`
        });
      } else {
        // 如果没有找到分类ID，使用旧的方式跳转
        router.push({
          path: '/articles',
          query: { category: categoryName }
        });
      }
    }

    onMounted(() => {
      loadData()
    })

    return {
      categories,
      isLoading,
      error,
      viewCategoryArticles
    }
  }
}
</script>

<style scoped>
.stack {
  width: 100%;
  max-width: 400px;
  transition: 0.25s ease;
  margin: 0 auto;
}

.stack:hover {
  transform: rotate(5deg);
}

.stack:hover .card:before {
  transform: translatey(-2%) rotate(-4deg);
}

.stack:hover .card:after {
  transform: translatey(2%) rotate(4deg);
}

.card {
  border: 4px solid;
  background-color: #fff;
  position: relative;
  transition: 0.15s ease;
  cursor: pointer;
  padding: 1.5rem;
}

.card:before,
.card:after {
  content: "";
  display: block;
  position: absolute;
  height: 100%;
  width: 100%;
  border: 4px solid;
  background-color: #fff;
  transform-origin: center center;
  z-index: -1;
  transition: 0.15s ease;
  top: 0;
  left: 0;
}

.card:before {
  transform: translatey(-2%) rotate(-6deg);
}

.card:after {
  transform: translatey(2%) rotate(6deg);
}

.content-box {
  padding: 1rem;
}

.card-title {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.card-content {
  color: #4a5568;
}

/* 暗黑模式适配 */
.dark .card,
.dark .card:before,
.dark .card:after {
  background-color: #1a202c;
  border-color: #4a5568;
}

.dark .card-title {
  color: #e2e8f0;
}

.dark .card-content {
  color: #a0aec0;
}
</style>