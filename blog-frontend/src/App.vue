<template>
  <div class="min-h-screen flex flex-col bg-primary dark:bg-dark-primary text-secondary dark:text-dark-secondary">
    <router-view />
    <Stick :initial-dark-mode="isDark" @update:dark-mode="updateDarkMode" />
    <NotificationContainer />
    <Toast />
  </div>
</template>

<script>
import { onMounted, computed } from 'vue'
import { userStore, themeStore } from './store'
import Stick from './components/ui/stick.vue'
import NotificationContainer from './components/ui/NotificationContainer.vue'
import Toast from './components/ui/Toast.vue'
import { initWebSocketService } from './services/websocket'

export default {
  name: 'App',
  components: {
    Stick,
    NotificationContainer,
    Toast
  },
  setup() {
    // 初始化主题
    themeStore.initTheme()

    // 使用计算属性获取暗黑模式状态
    const isDark = computed(() => themeStore.state.isDark)

    // 更新暗黑模式
    const updateDarkMode = (value) => {
      themeStore.setTheme(value)
    }

    // 初始化平滑滚动和用户状态
    onMounted(async () => {
      // 初始化 WebSocket 服务
      initWebSocketService();

      // 初始化平滑滚动
      try {
        if (typeof Lenis !== 'undefined') {
          const lenis = new Lenis({
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
      updateDarkMode
    }
  }
}
</script>

<style>
@import './assets/css/style.css';

/* 隐藏滚动条 */
::-webkit-scrollbar {
  display: none;
}

* {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>