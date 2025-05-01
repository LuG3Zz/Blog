<template>
    <div class="relative flex w-full flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md dark:bg-gray-800 dark:text-gray-300">
    <!-- 顶部渐变背景区域 -->
    <div class="relative   h-32 overflow-hidden rounded-xl bg-blue-gray-500 bg-clip-border text-white shadow-lg shadow-blue-gray-500/40 bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center">
      <img
        :src="adminData.avatar || '/images/avatar.jpg'"
        :alt="adminData.username || '管理员'"
        class="w-20 h-20 rounded-full border-4 border-white object-cover shadow-lg"
      />
    </div>

    <!-- 内容区域 -->
    <div class="p-4">
      <div class="flex flex-col items-center">
        <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased dark:text-white">
          {{ adminData.username || '博主名称' }}
        </h5>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100 mb-2">
          {{ getRoleName(adminData.role) }}
        </span>
        <p v-if="adminData.bio" class="block font-sans text-base font-light leading-relaxed text-center text-gray-600 dark:text-gray-400 antialiased mb-4">
          {{ adminData.bio }}
        </p>


        <!-- 用户信息 -->
        <div class="w-full mt-4 space-y-3 text-sm">
          <div class="flex items-center bg-gray-50 dark:bg-gray-700 rounded-lg p-2.5 transition-all duration-300 hover:shadow-md">
            <div class="flex-shrink-0 bg-blue-100 dark:bg-blue-900 p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600 dark:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-3">
              <span class="text-xs uppercase font-semibold text-gray-500 dark:text-gray-400">加入时间</span>
              <p class="font-medium text-gray-700 dark:text-gray-200">{{ formatDate(adminData.created_at) }}</p>
            </div>
          </div>

          <div class="flex items-center bg-gray-50 dark:bg-gray-700 rounded-lg p-2.5 transition-all duration-300 hover:shadow-md">
            <div class="flex-shrink-0 bg-green-100 dark:bg-green-900 p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600 dark:text-green-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <span class="text-xs uppercase font-semibold text-gray-500 dark:text-gray-400">最近活动</span>
              <p class="font-medium text-gray-700 dark:text-gray-200">{{ formatDate(adminData.last_active || new Date()) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 社交媒体图标 -->
    <div class="p-6 pt-0 flex justify-center space-x-4">
      <a v-if="adminData.social_media?.github" :href="adminData.social_media.github" target="_blank" class="social-icon github">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
      </a>
      <a v-if="adminData.social_media?.bilibili" :href="adminData.social_media.bilibili" target="_blank" class="social-icon bilibili">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 0 1-.373-.906c0-.356.124-.658.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 0 1 .16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906L17.813 4.653zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.786 1.894v7.52c.017.764.28 1.395.786 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.786-1.893v-7.52c-.017-.765-.28-1.396-.786-1.894-.507-.497-1.134-.755-1.88-.773H5.333zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373zm-4 2.88c.711 0 1.289.257 1.733.773.444.516.667 1.112.667 1.787v.747c0 .675-.223 1.271-.667 1.787-.444.516-1.022.773-1.733.773-.711 0-1.289-.257-1.733-.773-.444-.516-.667-1.112-.667-1.787v-.747c0-.675.223-1.271.667-1.787.444-.516 1.022-.773 1.733-.773z"/>
        </svg>
      </a>
      <a v-if="adminData.social_media?.xiaohongshu" :href="adminData.social_media.xiaohongshu" target="_blank" class="social-icon xiaohongshu">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M19.2,6.8H4.8C3.4,6.8,2.4,7.9,2.4,9.2v5.6c0,1.3,1.1,2.4,2.4,2.4h14.4c1.3,0,2.4-1.1,2.4-2.4V9.2C21.6,7.9,20.5,6.8,19.2,6.8z M8.4,14.8c-1.3,0-2.4-1.1-2.4-2.4c0-1.3,1.1-2.4,2.4-2.4c1.3,0,2.4,1.1,2.4,2.4C10.8,13.7,9.7,14.8,8.4,14.8z M15.6,14.8c-1.3,0-2.4-1.1-2.4-2.4c0-1.3,1.1-2.4,2.4-2.4c1.3,0,2.4,1.1,2.4,2.4C18,13.7,16.9,14.8,15.6,14.8z"/>
        </svg>
      </a>
    </div>

    <!-- 按钮区域 -->
    <div class="p-6 pt-2">
      <div class="flex gap-2">
        <GradientButton
          @click="triggerConfetti"
          class="w-full font-sans text-xs font-bold uppercase text-white animate__animated"
          :class="{ 'animate__rubberBand': buttonClicked }"
          :bgColor="isDarkMode ? '#1e293b' : '#3b82f6'"
          :borderRadius="8"
          :borderWidth="3"
          :blur="5"
          :colors="['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082', '#EE82EE', '#FF0000']"
          :duration="2500"
        >
          🎉查看详情
        </GradientButton>

        <GradientButton
          @click="openSubscriptionModal"
          class="w-full font-sans text-xs font-bold uppercase text-white animate__animated"
          :bgColor="isDarkMode ? '#0f766e' : '#10b981'"
          :borderRadius="8"
          :borderWidth="3"
          :blur="5"
          :colors="['#10b981', '#059669', '#047857', '#065f46', '#064e3b', '#10b981']"
          :duration="2500"
        >
          📧订阅博客
        </GradientButton>
      </div>
    </div>

  </div>

  <!-- 订阅弹窗 -->
  <SubscriptionModal
    :show="showSubscriptionModal"
    @close="showSubscriptionModal = false"
    @subscribed="handleSubscribed"
  />
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import confetti from 'canvas-confetti'

import { adminApi, userApi } from '../../api'
import GradientButton from '@/components/ui/GradientButton.vue'
import SubscriptionModal from './SubscriptionModal.vue'
import message from '@/utils/message'

export default {
  name: 'UserProfile',
  components: {
    GradientButton,
    SubscriptionModal
  },
  props: {
    userData: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    // 管理员数据
    const adminData = ref({})
    const isLoading = ref(false)
    const error = ref(null)

    // 获取管理员数据
    const fetchAdminData = async () => {
      isLoading.value = true
      error.value = null

      try {
        // 如果传入了userData且不为空对象，则使用传入的数据
        if (props.userData && Object.keys(props.userData).length > 0) {
          adminData.value = props.userData
          return
        }

        // 使用新的 API 端点获取管理员信息
        try {
          const adminInfo = await userApi.getAdminInfo()
          if (adminInfo) {
            adminData.value = adminInfo
            console.log('使用 /users/admin/info 获取到管理员信息:', adminInfo)
            return
          }
        } catch (adminInfoError) {
          console.warn('使用 /users/admin/info 获取管理员信息失败，尝试备用方法:', adminInfoError)
        }

        // 如果上面的方法失败，尝试获取管理员用户列表
        const users = await adminApi.getUsers({ role: 'admin', page: 1, page_size: 1 })

        // 如果有管理员用户，获取第一个管理员的详细信息
        if (Array.isArray(users) && users.length > 0) {
          const adminId = users[0].id
          const adminDetail = await userApi.getUserById(adminId)
          adminData.value = adminDetail
          console.log('使用备用方法获取到管理员信息:', adminDetail)
        } else {
          // 如果没有管理员用户，使用默认数据
          adminData.value = getDefaultAdminData()
        }
      } catch (err) {
        console.error('获取管理员信息失败:', err)
        error.value = err.message
        // 使用默认数据
        adminData.value = getDefaultAdminData()
      } finally {
        isLoading.value = false
      }
    }

    // 获取默认管理员数据
    const getDefaultAdminData = () => {
      return {
        username: 'BrownLu',
        role: 'admin',
        bio: '博客管理员，热爱技术与分享',
        avatar: '/images/avatar.jpg',
        article_count: 0,
        comment_count: 0,
        created_at: new Date(),
        last_active: new Date(),
        social_media: {
          github: 'https://github.com',
          bilibili: 'https://space.bilibili.com',
          xiaohongshu: 'https://www.xiaohongshu.com'
        }
      }
    }

    // 获取角色名称
    const getRoleName = (role) => {
      const roleMap = {
        'admin': '管理员',
        'editor': '编辑',
        'user': '用户'
      }
      return roleMap[role] || '用户'
    }

    // 格式化日期
    const formatDate = (date) => {
      if (!date) return '未知时间'

      try {
        const d = new Date(date)

        // 获取当前日期
        const now = new Date()

        // 计算时间差异
        const diffTime = Math.abs(now - d)
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

        // 如果是今天
        if (d.toDateString() === now.toDateString()) {
          return `今天 ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
        }

        // 如果是昨天
        const yesterday = new Date(now)
        yesterday.setDate(yesterday.getDate() - 1)
        if (d.toDateString() === yesterday.toDateString()) {
          return `昨天 ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
        }

        // 如果在一周内
        if (diffDays < 7) {
          const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
          return `${days[d.getDay()]} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
        }

        // 如果是今年
        if (d.getFullYear() === now.getFullYear()) {
          return `${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
        }

        // 其他情况
        return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
      } catch (e) {
        console.error('日期格式化错误:', e)
        return '未知时间'
      }
    }

    // 检测暗黑模式
    const isDarkMode = computed(() => {
      if (typeof document !== 'undefined') {
        return document.documentElement.classList.contains('dark')
      }
      return false
    })

    // 按钮点击状态
    const buttonClicked = ref(false)

    // 订阅弹窗状态
    const showSubscriptionModal = ref(false)

    // 打开订阅弹窗
    const openSubscriptionModal = (event) => {
      // 阻止事件冒泡，防止触发路由导航
      if (event && event.stopPropagation) {
        event.stopPropagation()
      }
      console.log('打开订阅模态框')
      showSubscriptionModal.value = true

      // 确保模态框显示
      setTimeout(() => {
        console.log('订阅模态框状态:', showSubscriptionModal.value)
      }, 100)
    }

    // 处理订阅成功
    const handleSubscribed = () => {
      console.log('订阅成功')
      message.success('订阅成功！我们会在有新文章发布时通知您。')
      // 3秒后关闭弹窗
      setTimeout(() => {
        console.log('关闭订阅模态框')
        showSubscriptionModal.value = false
      }, 3000)
    }

    // 触发烟花效果
    const triggerConfetti = (event) => {
      // 阻止事件冒泡，防止触发路由导航
      event.stopPropagation()

      // 设置按钮点击状态
      buttonClicked.value = true
      setTimeout(() => {
        buttonClicked.value = false
      }, 1000)

      // 设置烟花持续时间
      const end = Date.now() + 3 * 1000 // 3秒

      // 设置烟花颜色，使用彩虹颜色
      const colors = [
        '#FF0000', // 红
        '#FFA500', // 橙
        '#FFFF00', // 黄
        '#008000', // 绿
        '#0000FF', // 蓝
        '#4B0082', // 青
        '#EE82EE'  // 紫
      ]

      // 帧函数，触发烟花炮
      function frame() {
        if (Date.now() > end) return

        // 左侧烟花炮
        confetti({
          particleCount: 3,
          angle: 60,
          spread: 55,
          startVelocity: 60,
          origin: { x: 0, y: 0.5 },
          colors: colors,
        })

        // 右侧烟花炮
        confetti({
          particleCount: 3,
          angle: 120,
          spread: 55,
          startVelocity: 60,
          origin: { x: 1, y: 0.5 },
          colors: colors,
        })

        requestAnimationFrame(frame)
      }

      frame()

      // 延迟导航，等烟花效果显示一会儿
      setTimeout(() => {
        if (adminData.value && adminData.value.id) {
          window.location.href = `/user/${adminData.value.id}`
        }
      }, 800)
    }

    // 组件挂载时获取管理员数据
    onMounted(() => {
      fetchAdminData()
    })

    return {
      adminData,
      isLoading,
      error,
      getRoleName,
      formatDate,
      triggerConfetti,
      buttonClicked,
      isDarkMode,
      showSubscriptionModal,
      openSubscriptionModal,
      handleSubscribed
    }
  }
}
</script>

<style scoped>
/* 添加卡片悬停效果 */
.relative.flex.w-80 {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.relative.flex.w-80:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 头像悬停效果 */
.w-24.h-24 {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.w-24.h-24:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
}

/* 按钮波纹效果 */
[data-ripple-light="true"] {
  position: relative;
  overflow: hidden;
}

[data-ripple-light="true"]::after {
  content: "";
  display: block;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  background-image: radial-gradient(circle, #fff 10%, transparent 10.01%);
  background-repeat: no-repeat;
  background-position: 50%;
  transform: scale(10, 10);
  opacity: 0;
  transition: transform .5s, opacity 1s;
}

[data-ripple-light="true"]:active::after {
  transform: scale(0, 0);
  opacity: .3;
  transition: 0s;
}

/* 社交图标样式 */
.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: #fff;
  transition: all 0.3s ease;
  transform: scale(1);
}

.social-icon:hover {
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.social-icon.github {
  background-color: #333;
}

.social-icon.bilibili {
  background-color: #00a1d6;
}

.social-icon.xiaohongshu {
  background-color: #fe2c55;
}

/* 暗黑模式下的社交图标 */
.dark .social-icon {
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
}

.dark .social-icon:hover {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
</style>
