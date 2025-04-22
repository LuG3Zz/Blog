<template>
  <div class="min-h-screen flex items-center justify-center bg-primary dark:bg-dark-primary">
    <div class="max-w-md w-full p-8 bg-white dark:bg-gray-800 shadow-lg rounded-lg text-center">
      <div class="mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m0 0v2m0-2h2m-2 0H9m3-4V8m0 0V6m0 2h2m-2 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">访问被拒绝</h1>
      <p class="text-gray-600 dark:text-gray-300 mb-6">
        {{ message || '您没有权限访问此页面。只有管理员用户才能访问后台管理功能。' }}
      </p>
      <div class="flex flex-col space-y-3">
        <button 
          @click="goToHome" 
          class="px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-lg hover:bg-gray-800 dark:hover:bg-gray-300 transition-colors duration-300"
        >
          返回首页
        </button>
        <button 
          @click="goToLogin" 
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-300"
        >
          重新登录
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'UnauthorizedAccess',
  props: {
    message: {
      type: String,
      default: ''
    }
  },
  setup() {
    const router = useRouter()

    const goToHome = () => {
      router.push('/')
    }

    const goToLogin = () => {
      // 先登出当前用户
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('userInfo')
      
      // 跳转到登录页
      router.push('/login')
    }

    return {
      goToHome,
      goToLogin
    }
  }
}
</script>
