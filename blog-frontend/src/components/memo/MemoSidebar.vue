<template>
  <div class="memo-sidebar bg-white dark:bg-gray-800 h-full flex flex-col overflow-hidden">
    <!-- 顶部标题 -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center space-x-2">
        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
          <i class="fas fa-sticky-note"></i>
        </div>
        <h1 class="text-xl font-bold text-gray-800 dark:text-white">备忘录</h1>
      </div>
    </div>

    <!-- 导航菜单 -->
    <nav class="p-3 space-y-0.5 flex-shrink-0 border-b border-gray-200 dark:border-gray-700">
      <router-link
        to="/memos"
        class="flex items-center px-3 py-1.5 text-sm font-medium rounded-md"
        :class="[
          isActive('/memos') && !hasTag
            ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
        ]"
      >
        <i class="fas fa-home w-5 h-5 mr-2"></i>
        <span>{{ isLoggedIn ? '我的备忘录' : '备忘录' }}</span>
      </router-link>

      <router-link
        to="/memos/explore"
        class="flex items-center px-3 py-1.5 text-sm font-medium rounded-md"
        :class="[
          isActive('/memos/explore')
            ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
        ]"
      >
        <i class="fas fa-compass w-5 h-5 mr-2"></i>
        <span>发现</span>
      </router-link>

      <router-link
        to="/memos/archive"
        class="flex items-center px-3 py-1.5 text-sm font-medium rounded-md"
        :class="[
          isActive('/memos/archive')
            ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
        ]"
      >
        <i class="fas fa-archive w-5 h-5 mr-2"></i>
        <span>归档</span>
      </router-link>
    </nav>

    <!-- 搜索框 -->
    <div class="p-3 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
      <div class="relative">
        <input
          type="text"
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          placeholder="搜索备忘录..."
          class="w-full px-3 py-2 pl-10 text-sm border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <i class="fas fa-search text-gray-400 dark:text-gray-500"></i>
        </div>
        <button
          v-if="searchQuery"
          @click="clearSearch"
          class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <!-- 日历组件 -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
      <h2 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
        日历
      </h2>
      <div class="calendar-container">
        <div class="flex justify-between items-center mb-2">
          <button
            @click="prevMonth"
            class="p-1 text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ currentMonthName }} {{ currentYear }}
          </span>
          <button
            @click="nextMonth"
            class="p-1 text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <!-- 星期标题 -->
        <div class="grid grid-cols-7 gap-1 text-center mb-1">
          <div v-for="day in weekDays" :key="day" class="text-xs text-gray-500 dark:text-gray-400">
            {{ day }}
          </div>
        </div>

        <!-- 日期网格 -->
        <div class="grid grid-cols-7 gap-1">
          <!-- 填充前面的空白 -->
          <div
            v-for="_ in firstDayOfMonth"
            :key="'empty-' + _"
            class="h-7 w-7 rounded-full"
          ></div>

          <!-- 日期 -->
          <div
            v-for="day in daysInMonth"
            :key="day"
            @click="selectDate(day)"
            class="h-7 w-7 flex items-center justify-center text-xs rounded-full cursor-pointer"
            :class="[
              isSelectedDate(day)
                ? 'bg-blue-500 text-white'
                : hasMemosOnDate(day)
                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-800/50'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            ]"
          >
            {{ day }}
          </div>
        </div>

        <!-- 清除日期筛选按钮 -->
        <div v-if="selectedDate" class="mt-2 text-center">
          <button
            @click="clearDateFilter"
            class="text-xs text-blue-500 dark:text-blue-400 hover:underline"
          >
            清除日期筛选
          </button>
        </div>
      </div>
    </div>

    <!-- 筛选选项 -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
      <h2 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
        筛选
      </h2>
      <div class="space-y-1">
        <a
          href="#"
          @click.prevent="toggleEncryptedFilter"
          class="flex items-center group px-3 py-2 text-sm font-medium rounded-md"
          :class="[
            isEncryptedFilterActive
              ? 'bg-yellow-50 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <span>加密动态</span>
        </a>
      </div>
    </div>

    <!-- 标签列表 -->
    <div class="p-4 flex-grow overflow-hidden">
      <h2 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
        标签
      </h2>
      <div class="space-y-1 overflow-y-auto max-h-[calc(100%-2rem)] pr-1">
        <div v-if="tags.length === 0" class="text-sm text-gray-500 dark:text-gray-400 text-center py-2">
          暂无标签
        </div>
        <a
          v-for="tag in tags"
          :key="tag.name"
          href="#"
          @click.prevent="selectTag(tag.name)"
          class="flex items-center group px-3 py-2 text-sm font-medium rounded-md"
          :class="[
            activeTag === tag.name
              ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          <span class="truncate">#{{ tag.name }}</span>
          <span class="ml-auto text-xs text-gray-500 dark:text-gray-400">{{ tag.count }}</span>
        </a>
      </div>
    </div>

    <!-- 底部用户信息 -->
    <div class="p-3 border-t border-gray-200 dark:border-gray-700 flex-shrink-0" v-if="isLoggedIn">
      <div class="flex items-center space-x-2">
        <img
          :src="userAvatar || '/images/default-avatar.png'"
          alt="用户头像"
          class="w-7 h-7 rounded-full"
        >
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ userName || '用户' }}
          </p>
        </div>
        <button
          @click="$emit('create-memo')"
          class="flex-shrink-0 p-1 rounded-full text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/30"
        >
          <i class="fas fa-plus"></i>
        </button>
        <button
          @click="$emit('open-settings')"
          class="flex-shrink-0 p-1 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </div>
    <!-- 删除登录按钮 -->
  </div>
</template>

<script>
import { computed, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores';
import { formatDateTime } from '@/utils/date-utils';

export default {
  name: 'MemoSidebar',
  props: {
    tags: {
      type: Array,
      default: () => [],
      required: true
    },
    memosDates: {
      type: Array,
      default: () => [],
      required: true
    },
    isLoggedIn: {
      type: Boolean,
      default: false,
      required: true
    }
  },
  emits: ['tag-selected', 'date-selected', 'create-memo', 'open-settings', 'search', 'encrypted-filter'],
  setup(props, { emit }) {
    const route = useRoute();
    const router = useRouter();
    const userStore = useUserStore();

    // 监听标签数据变化
    watch(() => props.tags, (newTags) => {
      console.log('MemoSidebar 接收到新的标签数据:', newTags);
    }, { immediate: true, deep: true });

    // 监听日期数据变化
    watch(() => props.memosDates, (newDates) => {
      console.log('MemoSidebar 接收到新的日期数据:', newDates);
    }, { immediate: true, deep: true });

    const activeTag = ref('');
    const hasTag = computed(() => !!activeTag.value);

    // 加密动态筛选
    const isEncryptedFilterActive = ref(false);
    const toggleEncryptedFilter = () => {
      isEncryptedFilterActive.value = !isEncryptedFilterActive.value;
      emit('encrypted-filter', isEncryptedFilterActive.value);

      // 清除标签和日期筛选
      if (isEncryptedFilterActive.value) {
        activeTag.value = '';
        selectedDate.value = null;
      }
    };

    // 搜索相关
    const searchQuery = ref('');

    // 处理搜索
    const handleSearch = () => {
      if (searchQuery.value.trim()) {
        emit('search', searchQuery.value.trim());
      }
    };

    // 清除搜索
    const clearSearch = () => {
      searchQuery.value = '';
      emit('search', '');
    };

    // 使用传入的 isLoggedIn 属性
    const userName = computed(() => userStore.userInfo?.username || '');
    const userAvatar = computed(() => userStore.userInfo?.avatar || '');

    // 日历相关
    const currentDate = ref(new Date());
    const selectedDate = ref(null);

    // 星期几
    const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

    // 当前年份和月份
    const currentYear = computed(() => currentDate.value.getFullYear());
    const currentMonth = computed(() => currentDate.value.getMonth());
    const currentMonthName = computed(() => {
      const months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
      return months[currentMonth.value];
    });

    // 当月第一天是星期几（0-6，0表示星期日）
    const firstDayOfMonth = computed(() => {
      const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay();
      return firstDay;
    });

    // 当月天数
    const daysInMonth = computed(() => {
      return new Date(currentYear.value, currentMonth.value + 1, 0).getDate();
    });

    // 上个月
    const prevMonth = () => {
      currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1);
    };

    // 下个月
    const nextMonth = () => {
      currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1);
    };

    // 选择日期
    const selectDate = (day) => {
      const date = new Date(currentYear.value, currentMonth.value, day);

      // 如果已经选择了这个日期，则取消选择
      if (selectedDate.value &&
          selectedDate.value.getFullYear() === date.getFullYear() &&
          selectedDate.value.getMonth() === date.getMonth() &&
          selectedDate.value.getDate() === date.getDate()) {
        selectedDate.value = null;
        emit('date-selected', null);
      } else {
        selectedDate.value = date;
        emit('date-selected', date);
      }
    };

    // 清除日期筛选
    const clearDateFilter = () => {
      selectedDate.value = null;
      emit('date-selected', null);
    };

    // 检查日期是否被选中
    const isSelectedDate = (day) => {
      return selectedDate.value &&
             selectedDate.value.getFullYear() === currentYear.value &&
             selectedDate.value.getMonth() === currentMonth.value &&
             selectedDate.value.getDate() === day;
    };

    // 检查日期是否有备忘录
    const hasMemosOnDate = (day) => {
      // 使用formatDateTime格式化日期
      const date = new Date(currentYear.value, currentMonth.value, day);
      const dateStr = formatDateTime(date, 'yyyy-MM-dd');
      return props.memosDates.includes(dateStr);
    };

    const isActive = (path) => {
      // 对于首页路径，只有完全匹配时才返回true
      if (path === '/memos') {
        return route.path === '/memos';
      }
      // 对于其他路径，使用startsWith检查
      return route.path === path || route.path.startsWith(`${path}/`);
    };

    const selectTag = (tagName) => {
      if (activeTag.value === tagName) {
        // 取消选择
        activeTag.value = '';
        emit('tag-selected', '');
      } else {
        // 选择标签
        activeTag.value = tagName;
        emit('tag-selected', tagName);
      }
    };

    return {
      activeTag,
      hasTag,
      userName,
      userAvatar,
      isActive,
      selectTag,
      // 加密动态筛选
      isEncryptedFilterActive,
      toggleEncryptedFilter,
      // 搜索相关
      searchQuery,
      handleSearch,
      clearSearch,
      // 日历相关
      currentDate,
      selectedDate,
      weekDays,
      currentYear,
      currentMonth,
      currentMonthName,
      firstDayOfMonth,
      daysInMonth,
      prevMonth,
      nextMonth,
      selectDate,
      clearDateFilter,
      isSelectedDate,
      hasMemosOnDate
    };
  }
};
</script>

<style scoped>
.memo-sidebar {
  width: 100%;
  height: 100%;
  max-height: calc(100vh - 64px);
  transition: all 0.3s;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 日历样式 */
.calendar-container {
  user-select: none;
}

.grid-cols-7 {
  grid-template-columns: repeat(7, minmax(0, 1fr));
}

.grid-cols-7 > div {
  transition: all 0.2s ease;
}

/* 日期悬停效果 */
.grid-cols-7 > div:hover {
  transform: scale(1.1);
}
</style>
