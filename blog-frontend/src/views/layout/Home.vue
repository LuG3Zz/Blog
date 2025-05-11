<template>
  <div class="min-h-screen flex flex-col overflow-hidden bg-primary text-secondary dark:bg-dark-primary dark:text-dark-secondary">

    <div v-if="error" class="w-full p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 text-center animate__animated animate__shakeX">
      {{ error }}
    </div>

    <transition name="fade">
      <div v-if="isLoading" class="loader-overlay">
        <div class="loader-content animate__animated animate__fadeIn">
          <div class="hand-container animate__animated animate__bounceIn">
            <HandLoader />
          </div>
          <p class="loader-text animate-pulse animate__animated animate__fadeIn animate__delay-1s">正在加载精彩内容...</p>
        </div>
      </div>
    </transition>

    <template v-if="!isLoading && homeData">
      <section class="p-0 m-0 h-auto">
        <div class="flex flex-col lg:flex-row w-full h-auto min-h-[70vh] mb-0 gap-4 lg:gap-6 px-4 lg:px-6 border-l-10 border-r-2 border-secondary dark:border-l-2 dark:border-r-2 dark:border-dark-secondary">
          <div class="w-full lg:w-1/4 p-2 lg:p-4 flex flex-col gap-4">
            <UserProfile :userData="homeData.userData" class="mt-5 animate__animated animate__fadeInLeft animate__delay-1s animate-hover-scale"/>

            <StatsOverview class="animate__animated animate__fadeInLeft animate__delay-2s" />
            <CategoryDistribution class="animate__animated animate__fadeInLeft animate__delay-3s" />
          </div>
          <div class="w-full lg:w-1/2 p-2 lg:p-4 flex flex-col gap-4">
            <ActivityHeatmap :activityData="processActivityData(homeData.activityData)" class="w-full animate__animated animate__fadeInUp animate__delay-1s" />
            <Hitokoto class="w-full animate__animated animate__fadeInUp animate__delay-2s" />
            <Carousel :featuredPosts="homeData.featuredPosts" class="animate__animated animate__fadeInUp animate__delay-3s animate-hover-brightness" />
          </div>
          <div class="w-full lg:w-1/4 p-2 lg:p-4 flex flex-col gap-4">
            <PopularArticles class="mt-5 animate__animated animate__fadeInRight animate__delay-1s"/>
            <FlipClock class="animate__animated animate__fadeInRight animate__delay-2s animate-hover-scale" />
            <RecentActivities class="animate__animated animate__fadeInRight animate__delay-3s" />
          </div>
        </div>
      </section>
      <section class="w-full h-auto border-t-2 border-secondary dark:border-t-2 dark:border-dark-secondary p-0 m-0 overflow-hidden animate__animated animate__fadeIn animate__delay-4s">
        <div class="w-full h-32 bg-cover bg-center" :style="bannerImage ? `background-image: url('${bannerImage}')` : `background-image: url('https://see.fontimg.com/api/rf5/nRWO0/YjYzZjZhMjcyNzM5NDM0ZGE2NmY1NzM1OTAwNmZiOWUudHRm/SGkgICBCcm93bmx1/scoreboard-type-italic-personal.png?r=fs&h=70&w=10000&fg=000000&bg=FFFFFF&s=57')`"></div>
        <div class="flex w-full h-auto gap-8 px-8">
          <div class="w-1/5 h-full overflow-y-auto p-4">
            <Categories v-model="selectedCategory" :categories="homeData.categories" class="animate__animated animate__fadeInLeft animate__delay-5s" />
          </div>
          <div class="w-4/5 h-full overflow-y-auto p-4">
            <PostsList :selectedCategory="selectedCategory" :posts="homeData.posts" class="animate__animated animate__fadeInRight animate__delay-5s" />
          </div>
        </div>
      </section>
    </template>
    <section class="flex justify-center items-center">
      <h1 class="text-6xl font-extrabold uppercase tracking-tight leading-tight text-secondary dark:text-dark-secondary animate__animated animate__zoomIn animate__delay-1s animate__infinite animate__slow">🎉欢迎来到{{ siteTitle }}🎉</h1>
    </section>
    <Footer class="animate__animated animate__fadeInUp animate__delay-4s" />

    <!-- 暗黑模式切换按钮 -->
    <div class="dark-mode-toggle animate__animated animate__fadeIn animate__delay-5s">
      <Stick v-model:darkMode="isDarkMode" :initialDarkMode="isDarkMode" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { Footer } from '../../components/layout'
import { UserProfile, ActivityHeatmap, RecentActivities, SocialMedia, Categories, PostsList, Carousel, StatsOverview, PopularArticles, CategoryDistribution, Hitokoto } from '../../components/blog'
import { HandLoader, Stick ,FlipClock} from '../../components/ui'
import { homeApi } from '../../api'
import message from '../../utils/message.js'
import { useSiteSettingsStore } from '../../stores'

export default {
  name: 'Home',
  components: {
    Footer,
    UserProfile,
    ActivityHeatmap,
    SocialMedia,
    Categories,
    PostsList,
    Carousel,
    HandLoader,
    StatsOverview,
    PopularArticles,
    CategoryDistribution,
    RecentActivities,
    Stick,
    FlipClock,
    Hitokoto
  },
  setup() {
    const selectedCategory = ref('')
    const isLoading = ref(true)
    const homeData = ref(null)
    const error = ref(null)

    // 暗黑模式状态
    const isDarkMode = ref(false)

    // 获取系统设置
    const siteSettingsStore = useSiteSettingsStore()
    const bannerImage = computed(() => siteSettingsStore.bannerImage)
    const siteTitle = computed(() => siteSettingsStore.siteTitle || 'BrownLu的博客')

    // 检查系统偏好和本地存储
    onMounted(() => {
      console.log('组件挂载，初始化暗黑模式');
      // 从本地存储中获取暗黑模式设置
      const savedDarkMode = localStorage.getItem('darkMode');
      console.log('本地存储中的暗黑模式设置:', savedDarkMode);

      if (savedDarkMode !== null) {
        isDarkMode.value = savedDarkMode === 'true';
        console.log('使用本地存储的设置:', isDarkMode.value);
      } else {
        // 如果没有本地设置，检查系统偏好
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        isDarkMode.value = prefersDark;
        console.log('使用系统偏好设置:', isDarkMode.value);
      }

      // 不需要在这里调用 applyDarkMode，因为 watch 中的 immediate: true 会自动调用
      // applyDarkMode();
    })

    // 应用暗黑模式
    const applyDarkMode = () => {
      console.log('应用暗黑模式，当前状态:', isDarkMode.value);
      if (isDarkMode.value) {
        document.documentElement.classList.add('dark');
        document.body.classList.add('dark');
        console.log('添加 dark 类');
      } else {
        document.documentElement.classList.remove('dark');
        document.body.classList.remove('dark');
        console.log('移除 dark 类');
      }
      console.log('HTML 类列表:', document.documentElement.classList);
    }

    // 监听暗黑模式变化
    watch(isDarkMode, (newValue, oldValue) => {
      console.log('暗黑模式变化:', oldValue, '->', newValue);
      // 保存到本地存储
      localStorage.setItem('darkMode', newValue.toString());
      console.log('已保存到本地存储');
      // 应用暗黑模式
      applyDarkMode();
    }, { immediate: true })

    // 处理活动数据，确保符合热力图组件需要的格式
    const processActivityData = (activityData) => {
      if (!activityData) {
        console.log('活动数据为空，返回空数组');
        return [];
      }

      console.log('处理活动数据:', typeof activityData, activityData);

      // 如果数据已经包含 values 属性，说明是从 activity-heatmap 接口获取的
      if (activityData && activityData.values && Array.isArray(activityData.values)) {
        console.log('数据包含values属性，直接返回values数组');
        return activityData.values;
      }

      // 如果是数组，检查是否已经是正确的格式
      if (Array.isArray(activityData)) {
        // 检查数组中的项是否有 date 和 count 属性
        if (activityData.length > 0 && 'date' in activityData[0] && 'count' in activityData[0]) {
          console.log('数据已经是正确的格式，直接返回');
          return activityData;
        }

        console.log('转换活动数据数组为热力图格式');
        // 如果是活动数据数组，需要转换为热力图格式
        const activityMap = {};

        activityData.forEach(activity => {
          try {
            // 确保 created_at 是有效的日期字符串
            if (!activity.created_at) {
              console.log('活动缺少created_at字段，跳过');
              return;
            }

            // 尝试解析日期
            const dateObj = new Date(activity.created_at);

            // 检查日期是否有效
            if (isNaN(dateObj.getTime())) {
              console.log('无效的日期:', activity.created_at);
              return;
            }

            const date = dateObj.toISOString().split('T')[0];
            if (!activityMap[date]) {
              activityMap[date] = 0;
            }
            activityMap[date]++;
          } catch (error) {
            console.error('处理活动数据时出错:', error);
            // 跳过无效的活动数据
          }
        });

        // 转换为热力图所需的格式
        const result = Object.entries(activityMap).map(([date, count]) => ({
          date,
          count
        }));

        console.log('转换后的热力图数据:', result.length, '条记录');
        return result;
      }

      // 处理可能的对象格式
      if (typeof activityData === 'object' && activityData !== null) {
        console.log('尝试从对象中提取活动数据');
        // 尝试从对象中提取数据
        if (activityData.data && Array.isArray(activityData.data)) {
          return processActivityData(activityData.data);
        }
      }

      console.warn('数据格式不符合预期，返回空数组:', activityData);
      // 如果数据格式不符合预期，返回空数组
      return [];
    }

    // 获取社交媒体数据
    const getSocialData = () => {
      // 如果用户数据中包含社交媒体信息，使用用户数据中的
      if (homeData.value?.userData?.social) {
        return homeData.value.userData.social
      }

      // 否则返回默认数据
      return {
        github: 'https://github.com',
        twitter: 'https://twitter.com',
        linkedin: 'https://linkedin.com',
        weibo: 'https://weibo.com',
        zhihu: 'https://zhihu.com'
      }
    }

    const loadHomeData = async () => {
      try {
        isLoading.value = true
        error.value = null
        const response = await homeApi.getHomeData()
        homeData.value = response
        console.log('首页数据加载成功:', response)
      } catch (err) {
        console.error('加载首页数据失败:', err)
        error.value = err.message
        message.error('加载首页数据失败')
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      loadHomeData()
    })

    return {
      selectedCategory,
      isLoading,
      homeData,
      error,
      processActivityData,
      getSocialData,
      isDarkMode,
      FlipClock,
      bannerImage,
      siteTitle
    }
  }
}
</script>

<style scoped>
/* 添加淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 加载器容器样式 */
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.85); /* 调整透明度，使背景更加模糊 */
  backdrop-filter: blur(5px); /* 添加模糊效果，增强视觉效果 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.dark .loader-overlay {
  background-color: rgba(17, 24, 39, 0.85); /* 暗色模式下的背景颜色 */
}

/* 自定义动画效果 */
.animate-hover-scale {
  transition: transform 0.3s ease;
}

.animate-hover-scale:hover {
  transform: scale(1.05);
}

.animate-hover-brightness {
  transition: filter 0.3s ease;
}

.animate-hover-brightness:hover {
  filter: brightness(1.1);
}

/* 添加动画延迟类 */
.animate-delay-6s {
  animation-delay: 6s;
}

.animate-delay-7s {
  animation-delay: 7s;
}

.animate-delay-8s {
  animation-delay: 8s;
}

/* 移除了卡片背景样式 */

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 90%;
  width: 300px;
}

.hand-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 2rem; /* 增加与文字的间距 */
  height: 120px; /* 增加高度，使手动画更加突出 */
  position: relative; /* 为可能的动画效果做准备 */
}

.loader-text {
  margin-top: 0; /* 移除上边距，因为我们已经在手动画容器中设置了边距 */
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  text-align: center;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8); /* 添加文字阴影提高可读性 */
}

.dark .loader-text {
  color: #e5e7eb;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8); /* 暗色模式下的文字阴影 */
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 暗黑模式切换按钮容器 */
.dark-mode-toggle {
  position: fixed;
  bottom: 20px;    /* 增加底部间距 */
  right: 20px;     /* 增加右侧间距 */
  z-index: 9000;
  pointer-events: auto;  /* 启用点击事件 */
}

/* 确保所有组件高度一致 */
.flex-col > div {
  height: 100%;
}

/* 确保组件对齐 */
@media (min-width: 1024px) {
  .lg\:p-4 {
    padding: 1rem !important;
  }

  .lg\:gap-6 {
    gap: 1.5rem !important;
  }
}
</style>
