<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto px-4 py-8">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-200 px-4 py-3 rounded-md mb-4">
      <p>{{ error }}</p>
      <button
        @click="fetchMemo"
        class="mt-2 px-3 py-1 bg-red-200 dark:bg-red-800 hover:bg-red-300 dark:hover:bg-red-700 rounded-md text-sm"
      >
        重试
      </button>
    </div>

    <!-- 备忘录详情 -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div class="p-6">
        <div class="flex justify-between items-start mb-4">
          <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-200">
            {{ cleanTitle(memo.title) }}
            <span
              v-if="hasTag(memo)"
              class="ml-2 text-blue-500 dark:text-blue-400 text-lg"
            >
              #{{ formatTag(memo) }}
            </span>
          </h1>
          <div class="flex items-center space-x-2">
            <span v-if="memo.is_encrypted" class="text-yellow-500 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
              <span class="text-sm">已加密</span>
            </span>
          </div>
        </div>

        <div class="mb-6 text-sm text-gray-500 dark:text-gray-400">
          创建于: {{ formatDate(memo.created_at) }}
          <span v-if="memo.updated_at !== memo.created_at">
            | 更新于: {{ formatDate(memo.updated_at) }}
          </span>
        </div>

        <div class="border-t border-gray-200 dark:border-gray-700 pt-6 mb-6">
          <div v-if="memo.is_encrypted && !decryptedContent" class="flex flex-col items-center justify-center py-12">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-gray-400 dark:text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <p class="text-gray-500 dark:text-gray-400 text-center text-lg mb-4">此备忘录已加密</p>
            <button
              @click="showPasswordDialog = true"
              class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors text-lg"
            >
              输入密码查看
            </button>
          </div>
          <div v-else class="prose dark:prose-invert max-w-none markdown-content">
            <div v-html="formatContent(decryptedContent || memo.content)"></div>
          </div>
        </div>

        <div class="flex justify-between">
          <button
            @click="goBack"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            返回
          </button>

          <div class="flex space-x-3">
            <button
              v-if="isLoggedIn"
              @click="handleEdit"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              编辑
            </button>
            <button
              v-if="isLoggedIn"
              @click="showDeleteDialog = true"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑表单对话框 -->
    <div v-if="showEditForm" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="w-full max-w-2xl">
        <MemoForm
          :initial-data="memo"
          :is-edit="true"
          @submit="handleSubmit"
          @cancel="showEditForm = false"
        />
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            确认删除
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            您确定要删除备忘录 "{{ memo.title }}" 吗？此操作无法撤销。
          </p>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteDialog = false"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button
            @click="confirmDelete"
            :disabled="isDeleting"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isDeleting">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 密码对话框 -->
    <PasswordDialog
      v-if="showPasswordDialog"
      :memo-id="memoId"
      @close="showPasswordDialog = false"
      @verify-success="handlePasswordVerified"
    />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { memoApi } from '@/api';
import { MemoForm, PasswordDialog } from '@/components/memo';
import useToast from '@/composables/useToast';
import { useUserStore } from '@/stores';
import { formatDateTime } from '@/utils/date-utils';
import { useMemoMarkdown } from '@/composables/useMemoMarkdown';

export default {
  name: 'MemoDetailView',
  components: {
    MemoForm,
    PasswordDialog
  },
  setup() {
    // 获取用户状态
    const userStore = useUserStore();
    const isLoggedIn = computed(() => userStore.isLoggedIn);

    // 路由相关
    const route = useRoute();
    const router = useRouter();
    const memoId = computed(() => parseInt(route.params.id));

    // 组件状态
    const memo = ref({});
    const loading = ref(true);
    const error = ref('');
    const decryptedContent = ref('');
    const showEditForm = ref(false);
    const showDeleteDialog = ref(false);
    const showPasswordDialog = ref(false);
    const isDeleting = ref(false);

    // 使用消息提示
    const toast = useToast;

    // 格式化日期
    const formatDate = (dateString) => {
      try {
        return formatDateTime(dateString, 'yyyy年MM月dd日 HH:mm');
      } catch (error) {
        console.error('日期格式化错误:', error);
        return dateString;
      }
    };

    // 获取备忘录详情
    const fetchMemo = async () => {
      loading.value = true;
      error.value = '';

      try {
        // 根据登录状态选择不同的API
        const apiMethod = isLoggedIn.value ? memoApi.getMemo : memoApi.getPublicMemo;

        const response = await apiMethod(memoId.value);
        memo.value = response;
      } catch (err) {
        console.error('获取备忘录详情失败:', err);
        error.value = err.message || '获取备忘录详情失败';
      } finally {
        loading.value = false;
      }
    };

    // 返回上一页
    const goBack = () => {
      router.push('/memos');
    };

    // 处理编辑
    const handleEdit = () => {
      showEditForm.value = true;
    };

    // 处理表单提交
    const handleSubmit = async (formData) => {
      try {
        await memoApi.updateMemo(memoId.value, formData);
        toast.showToast('备忘录更新成功', 'success');
        showEditForm.value = false;

        // 刷新备忘录数据
        await fetchMemo();

        // 如果更新了加密状态，清空已解密的内容
        if (formData.is_encrypted !== memo.value.is_encrypted) {
          decryptedContent.value = '';
        }
      } catch (error) {
        console.error('更新备忘录失败:', error);
        toast.showToast(error.message || '更新备忘录失败', 'error');
      }
    };

    // 确认删除
    const confirmDelete = async () => {
      isDeleting.value = true;

      try {
        await memoApi.deleteMemo(memoId.value);
        toast.showToast('备忘录删除成功', 'success');
        router.push('/memos');
      } catch (error) {
        console.error('删除备忘录失败:', error);
        toast.showToast(error.message || '删除备忘录失败', 'error');
      } finally {
        isDeleting.value = false;
      }
    };

    // 处理密码验证成功
    const handlePasswordVerified = (content) => {
      decryptedContent.value = content;
      showPasswordDialog.value = false;
    };

    // 初始化Markdown渲染器
    const { renderMarkdown } = useMemoMarkdown();

    // 格式化内容，使用Markdown渲染
    const formatContent = (content) => {
      if (!content) return '';

      // 确保内容是字符串
      const contentStr = typeof content === 'string' ? content : String(content);

      // 使用Markdown渲染
      return renderMarkdown(contentStr);
    };

    // 检查内容是否包含标签
    const hasTag = (memo) => {
      if (!memo || !memo.content) return false;
      return memo.content.includes('#');
    };

    // 从内容中提取标签
    const formatTag = (memo) => {
      // 空值检查
      if (!memo || !memo.content) return '';

      // 检查内容是否包含标签标记 (#)
      if (memo.content.includes('#')) {
        // 提取标签，支持中文、字母、数字、下划线和连字符
        const tagMatch = memo.content.match(/#([\u4e00-\u9fa5a-zA-Z0-9_-]+)/);
        if (tagMatch && tagMatch[1]) {
          return tagMatch[1];
        }
      }

      return '';
    };

    // 清理标题，移除标签部分
    const cleanTitle = (title) => {
      if (!title) return '';

      // 如果标题只包含标签，返回空字符串
      if (/^#[\u4e00-\u9fa5a-zA-Z0-9_-]+$/.test(title.trim())) {
        return '';
      }

      // 移除标题中的所有标签
      // 匹配 "#标签" 或 " #标签"（前面有空格）
      return title.replace(/(^|\s)#[\u4e00-\u9fa5a-zA-Z0-9_-]+/g, '').trim();
    };

    // 组件挂载时获取数据
    onMounted(() => {
      fetchMemo();
    });

    return {
      memoId,
      memo,
      loading,
      error,
      decryptedContent,
      showEditForm,
      showDeleteDialog,
      showPasswordDialog,
      isDeleting,
      isLoggedIn,
      formatDate,
      formatContent,
      hasTag,
      formatTag,
      cleanTitle,
      fetchMemo,
      goBack,
      handleEdit,
      handleSubmit,
      confirmDelete,
      handlePasswordVerified
    };
  }
};
</script>

<style scoped>
/* 添加页面过渡效果 */
.container {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 添加卡片悬浮效果 */
.bg-white {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.bg-white:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 暗黑模式下的卡片悬浮效果 */
:global(.dark) .dark\:bg-gray-800:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
}

/* Markdown 内容样式 */
.markdown-content {
  /* 基础样式 */
  font-size: 1rem;
  line-height: 1.6;

  /* 标题样式 */
  :deep(h1) {
    font-size: 1.5rem;
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
  }

  :deep(h2) {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 1.25rem;
    margin-bottom: 0.75rem;
  }

  :deep(h3, h4, h5, h6) {
    font-size: 1.125rem;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }

  /* 段落样式 */
  :deep(p) {
    margin-bottom: 0.75rem;
  }

  /* 列表样式 */
  :deep(ul, ol) {
    padding-left: 1.5rem;
    margin-bottom: 0.75rem;
  }

  :deep(li) {
    margin-bottom: 0.375rem;
  }

  /* 任务列表样式 */
  :deep(input[type="checkbox"]) {
    margin-right: 0.5rem;
  }

  /* 链接样式 */
  :deep(a) {
    color: #3b82f6;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }

  /* 代码样式 */
  :deep(code) {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 0.875em;
    background-color: rgba(0, 0, 0, 0.05);
    padding: 0.2em 0.4em;
    border-radius: 0.25rem;
  }

  :deep(pre) {
    background-color: rgba(0, 0, 0, 0.05);
    padding: 0.75rem;
    border-radius: 0.25rem;
    overflow-x: auto;
    margin-bottom: 0.75rem;

    code {
      background-color: transparent;
      padding: 0;
    }
  }

  /* 引用样式 */
  :deep(blockquote) {
    border-left: 4px solid #e5e7eb;
    padding-left: 1rem;
    color: #6b7280;
    margin-bottom: 0.75rem;
  }

  /* 表格样式 */
  :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 0.75rem;

    th, td {
      border: 1px solid #e5e7eb;
      padding: 0.5rem;
    }

    th {
      background-color: rgba(0, 0, 0, 0.05);
    }
  }

  /* 水平线样式 */
  :deep(hr) {
    border: 0;
    border-top: 1px solid #e5e7eb;
    margin: 1rem 0;
  }

  /* 图片样式 */
  :deep(img) {
    max-width: 100%;
    border-radius: 0.375rem;
    margin: 0.5rem 0;
  }
}
</style>
