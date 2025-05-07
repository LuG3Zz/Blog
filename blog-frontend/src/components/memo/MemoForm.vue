<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
    <!-- Instagram风格的表单头部 -->
    <div class="border-b border-gray-200 dark:border-gray-700 p-4">
      <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 flex items-center">
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-pink-500 mr-2">
          {{ isEdit ? '✏️' : '✨' }}
        </span>
        {{ isEdit ? '编辑动态' : '创建新动态' }}
      </h2>
    </div>

    <form @submit.prevent="handleSubmit" class="p-4">
      <!-- 标题输入 -->
      <div class="mb-4">
        <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          标题
        </label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
          placeholder="给你的动态起个标题... (可选)"
        />
        <p v-if="errors.title" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.title }}</p>
      </div>

      <!-- 内容输入 -->
      <div class="mb-4">
        <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          内容
        </label>
        <textarea
          id="content"
          v-model="formData.content"
          rows="8"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
          placeholder="分享你的想法..."
          required
        ></textarea>
        <p v-if="errors.content" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.content }}</p>
      </div>

      <!-- 加密选项 -->
      <div class="mb-6 bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
        <div class="flex items-center">
          <input
            id="is_encrypted"
            v-model="formData.is_encrypted"
            type="checkbox"
            class="h-5 w-5 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
          />
          <label for="is_encrypted" class="ml-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
            私密动态 (仅自己可见)
          </label>
        </div>

        <div v-if="formData.is_encrypted" class="mt-4">
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            访问密码
          </label>
          <div class="relative">
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
              placeholder="设置访问密码"
              :required="formData.is_encrypted"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          <p v-if="errors.password" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.password }}</p>
          <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
            设置密码后，查看动态内容时需要输入密码才能查看
          </p>
        </div>
      </div>

      <!-- 按钮区域 -->
      <div class="flex justify-end space-x-3">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-5 py-2 border border-gray-300 dark:border-gray-600 rounded-full shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          取消
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-5 py-2 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isSubmitting">{{ isEdit ? '更新中...' : '发布中...' }}</span>
          <span v-else>{{ isEdit ? '更新' : '发布' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      content: '',
      is_encrypted: false,
      password: ''
    })
  },
  isEdit: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit', 'cancel']);

// 表单数据
const formData = ref({
  title: props.initialData.title || '',
  content: props.initialData.content || '',
  is_encrypted: props.initialData.is_encrypted || false,
  password: ''
});

// 表单错误信息
const errors = ref({
  title: '',
  content: '',
  password: ''
});

// 提交状态
const isSubmitting = ref(false);

// 表单验证
const validateForm = () => {
  errors.value = {
    title: '', // 标题是可选的
    content: !formData.value.content ? '请输入备忘录内容' : '',
    password: formData.value.is_encrypted && !formData.value.password ? '请设置访问密码' : ''
  };

  return !Object.values(errors.value).some(error => error);
};

// 表单提交处理
const handleSubmit = async () => {
  if (!validateForm()) return;

  try {
    isSubmitting.value = true;

    // 记录表单数据
    console.log('表单数据:', {
      title: formData.value.title,
      content_length: formData.value.content ? formData.value.content.length : 0,
      is_encrypted: formData.value.is_encrypted,
      has_password: !!formData.value.password
    });

    // 提交表单数据
    const submitData = {
      title: formData.value.title,
      content: formData.value.content,
      is_encrypted: formData.value.is_encrypted,
      password: formData.value.password || null
    };

    console.log('提交的数据:', JSON.stringify(submitData, (key, value) => {
      if (key === 'content') return `[内容长度: ${value ? value.length : 0}]`;
      if (key === 'password' && value) return '[已设置]';
      return value;
    }, 2));

    await emit('submit', submitData);
  } catch (error) {
    console.error('表单提交失败:', error);
  } finally {
    isSubmitting.value = false;
  }
};

// 组件挂载时初始化
onMounted(() => {
  // 如果是编辑模式，不显示密码（出于安全考虑）
  if (props.isEdit) {
    formData.value = {
      ...props.initialData,
      password: '' // 清空密码字段
    };
  }
});
</script>

<style scoped>
/* 添加过渡效果 */
input, textarea {
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

/* 暗黑模式下的表单元素聚焦效果 */
:global(.dark) input:focus,
:global(.dark) textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.5);
}
</style>
