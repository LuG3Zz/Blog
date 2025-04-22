<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
      <input 
        type="text" 
        id="title" 
        v-model="formData.title" 
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white" 
        required
        @input="validateForm"
      />
      <p v-if="errors.title" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.title }}</p>
    </div>
    
    <div>
      <label for="category" class="block text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
      <select 
        id="category" 
        v-model="formData.category" 
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
        required
        @change="validateForm"
      >
        <option value="">请选择分类</option>
        <option v-for="category in categories" :key="category.id" :value="category.name">
          {{ category.category_name }}
        </option>
      </select>
      <p v-if="errors.category" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.category }}</p>
    </div>

    <div>
      <label for="summary" class="block text-sm font-medium text-gray-700 dark:text-gray-300">摘要</label>
      <input 
        type="text" 
        id="summary" 
        v-model="formData.summary" 
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-secondary focus:border-secondary dark:bg-gray-700 dark:text-white"
        required
        @input="validateForm"
      />
      <p v-if="errors.summary" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.summary }}</p>
    </div>

    <div>
      <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">内容</label>
      <div id="vditor" class="w-full rounded-md overflow-hidden"></div>
      <p v-if="errors.content" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.content }}</p>
    </div>

    <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
      <button 
        type="submit" 
        :disabled="isSubmitting || !isValid"
        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary text-base font-medium sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="isSubmitting" class="mr-2">
          <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
        {{ submitButtonText }}
      </button>
      <button 
        type="button" 
        @click="$emit('cancel')" 
        class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 text-base font-medium hover:bg-gray-50 dark:hover:bg-gray-600 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
      >
        取消
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      category: '',
      summary: '',
      content: ''
    })
  },
  categories: {
    type: Array,
    required: true
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

// 表单数据
const formData = ref({
  title: props.initialData.title,
  category: props.initialData.category,
  summary: props.initialData.summary,
  content: props.initialData.content
})

// 表单错误信息
const errors = ref({
  title: '',
  category: '',
  summary: '',
  content: ''
})

// 提交状态
const isSubmitting = ref(false)

// 表单验证
const validateForm = () => {
  errors.value = {
    title: !formData.value.title ? '请输入文章标题' : '',
    category: !formData.value.category ? '请选择文章分类' : '',
    summary: !formData.value.summary ? '请输入文章摘要' : '',
    content: !formData.value.content ? '请输入文章内容' : ''
  }
  return !Object.values(errors.value).some(error => error)
}

// 表单是否有效
const isValid = computed(() => {
  return formData.value.title && 
         formData.value.category && 
         formData.value.summary && 
         formData.value.content
})

// 提交按钮文本
const submitButtonText = computed(() => {
  if (isSubmitting.value) {
    return props.isEdit ? '更新中...' : '保存中...'
  }
  return props.isEdit ? '更新' : '保存'
})

// 富文本编辑器实例
let vditor = null

// 初始化富文本编辑器
onMounted(() => {
  vditor = new Vditor('vditor', {
    height: 400,
    mode: 'ir',
    theme: document.documentElement.classList.contains('dark') ? 'dark' : 'light',
    toolbar: [
      'emoji',
      'headings',
      'bold',
      'italic',
      'strike',
      'link',
      '|',
      'list',
      'ordered-list',
      'check',
      'outdent',
      'indent',
      '|',
      'quote',
      'line',
      'code',
      'inline-code',
      'insert-before',
      'insert-after',
      '|',
      'upload',
      'table',
      '|',
      'undo',
      'redo',
      '|',
      'fullscreen',
      'preview',
      'outline',
      'export',
      'help'
    ],
    after: () => {
      vditor.setValue(formData.value.content)
      vditor.vditor.element.addEventListener('input', () => {
        formData.value.content = vditor.getValue()
        validateForm()
      })
    }
  })
})

// 监听暗色模式变化
watch(
  () => document.documentElement.classList.contains('dark'),
  (isDark) => {
    if (vditor) {
      vditor.setTheme(isDark ? 'dark' : 'light')
    }
  }
)

// 表单提交处理
const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    isSubmitting.value = true
    await emit('submit', formData.value)
  } catch (error) {
    console.error('表单提交失败:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>