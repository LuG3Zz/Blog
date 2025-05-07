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
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-xl font-medium text-gray-800 dark:text-gray-200">
              <span class="text-blue-500 dark:text-blue-400 mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
              </span>
              归档
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

          <!-- 归档内容 -->
          <div class="space-y-8">
            <!-- 按年份分组 -->
            <div v-for="(yearGroup, year) in groupedByYear" :key="year" class="mb-8">
              <!-- 年份标题（可点击收缩/展开） -->
              <div
                @click="toggleYear(year)"
                class="flex items-center cursor-pointer py-2 px-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                <!-- 收缩/展开图标 -->
                <div class="mr-2 text-blue-500 dark:text-blue-400 transition-transform duration-300" :class="{'transform rotate-90': expandedYears[year]}">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <h2 class="text-lg font-medium text-gray-700 dark:text-gray-300">{{ year }}</h2>
                <!-- 备忘录数量 -->
                <span class="ml-2 text-sm text-gray-500 dark:text-gray-400">
                  ({{ Object.values(yearGroup).flat().length }}条)
                </span>
              </div>

              <!-- 按月份分组（仅在年份展开时显示） -->
              <div v-if="expandedYears[year]" class="space-y-4 pl-4 mt-2 animate__animated animate__fadeIn">
                <div v-for="(monthGroup, month) in yearGroup" :key="`${year}-${month}`" class="mb-4">
                  <!-- 月份标题（可点击收缩/展开） -->
                  <div
                    @click="toggleMonth(year, month)"
                    class="flex items-center cursor-pointer py-1 px-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                  >
                    <!-- 收缩/展开图标 -->
                    <div class="mr-2 text-blue-500 dark:text-blue-400 transition-transform duration-300" :class="{'transform rotate-90': expandedMonths[`${year}-${month}`]}">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                    <h3 class="text-md font-medium text-gray-600 dark:text-gray-400">{{ getMonthName(month) }}</h3>
                    <!-- 备忘录数量 -->
                    <span class="ml-2 text-sm text-gray-500 dark:text-gray-400">
                      ({{ monthGroup.length }}条)
                    </span>
                  </div>

                  <!-- 月份内的备忘录（仅在月份展开时显示） -->
                  <div v-if="expandedMonths[`${year}-${month}`]" class="space-y-2 pl-6 mt-2 animate__animated animate__fadeIn">
                    <div
                      v-for="memo in monthGroup"
                      :key="memo.id"
                      class="flex items-center py-2 px-3 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer border-l-2 border-gray-200 dark:border-gray-700"
                      @click="handleView(memo)"
                    >
                      <div class="text-sm text-gray-500 dark:text-gray-400 w-16">{{ formatDay(memo.created_at) }}</div>
                      <div class="ml-4 flex-1 text-gray-700 dark:text-gray-300 truncate">
                        {{ memo.title || (memo.content ? memo.content.substring(0, 20) + '...' : '') }}
                      </div>
                      <div v-if="memo.is_encrypted" class="ml-2 text-yellow-500 dark:text-yellow-400">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 加载更多按钮 -->
            <div v-if="hasMore" class="flex justify-center mt-8 mb-4">
              <button
                @click="loadMore"
                class="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors text-sm"
              >
                加载更多
              </button>
            </div>
          </div>
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
import { PasswordDialog, MemoSidebar } from '@/components/memo';
import { Navbar } from '@/components/layout';
import toast from '@/composables/useToast';  // 导入为单例
import { useUserStore } from '@/stores';
import { formatDateTime } from '@/utils/date-utils';
import { useMemoMarkdown } from '@/composables/useMemoMarkdown';

export default {
  name: 'MemoArchive',
  components: {
    PasswordDialog,
    Navbar,
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

    // 备忘录数据
    const memos = ref([]);
    const loading = ref(true);
    const error = ref('');
    const page = ref(1);
    const hasMore = ref(true);
    const limit = 100;

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

    // 收缩/展开状态
    const expandedYears = ref({});
    const expandedMonths = ref({});

    // 按年份和月份分组备忘录
    const groupedByYear = computed(() => {
      const groups = {};

      // 过滤备忘录
      let filteredMemos = memos.value;

      // 标签筛选
      if (selectedTag.value) {
        filteredMemos = filteredMemos.filter(memo => {
          // 从内容中提取标签
          if (memo.content) {
            // 检查是否包含标签格式
            if (memo.content.includes('#')) {
              // 查找所有标签
              const tags = memo.content.match(/#([\u4e00-\u9fa5a-zA-Z0-9_-]+)/g) || [];
              // 检查是否包含筛选标签
              return tags.some(tag => tag.substring(1) === selectedTag.value);
            }
          }
          return false;
        });
      }

      // 日期筛选
      if (selectedDate.value) {
        filteredMemos = filteredMemos.filter(memo => {
          const memoDate = new Date(memo.created_at);
          return memoDate.getFullYear() === selectedDate.value.getFullYear() &&
                 memoDate.getMonth() === selectedDate.value.getMonth() &&
                 memoDate.getDate() === selectedDate.value.getDate();
        });
      }

      // 加密动态筛选
      if (isEncryptedFilterActive.value) {
        filteredMemos = filteredMemos.filter(memo => memo.is_encrypted);
      }

      filteredMemos.forEach(memo => {
        const date = new Date(memo.created_at);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;

        if (!groups[year]) {
          groups[year] = {};
        }

        if (!groups[year][month]) {
          groups[year][month] = [];
        }

        groups[year][month].push(memo);
      });

      // 按年份降序排序
      return Object.fromEntries(
        Object.entries(groups).sort((a, b) => b[0] - a[0])
      );
    });

    // 获取月份名称
    const getMonthName = (month) => {
      const months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
      return months[parseInt(month) - 1];
    };

    // 格式化日期
    const formatDate = (dateString) => {
      try {
        return formatDateTime(dateString, 'yyyy年MM月dd日 HH:mm');
      } catch (error) {
        console.error('日期格式化错误:', error);
        return dateString;
      }
    };

    // 格式化日期（只显示日）
    const formatDay = (dateString) => {
      try {
        return formatDateTime(dateString, 'dd日');
      } catch (error) {
        console.error('日期格式化错误:', error);
        return dateString;
      }
    };

    // 获取备忘录列表
    const fetchMemos = async (reset = true) => {
      if (reset) {
        page.value = 1;
        memos.value = [];
        hasMore.value = true;
      }

      if (!hasMore.value) return;

      loading.value = true;
      error.value = '';

      try {
        // 根据登录状态选择不同的API
        const apiMethod = isLoggedIn.value ? memoApi.getMemos : memoApi.getPublicMemos;

        const response = await apiMethod({
          skip: (page.value - 1) * limit,
          limit: limit
        });

        const newMemos = Array.isArray(response) ? response : [];

        if (reset) {
          memos.value = newMemos;
        } else {
          memos.value = [...memos.value, ...newMemos];
        }

        // 如果返回的数据少于请求的数量，说明没有更多数据了
        hasMore.value = newMemos.length >= limit;

        // 提取标签
        extractTags();
      } catch (err) {
        console.error('获取备忘录列表失败:', err);
        error.value = err.message || '获取备忘录列表失败';
      } finally {
        loading.value = false;
      }
    };

    // 加载更多数据
    const loadMore = async () => {
      if (loading.value || !hasMore.value) return;

      page.value++;
      await fetchMemos(false);
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

      // 重新获取备忘录数据
      fetchMemos(true);
    };

    // 处理日期选择
    const handleDateSelected = (date) => {
      selectedDate.value = date;
      // 清除标签筛选和加密筛选
      selectedTag.value = '';
      isEncryptedFilterActive.value = false;

      // 重新获取备忘录数据
      fetchMemos(true);
    };

    // 处理加密动态筛选
    const handleEncryptedFilter = (isActive) => {
      isEncryptedFilterActive.value = isActive;

      // 清除标签和日期筛选
      if (isActive) {
        selectedTag.value = '';
        selectedDate.value = null;
      }

      // 重新获取备忘录数据
      fetchMemos(true);
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

    // 切换年份展开/收缩
    const toggleYear = (year) => {
      expandedYears.value = {
        ...expandedYears.value,
        [year]: !expandedYears.value[year]
      };
    };

    // 切换月份展开/收缩
    const toggleMonth = (year, month) => {
      const key = `${year}-${month}`;
      expandedMonths.value = {
        ...expandedMonths.value,
        [key]: !expandedMonths.value[key]
      };
    };

    // 初始化展开状态
    const initExpandedState = () => {
      // 默认展开第一个年份
      const years = Object.keys(groupedByYear.value);
      if (years.length > 0) {
        const firstYear = years[0];
        expandedYears.value = { [firstYear]: true };

        // 默认展开第一个年份的第一个月份
        const months = Object.keys(groupedByYear.value[firstYear] || {});
        if (months.length > 0) {
          const firstMonth = months[0];
          expandedMonths.value = { [`${firstYear}-${firstMonth}`]: true };
        }
      }
    };

    // 提取标签并更新标签列表，同时收集备忘录日期
    const extractTags = () => {
      const tagsMap = new Map();
      const datesSet = new Set();

      // 从备忘录内容中提取标签，同时收集日期
      memos.value.forEach(memo => {
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

    // 组件挂载后获取数据
    onMounted(() => {
      fetchMemos().then(() => {
        // 数据加载完成后初始化展开状态
        initExpandedState();
      });
    });

    return {
      memos,
      loading,
      error,
      hasMore,
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
      groupedByYear,
      expandedYears,
      expandedMonths,
      formatDate,
      formatDay,
      getMonthName,
      fetchMemos,
      loadMore,
      handleView,
      handlePasswordVerified,
      handleTagSelected,
      handleDateSelected,
      handleEncryptedFilter,
      openSettings,
      toggleYear,
      toggleMonth,
      formatContent
    };
  }
};
</script>

<style scoped>
/* 添加页面动画 */
.animate__animated {
  animation-duration: 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate__fadeIn {
  animation-name: fadeIn;
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

/* Markdown 内容样式 */
.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-content p {
  margin-bottom: 1em;
}

.markdown-content ul,
.markdown-content ol {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.markdown-content li {
  margin-bottom: 0.5em;
}

.markdown-content blockquote {
  border-left: 4px solid #e2e8f0;
  padding-left: 1em;
  color: #718096;
  margin: 1em 0;
}

.markdown-content pre {
  background-color: #f7fafc;
  border-radius: 0.375rem;
  padding: 1em;
  overflow-x: auto;
  margin: 1em 0;
}

.dark .markdown-content pre {
  background-color: #2d3748;
}

.markdown-content code {
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  background-color: rgba(0, 0, 0, 0.05);
}

.dark .markdown-content code {
  background-color: rgba(255, 255, 255, 0.1);
}

.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: 0.375rem;
  margin: 1em auto;
  display: block;
}

.markdown-content a {
  color: #3182ce;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

.dark .markdown-content a {
  color: #63b3ed;
}

/* 任务列表样式 */
.markdown-content input[type="checkbox"] {
  margin-right: 0.5em;
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
</style>
