<template>
  <div class="min-h-screen flex flex-col bg-primary dark:bg-dark-primary">
    <!-- 顶部导航栏 -->
    <header class="bg-secondary dark:bg-dark-primary text-primary dark:text-dark-secondary p-4 shadow-md">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-xl font-bold">博客后台管理系统</h1>
        <div class="flex items-center gap-4">
          <span class="text-sm">欢迎，{{ userInfo?.username || '管理员' }} <span class="text-xs text-gray-400">({{ userInfo?.email || '' }})</span></span>
          <router-link to="/" class="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-500 text-white rounded transition-colors flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            博客首页
          </router-link>
          <button @click="logout" class="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
            退出登录
          </button>
        </div>
      </div>
    </header>

    <div class="flex flex-1">
      <!-- 侧边栏导航 -->
      <aside :class="[isCollapsed ? 'w-16' : 'w-64', 'bg-white dark:bg-gray-800 shadow-lg overflow-hidden']">
        <nav class="p-4 relative">
          <button
            @click="toggleSidebar"
            class="absolute -right-3 top-4 bg-white dark:bg-gray-800 rounded-full p-1.5 shadow-lg border border-gray-200 dark:border-gray-700 hover:bg-blue-50 dark:hover:bg-blue-900 hover:border-blue-300 dark:hover:border-blue-700 z-10 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-600"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 dark:text-blue-400" :class="{ 'transform rotate-180': isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
          <div class="mb-8 text-center">
            <div class="relative mx-auto mb-3 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700 shadow-md border-2 border-white dark:border-gray-600"
                 :class="{ 'w-20 h-20': !isCollapsed, 'w-12 h-12': isCollapsed }">
              <img v-if="userInfo?.avatar" :src="userInfo.avatar" alt="用户头像" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-400 to-purple-500 dark:from-blue-600 dark:to-purple-700">
                <span :class="{ 'text-3xl': !isCollapsed, 'text-xl': isCollapsed }" class="font-bold text-white">{{ userInfo?.username?.charAt(0)?.toUpperCase() || 'A' }}</span>
              </div>
            </div>
            <div v-if="!isCollapsed">
                <h2 class="text-lg font-bold text-gray-800 dark:text-gray-200">{{ userInfo?.username || '管理员' }}</h2>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ userInfo?.email || '系统管理员' }}</p>
            </div>
          </div>

          <div class="space-y-1">
            <router-link
              to="/admin"
              exact-active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">控制面板</span>
            </router-link>

            <router-link
              to="/admin/articles"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">文章管理</span>
            </router-link>

            <router-link
              to="/admin/categories"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">分类管理</span>
            </router-link>

            <router-link
              to="/admin/tags"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">标签管理</span>
            </router-link>

            <!-- 用户管理（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/users"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">用户管理</span>
            </router-link>

            <router-link
              to="/admin/comments"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">评论管理</span>
            </router-link>

            <!-- 活动管理（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/activities"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">活动管理</span>
            </router-link>

            <!-- 通知管理（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/notifications"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">通知管理</span>
            </router-link>

            <!-- 关于页面管理（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/about"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">关于页面</span>
            </router-link>

            <router-link
              to="/admin/files"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">文件管理</span>
            </router-link>

            <!-- 访客记录（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/visitors"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">访客记录</span>
            </router-link>

            <!-- 备忘录管理 -->
            <router-link
              to="/admin/memos"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">备忘录管理</span>
            </router-link>

            <!-- 订阅管理（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/subscriptions"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">订阅管理</span>
            </router-link>



            <!-- 系统设置（仅超级管理员可见） -->
            <router-link
              v-if="isUserSuperAdmin"
              to="/admin/settings"
              active-class="bg-gray-200 dark:bg-gray-700"
              class="flex items-center py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              :class="{ 'justify-center px-2': isCollapsed, 'px-4': !isCollapsed }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span :class="{ 'hidden': isCollapsed }">系统设置</span>
            </router-link>
          </div>
        </nav>
      </aside>

      <!-- 主内容区 -->
      <main class="flex-1 p-6 overflow-y-auto bg-gray-50 dark:bg-gray-900">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '@/api'
import { useUserStore } from '@/stores'
import message from '@/utils/message'
import { isAdmin, isSuperAdmin, isEditor } from '@/utils/permission'

export default {
  name: 'Admin',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const isCollapsed = ref(false)

    // 使用计算属性获取用户信息
    const userInfo = computed(() => userStore.userInfo)

    // 在组件挂载时检查登录状态和权限
    onMounted(async () => {
      console.log('后台组件挂载，检查登录状态和权限');
      console.log('当前登录状态:', userStore.isLoggedIn);
      console.log('当前用户信息:', userStore.userInfo);

      // 先检查本地存储中是否有令牌
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('本地存储中没有令牌');
        message.error('您尚未登录或登录已过期，请重新登录');
        router.push('/login');
        return;
      }

      // 如果没有登录状态，先设置登录状态并初始化
      if (!userStore.isLoggedIn) {
        userStore.initState();
      }

      // 检查是否为管理员
      if (!isAdmin(userStore.userInfo)) {
        console.warn('非管理员用户尝试访问后台');
        message.error('您没有权限访问后台管理页面');
        router.push('/unauthorized');
        return;
      }

      // 如果没有用户信息，尝试检查登录状态
      if (!userStore.userInfo) {
        try {
          await userStore.checkLoginStatus();
        } catch (error) {
          console.error('检查登录状态失败:', error);
          message.error('获取用户信息失败，请重新登录');
          router.push('/login');
        }
      }
    })

    // 切换侧边栏
    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value
    }

    // 登出操作
    const logout = () => {
      // 调用状态管理模块的登出方法
      userStore.logout()
      message.success('退出成功')

      // 重定向到登录页
      router.push('/login')
    }

    // 检查用户是否有权限访问特定页面
    const canAccessPage = (requiresSuperAdmin = false) => {
      if (requiresSuperAdmin) {
        return isSuperAdmin(userStore.userInfo)
      }
      return true
    }

    // 检查用户是否为编辑
    const isUserEditor = computed(() => {
      return isEditor(userStore.userInfo)
    })

    // 检查用户是否为超级管理员
    const isUserSuperAdmin = computed(() => {
      return isSuperAdmin(userStore.userInfo)
    })

    return {
      isCollapsed,
      toggleSidebar,
      logout,
      userInfo,
      isUserEditor,
      isUserSuperAdmin,
      canAccessPage
    }
  }
}
</script>

<style scoped>
/* 侧边栏图标样式 */
.router-link-active svg,
.router-link-exact-active svg {
  color: #3b82f6 !important;
}

/* 收缩状态下的图标样式 */
.w-16 .router-link-active,
.w-16 .router-link-exact-active {
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
}

/* 暗黑模式下的图标样式 */
.dark .w-16 .router-link-active,
.dark .w-16 .router-link-exact-active {
  background-color: rgba(59, 130, 246, 0.2);
}

/* 收缩状态下图标大小增大 */
.w-16 svg {
  width: 1.5rem;
  height: 1.5rem;
}
</style>