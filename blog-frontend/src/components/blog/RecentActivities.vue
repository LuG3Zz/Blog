<template>
  <div class="recent-activities bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700 transition-all duration-300 hover:shadow-lg relative">
    <h2 class="title-animation text-xl font-bold mb-4 text-gray-800 dark:text-white relative inline-block">
      最近活动
      <span class="absolute bottom-0 left-0 w-full h-0.5 bg-blue-500 transform scale-x-0 transition-transform duration-300 origin-left group-hover:scale-x-100"></span>
    </h2>

    <!-- 加载状态 -->
    <LoadingSpinner v-if="loading" message="正在加载活动数据..." />

    <!-- 错误提示 -->
    <ErrorDisplay
      v-else-if="error"
      title="加载活动失败"
      :message="error"
      :retry-function="fetchActivities"
    />

    <!-- 活动列表 -->
    <div v-else-if="activities.length > 0" ref="scrollContainer" class="scroll-container space-y-4 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent hover:scrollbar-thumb-gray-400 dark:hover:scrollbar-thumb-gray-500 pr-2 infinite-scroll-container">
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="activity-item flex items-start pb-3 border-b border-gray-200 dark:border-gray-700 last:border-0 last:pb-0 transition-all duration-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg p-2 cursor-pointer"
        @click="navigateToActivity(activity)"
      >
        <div class="flex-shrink-0 mr-3">
          <div v-if="activity.user && activity.user.avatar" class="w-8 h-8 rounded-full overflow-hidden border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:scale-110 hover:shadow-md">
            <img :src="activity.user.avatar" :alt="activity.user.username" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 dark:from-blue-600 dark:to-indigo-700 flex items-center justify-center transform transition-all duration-300 hover:scale-110 hover:shadow-md">
            <span class="text-white text-xs font-semibold">{{ getUserInitial(activity.user ? activity.user.username : '') }}</span>
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
            {{ activity.formatted_description || activity.description }}
          </p>
          <div class="flex items-center justify-between mt-1">
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ activity.relative_time || formatTime(activity.created_at) }}
            </p>
            <span v-if="activity.action_type" class="text-xs px-2 py-0.5 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
              {{ formatActionType(activity.action_type) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 无数据提示 -->
    <EmptyState
      v-else
      title="暂无活动记录"
      description="最近没有任何活动记录"
      icon="inbox"
    />

    <!-- 滚动指示器 -->
    <div class="scroll-indicator">
      <div class="scroll-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { activityApi, userApi } from '@/api'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import { ErrorDisplay, LoadingSpinner, EmptyState } from '@/components/ui'

export default {
  name: 'RecentActivities',
  components: {
    ErrorDisplay,
    LoadingSpinner,
    EmptyState
  },
  props: {
    days: {
      type: Number,
      default: 7
    },
    limit: {
      type: Number,
      default: 10
    }
  },
  setup(props) {
    const router = useRouter()
    const activities = ref([])
    const loading = ref(true)
    const error = ref(null)
    const scrollContainer = ref(null)

    // 检查用户是否已登录
    const isLoggedIn = computed(() => userApi.isLoggedIn())
    const currentUserId = computed(() => localStorage.getItem('userId'))

    // 定义存储事件监听器
    const handleStorageChange = (event) => {
      if (event.key === 'token' || event.key === 'userId') {
        console.log('存储变化，重新获取活动数据')
        fetchActivities()
      }
    }

    // 获取活动列表
    const fetchActivities = async () => {
      loading.value = true
      error.value = null

      try {
        let response

        // 根据登录状态选择不同的API接口
        if (isLoggedIn.value) {
          console.log('用户已登录，使用完整活动接口')
          // 如果用户已登录，使用完整活动接口
          response = await activityApi.getActivities({
            days: props.days,
            limit: props.limit
          })
        } else {
          console.log('用户未登录，使用公共活动接口')
          // 如果用户未登录，使用公共活动接口
          response = await activityApi.getPublicActivities({
            days: props.days,
            limit: props.limit
          })
        }

        // 处理响应数据
        activities.value = Array.isArray(response)
          ? response
          : []

        console.log('获取到的活动数据:', activities.value)
      } catch (err) {
        console.error('获取活动列表失败:', err)
        error.value = '获取活动列表失败'
      } finally {
        loading.value = false
      }
    }

    // 格式化时间
    const formatTime = (dateString) => {
      if (!dateString) return ''
      try {
        return formatDistanceToNow(new Date(dateString), {
          addSuffix: true,
          locale: zhCN
        })
      } catch (error) {
        return dateString
      }
    }

    // 获取用户首字母
    const getUserInitial = (username) => {
      if (!username) return 'A'
      return username.charAt(0).toUpperCase()
    }

    // 格式化活动类型
    const formatActionType = (actionType) => {
      const actionMap = {
        'article_created': '发布文章',
        'article_updated': '更新文章',
        'comment_created': '发表评论',
        'comment_liked': '点赞评论',
        'article_liked': '点赞文章',
        'user_registered': '新用户',
        'tag_created': '创建标签',
        'category_created': '创建分类'
      }
      return actionMap[actionType] || actionType
    }

    // 导航到活动相关页面
    const navigateToActivity = (activity) => {
      if (!activity) return

      // 根据活动类型和目标ID进行导航
      const actionType = activity.action_type
      const targetId = activity.target_id

      if (!actionType || !targetId) return

      // 文章相关活动
      if (actionType.includes('article')) {
        router.push(`/article/${targetId}`)
      }
      // 评论相关活动
      else if (actionType.includes('comment')) {
        // 如果有文章详情，导航到文章详情页并定位到评论
        if (activity.target_detail && activity.target_detail.article_id) {
          router.push(`/article/${activity.target_detail.article_id}#comment-${targetId}`)
        }
      }
      // 用户相关活动
      else if (actionType.includes('user')) {
        router.push(`/user/${targetId}`)
      }
      // 标签相关活动
      else if (actionType.includes('tag')) {
        router.push(`/tags/${targetId}`)
      }
      // 分类相关活动
      else if (actionType.includes('category')) {
        router.push(`/categories/${targetId}`)
      }
    }

    // 自动滚动功能 - 向下循环滚动
    const startAutoScroll = () => {
      if (!scrollContainer.value) return;

      const container = scrollContainer.value;
      let scrolling = false;
      const scrollSpeed = 1; // 滚动速度，可以调整
      let animationFrameId = null;

      // 创建一个克隆的活动列表用于循环显示
      const cloneItems = () => {
        // 确保容器存在且有内容
        if (!container || !container.firstElementChild) return;

        // 获取所有活动项
        const items = container.querySelectorAll('.activity-item');
        if (items.length === 0) return;

        // 如果内容不足以滚动，复制更多项目
        if (container.scrollHeight <= container.clientHeight && items.length > 0) {
          // 复制前三个活动项（或所有项目，如果少于三个）
          const itemsToClone = Math.min(items.length, 3);
          for (let i = 0; i < itemsToClone; i++) {
            const clone = items[i].cloneNode(true);
            clone.classList.add('cloned-item');
            container.appendChild(clone);
          }
        }
      };

      // 平滑滚动函数
      const smoothScroll = () => {
        if (!scrolling) {
          if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
          }
          return;
        }

        // 向下滚动
        container.scrollTop += scrollSpeed;

        // 如果到达底部，跳回顶部
        if (container.scrollTop >= container.scrollHeight - container.clientHeight) {
          // 添加平滑过渡效果
          container.classList.add('scrolling-reset');

          // 将滚动位置重置到顶部
          setTimeout(() => {
            container.scrollTop = 0;
            container.classList.remove('scrolling-reset');
          }, 300);
        }

        // 继续滚动
        animationFrameId = requestAnimationFrame(smoothScroll);
      };

      // 鼠标进入时停止滚动
      container.addEventListener('mouseenter', () => {
        scrolling = false;
      });

      // 鼠标离开时开始滚动
      container.addEventListener('mouseleave', () => {
        scrolling = true;
        if (!animationFrameId) {
          animationFrameId = requestAnimationFrame(smoothScroll);
        }
      });

      // 初始化时复制项目（如果需要）
      cloneItems();

      // 延迟启动滚动，等待初始动画完成
      setTimeout(() => {
        scrolling = true;
        animationFrameId = requestAnimationFrame(smoothScroll);
      }, 2000);

      // 清理函数
      return () => {
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
        }
        container.removeEventListener('mouseenter', () => { scrolling = false; });
        container.removeEventListener('mouseleave', () => { scrolling = true; });
      };
    };

    // 监听登录状态变化
    watch(isLoggedIn, (newValue, oldValue) => {
      if (newValue !== oldValue) {
        console.log('登录状态变化，重新获取活动数据')
        fetchActivities()
      }
    })

    onMounted(() => {
      fetchActivities();

      // 在数据加载完成后启动自动滚动
      setTimeout(() => {
        startAutoScroll();
      }, 1000);

      // 添加存储事件监听，以检测登录状态变化
      window.addEventListener('storage', handleStorageChange)
    })

    // 清理事件监听器
    onUnmounted(() => {
      // 清理存储事件监听器
      window.removeEventListener('storage', handleStorageChange)
    })

    return {
      activities,
      loading,
      error,
      formatTime,
      getUserInitial,
      formatActionType,
      fetchActivities,
      navigateToActivity,
      scrollContainer,
      isLoggedIn
    }
  }
}
</script>

<style scoped>
/* 自定义滚动条样式 */
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 2px;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: #4b5563;
}

/* 滚动动效样式 */
@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.activity-item {
  animation: slideInUp 0.5s ease-out forwards;
  opacity: 0;
}

/* 为每个活动项添加不同的动画延迟 */
.activity-item:nth-child(1) { animation-delay: 0.1s; }
.activity-item:nth-child(2) { animation-delay: 0.2s; }
.activity-item:nth-child(3) { animation-delay: 0.3s; }
.activity-item:nth-child(4) { animation-delay: 0.4s; }
.activity-item:nth-child(5) { animation-delay: 0.5s; }
.activity-item:nth-child(6) { animation-delay: 0.6s; }
.activity-item:nth-child(7) { animation-delay: 0.7s; }
.activity-item:nth-child(8) { animation-delay: 0.8s; }
.activity-item:nth-child(9) { animation-delay: 0.9s; }
.activity-item:nth-child(10) { animation-delay: 1s; }

/* 滚动容器样式 */
.scroll-container {
  animation: fadeIn 0.5s ease-out forwards;
  scroll-behavior: smooth;
}

/* 滚动重置时的渐变效果 */
.scrolling-reset {
  transition: opacity 0.3s ease;
  opacity: 0.3;
}

/* 克隆项目样式 */
.cloned-item {
  opacity: 0.9;
  border-top: 1px dashed #e5e7eb;
}

.dark .cloned-item {
  border-top: 1px dashed #4b5563;
}

/* 无限滚动容器 */
.infinite-scroll-container {
  position: relative;
  mask-image: linear-gradient(to bottom, transparent 0%, black 5%, black 95%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 5%, black 95%, transparent 100%);
}

/* 滚动指示器样式 */
.scroll-indicator {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 24px;
  height: 24px;
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  opacity: 0.7;
  transition: all 0.3s ease;
  animation: bounce 2s infinite;
  z-index: 10;
}

.dark .scroll-indicator {
  background-color: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.scroll-indicator:hover {
  opacity: 1;
  transform: scale(1.1);
}

.scroll-arrow {
  animation: arrowBounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-5px);
  }
  60% {
    transform: translateY(-3px);
  }
}

@keyframes arrowBounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(3px);
  }
  60% {
    transform: translateY(2px);
  }
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

/* 悬停效果 */
.activity-item:hover {
  transform: translateY(-2px);
  transition: transform 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.dark .activity-item:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}
</style>
