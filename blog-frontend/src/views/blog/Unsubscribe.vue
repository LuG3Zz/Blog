<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    
    <main class="flex-grow container mx-auto px-4 py-8">
      <div class="max-w-lg mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold mb-4 text-center">取消订阅</h1>
        
        <div v-if="loading" class="flex justify-center my-8">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
        
        <div v-else-if="error" class="bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100 p-4 rounded-md mb-4">
          {{ error }}
        </div>
        
        <div v-else-if="success" class="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100 p-4 rounded-md mb-4">
          <p>{{ success }}</p>
          <div class="mt-4 flex justify-center">
            <router-link to="/" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              返回首页
            </router-link>
          </div>
        </div>
        
        <div v-else>
          <p class="mb-4">
            您确定要取消订阅吗？取消后，您将不再收到相关的邮件通知。
          </p>
          
          <div class="flex justify-center space-x-4">
            <button 
              @click="handleUnsubscribe" 
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              :disabled="loading"
            >
              确认取消订阅
            </button>
            
            <router-link 
              to="/" 
              class="px-4 py-2 bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-400 dark:hover:bg-gray-600"
            >
              返回首页
            </router-link>
          </div>
        </div>
      </div>
    </main>
    
    <Footer />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { subscriptionApi } from '@/api';
import Navbar from '@/components/blog/Navbar.vue';
import Footer from '@/components/blog/Footer.vue';

export default {
  name: 'Unsubscribe',
  components: {
    Navbar,
    Footer
  },
  
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const loading = ref(false);
    const error = ref(null);
    const success = ref(null);
    
    // 获取令牌
    const token = ref(route.query.token);
    
    // 处理取消订阅
    const handleUnsubscribe = async () => {
      if (!token.value) {
        error.value = '无效的取消订阅链接';
        return;
      }
      
      loading.value = true;
      error.value = null;
      
      try {
        await subscriptionApi.unsubscribeByToken(token.value);
        success.value = '您已成功取消订阅，不会再收到相关邮件通知。';
      } catch (err) {
        console.error('取消订阅失败:', err);
        error.value = '取消订阅失败，请稍后重试或联系管理员。';
      } finally {
        loading.value = false;
      }
    };
    
    // 如果是自动取消订阅模式，直接执行取消订阅
    onMounted(() => {
      if (route.query.auto === 'true' && token.value) {
        handleUnsubscribe();
      }
    });
    
    return {
      loading,
      error,
      success,
      handleUnsubscribe
    };
  }
};
</script>
