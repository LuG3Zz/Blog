<template>
  <nav class="flex justify-between items-center px-8 py-4 bg-secondary/80 dark:bg-dark-primary/80 backdrop-blur-md text-primary dark:text-dark-secondary sticky top-0 z-50 shadow-lg border-b border-white/10 dark:border-black/10">
    <div class="navbar-brand">
      <router-link to="/" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors">
        <h2 class="text-2xl font-bold uppercase m-0">😊BrownLu的博客</h2>
      </router-link>
    </div>
    <div class="flex gap-6">
      <router-link to="/" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors uppercase font-medium" :class="{ 'active': $route.path === '/' }">首页</router-link>
      <router-link to="/articles" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors uppercase font-medium" :class="{ 'active': $route.path.includes('/article') }">文章</router-link>
      <router-link to="/categories" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors uppercase font-medium" :class="{ 'active': $route.path.includes('/categories') }">分类</router-link>
      <router-link to="/about" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors uppercase font-medium" :class="{ 'active': $route.path === '/about' }">关于</router-link>
    </div>
    <div class="flex items-center gap-4">
      <!-- 搜索按钮 -->
      <router-link to="/search" class="p-2 rounded-full hover:bg-gray-700 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary dark:text-dark-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </router-link>

      <!-- 主题切换按钮 -->
      <button @click="toggleTheme" class="p-2 rounded-full hover:bg-gray-700 transition-colors">
        <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary dark:text-dark-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary dark:text-dark-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>
      <router-link v-if="!isLoggedIn" to="/login" class="text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors uppercase font-medium">登录</router-link>
      <!-- 如果已登录但正在加载用户信息，显示加载状态 -->
      <div v-else-if="isLoadingUserInfo" class="flex items-center gap-2 text-primary dark:text-dark-secondary">
        <div class="w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center overflow-hidden animate-pulse">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </div>
        <span class="text-sm">加载中...</span>
      </div>

      <!-- 如果已登录且用户信息已加载完成 -->
      <div v-else class="relative">
        <button
          @click="toggleUserMenu"
          class="flex items-center gap-2 text-primary dark:text-dark-secondary hover:text-gray-400 transition-colors font-medium rounded-full pl-2 pr-3 py-1 hover:bg-gray-700/30"
        >
          <div class="w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center overflow-hidden border-2 border-primary/20 dark:border-dark-secondary/20">
            <template v-if="userInfo?.avatar">
              <!-- 如果头像是完整的 URL -->
              <img
                v-if="userInfo.avatar.startsWith('http')"
                :src="userInfo.avatar"
                alt="用户头像"
                class="w-full h-full object-cover"
                @error="handleAvatarError"
              />
              <!-- 如果头像是相对路径 -->
              <img
                v-else
                :src="`${userInfo.avatar.startsWith('/') ? userInfo.avatar : '/' + userInfo.avatar}`"
                alt="用户头像"
                class="w-full h-full object-cover"
                @error="handleAvatarError"
              />
            </template>
            <span v-else class="text-sm font-bold">{{ userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
          </div>
          <div class="flex flex-col items-start leading-tight">
            <span class="font-medium">{{ userInfo?.username || '用户' }}</span>
            <span class="text-xs opacity-70 flex items-center gap-1">
              <span v-if="userInfo?.is_admin" class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">管理员</span>
              <span v-else-if="userInfo?.role === 'editor'" class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">编辑</span>
              <span v-else class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">用户</span>
            </span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- 用户菜单 -->
        <transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div
            v-if="showUserMenu"
            class="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-xl py-2 z-50 border border-gray-200 dark:border-gray-700 overflow-hidden origin-top-right"
          >
          <!-- 用户信息头部 -->
          <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 mb-1">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-gray-300 dark:bg-gray-700 flex items-center justify-center overflow-hidden border-2 border-primary/20 dark:border-dark-secondary/20">
                <template v-if="userInfo?.avatar">
                  <!-- 如果头像是完整的 URL -->
                  <img
                    v-if="userInfo.avatar.startsWith('http')"
                    :src="userInfo.avatar"
                    alt="用户头像"
                    class="w-full h-full object-cover"
                    @error="handleAvatarError"
                  />
                  <!-- 如果头像是相对路径 -->
                  <img
                    v-else
                    :src="`${userInfo.avatar.startsWith('/') ? userInfo.avatar : '/' + userInfo.avatar}`"
                    alt="用户头像"
                    class="w-full h-full object-cover"
                    @error="handleAvatarError"
                  />
                </template>
                <span v-else class="text-sm font-bold">{{ userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <div class="font-medium text-gray-900 dark:text-gray-100">{{ userInfo?.username || '用户' }}</div>
                  <span v-if="userInfo?.is_admin" class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">管理员</span>
                  <span v-else-if="userInfo?.role === 'editor'" class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">编辑</span>
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">{{ userInfo?.email || '未设置邮箱' }}</div>
              </div>
            </div>
          </div>

          <!-- 菜单项 -->
          <router-link
            :to="`/user/${userInfo?.id}`"
            class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            @click="showUserMenu = false"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span>个人资料</span>
          </router-link>

          <router-link
            v-if="userInfo?.is_admin"
            to="/admin"
            class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            @click="showUserMenu = false"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>后台管理</span>
          </router-link>

          <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>

          <button
            @click="handleLogout"
            class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>退出登录</span>
          </button>
          </div>
        </transition>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { userStore, themeStore } from '../../store'
import message from '../../utils/message'
import { usersApi } from '@/api'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()

    // 使用全局主题状态
    const isDark = computed(() => themeStore.state.isDark)

    // 切换主题
    const toggleTheme = () => {
      themeStore.toggleTheme()
    }

    // 用户菜单状态
    const showUserMenu = ref(false)

    // 切换用户菜单
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }

    // 点击外部关闭菜单
    onMounted(() => {
      // 添加点击外部关闭菜单的事件监听
      document.addEventListener('click', (e) => {
        if (showUserMenu.value && !e.target.closest('.relative')) {
          showUserMenu.value = false
        }
      })

      // 如果已登录，获取用户信息
      if (isLoggedIn.value) {
        fetchUserInfo()
      }
    })

    // 使用计算属性获取登录状态
    const isLoggedIn = computed(() => userStore.state.isLoggedIn)

    // 用于存储用户信息的响应式对象
    const apiUserInfo = ref(null)
    const isLoadingUserInfo = ref(false)
    const userInfoError = ref(null)

    // 处理头像加载错误
    const handleAvatarError = (event) => {
      console.error('头像加载失败:', event)
      // 将目标元素隐藏，这样就会显示默认的文字头像
      event.target.style.display = 'none'

      // 如果用户信息存在，将头像设置为 null，这样就会显示默认的文字头像
      if (apiUserInfo.value) {
        // 创建一个新对象，避免直接修改原始对象
        const updatedInfo = { ...apiUserInfo.value }
        updatedInfo.avatar = null
        apiUserInfo.value = updatedInfo
      }
    }

    // 从 API 获取用户信息
    const fetchUserInfo = async () => {
      if (!isLoggedIn.value) return

      isLoadingUserInfo.value = true
      userInfoError.value = null

      try {
        console.log('从 API 获取用户信息')
        const response = await usersApi.getUserInfo()
        console.log('从 API 获取的用户信息:', response)
        apiUserInfo.value = response
      } catch (error) {
        console.error('获取用户信息失败:', error)
        userInfoError.value = error
      } finally {
        isLoadingUserInfo.value = false
      }
    }

    // 监听登录状态变化，当登录时获取用户信息
    watch(() => isLoggedIn.value, (newValue) => {
      if (newValue) {
        fetchUserInfo()
      } else {
        apiUserInfo.value = null
      }
    }, { immediate: true })

    // 获取用户信息，优先使用 API 数据，如果失败则使用本地存储
    const userInfo = computed(() => {
      // 如果有 API 获取的用户信息，优先使用
      if (apiUserInfo.value) {
        const info = { ...apiUserInfo.value }

        // 根据用户角色判断是否为管理员
        if (info.role) {
          info.is_admin = ['admin', 'administrator'].includes(info.role.toLowerCase())
        } else if (info.is_admin === undefined) {
          // 默认非管理员
          info.is_admin = false
        }

        // 确保有用户 ID
        if (!info.id && info.user_id) {
          info.id = info.user_id
        }

        return info
      }

      // 如果 API 获取失败，尝试使用本地存储
      const userInfoStr = localStorage.getItem('userInfo')
      if (userInfoStr) {
        try {
          const parsedInfo = JSON.parse(userInfoStr)

          // 根据用户角色判断是否为管理员
          if (parsedInfo) {
            // 如果数据中有 role 字段，使用它来判断
            if (parsedInfo.role) {
              parsedInfo.is_admin = ['admin', 'administrator'].includes(parsedInfo.role.toLowerCase())
            }
            // 如果有 is_admin 字段，直接使用
            else if (parsedInfo.is_admin === undefined) {
              // 默认非管理员
              parsedInfo.is_admin = false
            }

            // 确保有用户 ID
            if (!parsedInfo.id && parsedInfo.user_id) {
              parsedInfo.id = parsedInfo.user_id
            }

            return parsedInfo
          }
        } catch (e) {
          console.error('解析用户信息失败:', e)
          return null
        }
      }
      return null
    })

    const handleLogin = () => {
      router.push('/login')
    }

    const handleLogout = () => {
      userStore.logout()
      message.success('退出成功')
      // 如果当前在后台页面，退出后跳转到首页
      if (router.currentRoute.value.path.includes('/admin')) {
        router.push('/')
      }
    }

    return {
      isDark,
      toggleTheme,
      handleLogin,
      handleLogout,
      isLoggedIn,
      userInfo,
      showUserMenu,
      toggleUserMenu,
      isLoadingUserInfo,
      userInfoError,
      fetchUserInfo, // 导出获取用户信息的函数，便于手动刷新
      handleAvatarError // 导出头像错误处理函数
    }
  }
}
</script>

<style scoped>
/* 导航栏毛玻璃效果 */
nav {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px); /* Safari 支持 */
  transition: all 0.3s ease;
}

/* 亮色模式下的导航栏 */
:global(.light) nav {
  background-color: rgba(0, 0, 0, 0.75);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 暗色模式下的导航栏 */
:global(.dark) nav {
  background-color: rgba(26, 26, 26, 0.75);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.active {
  @apply text-gray-400;
}

/* 用户菜单按钮悬停效果 */
.relative button:hover .w-8 {
  @apply border-primary/40 dark:border-dark-secondary/40;
  transform: scale(1.05);
  transition: all 0.2s ease;
}

/* 用户头像过渡效果 */
.w-8, .w-10 {
  transition: all 0.2s ease;
}

/* 头像容器样式 */
.w-8, .w-10 {
  position: relative;
  z-index: 1;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* 头像悬停效果 */
.w-8:hover, .w-10:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

/* 确保头像图片正确显示 */
.w-8 img, .w-10 img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* 菜单项悬停效果 */
.flex.items-center.gap-2:hover svg {
  @apply text-secondary dark:text-dark-secondary;
  transform: translateX(2px);
  transition: all 0.2s ease;
}

/* SVG 图标过渡效果 */
svg {
  transition: all 0.2s ease;
}

/* 导航链接悬停效果 */
.router-link-active, .router-link-exact-active {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* 搜索和主题按钮悬停效果 */
.p-2.rounded-full:hover {
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}
</style>
