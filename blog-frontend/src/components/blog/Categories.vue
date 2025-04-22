<template>
  <div class="categories-container p-6">
    <div class="categories-header stack mb-5">
      <div class="card">
        <div class="card-content flex flex-col items-center">
          <h2 class="text-xl font-bold uppercase mb-2 category-title">文章分类</h2>
          <p class="text-sm text-center mb-2 category-subtitle">选择一个分类浏览相关文章</p>
        </div>
      </div>
    </div>

    <div class="categories-list">
      <TerminalLoader v-if="isLoading" />
      <div v-else-if="error" class="py-5 text-center text-red-500">{{ error }}</div>
      <div v-else>
        <div
          v-for="(category, index) in categories"
          :key="category.id"
          class="category-stack"
          :style="{ 'animation-delay': `${index * 0.1}s` }"
          :class="{ 'selected': selectedCategory === category.name }"
          @click="selectCategory(category.name)"
        >
          <div class="category-card">
            <div class="category-content">
              <h3 class="category-name">{{ category.name }}</h3>
              <p class="category-description">{{ category.description || '暂无描述' }}</p>

              <div class="category-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ category.articleCount || 0 }}</span>
                  <span class="stat-label">文章</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 全部分类选项 -->
        <div
          class="category-stack all-categories"
          :class="{ 'selected': selectedCategory === '' }"
          @click="selectCategory('')"
        >
          <div class="category-card">
            <div class="category-content">
              <h3 class="category-name">全部分类</h3>
              <p class="category-description">查看所有文章</p>

              <div class="category-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ getTotalArticleCount() }}</span>
                  <span class="stat-label">文章</span>
                </div>
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
import { categoryApi } from '../../api'
import { TerminalLoader } from '../ui'

export default {
  components: { TerminalLoader },
  name: 'Categories',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const categories = ref([])
    const isLoading = ref(false)
    const error = ref(null)
    const selectedCategory = ref(props.modelValue)

    // 从API获取分类数据
    const loadCategories = async () => {
      isLoading.value = true
      error.value = null

      try {
        // 根据 OpenAPI 文档，分类列表返回的是 CategoryWithCount 数组
        // CategoryWithCount 包含: id, name, description, articleCount
        const response = await categoryApi.getCategories()
        categories.value = response
      } catch (err) {
        console.error('加载分类数据失败:', err)
        error.value = `加载分类数据失败: ${err.message}`
      } finally {
        isLoading.value = false
      }
    }

    // 选择分类
    const selectCategory = (categoryName) => {
      selectedCategory.value = categoryName
      emit('update:modelValue', categoryName)
    }

    // 计算所有文章数量
    const getTotalArticleCount = () => {
      return categories.value.reduce((total, category) => {
        return total + (category.articleCount || 0)
      }, 0)
    }

    onMounted(() => {
      loadCategories()
    })

    return {
      categories,
      isLoading,
      error,
      selectedCategory,
      selectCategory,
      getTotalArticleCount
    }
  }
}
</script>

<style scoped>
.categories-container {
  /* 颜色变量 */
  --color-bg-light: #fff;
  --color-bg-dark: #1f2937;
  --color-border-light: #000;
  --color-border-dark: #374151;
  --color-text-primary-light: #2c3e50;
  --color-text-primary-dark: #e5e7eb;
  --color-text-secondary-light: #6b7280;
  --color-text-secondary-dark: #9ca3af;
  --color-selected-light: #3b82f6;
  --color-selected-bg-light: #eff6ff;
  --color-selected-dark: #60a5fa;
  --color-selected-bg-dark: #1e3a8a;

  /* 动画变量 */
  --transition-normal: 0.15s ease;
  --transition-hover: 0.25s ease;
  --animation-duration: 0.5s;

  /* 布局变量 */
  --border-width: 4px;
  --card-padding: 1rem;
  --card-gap: 1.5rem;
}

/* 容器样式 - 已在上面定义了CSS变量 */
.categories-container {
  margin: 0 auto;
}

/* 卡片基础样式 - 用于标题卡片和分类卡片 */
.card, .category-card {
  border: var(--border-width) solid var(--color-border-light);
  background-color: var(--color-bg-light);
  position: relative;
  transition: var(--transition-normal);
  cursor: pointer;
  padding: var(--card-padding);
  z-index: 2;
}

.card {
  margin-bottom: 10px;
}

.category-card {
  margin-bottom: var(--card-gap);
}


/* 卡片伪元素旋转角度 */
.card:before, .category-card:before {
  transform: translatey(-2%) rotate(-4deg);
}

.card:after, .category-card:after {
  transform: translatey(2%) rotate(4deg);
}

/* 分类卡片微调旋转角度 - 覆盖上面的设置 */
.category-card:before {
  transform: translatey(-2%) rotate(-3deg);
}

/* 暗色模式样式 */
.dark .card, .dark .category-card {
  background-color: var(--color-bg-dark);
  border-color: var(--color-border-dark);
}

.dark .card:before, .dark .card:after,
.dark .category-card:before, .dark .category-card:after {
  background-color: var(--color-bg-dark);
  border-color: var(--color-border-dark);
}

/* 标题卡片样式 */
.categories-header {
  width: 100%;
  transition: var(--transition-hover);
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 标题卡片悬停效果 */
.categories-header:hover {
  transform: rotate(3deg);
}

.categories-header:hover .card:before {
  transform: translatey(-2%) rotate(-3deg);
}

.categories-header:hover .card:after {
  transform: translatey(2%) rotate(3deg);
}

/* 卡片内容样式 */
.card-content, .category-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  z-index: 2; /* 确保内容在伪元素之上 */
}

.category-content {
  gap: 0.75rem;
}

/* 分类列表样式 */
.categories-list {
  display: flex;
  flex-direction: column;
  gap: var(--card-gap);
  margin-bottom: 10px;
}



/* 淡入动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}



/* 选中状态样式 */
.category-stack.selected .category-card {
  border-color: var(--color-selected-light);
  background-color: var(--color-selected-bg-light);
}

.dark .category-stack.selected .category-card {
  border-color: var(--color-selected-dark);
  background-color: var(--color-selected-bg-dark);
}

/* 标题和副标题样式 */
.category-title {
  color: var(--color-text-primary-light);
}

.dark .category-title {
  color: var(--color-text-primary-dark);
}

.category-subtitle {
  color: var(--color-text-secondary-light);
}

.dark .category-subtitle {
  color: var(--color-text-secondary-dark);
}

/* 分类名称样式 */
.category-name {
  font-size: 1.125rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--color-text-primary-light);
}

.dark .category-name {
  color: var(--color-text-primary-dark);
}

/* 分类描述样式 */
.category-description {
  font-size: 0.875rem;
  color: var(--color-text-secondary-light);
}

.dark .category-description {
  color: var(--color-text-secondary-dark);
}

/* 分类统计样式 */
.category-stats {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1rem;
  font-weight: bold;
  color: var(--color-text-primary-light);
}

.dark .stat-value {
  color: var(--color-text-primary-dark);
}

.stat-label {
  font-size: 0.625rem;
  color: var(--color-text-secondary-light);
}

.dark .stat-label {
  color: var(--color-text-secondary-dark);
}

/* 全部分类样式 */
.all-categories {
  margin-top: 1rem;
  position: relative;
  z-index: 1;
}

.all-categories .category-card {
  border-style: dashed;
}

/* 确保所有内容可见 */
.categories-container * {
  position: relative;
}
</style>
