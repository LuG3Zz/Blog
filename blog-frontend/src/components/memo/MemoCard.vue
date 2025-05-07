<template>
  <div class="memo-card bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden border border-gray-100 dark:border-gray-700 mb-4">
    <!-- 卡片内容 -->
    <div class="p-4">
      <!-- 内容区域 -->
      <div class="mb-3">
        <!-- 加密内容 -->
        <div v-if="memo.is_encrypted && !decryptedContent">
          <!-- 标题 (如果有) -->
          <h3 v-if="memo.title" class="text-base font-medium text-gray-800 dark:text-gray-200 mb-2">
            {{ memo.title }}
          </h3>

          <!-- 加密内容提示 -->
          <div class="flex flex-col items-center justify-center py-4 px-4 bg-gray-50 dark:bg-gray-900 rounded-md">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-500 dark:text-yellow-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <p class="text-gray-600 dark:text-gray-300 text-center text-sm mb-2">内容已加密，需要密码才能查看</p>
            <button
              @click="openPasswordDialog"
              class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-md transition-colors"
            >
              输入密码查看
            </button>
          </div>
        </div>

        <!-- 普通内容 -->
        <div v-else>
          <!-- 标题 (如果有) -->
          <h3 v-if="memo.title && !isTagOnlyTitle(memo.title)" class="text-base font-medium text-gray-800 dark:text-gray-200 mb-2">
            {{ cleanTitle(memo.title) }}
          </h3>

          <!-- 内容 -->
          <div class="prose dark:prose-invert prose-sm max-w-none text-gray-700 dark:text-gray-300 break-words markdown-content">
            <div v-if="hasContent" v-html="formattedContent"></div>
            <div v-else>无内容</div>
          </div>
        </div>
      </div>

      <!-- 底部信息栏 -->
      <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-700">
        <!-- 左侧：发布者、时间和标签 -->
        <div class="flex items-center text-xs text-gray-500 dark:text-gray-400 overflow-hidden flex-1 min-w-0">
          <!-- 发布者信息 -->
          <span v-if="memo.user" class="flex items-center mr-2 flex-shrink-0">
            <span class="w-4 h-4 relative flex-shrink-0 mr-1">
              <img
                v-if="memo.user.avatar"
                :src="memo.user.avatar"
                class="w-full h-full rounded-full object-cover"
                :alt="memo.user.username"
              />
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-full h-full text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </span>
            <span class="text-gray-600 dark:text-gray-300 font-medium truncate max-w-[80px]">{{ memo.user.username }}</span>
          </span>

          <!-- 时间 -->
          <span class="flex items-center flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="whitespace-nowrap">{{ formatTime(memo.created_at) }}</span>
          </span>

          <!-- 加密标记 -->
          <span v-if="memo.is_encrypted" class="ml-2 flex items-center text-yellow-500 dark:text-yellow-400 flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span class="whitespace-nowrap">私密</span>
          </span>

          <!-- 标签 -->
          <span
            v-if="hasTag(memo)"
            class="ml-2 text-blue-500 dark:text-blue-400 cursor-pointer hover:underline truncate"
            @click="$emit('tag-click', formatTag(memo))"
          >
            #{{ formatTag(memo) }}
          </span>
        </div>

        <!-- 右侧：操作按钮 -->
        <div class="flex items-center space-x-1 flex-shrink-0 ml-2">
          <button
            @click="$emit('view', memo)"
            class="p-1 text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
            title="查看详情"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
          <button
            v-if="isLoggedIn && isOwnMemo"
            @click="$emit('edit', memo)"
            class="p-1 text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
            title="编辑"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
          <button
            v-if="isLoggedIn && isOwnMemo"
            @click="$emit('delete', memo)"
            class="p-1 text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
            title="删除"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 密码对话框 -->
  <PasswordDialog
    v-if="showPasswordDialog"
    :memo-id="memo.id"
    :local-verification="true"
    :correct-password="memo.password"
    :encrypted-content="memo.encryptedContent"
    @close="showPasswordDialog = false"
    @verify-success="handlePasswordVerified"
  />
</template>

<script setup>
import { ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import PasswordDialog from './PasswordDialog.vue';
import { formatRelativeTime } from '@/utils/date-utils';
import { useMemoMarkdown } from '@/composables/useMemoMarkdown';
import { useUserStore } from '@/stores';

const props = defineProps({
  memo: {
    type: Object,
    required: true
  },
  isLoggedIn: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['edit', 'delete', 'view', 'tag-click']);

const showPasswordDialog = ref(false);
const decryptedContent = ref('');

// 获取用户状态
const userStore = useUserStore();
const { userInfo } = storeToRefs(userStore);

// 计算属性：检查是否有内容
const hasContent = computed(() => {
  return !!(decryptedContent.value || (props.memo.content && props.memo.content.trim() !== ''));
});

// 计算属性：检查当前用户是否是备忘录的所有者
const isOwnMemo = computed(() => {
  return props.isLoggedIn && userInfo.value && userInfo.value.id === props.memo.user_id;
});

// 初始化Markdown渲染器
const { renderMarkdown } = useMemoMarkdown();

// 计算属性：格式化后的内容
const formattedContent = computed(() => {
  const content = decryptedContent.value || props.memo.content;
  if (!content) return '';

  // 确保内容是字符串
  const contentStr = typeof content === 'string' ? content : String(content);

  // 使用Markdown渲染
  return renderMarkdown(contentStr);
});

// 使用工具函数格式化时间
const formatTime = (dateString) => {
  return formatRelativeTime(dateString);
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

  // 如果没有标签标记或没有匹配到有效标签，返回空字符串
  return '';
};

// 打开密码对话框
const openPasswordDialog = () => {
  showPasswordDialog.value = true;
};

// 处理密码验证成功
const handlePasswordVerified = (content) => {
  decryptedContent.value = content;
  showPasswordDialog.value = false;
};

// 不再需要这个函数，使用 renderMarkdown 代替

// 检查标题是否只包含标签
const isTagOnlyTitle = (title) => {
  if (!title) return false;
  // 检查标题是否只是一个标签，例如 "#标签名"
  // 支持中文、字母、数字、下划线和连字符
  return /^#[\u4e00-\u9fa5a-zA-Z0-9_-]+$/.test(title.trim());
};

// 清理标题，移除标签部分
const cleanTitle = (title) => {
  if (!title) return '';

  // 如果标题只包含标签，返回空字符串
  if (isTagOnlyTitle(title)) {
    return '';
  }

  // 移除标题中的所有标签
  // 匹配 "#标签" 或 " #标签"（前面有空格）
  return title.replace(/(^|\s)#[\u4e00-\u9fa5a-zA-Z0-9_-]+/g, '').trim();
};
</script>

<style scoped>
.instagram-card {
  transition: all 0.3s ease;
}

.instagram-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 暗黑模式下的卡片悬停效果 */
:global(.dark) .instagram-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
}

/* 限制文本行数 */
.prose {
  display: -webkit-box;
  -webkit-line-clamp: 8;  /* 增加显示行数 */
  line-clamp: 8;  /* 增加显示行数 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 3em;  /* 确保至少有一定高度 */
}

/* Markdown 内容样式 */
.markdown-content {
  /* 基础样式 */
  font-size: 0.875rem;
  line-height: 1.5;

  /* 标题样式 */
  :deep(h1) {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
  }

  :deep(h2) {
    font-size: 1.125rem;
    font-weight: 600;
    margin-top: 0.75rem;
    margin-bottom: 0.5rem;
  }

  :deep(h3, h4, h5, h6) {
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.75rem;
    margin-bottom: 0.5rem;
  }

  /* 段落样式 */
  :deep(p) {
    margin-bottom: 0.5rem;
  }

  /* 列表样式 */
  :deep(ul, ol) {
    padding-left: 1.5rem;
    margin-bottom: 0.5rem;
  }

  :deep(li) {
    margin-bottom: 0.25rem;
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
