<template>
  <div class="visitor-list">
    <div class="mb-4 flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-gray-800 dark:text-gray-200">访客记录</h2>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
          <i class="fas fa-wifi text-green-500 mr-1"></i>
          通过WebSocket实时收集的访客数据
          <span class="ml-2 text-xs text-gray-400 dark:text-gray-500">
            <i class="fas fa-clock text-yellow-500 mr-1"></i>
            匿名用户同IP 30分钟内只记录一次；已登录用户按IP和用户ID组合记录
          </span>
          <button
            @click="toggleTimeFormat"
            class="ml-2 text-xs text-blue-500 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
            title="切换时间显示格式"
          >
            <i class="fas fa-sync-alt mr-1"></i>
            {{ useAbsoluteTime ? '显示相对时间' : '显示绝对时间' }}
          </button>
        </p>
      </div>

      <!-- 筛选器 -->
      <div class="flex gap-2">
        <button
          @click="showFilters = !showFilters"
          class="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-md text-sm flex items-center gap-1"
        >
          <i class="fas fa-filter"></i>
          筛选
        </button>

        <button
          v-if="selectedVisitors.length > 0"
          @click="batchDelete"
          class="px-3 py-1 bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300 rounded-md text-sm flex items-center gap-1"
        >
          <i class="fas fa-trash"></i>
          删除选中 ({{ selectedVisitors.length }})
        </button>
      </div>
    </div>

    <!-- 筛选面板 -->
    <div v-if="showFilters" class="mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">日期范围</label>
          <div class="flex gap-2">
            <input
              type="date"
              v-model="filters.startDate"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-gray-200"
            />
            <input
              type="date"
              v-model="filters.endDate"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-gray-200"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">IP地址</label>
          <input
            type="text"
            v-model="filters.ipAddress"
            placeholder="输入IP地址"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-gray-200"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">访问人员</label>
          <input
            type="text"
            v-model="filters.visitorName"
            placeholder="输入访问人员名称"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-gray-200"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">设备类型</label>
          <select
            v-model="filters.deviceType"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-gray-200"
          >
            <option value="">全部</option>
            <option value="mobile">移动设备</option>
            <option value="desktop">桌面设备</option>
            <option value="bot">爬虫</option>
          </select>
        </div>
      </div>

      <div class="mt-4 flex justify-end gap-2">
        <button
          @click="resetFilters"
          class="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded-md text-sm"
        >
          重置
        </button>
        <button
          @click="applyFilters"
          class="px-3 py-1 bg-blue-500 text-white rounded-md text-sm"
        >
          应用筛选
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="py-20 flex justify-center">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <!-- 数据表格 -->
    <div v-else-if="visitors.length > 0" class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th class="w-10 px-3 py-3 text-left">
              <input
                type="checkbox"
                :checked="isAllSelected"
                @change="toggleSelectAll"
                class="rounded border-gray-300 dark:border-gray-600 text-blue-500 focus:ring-blue-500"
              />
            </th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              访问人员
            </th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              IP地址
            </th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              IP属地
            </th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              设备类型
            </th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              访问时间
            </th>
            <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
          <tr v-for="visitor in visitors" :key="visitor.id" class="hover:bg-gray-50 dark:hover:bg-gray-800">
            <td class="px-3 py-4 whitespace-nowrap">
              <input
                type="checkbox"
                :value="visitor.id"
                v-model="selectedVisitors"
                class="rounded border-gray-300 dark:border-gray-600 text-blue-500 focus:ring-blue-500"
              />
            </td>
            <td class="px-3 py-4 whitespace-nowrap">
              <div class="text-sm font-medium" :class="visitor.user_id ? 'text-blue-600 dark:text-blue-400' : 'text-gray-900 dark:text-gray-100'">
                {{ visitor.visitor_name || '访客' }}
                <span v-if="visitor.user_id" class="ml-1 text-xs text-gray-500 dark:text-gray-400">(已登录)</span>
              </div>
            </td>
            <td class="px-3 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-gray-100">{{ visitor.ip_address }}</div>
            </td>
            <td class="px-3 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-gray-100">{{ visitor.ip_region || '未知地区' }}</div>
            </td>
            <td class="px-3 py-4 whitespace-nowrap">
              <span
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="{
                  'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': visitor.is_mobile,
                  'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': !visitor.is_mobile && !visitor.is_bot,
                  'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200': visitor.is_bot
                }"
              >
                {{ visitor.is_bot ? '爬虫' : (visitor.is_mobile ? '移动设备' : '桌面设备') }}
              </span>
            </td>
            <td class="px-3 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-gray-100">{{ formatTime(visitor.visit_time) }}</div>
            </td>
            <td class="px-3 py-4 whitespace-nowrap text-sm font-medium">
              <button
                @click="deleteVisitor(visitor.id)"
                class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 无数据提示 -->
    <div v-else class="py-20 text-center text-gray-500 dark:text-gray-400">
      暂无访客记录
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="mt-6 flex justify-between items-center">
      <div class="text-sm text-gray-600 dark:text-gray-400">
        共 {{ total }} 条记录
      </div>
      <div class="flex gap-2">
        <button
          v-for="p in pages"
          :key="p"
          @click="page = p"
          class="px-3 py-1 rounded-md"
          :class="{
            'bg-blue-500 text-white': page === p,
            'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700': page !== p
          }"
        >
          {{ p }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { visitorApi } from '@/api';
import { formatRelativeTime, formatDateTimeWithTimeZone, getCurrentTimeZone } from '@/utils/date-utils';
import message from '@/utils/message';

export default {
  name: 'VisitorList',
  setup() {
    // 状态
    const visitors = ref([]);
    const total = ref(0);
    const page = ref(1);
    const pageSize = ref(10);
    const loading = ref(false);
    const showFilters = ref(false);
    const selectedVisitors = ref([]);

    // 筛选条件
    const filters = ref({
      startDate: '',
      endDate: '',
      ipAddress: '',
      visitorName: '',
      deviceType: ''
    });

    // 应用的筛选条件
    const appliedFilters = ref({});

    // 计算属性
    const pages = computed(() => {
      const pageCount = Math.ceil(total.value / pageSize.value);
      return Array.from({ length: pageCount }, (_, i) => i + 1);
    });

    const isAllSelected = computed(() => {
      return visitors.value.length > 0 && selectedVisitors.value.length === visitors.value.length;
    });

    // 方法
    const fetchVisitors = async () => {
      loading.value = true;
      try {
        const params = {
          page: page.value,
          page_size: pageSize.value,
          ...appliedFilters.value
        };

        // 处理设备类型筛选
        if (appliedFilters.value.deviceType === 'mobile') {
          params.is_mobile = true;
          params.is_bot = false;
        } else if (appliedFilters.value.deviceType === 'desktop') {
          params.is_mobile = false;
          params.is_bot = false;
        } else if (appliedFilters.value.deviceType === 'bot') {
          params.is_bot = true;
        }

        const response = await visitorApi.getVisitors(params);
        visitors.value = response.items;
        total.value = response.total;
      } catch (error) {
        console.error('获取访客记录失败:', error);
        message.error('获取访客记录失败');
      } finally {
        loading.value = false;
      }
    };

    const deleteVisitor = async (id) => {
      try {
        await visitorApi.deleteVisitor(id);
        message.success('删除成功');
        fetchVisitors();
      } catch (error) {
        console.error('删除访客记录失败:', error);
        message.error('删除失败');
      }
    };

    const batchDelete = async () => {
      if (selectedVisitors.value.length === 0) {
        return;
      }

      try {
        await visitorApi.batchDeleteVisitors(selectedVisitors.value);
        message.success(`成功删除 ${selectedVisitors.value.length} 条记录`);
        selectedVisitors.value = [];
        fetchVisitors();
      } catch (error) {
        console.error('批量删除访客记录失败:', error);
        message.error('批量删除失败');
      }
    };

    const toggleSelectAll = () => {
      if (isAllSelected.value) {
        selectedVisitors.value = [];
      } else {
        selectedVisitors.value = visitors.value.map(visitor => visitor.id);
      }
    };

    const applyFilters = () => {
      // 复制筛选条件
      const newFilters = {};

      if (filters.value.startDate) {
        newFilters.start_date = filters.value.startDate;
      }

      if (filters.value.endDate) {
        newFilters.end_date = filters.value.endDate;
      }

      if (filters.value.ipAddress) {
        newFilters.ip_address = filters.value.ipAddress;
      }

      if (filters.value.visitorName) {
        newFilters.visitor_name = filters.value.visitorName;
      }

      if (filters.value.deviceType) {
        newFilters.deviceType = filters.value.deviceType;
      }

      appliedFilters.value = newFilters;
      page.value = 1;
    };

    const resetFilters = () => {
      filters.value = {
        startDate: '',
        endDate: '',
        ipAddress: '',
        visitorName: '',
        deviceType: ''
      };

      appliedFilters.value = {};
      page.value = 1;
    };

    // 时间格式切换
    const useAbsoluteTime = ref(false);

    // 切换时间显示格式
    const toggleTimeFormat = () => {
      useAbsoluteTime.value = !useAbsoluteTime.value;
    };

    // 获取当前时区
    const timeZone = getCurrentTimeZone();

    // 格式化时间
    const formatTime = (timestamp) => {
      return useAbsoluteTime.value
        ? formatDateTimeWithTimeZone(timestamp)
        : formatRelativeTime(timestamp);
    };

    // 监听分页和筛选条件变化
    watch([() => page.value, () => appliedFilters.value], () => {
      fetchVisitors();
    });

    // 初始加载
    fetchVisitors();

    return {
      visitors,
      total,
      page,
      pages,
      loading,
      showFilters,
      filters,
      selectedVisitors,
      isAllSelected,
      useAbsoluteTime,
      timeZone,
      fetchVisitors,
      deleteVisitor,
      batchDelete,
      toggleSelectAll,
      toggleTimeFormat,
      applyFilters,
      resetFilters,
      formatTime
    };
  }
};
</script>
