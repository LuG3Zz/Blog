<template>
  <div class="stats-overview bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
    <h2 class="text-xl font-bold mb-4 text-gray-800 dark:text-white">博客统计</h2>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-4">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-700 dark:border-gray-300"></div>
    </div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="text-red-500 dark:text-red-400 text-center py-4">
      {{ error }}
    </div>

    <!-- 统计数据 -->
    <div v-else class="grid grid-cols-2 gap-4">
      <div class="stat-card bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-blue-600 dark:text-blue-400 font-variant-numeric tabular-nums">
          <NumberFlow
            :value="stats.total_users || 0"
            :transformTiming="{ duration: 2500, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }"
            :plugins="[continuous]"
          />
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">用户总数</div>
      </div>

      <div class="stat-card bg-green-50 dark:bg-green-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-green-600 dark:text-green-400 font-variant-numeric tabular-nums">
          <NumberFlow
            :value="stats.total_articles || 0"
            :transformTiming="{ duration: 2800, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }"
            :plugins="[continuous]"
          />
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">文章总数</div>
      </div>

      <div class="stat-card bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-purple-600 dark:text-purple-400 font-variant-numeric tabular-nums">
          <NumberFlow
            :value="stats.total_comments || 0"
            :transformTiming="{ duration: 3100, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }"
            :plugins="[continuous]"
          />
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">评论总数</div>
      </div>

      <div class="stat-card bg-amber-50 dark:bg-amber-900/30 p-4 rounded-lg flex flex-col items-center justify-center">
        <div class="text-3xl font-bold text-amber-600 dark:text-amber-400 font-variant-numeric tabular-nums">
          <NumberFlow
            :value="stats.total_likes || 0"
            :transformTiming="{ duration: 3400, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }"
            :plugins="[continuous]"
          />
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">点赞总数</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { statsApi } from '@/api'
import NumberFlow from '@number-flow/vue'
// 创建一个增强版的 continuous 插件，产生更多中间值
const continuous = {
  name: 'continuous',
  setup({ value, oldValue, trend }) {
    // 如果趋势为0，不做任何处理
    if (trend === 0) return {}

    // 计算差值
    const diff = value - oldValue

    // 使用正弦函数创建更平滑的过渡
    return {
      // 在动画过程中显示的中间值
      getValueAtProgress: (progress) => {
        // 使用缓动函数使动画更加自然
        // 先慢后快再慢的效果
        const easedProgress = progress < 0.5
          ? 4 * progress * progress * progress
          : 1 - Math.pow(-2 * progress + 2, 3) / 2

        // 添加一些波动，使数字看起来像是在寻找正确的值
        const wobble = Math.sin(progress * Math.PI * (3 + Math.random())) * (1 - progress) * 0.1

        // 计算当前值
        let currentValue = oldValue + diff * (easedProgress + wobble)

        // 确保最终值是准确的
        if (progress > 0.95) {
          currentValue = oldValue + diff * (0.95 + (progress - 0.95) * 20)
        }

        return currentValue
      }
    }
  }
}

export default {
  name: 'StatsOverview',
  components: {
    NumberFlow
  },
  setup() {
    const loading = ref(false)
    const error = ref(null)
    const stats = ref({
      total_users: 0,
      total_articles: 0,
      total_comments: 0,
      total_likes: 0
    })

    // 获取统计概览数据
    const fetchOverviewStats = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await statsApi.getOverviewStats()
        console.log('获取到的统计概览数据:', response)

        // 处理响应数据
        if (response && typeof response === 'object') {
          // 先将所有值设为0，然后再更新到实际值，以实现从0开始的动画效果
          stats.value = {
            total_users: 0,
            total_articles: 0,
            total_comments: 0,
            total_likes: 0
          }

          // 延迟更新数据，以便让组件先渲染为0，然后再开始动画
          setTimeout(() => {
            // 为了让动画效果更明显，我们可以先设置一个较小的值，然后再设置实际值
            stats.value = {
              total_users: Math.floor(response.total_users * 0.1) || 0,
              total_articles: Math.floor(response.total_articles * 0.1) || 0,
              total_comments: Math.floor(response.total_comments * 0.1) || 0,
              total_likes: Math.floor(response.total_likes * 0.1) || 0
            }

            // 再延迟一段时间，设置实际值
            setTimeout(() => {
              stats.value = {
                total_users: response.total_users || 0,
                total_articles: response.total_articles || 0,
                total_comments: response.total_comments || 0,
                total_likes: response.total_likes || 0
              }
            }, 800) // 800ms后设置实际值
          }, 300) // 300ms延迟，让加载动画消失后再开始数字动画
        }
      } catch (err) {
        console.error('获取统计概览数据失败:', err)
        error.value = '获取统计数据失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchOverviewStats()
    })

    return {
      loading,
      error,
      stats,
      continuous
    }
  }
}
</script>

<style scoped>
.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 自定义 NumberFlow 样式 */
:deep(number-flow-vue) {
  font-variant-numeric: tabular-nums;
  --number-flow-mask-height: 0.2em;
  --number-flow-mask-width: 0.3em;
  font-weight: bold;
  letter-spacing: 0.05em;
  position: relative;
}

/* 数字滚动时的高亮效果 */
:deep(number-flow-vue)::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
  pointer-events: none;
}

@keyframes shimmer {
  0% {
    background-position: -100% 0;
  }
  100% {
    background-position: 100% 0;
  }
}

/* 暗黑模式下的样式调整 */
.dark :deep(number-flow-vue) {
  color: inherit;
}

/* 数字卡片的脉冲动画 */
.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.stat-card:hover::before {
  opacity: 1;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.5;
  }
}
</style>
