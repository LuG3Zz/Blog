<template>
  <div class="site-settings-manage p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-2">系统设置</h1>
      <p class="text-gray-600 dark:text-gray-400">自定义网站标题、副标题、导航栏文字和首页banner图片等</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="loader"></div>
    </div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 p-4 rounded mb-6">
      {{ error }}
      <button @click="fetchSettings" class="ml-4 px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700">
        重试
      </button>
    </div>

    <!-- 设置表单 -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 基本设置 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">基本设置</h2>
        <form @submit.prevent="saveSettings">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">网站标题</label>
            <input
              v-model="formData.site_title"
              type="text"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入网站标题"
            >
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">网站副标题</label>
            <input
              v-model="formData.site_subtitle"
              type="text"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入网站副标题"
            >
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">页脚文字</label>
            <input
              v-model="formData.footer_text"
              type="text"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入页脚文字"
            >
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">网站描述</label>
            <textarea
              v-model="formData.meta_description"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入网站描述"
              rows="3"
            ></textarea>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">网站关键词</label>
            <input
              v-model="formData.meta_keywords"
              type="text"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入网站关键词，用逗号分隔"
            >
          </div>
        </form>
      </div>

      <!-- 导航栏设置 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">导航栏设置</h2>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">导航栏文字</label>
          <div v-for="(value, key) in navItems" :key="key" class="flex items-center mb-2">
            <span class="w-1/3">{{ key }}:</span>
            <input
              v-model="navItems[key]"
              type="text"
              class="w-2/3 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
            >
          </div>
        </div>
      </div>

      <!-- 图片设置 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">图片设置</h2>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">首页Banner图片</label>
          <div class="flex items-center">
            <input
              v-model="formData.banner_image"
              type="text"
              class="flex-1 px-3 py-2 border rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入图片URL或从文件管理器选择"
            >
            <button
              @click="openFileManager('banner_image')"
              class="px-4 py-2 bg-blue-600 text-white rounded-r hover:bg-blue-700"
            >
              选择
            </button>
          </div>
          <div v-if="formData.banner_image" class="mt-2">
            <img :src="formData.banner_image" alt="Banner预览" class="max-h-40 rounded border">
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">网站Logo</label>
          <div class="flex items-center">
            <input
              v-model="formData.logo_image"
              type="text"
              class="flex-1 px-3 py-2 border rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入图片URL或从文件管理器选择"
            >
            <button
              @click="openFileManager('logo_image')"
              class="px-4 py-2 bg-blue-600 text-white rounded-r hover:bg-blue-700"
            >
              选择
            </button>
          </div>
          <div v-if="formData.logo_image" class="mt-2">
            <img :src="formData.logo_image" alt="Logo预览" class="max-h-20 rounded border">
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">网站Favicon</label>
          <div class="flex items-center">
            <input
              v-model="formData.favicon"
              type="text"
              class="flex-1 px-3 py-2 border rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
              placeholder="请输入图片URL或从文件管理器选择"
            >
            <button
              @click="openFileManager('favicon')"
              class="px-4 py-2 bg-blue-600 text-white rounded-r hover:bg-blue-700"
            >
              选择
            </button>
          </div>
          <div v-if="formData.favicon" class="mt-2">
            <img :src="formData.favicon" alt="Favicon预览" class="max-h-10 rounded border">
          </div>
        </div>
      </div>

      <!-- 自定义代码 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">自定义代码</h2>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">自定义CSS</label>
          <textarea
            v-model="formData.custom_css"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 font-mono"
            placeholder="请输入自定义CSS代码"
            rows="5"
          ></textarea>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">自定义JavaScript</label>
          <textarea
            v-model="formData.custom_js"
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 font-mono"
            placeholder="请输入自定义JavaScript代码"
            rows="5"
          ></textarea>
        </div>
      </div>

      <!-- 安全设置 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">安全设置</h2>

        <div class="mb-4">
          <label class="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              v-model="formData.require_email_verification"
              class="form-checkbox h-5 w-5 text-blue-600"
            >
            <span class="text-sm font-medium">要求邮箱验证</span>
          </label>
          <p class="text-xs text-gray-500 mt-1 ml-7">
            启用后，用户注册时需要验证邮箱。这有助于减少垃圾注册和提高账户安全性。
          </p>
        </div>
      </div>

      <!-- 保存按钮 -->
      <div class="col-span-1 lg:col-span-2 flex justify-end">
        <button
          @click="saveSettings"
          class="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 flex items-center"
          :disabled="saving"
        >
          <span v-if="saving">保存中...</span>
          <span v-else>保存设置</span>
        </button>
      </div>
    </div>

    <!-- 文件选择器 -->
    <FileSelector
      v-if="showFileSelector"
      @close="showFileSelector = false"
      @select="handleFileSelected"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { siteSettingsApi, fileApi } from '@/api'
import message from '@/utils/message'
import FileSelector from '@/components/admin/FileSelector.vue'

export default {
  name: 'SiteSettingsManage',
  components: {
    FileSelector
  },
  setup() {
    // 状态
    const loading = ref(true)
    const saving = ref(false)
    const error = ref(null)

    // 表单数据
    const formData = reactive({
      site_title: '',
      site_subtitle: '',
      footer_text: '',
      banner_image: '',
      logo_image: '',
      favicon: '',
      meta_description: '',
      meta_keywords: '',
      custom_css: '',
      custom_js: '',
      require_email_verification: false
    })

    // 导航栏项目
    const navItems = reactive({
      Home: '首页',
      ArticleList: '文章',
      CategoryList: '分类',
      MemoList: '备忘录',
      About: '关于',
      Login: '登录'
    })

    // 文件选择器相关
    const currentFileField = ref('')
    const showFileSelector = ref(false)

    // 获取设置
    const fetchSettings = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await siteSettingsApi.getSiteSettings()

        // 填充表单数据
        Object.keys(formData).forEach(key => {
          if (response[key] !== undefined) {
            formData[key] = response[key]
          }
        })

        // 填充导航栏项目
        if (response.nav_text) {
          Object.keys(response.nav_text).forEach(key => {
            if (navItems[key] !== undefined) {
              navItems[key] = response.nav_text[key]
            }
          })
        }
      } catch (err) {
        console.error('获取系统设置失败:', err)
        error.value = '获取系统设置失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    // 保存设置
    const saveSettings = async () => {
      saving.value = true

      try {
        // 准备提交数据
        const submitData = { ...formData }

        // 添加导航栏文字
        submitData.nav_text = { ...navItems }

        // 发送请求
        await siteSettingsApi.updateSiteSettings(submitData)

        message.success('系统设置保存成功')
      } catch (err) {
        console.error('保存系统设置失败:', err)
        message.error('保存系统设置失败，请稍后重试')
      } finally {
        saving.value = false
      }
    }

    // 打开文件选择器
    const openFileManager = (field) => {
      currentFileField.value = field
      showFileSelector.value = true
    }

    // 处理文件选择
    const handleFileSelected = (file) => {
      if (currentFileField.value && file) {
        formData[currentFileField.value] = file.url
      }
      showFileSelector.value = false
    }

    // 初始化
    onMounted(() => {
      fetchSettings()
    })

    return {
      loading,
      saving,
      error,
      formData,
      navItems,
      fetchSettings,
      saveSettings,
      openFileManager,
      showFileSelector,
      handleFileSelected
    }
  }
}
</script>

<style scoped>
.loader {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.dark .loader {
  border-color: rgba(255, 255, 255, 0.1);
  border-left-color: #3498db;
}
</style>
