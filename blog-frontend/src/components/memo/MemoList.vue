<template>
  <div class="h-full overflow-y-auto w-full">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-200 px-4 py-3 rounded-md mb-4">
      <p>{{ error }}</p>
      <button
        @click="fetchMemos"
        class="mt-2 px-3 py-1 bg-red-200 dark:bg-red-800 hover:bg-red-300 dark:hover:bg-red-700 rounded-md text-sm"
      >
        重试
      </button>
    </div>

    <!-- 空状态 -->
    <div v-else-if="memos.length === 0" class="flex flex-col items-center justify-center py-12 text-gray-500 dark:text-gray-400">
      <!-- 搜索结果为空 -->
      <template v-if="isSearching">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <p class="text-lg font-medium mb-2">未找到相关备忘录</p>
        <p class="text-sm mb-4">没有找到包含 "{{ searchKeyword }}" 的备忘录</p>
        <button
          @click="$emit('clear-search')"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-md transition-colors mr-2"
        >
          清除搜索
        </button>
        <button
          @click="$emit('create')"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
        >
          创建新备忘录
        </button>
      </template>

      <!-- 普通空状态 -->
      <template v-else>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p class="text-lg font-medium mb-2">暂无备忘录</p>
        <p class="text-sm mb-4">点击下方按钮创建您的第一个备忘录</p>
        <button
          @click="$emit('create')"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
        >
          创建备忘录
        </button>
      </template>
    </div>

    <!-- UseMemos风格的备忘录列表 -->
    <div v-else>
      <!-- 时间线分组 -->
      <div v-for="(group, date) in groupedMemos" :key="date" class="mb-6">
        <!-- 日期分隔线 -->
        <div class="flex items-center mb-3">
          <div class="h-px bg-gray-200 dark:bg-gray-700 flex-grow"></div>
          <div class="px-3 text-sm text-gray-500 dark:text-gray-400 font-medium">{{ formatGroupDate(date) }}</div>
          <div class="h-px bg-gray-200 dark:bg-gray-700 flex-grow"></div>
        </div>

        <!-- 当天的备忘录 -->
        <div class="space-y-4">
          <div v-for="memo in group" :key="memo.id">
            <MemoCard
              :memo="memo"
              :is-logged-in="isLoggedIn"
              @edit="$emit('edit', memo)"
              @delete="$emit('delete', memo)"
              @view="$emit('view', memo)"
              @tag-click="handleTagClick"
            />
          </div>
        </div>
      </div>

      <!-- 加载更多指示器 -->
      <div v-if="memos.length > 0" class="flex justify-center mt-8 mb-4">
        <div v-if="loading" class="flex items-center justify-center py-4">
          <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-500"></div>
          <span class="ml-2 text-gray-600 dark:text-gray-400">加载中...</span>
        </div>
        <div v-else-if="hasMore" ref="loadMoreTrigger" class="py-4 text-center text-gray-500 dark:text-gray-400 text-sm">
          向下滚动加载更多
        </div>
        <div v-else class="py-4 text-center text-gray-500 dark:text-gray-400 text-sm">
          没有更多内容了
        </div>
      </div>

      <!-- 没有更多数据 -->
      <div v-if="memos.length === 0 && !loading" class="flex flex-col items-center justify-center py-12">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300 dark:text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 dark:text-gray-400 text-center">
          暂无动态，开始记录你的第一条想法吧！
        </p>
      </div>

      <!-- 占位内容，确保有足够的内容触发滚动 -->
      <div v-if="memos.length > 0 && memos.length < 5" class="h-[500px]"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import { memoApi } from '@/api';
import MemoCard from './MemoCard.vue';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

const props = defineProps({
  limit: {
    type: Number,
    default: 100
  },
  isLoggedIn: {
    type: Boolean,
    default: false
  },
  tagFilter: {
    type: String,
    default: ''
  },
  dateFilter: {
    type: Object,
    default: null
  },
  encryptedFilter: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['create', 'edit', 'delete', 'view', 'tag-click', 'data-updated', 'clear-search']);

const memos = ref([]);
const loading = ref(true);
const error = ref('');
const page = ref(1);
const hasMore = ref(true);
const loadMoreTrigger = ref(null);
const observer = ref(null);
const isSearching = ref(false);
const searchKeyword = ref('');

// 过滤备忘录
const filteredMemos = computed(() => {
  let result = memos.value;

  // 标签筛选
  if (props.tagFilter) {
    result = result.filter(memo => {
      // 从内容中提取标签
      if (memo.content) {
        // 检查是否包含标签格式
        if (memo.content.includes('#')) {
          // 查找所有标签
          const tags = memo.content.match(/#([\u4e00-\u9fa5a-zA-Z0-9_-]+)/g) || [];
          // 检查是否包含筛选标签
          return tags.some(tag => tag.substring(1) === props.tagFilter);
        }
      }
      return false;
    });
  }

  // 日期筛选
  if (props.dateFilter) {
    result = result.filter(memo => {
      const memoDate = new Date(memo.created_at);
      return memoDate.getFullYear() === props.dateFilter.getFullYear() &&
             memoDate.getMonth() === props.dateFilter.getMonth() &&
             memoDate.getDate() === props.dateFilter.getDate();
    });
  }

  // 加密动态筛选
  if (props.encryptedFilter) {
    result = result.filter(memo => memo.is_encrypted);
  }

  return result;
});

// 按日期分组备忘录
const groupedMemos = computed(() => {
  const groups = {};

  filteredMemos.value.forEach(memo => {
    // 提取日期部分 (YYYY-MM-DD)
    const date = new Date(memo.created_at);
    const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;

    if (!groups[dateKey]) {
      groups[dateKey] = [];
    }

    groups[dateKey].push(memo);
  });

  // 按日期降序排序
  return Object.fromEntries(
    Object.entries(groups).sort((a, b) => {
      return new Date(b[0]) - new Date(a[0]);
    })
  );
});

// 格式化分组日期
const formatGroupDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return format(date, 'yyyy年MM月dd日 EEEE', { locale: zhCN });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return dateString;
  }
};

// 获取备忘录列表
const fetchMemos = async (reset = true) => {
  console.log('MemoList.fetchMemos 开始获取备忘录, reset:', reset);

  if (reset) {
    page.value = 1;
    memos.value = [];
    hasMore.value = true;
    isSearching.value = false; // 重置搜索状态
    searchKeyword.value = ''; // 清空搜索关键词
  }

  if (!hasMore.value) {
    console.log('MemoList.fetchMemos 没有更多数据，返回');
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    // 根据登录状态和当前路由选择不同的API
    let apiMethod;

    // 如果是在首页，根据登录状态决定显示个人备忘录还是公开备忘录
    if (window.location.pathname === '/memos') {
      apiMethod = props.isLoggedIn ? memoApi.getMemos : memoApi.getPublicMemos;
      console.log('MemoList.fetchMemos 在首页使用API:', props.isLoggedIn ? 'getMemos (个人备忘录)' : 'getPublicMemos (公开备忘录)');
    }
    // 如果是在探索页面，显示所有备忘录（包括加密的）
    else if (window.location.pathname === '/memos/explore') {
      apiMethod = memoApi.getAllMemos;
      console.log('MemoList.fetchMemos 在探索页面使用API: getAllMemos (所有备忘录，包括加密的)');
    }
    // 默认情况
    else {
      apiMethod = props.isLoggedIn ? memoApi.getMemos : memoApi.getPublicMemos;
      console.log('MemoList.fetchMemos 使用默认API:', props.isLoggedIn ? 'getMemos' : 'getPublicMemos');
    }

    const response = await apiMethod({
      skip: (page.value - 1) * props.limit,
      limit: props.limit
    });

    const newMemos = Array.isArray(response) ? response : [];
    console.log('MemoList.fetchMemos 获取到备忘录数量:', newMemos.length);

    if (reset) {
      memos.value = newMemos;
    } else {
      memos.value = [...memos.value, ...newMemos];
    }

    // 如果返回的数据少于请求的数量，说明没有更多数据了
    hasMore.value = newMemos.length >= props.limit;

    // 更新无限滚动
    updateInfiniteScroll();

    // 触发自定义事件，通知父组件数据已更新
    console.log('MemoList.fetchMemos 数据已更新，通知父组件');
    emit('data-updated', memos.value);
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

// 处理标签点击
const handleTagClick = (tag) => {
  emit('tag-click', tag);
};

// 设置无限滚动
const setupInfiniteScroll = () => {
  // 如果已经有观察者，先断开连接
  if (observer.value) {
    observer.value.disconnect();
  }

  // 创建新的 Intersection Observer
  observer.value = new IntersectionObserver((entries) => {
    // 如果加载触发器可见，且不在加载中，且还有更多数据
    if (entries[0].isIntersecting && !loading.value && hasMore.value) {
      loadMore();
    }
  }, {
    root: null, // 使用视口作为根
    rootMargin: '0px 0px 200px 0px', // 提前 200px 触发
    threshold: 0.1 // 当 10% 的元素可见时触发
  });

  // 在下一个 DOM 更新周期后观察加载触发器
  nextTick(() => {
    if (loadMoreTrigger.value) {
      observer.value.observe(loadMoreTrigger.value);
    }
  });
};

// 组件挂载时获取数据并设置无限滚动
onMounted(() => {
  fetchMemos();

  // 设置无限滚动
  nextTick(() => {
    setupInfiniteScroll();
  });
});

// 组件卸载时清理观察者
onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect();
    observer.value = null;
  }
});

// 监听备忘录数据变化，更新无限滚动
const updateInfiniteScroll = () => {
  nextTick(() => {
    setupInfiniteScroll();
  });
};

// 直接更新备忘录列表（用于搜索结果）
const updateMemosDirectly = (newMemos, keyword = '') => {
  memos.value = Array.isArray(newMemos) ? newMemos : [];
  hasMore.value = false; // 搜索结果不支持无限滚动
  isSearching.value = !!keyword; // 设置搜索状态
  searchKeyword.value = keyword; // 保存搜索关键词

  // 触发自定义事件，通知父组件数据已更新
  console.log('MemoList.updateMemosDirectly 数据已更新，通知父组件');
  emit('data-updated', memos.value);
};

// 设置加载状态
const setLoading = (state) => {
  loading.value = state;
};

// 暴露方法和数据给父组件
defineExpose({
  fetchMemos,
  memos,
  updateMemosDirectly,
  setLoading,
  isSearching,
  searchKeyword
});
</script>

<style scoped>
/* 添加列表项动画 */
.flex > div {
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 为每个卡片添加不同的延迟 */
.flex > div:nth-child(1) { animation-delay: 0.1s; }
.flex > div:nth-child(2) { animation-delay: 0.2s; }
.flex > div:nth-child(3) { animation-delay: 0.3s; }
.flex > div:nth-child(4) { animation-delay: 0.4s; }
.flex > div:nth-child(5) { animation-delay: 0.5s; }
.flex > div:nth-child(6) { animation-delay: 0.6s; }
/* 可以根据需要添加更多 */

/* 加载更多触发器样式 */
.py-4 {
  transition: opacity 0.3s ease;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(107, 114, 128, 0.7);
}

/* 确保列表容器可以正确滚动 */
:deep(.memo-content-area) {
  height: 100%;
  overflow-y: auto;
  overscroll-behavior: contain;
}

/* 确保组件本身可以滚动 */
.h-full {
  height: auto;
  min-height: 200px;
  overflow-y: auto !important;
  width: 100%;
}
</style>
