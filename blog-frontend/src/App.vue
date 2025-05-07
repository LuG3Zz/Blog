<template>
  <div class="min-h-screen flex flex-col bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <Navbar v-if="!isAdminRoute" class="animate__animated animate__fadeInDown" />
    <router-view />
    <Stick :initial-dark-mode="isDark" @update:dark-mode="updateDarkMode" />
    <NotificationContainer />
    <Toast />
    <WebSocketStatusIndicator v-if="showWebSocketIndicator" />
  </div>
</template>

<script>
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore, useThemeStore, useSiteSettingsStore } from './stores'
import Stick from './components/ui/stick.vue'
import NotificationContainer from './components/ui/NotificationContainer.vue'
import Toast from './components/ui/Toast.vue'
import WebSocketStatusIndicator from './components/ui/WebSocketStatusIndicator.vue'
import Navbar from './components/layout/Navbar.vue'
import { initWebSocketService, webSocketService, WebSocketStatus } from './services/websocket-new'

export default {
  name: 'App',
  components: {
    Stick,
    NotificationContainer,
    Toast,
    WebSocketStatusIndicator,
    Navbar
  },
  setup() {
    // 获取状态管理实例
    const router = useRouter()
    const themeStore = useThemeStore()
    const userStore = useUserStore()
    const siteSettingsStore = useSiteSettingsStore()

    // 控制WebSocket状态指示器的显示
    const showWebSocketIndicator = ref(true)

    // 初始化主题 (已在main.js中初始化)
    // themeStore.initTheme()

    // 使用计算属性获取暗黑模式状态
    const isDark = computed(() => themeStore.isDark)

    // 判断当前是否在管理后台路由
    const isAdminRoute = computed(() => {
      return router.currentRoute.value.path.startsWith('/admin')
    })

    // 更新暗黑模式
    const updateDarkMode = (value) => {
      themeStore.setTheme(value)
    }

    // 立即初始化WebSocket服务，不等待组件挂载
    // 这确保了WebSocket在应用启动时就开始连接
    initWebSocketService();

    // 初始化平滑滚动和用户状态
    onMounted(async () => {
      // 初始化用户状态
      userStore.initState()

      // 初始化系统设置
      siteSettingsStore.initSettings()

      // 确保WebSocket连接是活跃的
      // 如果连接已关闭，尝试重新连接
      if (!window.webSocketInitialized || webSocketService.status === WebSocketStatus.CLOSED) {
        console.log('确保WebSocket连接活跃');
        initWebSocketService();
      } else {
        console.log('WebSocket连接已活跃，状态:', webSocketService.status);
      }

      // 初始化平滑滚动 - 使用动态导入
      try {
        // 动态导入Lenis
        const LenisModule = await window.Lenis()
        if (LenisModule) {
          const lenis = new LenisModule({
            autoRaf: true,
          })
          // 使用 lenis 避免未使用变量的警告
          console.log('Lenis initialized:', lenis ? true : false)
        }
      } catch (error) {
        console.warn('Lenis not available:', error)
      }

      // 检查登录状态
      const token = localStorage.getItem('token');
      if (token) {
        console.log('应用启动时检测到令牌:', token);
        try {
          const isValid = await userStore.checkLoginStatus();
          console.log('令牌验证结果:', isValid ? '有效' : '无效');
        } catch (error) {
          console.error('检查登录状态失败:', error);
          // 清除无效的令牌
          userStore.logout();
        }
      } else {
        console.log('应用启动时未检测到令牌');
      }
    })

    return {
      isDark,
      updateDarkMode,
      showWebSocketIndicator,
      isAdminRoute
    }
  }
}
</script>
