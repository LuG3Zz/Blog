<template>
  <div class="hitokoto-card bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700 transition-all duration-300 hover:shadow-lg">
    <h2 class="title-animation text-xl font-bold mb-4 text-gray-800 dark:text-white relative inline-block">
      一言
      <span class="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 transform scale-x-0 transition-transform duration-300 origin-left group-hover:scale-x-100"></span>
    </h2>

    <!-- 加载状态 -->
    <LoadingSpinner v-if="loading" message="正在加载一言..." />

    <!-- 错误提示 -->
    <ErrorDisplay
      v-else-if="error"
      title="加载一言失败"
      :message="error"
      :retry-function="fetchHitokoto"
    />

    <!-- 一言内容 -->
    <div v-else class="hitokoto-content">
      <div class="flex justify-between items-center">
      <p class="text-lg text-gray-700 dark:text-gray-300 italic font-serif leading-relaxed mb-4 quote-text">
        "{{ hitokoto.hitokoto }}"
      </p>

        <p class="text-sm text-gray-500 dark:text-gray-400">
          <span v-if="hitokoto.from_who" class="font-medium">{{ hitokoto.from_who }}</span>
          <span v-if="hitokoto.from_who && hitokoto.from">《{{ hitokoto.from }}》</span>
          <span v-else-if="hitokoto.from">《{{ hitokoto.from }}》</span>
        </p>
      </div>
      <div class="mt-4 flex justify-between items-center">
        <span class="text-xs text-gray-500 dark:text-gray-400">分类: {{ getCategoryName(hitokoto.type) }}</span>
        <button @click="fetchHitokoto" class="refresh-button text-blue-500 dark:text-blue-400 hover:text-blue-600 dark:hover:text-blue-300 transition-colors duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ErrorDisplay, LoadingSpinner } from '@/components/ui'

export default {
  name: 'Hitokoto',
  components: {
    ErrorDisplay,
    LoadingSpinner
  },
  props: {
    category: {
      type: String,
      default: '' // 可选的分类: a=动画, b=漫画, c=游戏, d=文学, e=原创, f=来自网络, g=其他, h=影视, i=诗词, j=网易云, k=哲学, l=抖机灵
    }
  },
  setup(props) {
    const hitokoto = ref({})
    const loading = ref(true)
    const error = ref(null)

    // 获取一言
    const fetchHitokoto = async () => {
      loading.value = true
      error.value = null

      try {
        // 构建API URL
        let url = 'https://v1.hitokoto.cn'
        if (props.category) {
          url += `?c=${props.category}`
        }

        const response = await fetch(url)
        if (!response.ok) {
          throw new Error('获取一言失败')
        }

        const data = await response.json()
        hitokoto.value = data
        error.value = null
      } catch (err) {
        console.error('获取一言失败:', err)
        error.value = '获取一言失败，请稍后再试'
      } finally {
        loading.value = false
      }
    }

    // 获取分类名称
    const getCategoryName = (type) => {
      const categories = {
        a: '动画',
        b: '漫画',
        c: '游戏',
        d: '文学',
        e: '原创',
        f: '来自网络',
        g: '其他',
        h: '影视',
        i: '诗词',
        j: '网易云',
        k: '哲学',
        l: '抖机灵'
      }
      return categories[type] || '未知'
    }

    onMounted(() => {
      fetchHitokoto()
    })

    return {
      hitokoto,
      loading,
      error,
      fetchHitokoto,
      getCategoryName
    }
  }
}
</script>

<style scoped>
.hitokoto-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.hitokoto-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.quote-text {
  position: relative;
  padding-left: 1.5rem;
}

.quote-text::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(to bottom, #3b82f6, #60a5fa);
  border-radius: 2px;
}

.refresh-button {
  border-radius: 50%;
  padding: 0.25rem;
  transition: all 0.3s ease;
}

.refresh-button:hover {
  background-color: rgba(59, 130, 246, 0.1);
  transform: rotate(45deg);
}

.dark .refresh-button:hover {
  background-color: rgba(59, 130, 246, 0.2);
}

/* 标题动画 */
@keyframes titleAnimation {
  0% {
    transform: translateY(-10px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.title-animation {
  animation: titleAnimation 0.8s ease-out forwards;
  position: relative;
}

.title-animation::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #3b82f6;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.title-animation:hover::after {
  transform: scaleX(1);
}
</style>
