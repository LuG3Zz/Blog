<template>
  <div class="tag-cloud bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 border border-gray-100 dark:border-gray-700">
    <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">标签词云</h3>

    <!-- 加载状态 -->
    <LoadingSpinner v-if="loading" message="正在加载标签..." />

    <!-- 错误提示 -->
    <ErrorDisplay
      v-else-if="error"
      title="加载标签失败"
      :message="error"
      :retry-function="fetchTags"
    />

    <!-- 无数据状态 -->
    <EmptyState
      v-else-if="!tags.length"
      title="暂无标签"
      description="还没有任何标签"
      icon="search"
    />

    <!-- 标签云 -->
    <div v-else class="tag-cloud-container">
      <vue-word-cloud
        :words="cloudWords"
        :color="getTagColor"
        :font-size-ratio="3"
        :spacing="1"
        :rotation="getTagRotation"
        :animation-duration="1000"
        :animation-easing="'ease'"
        :enter-animation="{opacity: 0, transform: 'scale3d(0.6, 0.6, 0.6)'}"
        :leave-animation="{opacity: 0}"
        :font-family="'Inter, system-ui, sans-serif'"
        :font-weight="'bold'"
        style="height: 300px; width: 100%;"
      >
        <template v-slot:default="{text, weight, word}">
          <div
            @click="navigateToTag(word[2])"
            class="tag-item inline-block px-3 py-1.5 rounded-full transition-all duration-300 hover:shadow-md cursor-pointer"
            :title="`${text} (${weight} 篇文章)`"
          >
            {{ text }}
          </div>
        </template>
      </vue-word-cloud>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { tagApi } from '@/api'
// 直接导入 UI 组件，避免可能的循环引用
import ErrorDisplay from '@/components/ui/ErrorDisplay.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
// 导入 VueWordCloud 组件
import VueWordCloud from 'vuewordcloud'

export default {
  name: 'TagCloud',
  components: {
    ErrorDisplay,
    LoadingSpinner,
    EmptyState,
    VueWordCloud
  },
  props: {
    limit: {
      type: Number,
      default: 50
    }
  },
  setup(props) {
    const router = useRouter()
    const tags = ref([])
    const loading = ref(true)
    const error = ref(null)

    // 将标签数据转换为 VueWordCloud 需要的格式
    const cloudWords = computed(() => {
      return tags.value.map(tag => {
        // 将标签对象转换为 [text, weight, ...] 格式
        // 并保留原始标签对象作为第三个参数
        return [tag.name, tag.article_count || 1, tag]
      })
    })

    // 获取所有标签
    const fetchTags = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await tagApi.getTags()
        tags.value = response

        // 如果有文章计数，按文章数量排序
        if (tags.value.length > 0 && tags.value[0].article_count !== undefined) {
          tags.value.sort((a, b) => b.article_count - a.article_count)
        }

        // 限制标签数量
        if (props.limit && tags.value.length > props.limit) {
          tags.value = tags.value.slice(0, props.limit)
        }
      } catch (err) {
        console.error('获取标签失败:', err)
        error.value = '获取标签失败，请稍后再试'
      } finally {
        loading.value = false
      }
    }

    // 导航到标签页面
    const navigateToTag = (tag) => {
      if (tag && tag.id) {
        router.push(`/tags/${tag.id}`)
      }
    }

    // 根据标签的权重计算颜色
    const getTagColor = ([, weight]) => {
      // 根据权重计算颜色
      // 找出最大和最小文章数
      const maxWeight = Math.max(...cloudWords.value.map(w => w[1]))
      const minWeight = Math.min(...cloudWords.value.map(w => w[1]))

      // 计算权重比例 (0-1范围)
      let weightRatio = 0.5
      if (maxWeight > minWeight) {
        weightRatio = (weight - minWeight) / (maxWeight - minWeight)
      }

      // 生成蓝色调的颜色
      const hue = 210 + Math.floor(weightRatio * 30) - 15 // 195-225 (蓝色调范围)
      const saturation = 70 + Math.floor(weightRatio * 30) // 70-100%
      const lightness = 45 + Math.floor((1 - weightRatio) * 20) // 45-65%

      return `hsl(${hue}, ${saturation}%, ${lightness}%)`
    }

    // 根据标签的权重计算旋转角度
    const getTagRotation = ([, weight]) => {
      // 根据文章数量决定是否旋转
      // 文章数量越多，旋转的可能性越小
      const maxWeight = Math.max(...cloudWords.value.map(w => w[1]))
      const weightRatio = weight / maxWeight

      // 权重越高，旋转的可能性越小
      if (weightRatio > 0.7) {
        return 0; // 不旋转
      }

      // 随机决定是否旋转以及旋转方向
      const shouldRotate = Math.random() > 0.7;
      if (!shouldRotate) {
        return 0;
      }

      // 随机生成 -30 到 30 度之间的旋转角度
      return (Math.random() * 60 - 30) / 360;
    }

    onMounted(() => {
      fetchTags()
    })

    return {
      tags,
      loading,
      error,
      fetchTags,
      cloudWords,
      getTagColor,
      getTagRotation,
      navigateToTag
    }
  }
}
</script>

<style scoped>
.tag-cloud-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 0.5rem;
  height: 300px;
  width: 100%;
}

.tag-item {
  transition: all 0.3s ease;
  text-decoration: none;
  color: #3b82f6;
}

.tag-item:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}

/* 暗黑模式样式 */
:global(.dark) .tag-item {
  background-color: rgba(59, 130, 246, 0.15);
  color: rgb(147, 197, 253);
  border-color: rgba(59, 130, 246, 0.3);
}

:global(.dark) .tag-item:hover {
  background-color: rgba(59, 130, 246, 0.25);
  color: rgb(191, 219, 254);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* VueWordCloud 组件样式覆盖 */
:deep(.vue-word-cloud) {
  height: 100%;
  width: 100%;
}

:deep(.vue-word-cloud-text) {
  cursor: pointer;
  transition: all 0.3s ease;
}

:deep(.vue-word-cloud-text:hover) {
  filter: brightness(1.2);
}
</style>
