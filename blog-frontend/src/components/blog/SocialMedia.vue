<template>
  <div class="social-media">
    <TerminalLoader v-if="isLoading" />
    <template v-else>
    <div class="social-links stack">
      <div class="card">
        <a href="#" class="social-link">
          <span class="social-icon">📱</span>
          <span class="social-name">微博</span>
        </a>
        <a href="#" class="social-link">
          <span class="social-icon">💬</span>
          <span class="social-name">微信</span>
        </a>
        <a href="#" class="social-link">
          <span class="social-icon">📷</span>
          <span class="social-name">Instagram</span>
        </a>
        <a href="#" class="social-link">
          <span class="social-icon">🐦</span>
          <span class="social-name">Twitter</span>
        </a>
        <a href="https://space.bilibili.com/35391097" class="social-link">
          <span class="social-icon">📺</span>
          <span class="social-name">Bilibili</span>
        </a>
      </div>
    </div>
    <div class="recent-activity stack">
      <div class="card">
        <h3>最近动态</h3>
        <div class="activity-scroll-container">
          <!-- 加载中状态 -->
          <div v-if="activitiesLoading" class="flex justify-center items-center h-full">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-700"></div>
          </div>

          <!-- 错误提示 -->
          <div v-else-if="activitiesError" class="text-red-500 text-center py-4">
            {{ activitiesError }}
          </div>

          <!-- 无数据提示 -->
          <div v-else-if="activities.length === 0" class="text-gray-500 text-center py-4">
            暂无动态记录
          </div>

          <!-- 活动列表 -->
          <div v-else class="activity-scroll-content">
            <div v-for="activity in activities" :key="activity.id" class="activity-item">
              <p class="activity-date">{{ formatDate(activity.created_at) }}</p>
              <p class="activity-content">{{ activity.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </template>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { TerminalLoader } from '../ui'
import { activityApi } from '@/api'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

export default {
  name: 'SocialMedia',
  components: { TerminalLoader },
  props: {
    socialData: {
      type: Object,
      default: () => ({})
    },
    limit: {
      type: Number,
      default: 5
    }
  },
  setup(props) {
    const isLoading = ref(true)
    const activities = ref([])
    const activitiesLoading = ref(true)
    const activitiesError = ref(null)

    // 获取社交媒体数据
    const fetchSocialData = () => {
      isLoading.value = true
      // 模拟数据加载
      setTimeout(() => {
        isLoading.value = false
      }, 1000)
    }

    // 获取活动数据
    const fetchActivities = async () => {
      activitiesLoading.value = true
      activitiesError.value = null

      try {
        const response = await activityApi.getActivities({
          days: 30 // 获取最近30天的活动
        })

        if (Array.isArray(response)) {
          // 取最新的几条活动
          activities.value = response.slice(0, props.limit)
        } else {
          activities.value = []
        }
      } catch (err) {
        console.error('获取活动数据失败:', err)
        activitiesError.value = '获取活动数据失败'
      } finally {
        activitiesLoading.value = false
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(new Date(dateString), 'yyyy年MM月dd日', { locale: zhCN })
      } catch (error) {
        return dateString
      }
    }

    onMounted(() => {
      fetchSocialData()
      fetchActivities()
    })

    return {
      isLoading,
      activities,
      activitiesLoading,
      activitiesError,
      formatDate
    }
  }
}
</script>

<style scoped>
.social-media {
  text-align: center;
  
  max-width: 500px;
  margin: 0 auto;
}

/* 共享的卡片堆叠样式 */
.stack {
  width: 100%;
  max-width: 300px;
  transition: 0.25s ease;
  margin: auto;
}

.stack:hover {
  transform: rotate(5deg);
}

/* 基础卡片样式 */
.card, .social-link, .activity-item {
  border: 4px solid;
  background-color: #fff;
  position: relative;
  transition: 0.15s ease;
  cursor: pointer;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 27px;
}

/* 卡片伪元素共享样式 */
.card:before, .card:after,
.social-link:before, .social-link:after {
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

.card:before, .social-link:before { transform: translatey(-2%) rotate(-6deg); }
.card:after, .social-link:after { transform: translatey(2%) rotate(6deg); }

/* 悬停效果 */
.stack:hover .card:before { transform: translatey(-2%) rotate(-4deg); }
.stack:hover .card:after { transform: translatey(2%) rotate(4deg); }

/* 社交链接样式 */
.social-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-decoration: none;
  color: #2c3e50;
}

.social-link:hover {
  background-color: #f8fafc;
  transform: translateX(8px) rotate(2deg);
}

.social-icon {
  font-size: 1.25rem;
  margin-right: 0.875rem;
}

.social-name {
  font-size: 0.9375rem;
  font-weight: bold;
}

/* 活动区域样式 */
.recent-activity {
  margin-top: 1.5rem;
}

.recent-activity h3 {
  font-size: 1.125rem;
  margin-bottom: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  color: #2c3e50;
  letter-spacing: 0.05em;
  text-align: center;
}

.activity-scroll-container {
  height: 240px;
  overflow: hidden;
  position: relative;
  border: 4px solid;
  background-color: #fff;
  border-radius: 8px;
  padding: 1rem;
}

.activity-scroll-content {
  width: 100%;
  animation: scroll 15s linear infinite;
  padding: 0.5rem;
}

.activity-item {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.activity-item:last-child {
  margin-bottom: 1.5rem;
}

.activity-scroll-content:hover {
  animation-play-state: paused;
}

@keyframes scroll {
  0% { transform: translateY(0); }
  100% { transform: translateY(-100%); }
}

.activity-date {
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.375rem;
}

.activity-content {
  font-size: 0.875rem;
  color: #334155;
  line-height: 1.4;
}
</style>
