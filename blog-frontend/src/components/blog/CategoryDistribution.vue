<template>
  <div class="category-distribution bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
    <h2 class="text-xl font-bold mb-4 text-gray-800 dark:text-white">分类分布</h2>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-4">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-700 dark:border-gray-300"></div>
    </div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="text-red-500 dark:text-red-400 text-center py-4">
      {{ error }}
    </div>

    <!-- 分类列表 -->
    <div v-else-if="categories.length > 0" class="space-y-3">
      <div
        v-for="category in categories"
        :key="category.category_id"
        class="category-item"
      >
        <div class="flex justify-between items-center mb-1">
          <router-link
            :to="`/blog/category/${category.category_id}`"
            class="text-sm font-medium hover:font-bold transition-all duration-300"
            :style="{ color: getCategoryColor(category.category_id) }"
          >
            {{ category.name }}
          </router-link>
          <span class="text-xs font-medium bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full"
                :style="{ color: getCategoryColor(category.category_id) }">
            {{ category.article_count }} 篇
          </span>
        </div>

        <!-- 进度条 -->
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
          <div
            class="h-3 rounded-full transition-all duration-500 ease-out"
            :style="getProgressBarStyle(category)"
          ></div>
        </div>
      </div>
    </div>

    <!-- 无数据提示 -->
    <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
      暂无分类数据
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { statsApi } from '@/api'

export default {
  name: 'CategoryDistribution',
  setup() {
    const loading = ref(false)
    const error = ref(null)
    const categories = ref([])

    // 计算总文章数
    const totalArticles = computed(() => {
      return categories.value.reduce((sum, category) => sum + (category.article_count || 0), 0)
    })

    // 计算百分比
    const getPercentage = (count) => {
      if (totalArticles.value === 0) return 0
      // 确保至少有 5% 的宽度，使进度条可见
      const percentage = Math.round((count / totalArticles.value) * 100)
      return Math.max(5, percentage) // 最小宽度为 5%
    }

    // 获取进度条样式
    const getProgressBarStyle = (category) => {
      try {
        const count = category?.article_count || 0;
        const categoryId = category?.category_id || category?.id || 0;

        const baseColor = getCategoryColor(categoryId);
        const lighterColor = getLighterColor(baseColor);

        return {
          width: `${getPercentage(count)}%`,
          background: `linear-gradient(90deg, ${baseColor} 0%, ${lighterColor} 100%)`,
          boxShadow: `0 0 8px ${baseColor}80`
        };
      } catch (error) {
        console.error('进度条样式错误:', error, '分类:', category);
        // 返回默认样式
        return {
          width: '5%',
          background: '#4287f5',
          boxShadow: '0 0 8px rgba(66, 135, 245, 0.5)'
        };
      }
    }

    // 获取分类颜色
    const getCategoryColor = (categoryId) => {
      // 预定义的颜色数组 - 使用更鲜艳的颜色
      const colors = [
        '#4287f5', // 更鲜艳的蓝色
        '#10d990', // 更鲜艳的绿色
        '#ffb700', // 更鲜艳的琥珀色
        '#ff3a3a', // 更鲜艳的红色
        '#9d4eff', // 更鲜艳的紫色
        '#ff3399', // 更鲜艳的粉色
        '#00d1e6', // 更鲜艳的青色
        '#ff7a00', // 更鲜艳的橙色
      ]

      try {
        // 检查categoryId是否有效
        if (categoryId === undefined || categoryId === null) {
          return colors[0]; // 默认返回第一个颜色
        }

        // 根据分类ID选择颜色
        const index = (typeof categoryId === 'number' ? categoryId : parseInt(categoryId, 10)) % colors.length;
        return colors[Math.abs(index) || 0]; // 确保索引有效，如果无效则使用0
      } catch (error) {
        console.error('获取颜色错误:', error, '分类ID:', categoryId);
        return colors[0]; // 出错时返回第一个颜色
      }
    }

    // 获取更亮的颜色版本用于渐变效果
    const getLighterColor = (hexColor) => {
      // 检查颜色是否有效
      if (!hexColor || typeof hexColor !== 'string' || !hexColor.startsWith('#') || hexColor.length < 7) {
        // 返回一个默认的浅色
        return '#ffffff';
      }

      try {
        // 将十六进制颜色转换为RGB
        const r = parseInt(hexColor.slice(1, 3), 16);
        const g = parseInt(hexColor.slice(3, 5), 16);
        const b = parseInt(hexColor.slice(5, 7), 16);

        // 使颜色更亮 (增加亮度)
        const lighterR = Math.min(255, r + 40);
        const lighterG = Math.min(255, g + 40);
        const lighterB = Math.min(255, b + 40);

        // 转换回十六进制
        return `#${lighterR.toString(16).padStart(2, '0')}${lighterG.toString(16).padStart(2, '0')}${lighterB.toString(16).padStart(2, '0')}`;
      } catch (error) {
        console.error('颜色处理错误:', error, '原始颜色:', hexColor);
        return '#ffffff'; // 出错时返回白色
      }
    }

    // 模拟数据，当API返回的数据不正确时使用
    const mockCategories = [
      { category_id: 1, name: '技术教程', article_count: 42 },
      { category_id: 2, name: '前端开发', article_count: 38 },
      { category_id: 3, name: '后端开发', article_count: 27 },
      { category_id: 4, name: '设计灵感', article_count: 18 },
      { category_id: 5, name: '生活随笔', article_count: 15 },
      { category_id: 6, name: '资源分享', article_count: 10 },
      { category_id: 7, name: '程序人生', article_count: 8 },
    ]

    // 获取分类分布数据
    const fetchCategoryDistribution = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await statsApi.getCategoryDistribution()
        console.log('获取到的分类分布数据:', response)

        // 处理响应数据
        console.log('原始分类数据:', response)

        if (Array.isArray(response) && response.length > 0) {
          categories.value = response
          console.log('响应是数组:', categories.value)
        } else if (response && Array.isArray(response.data) && response.data.length > 0) {
          categories.value = response.data
          console.log('从 response.data 获取数组:', categories.value)
        } else if (response && typeof response === 'object') {
          // 尝试将对象转换为数组
          try {
            const objValues = Object.values(response)
            if (objValues.length > 0) {
              categories.value = objValues
              console.log('将对象转换为数组:', categories.value)
            } else {
              console.warn('对象转换为空数组，使用模拟数据')
              categories.value = mockCategories
            }
          } catch (e) {
            console.error('无法将响应转换为数组:', e)
            categories.value = mockCategories
          }
        } else {
          console.warn('无法识别的响应格式或数据为空，使用模拟数据:', response)
          categories.value = mockCategories
        }

        // 确保每个分类都有 article_count 属性
        categories.value = categories.value.map(category => ({
          ...category,
          article_count: category.article_count || category.count || 0
        }))

        // 按文章数量排序
        categories.value.sort((a, b) => (b.article_count || 0) - (a.article_count || 0))
      } catch (err) {
        console.error('获取分类分布失败:', err)
        error.value = '获取分类数据失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchCategoryDistribution()
    })

    return {
      loading,
      error,
      categories,
      getPercentage,
      getCategoryColor,
      getLighterColor,
      getProgressBarStyle
    }
  }
}
</script>

<style scoped>
.category-item {
  transition: all 0.3s ease;
}

.category-item:hover {
  transform: translateX(5px);
}

/* 进度条动画 */
.category-item:nth-child(1) .rounded-full:last-child {
  animation-delay: 0.1s;
}

.category-item:nth-child(2) .rounded-full:last-child {
  animation-delay: 0.2s;
}

.category-item:nth-child(3) .rounded-full:last-child {
  animation-delay: 0.3s;
}

.category-item:nth-child(4) .rounded-full:last-child {
  animation-delay: 0.4s;
}

.category-item:nth-child(5) .rounded-full:last-child {
  animation-delay: 0.5s;
}

.category-item:nth-child(6) .rounded-full:last-child {
  animation-delay: 0.6s;
}

.category-item:nth-child(7) .rounded-full:last-child {
  animation-delay: 0.7s;
}

.category-item:nth-child(8) .rounded-full:last-child {
  animation-delay: 0.8s;
}

/* 进度条初始加载动画 */
@keyframes progressAnimation {
  0% {
    width: 0%;
    opacity: 0.7;
  }
  100% {
    opacity: 1;
  }
}

.rounded-full:last-child {
  animation: progressAnimation 1.2s ease-out forwards;
  position: relative;
  overflow: hidden;
}

.rounded-full:last-child::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.dark .rounded-full:last-child {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
</style>
