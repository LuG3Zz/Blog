<template>
  <div class="bg-gray-50 dark:bg-gray-900 min-h-screen flex flex-col">

    <!-- UseMemos风格的主布局 -->
    <div class="relative flex-1 flex">
      <!-- 遮罩层 - 仅在小屏幕上侧边栏可见时显示 -->
      <div
        v-if="sidebarVisible"
        @click="toggleSidebar"
        class="md:hidden fixed inset-0 bg-black bg-opacity-50 z-5 transition-opacity"
      ></div>

      <!-- 左侧边栏 - 固定 -->
      <div :class="['fixed left-0 top-[64px] bottom-0 z-10 sidebar-width border-r border-gray-200 dark:border-gray-700 shadow-lg transition-transform bg-white dark:bg-gray-800',
                   {'sidebar-visible': sidebarVisible}]">
        <MemoSidebar
          :tags="tagsList"
          :memos-dates="memosDates"
          :is-logged-in="isLoggedIn"
          @tag-selected="handleTagSelected"
          @date-selected="handleDateSelected"
          @create-memo="$router.push('/memos')"
          @open-settings="openSettings"
          @search="handleSearch"
          @encrypted-filter="handleEncryptedFilter"
        />
      </div>

      <!-- 侧边栏切换按钮 - 在所有屏幕尺寸下显示 -->
      <button
        @click="toggleSidebar"
        class="fixed left-4 top-[80px] z-20 bg-blue-500 text-white rounded-full p-2 shadow-lg hover:bg-blue-600 transition-colors"
        :class="{'left-[250px]': sidebarVisible}"
      >
        <svg v-if="!sidebarVisible" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- 主内容区 -->
      <div class="flex-1 overflow-y-auto pl-sidebar pr-4 py-6 scroll-smooth memo-content-area overflow-x-hidden" :class="{'pl-4': !sidebarVisible}" style="height: calc(100vh - 64px); margin-top: 0; padding-bottom: 100px;">
        <div class="max-w-2xl mx-auto">
          <!-- 页面标题 -->
          <div class="mb-6">
            <div class="flex justify-between items-center">
              <h1 class="text-xl font-medium text-gray-800 dark:text-gray-200">
                <span class="text-blue-500 dark:text-blue-400 mr-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </span>
                发现
                <span class="ml-2 text-xs text-yellow-500 dark:text-yellow-400 font-normal">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  包含加密内容
                </span>
              </h1>

              <!-- 筛选和搜索按钮 -->
              <div class="flex items-center space-x-2">
                <button class="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                  </svg>
                </button>
                <button class="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </div>
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              浏览所有用户的备忘录（包括加密内容），发现有趣的内容
            </p>
          </div>

          <!-- 备忘录列表 -->
          <MemoListComponent
            ref="memoListRef"
            :is-logged-in="isLoggedIn"
            :tag-filter="selectedTag"
            :date-filter="selectedDate"
            :encrypted-filter="isEncryptedFilterActive"
            @create="$router.push('/memos')"
            @edit="$router.push('/memos')"
            @delete="$router.push('/memos')"
            @view="handleView"
            @tag-click="handleTagSelected"
            @clear-search="clearSearch"
            @data-updated="updateData"
          />
        </div>
      </div>
    </div>
  </div>

  <!-- 查看备忘录对话框 -->
  <div v-if="showViewDialog" class="fixed inset-0 z-50 flex items-center justify-center modal-container" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- 背景遮罩 -->
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showViewDialog = false"></div>

    <!-- 对话框内容 -->
    <div class="relative bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all max-w-2xl w-full mx-auto modal-content">
      <!-- 标题栏 -->
      <div class="flex justify-between items-center px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">备忘录详情</h3>
        <button
          @click="showViewDialog = false"
          class="text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
        >
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 内容区 -->
      <div v-if="currentMemo" class="p-6 overflow-y-auto modal-body">
        <!-- 标题 (如果有) -->
        <h3 v-if="currentMemo.title" class="text-xl font-medium text-gray-800 dark:text-gray-200 mb-4 text-center">
          {{ currentMemo.title }}
        </h3>

        <!-- Markdown 内容 -->
        <div class="prose dark:prose-invert prose-sm md:prose-base max-w-none text-gray-700 dark:text-gray-300 mb-6 markdown-content">
          <div v-html="formatContent(decryptedContent || currentMemo.content || '无内容')"></div>
        </div>

        <!-- 创建时间 -->
        <div class="text-sm text-gray-500 dark:text-gray-400 text-center">
          创建于 {{ formatDate(currentMemo.created_at) }}
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="px-4 py-3 bg-gray-50 dark:bg-gray-700 flex justify-center">
        <button
          @click="showViewDialog = false"
          class="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          关闭
        </button>
      </div>
    </div>
  </div>

  <!-- 密码验证对话框 -->
  <PasswordDialog
    v-if="showPasswordDialog"
    :memo-id="currentMemo?.id"
    @close="showPasswordDialog = false"
    @verify-success="handlePasswordVerified"
  />
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { memoApi } from '@/api';
import { MemoList as MemoListComponent, PasswordDialog, MemoSidebar } from '@/components/memo';
import toast from '@/composables/useToast';  // 导入为单例
import { useUserStore } from '@/stores';
import { formatDateTime } from '@/utils/date-utils';
import { useMemoMarkdown } from '@/composables/useMemoMarkdown';

export default {
  name: 'MemoExplore',
  components: {
    MemoListComponent,
    PasswordDialog,
    MemoSidebar
  },
  setup() {
    const userStore = useUserStore();

    // 用户登录状态
    const isLoggedIn = computed(() => userStore.isAuthenticated);

    // 侧边栏状态
    const sidebarVisible = ref(window.innerWidth > 768); // 默认在大屏幕上显示

    // 切换侧边栏显示/隐藏
    const toggleSidebar = () => {
      sidebarVisible.value = !sidebarVisible.value;
    };

    // 备忘录列表组件引用
    const memoListRef = ref(null);

    // 搜索相关
    const searchQuery = ref('');

    // 处理搜索
    const handleSearch = async (query) => {
      searchQuery.value = query;

      // 清除标签和日期筛选
      selectedTag.value = '';
      selectedDate.value = null;

      if (query && query.trim() !== '') {
        try {
          // 显示加载状态
          if (memoListRef.value) {
            memoListRef.value.setLoading(true);
          }

          // 调用搜索API
          const results = await memoApi.searchMemos({
            q: query,
            skip: 0,
            limit: 100
          });

          // 更新备忘录列表
          if (memoListRef.value) {
            memoListRef.value.updateMemosDirectly(results, query);
          }
        } catch (error) {
          console.error('搜索备忘录失败:', error);
          toast.showToast(error.message || '搜索备忘录失败', 'error');
        } finally {
          // 隐藏加载状态
          if (memoListRef.value) {
            memoListRef.value.setLoading(false);
          }
        }
      } else {
        // 如果搜索关键词为空，重新获取所有备忘录
        if (memoListRef.value) {
          memoListRef.value.fetchMemos(true);
        }
      }
    };

    // 标签相关
    const selectedTag = ref('');
    const tagsList = ref([]);

    // 日期相关
    const selectedDate = ref(null);
    const memosDates = ref([]);

    // 加密动态筛选
    const isEncryptedFilterActive = ref(false);

    // 查看备忘录对话框
    const showViewDialog = ref(false);
    const showPasswordDialog = ref(false);
    const currentMemo = ref(null);
    const decryptedContent = ref('');

    // 格式化日期
    const formatDate = (dateString) => {
      try {
        return formatDateTime(dateString, 'yyyy年MM月dd日 HH:mm');
      } catch (error) {
        console.error('日期格式化错误:', error);
        return dateString;
      }
    };

    // 处理查看备忘录
    const handleView = (memo) => {
      currentMemo.value = memo;

      // 如果备忘录加密，显示密码对话框
      if (memo.is_encrypted) {
        showPasswordDialog.value = true;
      } else {
        // 否则直接显示详情
        showViewDialog.value = true;
      }
    };

    // 处理密码验证成功
    const handlePasswordVerified = (content) => {
      decryptedContent.value = content;
      showPasswordDialog.value = false;
      showViewDialog.value = true;
    };

    // 处理标签选择
    const handleTagSelected = (tag) => {
      selectedTag.value = tag;
      // 清除日期筛选和加密筛选
      selectedDate.value = null;
      isEncryptedFilterActive.value = false;
      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 处理日期选择
    const handleDateSelected = (date) => {
      selectedDate.value = date;
      // 清除标签筛选和加密筛选
      selectedTag.value = '';
      isEncryptedFilterActive.value = false;
      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 处理加密动态筛选
    const handleEncryptedFilter = (isActive) => {
      isEncryptedFilterActive.value = isActive;

      // 清除标签和日期筛选
      if (isActive) {
        selectedTag.value = '';
        selectedDate.value = null;
      }

      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 打开设置
    const openSettings = () => {
      // 这里可以实现设置功能，暂时只显示提示
      toast.showToast('设置功能即将推出', 'info');
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

    // 清除搜索
    const clearSearch = () => {
      searchQuery.value = '';
      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 提取标签并更新标签列表，同时收集备忘录日期
    const extractTags = () => {
      if (!memoListRef.value || !memoListRef.value.memos) return;

      const memos = memoListRef.value.memos;
      const tagsMap = new Map();
      const datesSet = new Set();

      // 从备忘录内容中提取标签，同时收集日期
      memos.forEach(memo => {
        // 提取标签
        if (memo.content) {
          // 检查内容是否包含标签标记 (#)
          if (memo.content.includes('#')) {
            const tagMatch = memo.content.match(/#([\u4e00-\u9fa5a-zA-Z0-9_-]+)/);
            if (tagMatch && tagMatch[1]) {
              const tagName = tagMatch[1];

              // 只有成功提取到标签时才添加到标签映射中
              if (tagsMap.has(tagName)) {
                tagsMap.set(tagName, tagsMap.get(tagName) + 1);
              } else {
                tagsMap.set(tagName, 1);
              }
            }
            // 如果没有匹配到标签，认为没有标签
          }
          // 如果没有标签标记，认为没有标签
        }

        // 收集日期，使用formatDateTime格式化
        if (memo.created_at) {
          const dateStr = formatDateTime(memo.created_at, 'yyyy-MM-dd');
          datesSet.add(dateStr);
        }
      });

      // 转换为数组格式
      tagsList.value = Array.from(tagsMap.entries()).map(([name, count]) => ({
        name,
        count
      })).sort((a, b) => b.count - a.count);

      // 更新日期列表
      memosDates.value = Array.from(datesSet);
    };

    // 监听备忘录列表组件的数据
    const updateData = () => {
      if (memoListRef.value && memoListRef.value.memos) {
        // 提取标签
        extractTags();
      }
    };

    // 组件挂载后获取数据
    onMounted(() => {
      // 初始化后更新标签
      setTimeout(() => {
        updateData();
      }, 500);
    });

    return {
      memoListRef,
      showViewDialog,
      showPasswordDialog,
      currentMemo,
      decryptedContent,
      isLoggedIn,
      sidebarVisible,
      toggleSidebar,
      selectedTag,
      tagsList,
      selectedDate,
      memosDates,
      isEncryptedFilterActive,
      searchQuery,
      handleSearch,
      clearSearch,
      formatDate,
      handleView,
      handlePasswordVerified,
      handleTagSelected,
      handleDateSelected,
      handleEncryptedFilter,
      openSettings,
      updateData,
      formatContent
    };
  }
};
</script>

<style scoped>
/* 添加页面动画 */
.animate__animated {
  animation-duration: 0.5s;
}

/* 侧边栏宽度 */
.sidebar-width {
  width: 240px;
  min-width: 240px;
  transform: translateX(0);
  transition: transform 0.3s ease, width 0.3s ease, min-width 0.3s ease;
}

/* 当侧边栏隐藏时 */
.sidebar-width:not(.sidebar-visible) {
  transform: translateX(-100%);
}

/* 内容区域左边距，与侧边栏宽度相同 */
.pl-sidebar {
  padding-left: 260px; /* 侧边栏宽度 + 额外间距 */
}

/* 确保内容区域独立滚动 */
.memo-content-area {
  position: relative;
  overscroll-behavior: contain;
  overflow-y: auto !important;
  height: auto !important;
  min-height: calc(100vh - 64px) !important;
}

/* 模态框样式 */
.modal-container {
  padding: 1rem;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.modal-content {
  max-height: 90vh;
  animation: modalFadeIn 0.3s ease-out;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  margin: 0 auto;
}

.modal-body {
  max-height: calc(90vh - 120px); /* 减去标题栏和底部按钮的高度 */
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Markdown 内容样式 */
.markdown-content {
  line-height: 1.6;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-content :deep(p) {
  margin-bottom: 1em;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5em;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #e2e8f0;
  padding-left: 1em;
  color: #718096;
  margin: 1em 0;
}

.markdown-content :deep(pre) {
  background-color: #f7fafc;
  border-radius: 0.375rem;
  padding: 1em;
  overflow-x: auto;
  margin: 1em 0;
}

.dark .markdown-content :deep(pre) {
  background-color: #2d3748;
}

.markdown-content :deep(code) {
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  background-color: rgba(0, 0, 0, 0.05);
}

.dark .markdown-content :deep(code) {
  background-color: rgba(255, 255, 255, 0.1);
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.375rem;
  margin: 1em auto;
  display: block;
}

.markdown-content :deep(a) {
  color: #3182ce;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

.dark .markdown-content :deep(a) {
  color: #63b3ed;
}
</style>
