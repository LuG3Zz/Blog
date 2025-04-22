<template>
  <div class="p-6 mt-4 flex flex-col bg-white dark:bg-gray-800 rounded-xl shadow-md text-center">
    <!-- 删除测试数据按钮 -->
    <h2 class="text-xl font-bold mb-1 uppercase text-gray-900 dark:text-white tracking-wider">活动热力图</h2>
    <p class="text-sm text-gray-600 dark:text-gray-400 mb-2 leading-relaxed">每日文章创建与修改数量统计</p>

    <!-- 过滤器控件 -->
    <div class="flex flex-wrap justify-center gap-2 mb-4">
      <div class="flex items-center">
        <label for="days-select" class="text-sm text-gray-600 mr-2">时间范围:</label>
        <select
          id="days-select"
          v-model="selectedDays"
          @change="refreshData"
          class="text-sm border border-gray-300 rounded-md px-2 py-1 bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200"
        >
          <option value="30">30 天</option>
          <option value="90">90 天</option>
          <option value="180">180 天</option>
          <option value="365">365 天</option>
          <option value="730">730 天</option>
        </select>
      </div>

      <div class="flex items-center">
        <label for="action-type-select" class="text-sm text-gray-600 mr-2">活动类型:</label>
        <select
          id="action-type-select"
          v-model="selectedActionType"
          @change="refreshData"
          class="text-sm border border-gray-300 rounded-md px-2 py-1 bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200"
        >
          <option value="">全部</option>
          <option value="article">文章</option>
          <option value="comment">评论</option>
          <option value="like">点赞</option>
        </select>
      </div>
    </div>

    <!-- 加载中状态 -->
    <LoadingSpinner v-if="loading" message="正在加载活动数据..." size="large" />

    <!-- 错误提示 -->
    <ErrorDisplay
      v-else-if="error"
      title="加载活动数据失败"
      :message="error"
      :retry-function="refreshData"
    />

    <!-- 热力图 -->
    <template v-else>
      <div class="heatmap-wrapper px-4 py-2">
        <calendar-heatmap
          :values="heatmapData"
          :end-date="endDate"
          :start-date="startDate"
          :range-color="['#ebedf0', '#dbeafe', '#93c5fd', '#3b82f6', '#1d4ed8']"
          :empty-color="isDarkMode ? '#374151' : '#ebedf0'"
          :tooltip="true"
          :tooltip-unit="selectedActionType ? selectedActionType : '活动'"
          :tooltip-formatter="formatTooltip"
          :max="15"
          :round="4"
          :dark-mode="isDarkMode"
          :no-data-text="'暂无数据'"
          :month-labels="['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']"
          :day-labels="['日', '一', '二', '三', '四', '五', '六']"
          :vertical="false"
          :gutter-size="1"
          :show-month-boundaries="true"
          class="mb-4"
        />
      </div>

      <!-- 热力图图例 -->
      <div class="flex justify-center flex-wrap gap-4 mb-6 p-3 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm">
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded bg-[#ebedf0] dark:bg-gray-500"></span>
          <span>无活动</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded bg-[#dbeafe]"></span>
          <span>1-3条</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded bg-[#93c5fd]"></span>
          <span>4-6条</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded bg-[#3b82f6]"></span>
          <span>7-10条</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded bg-[#1d4ed8]"></span>
          <span>10条以上</span>
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-400 ml-2">
          {{ selectedActionType ? `当前显示: ${selectedActionType} 类型` : '当前显示: 所有活动' }}
        </div>
      </div>
    </template>
  </div>

</template>

<script>
import { ref, onMounted } from 'vue'
import { CalendarHeatmap } from 'vue3-calendar-heatmap'
import 'vue3-calendar-heatmap/dist/style.css'
import { statsApi } from '@/api'
import { format } from 'date-fns'
import { ErrorDisplay, LoadingSpinner } from '@/components/ui'

export default {
  name: 'ActivityHeatmap',
  components: {
    CalendarHeatmap,
    ErrorDisplay,
    LoadingSpinner
  },
  props: {
    activityData: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    // 基本状态
    const loading = ref(false)
    const error = ref(null)
    const heatmapData = ref([])

    // 过滤器状态
    const selectedDays = ref('365')
    const selectedActionType = ref('')

    // 设置日期范围为过去一年
    const today = new Date()
    const endDate = ref(format(today, 'yyyy-MM-dd'))
    const oneYearAgo = new Date(today)
    oneYearAgo.setFullYear(today.getFullYear() - 1)
    const startDate = ref(format(oneYearAgo, 'yyyy-MM-dd'))

    // 统计数据和原始数据
    const rawData = ref([])

    // 刷新数据方法
    const refreshData = () => {
      const params = {
        days: parseInt(selectedDays.value),
        action_type: selectedActionType.value || undefined
      }
      fetchActivityHeatmap(params)
    }

    // 检测暗黑模式
    const isDarkMode = ref(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)

    // 监听暗黑模式变化
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        isDarkMode.value = e.matches
      })
    }

    // 删除不需要的计算属性

    // 统计数据
    const stats = ref({
      todayCount: 0,
      weeklyCount: 0,
      totalPublished: 0
    })

    // 处理传入的活动数据
    const processActivityData = () => {
      if (props.activityData && props.activityData.length > 0) {
        // 使用传入的数据
        // 设置日期范围
        if (props.activityData.length > 0) {
          const dates = props.activityData.map(item => item.date).sort();
          startDate.value = dates[0];
          endDate.value = dates[dates.length - 1];
        }
        return props.activityData;
      }
      return []
    }

    // 从后端获取活动热力图数据
    const fetchActivityHeatmap = async (params = {}) => {
      if (props.activityData && props.activityData.length > 0) {
        // 如果有传入的数据，就不需要获取
        heatmapData.value = processActivityData()
        return
      }

      loading.value = true
      error.value = null

      try {
        // 准备请求参数
        const requestParams = {
          days: params.days || 365,
          ...params.action_type ? { action_type: params.action_type } : {},
          ...params.user_id ? { user_id: params.user_id } : {}
        };

        // 使用 statsApi 的 getActivityHeatmap 方法
        const response = await statsApi.getActivityHeatmap(requestParams);

        // 处理响应数据
        const responseData = response.data || response;

        // 根据 API 文档，响应格式应为 { values: [{ date, count }] }
        if (responseData && responseData.values && Array.isArray(responseData.values)) {
          // 将数据设置到热力图
          heatmapData.value = responseData.values;

          // 设置日期范围
          if (responseData.values.length > 0) {
            const dates = responseData.values.map(item => item.date).sort();
            startDate.value = dates[0];
            endDate.value = dates[dates.length - 1];

            // 更新统计数据
            updateStats(responseData.values);

            // 存储原始数据用于月度统计
            rawData.value = responseData.values;
          } else {
            heatmapData.value = [];
          }
        } else {
          // 如果响应格式不符合预期，设置空数组
          console.warn('响应数据格式不符合预期:', responseData);
          heatmapData.value = [];
        }
      } catch (err) {
        console.error('获取活动热力图数据失败:', err.message);
        error.value = '获取活动热力图数据失败';
        heatmapData.value = [];
      } finally {
        loading.value = false;
      }
    }

    // 更新统计数据
    const updateStats = (data) => {
      if (!Array.isArray(data)) return

      // 获取当前日期
      const today = new Date()
      const todayStr = format(today, 'yyyy-MM-dd')
      const oneWeekAgo = new Date(today)
      oneWeekAgo.setDate(today.getDate() - 7)
      const oneWeekAgoStr = format(oneWeekAgo, 'yyyy-MM-dd')

      // 今日活动数
      const todayData = data.find(item => item.date === todayStr)
      stats.value.todayCount = todayData ? (todayData.count || 0) : 0;

      // 上周活跃度
      stats.value.weeklyCount = data
        .filter(item => item.date >= oneWeekAgoStr && item.date <= todayStr)
        .reduce((sum, item) => sum + (item.count || 0), 0);

      // 总活动数
      const totalActivities = data.reduce((sum, item) => sum + (item.count || 0), 0);
      stats.value.totalPublished = Math.floor(totalActivities * 0.4);
    }

    // 获取本月新增数量
    const getMonthlyCount = () => {
      if (!Array.isArray(rawData.value)) return 0

      const today = new Date()
      const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1)

      return rawData.value
        .filter(item => new Date(item.date) >= firstDayOfMonth)
        .reduce((sum, item) => sum + (item.count || 0), 0)
    }

    // 格式化热力图提示框
    const formatTooltip = (value) => {
      if (!value || value.count === null || value.count === undefined) {
        return '无活动'
      }

      const date = new Date(value.date)
      const dateStr = format(date, 'yyyy年MM月dd日')

      // 根据活动类型显示不同的提示文本
      let activityType = '活动'
      if (selectedActionType.value === 'article') {
        activityType = '文章'
      } else if (selectedActionType.value === 'comment') {
        activityType = '评论'
      } else if (selectedActionType.value === 'like') {
        activityType = '点赞'
      }

      return `${dateStr}: ${value.count} 条${activityType}`
    }


    onMounted(() => {
      // 从 API 获取数据，使用默认过滤器参数
      refreshData()
    })

    return {
      loading,
      error,
      heatmapData,
      endDate,
      startDate,
      stats,
      getMonthlyCount,
      formatTooltip,
      isDarkMode,
      // 过滤器相关
      selectedDays,
      selectedActionType,
      refreshData
    }
  }
}
</script>

<style scoped>
/* 热力图容器样式 */
.p-6 {
  background-color: #fff;
  position: relative;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dark .p-6 {
  background-color: #1f2937;
  border-color: #374151;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* 热力图包装器样式 */
.heatmap-wrapper {
  overflow-x: auto;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-radius: 12px;
}

/* 日历热力图样式 */
.calendar-heatmap {
  background-color: #fff;
  position: relative;
  padding: 1rem;
  border-radius: 8px;
}

.dark .calendar-heatmap {
  background-color: #1f2937;
}

/* 自定义 vue3-calendar-heatmap 样式 */
:deep(.vch__container) {
  max-width: 100%;
  overflow-x: auto;
}

:deep(.vch__months) {
  font-size: 0.75rem;
  color: #6b7280;
}

.dark :deep(.vch__months) {
  color: #9ca3af;
}

:deep(.vch__days) {
  font-size: 0.75rem;
  color: #6b7280;
}

.dark :deep(.vch__days) {
  color: #9ca3af;
}

:deep(.vch__legend) {
  display: none; /* 隐藏默认图例，使用我们自定义的图例 */
}
</style>
