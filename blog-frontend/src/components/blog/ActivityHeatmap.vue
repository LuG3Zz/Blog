<template>
  <div class="p-6 mt-4 flex flex-col bg-white dark:bg-gray-800 rounded-xl shadow-md text-center transition-all duration-300 hover:shadow-lg">
    <!-- 标题和描述 -->
    <div class="mb-3">
      <h2 class="text-xl font-bold mb-1 uppercase text-gray-900 dark:text-white tracking-wider">活动热力图</h2>
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-2 leading-relaxed">每日博客活动数量统计</p>
    </div>

    <!-- 过滤器控件 -->
    <div class="flex flex-wrap justify-center gap-3 mb-4">
      <div class="flex items-center">
        <label for="days-select" class="text-sm text-gray-600 dark:text-gray-400 mr-2">时间范围:</label>
        <select
          id="days-select"
          v-model="selectedDays"
          @change="refreshData"
          class="text-sm border border-gray-300 rounded-md px-2 py-1 bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
        >
          <option value="30">30 天</option>
          <option value="90">90 天</option>
          <option value="180">180 天</option>
          <option value="365">365 天</option>
          <option value="730">730 天</option>
        </select>
      </div>

      <div class="flex items-center">
        <label for="action-type-select" class="text-sm text-gray-600 dark:text-gray-400 mr-2">活动类型:</label>
        <select
          id="action-type-select"
          v-model="selectedActionType"
          @change="refreshData"
          class="text-sm border border-gray-300 rounded-md px-2 py-1 bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
        >
          <option value="">全部</option>
          <option value="article">文章</option>
          <option value="comment">评论</option>
          <option value="like">点赞</option>
          <option value="memo">备忘录</option>
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
      <!-- 热力图容器 -->
      <div class="heatmap-wrapper px-4 py-2 bg-white dark:bg-gray-800 rounded-lg transition-all duration-300">
        <calendar-heatmap
          :key="selectedActionType || 'all'"
          :values="heatmapData"
          :end-date="endDate"
          :start-date="startDate"
          :range-color="currentColorScheme"
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
      <div class="flex justify-center flex-wrap gap-4 mb-4 p-3 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm transition-all duration-300">
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded" :style="{ backgroundColor: isDarkMode ? '#374151' : currentColorScheme[0] }"></span>
          <span>无活动</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded" :style="{ backgroundColor: currentColorScheme[1] }"></span>
          <span>1-3条</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded" :style="{ backgroundColor: currentColorScheme[2] }"></span>
          <span>4-6条</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded" :style="{ backgroundColor: currentColorScheme[3] }"></span>
          <span>7-10条</span>
        </div>
        <div class="flex items-center text-sm dark:text-gray-300">
          <span class="inline-block w-4 h-4 mr-2 rounded" :style="{ backgroundColor: currentColorScheme[4] }"></span>
          <span>10条以上</span>
        </div>
      </div>

      <!-- 当前过滤器状态 -->
      <div class="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 py-1 px-3 rounded-full inline-block">
        {{ getFilterStatusText() }}
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
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

    // 不同活动类型的颜色方案
    const colorSchemes = {
      '': ['#ebedf0', '#dbeafe', '#93c5fd', '#3b82f6', '#1d4ed8'], // 默认蓝色
      'article': ['#ebedf0', '#dcfce7', '#86efac', '#22c55e', '#15803d'], // 文章-绿色
      'comment': ['#ebedf0', '#fef9c3', '#fde047', '#eab308', '#a16207'], // 评论-黄色
      'like': ['#ebedf0', '#fee2e2', '#fca5a5', '#ef4444', '#b91c1c'], // 点赞-红色
      'memo': ['#ebedf0', '#f3e8ff', '#d8b4fe', '#a855f7', '#7e22ce']  // 备忘录-紫色
    }

    // 当前选择的颜色方案
    const currentColorScheme = computed(() => {
      return colorSchemes[selectedActionType.value] || colorSchemes['']
    })

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
    const isDarkMode = ref(false)

    // 初始化暗黑模式状态
    const initDarkMode = () => {
      // 首先检查HTML元素是否有dark类
      if (document.documentElement.classList.contains('dark')) {
        isDarkMode.value = true
        console.log('ActivityHeatmap: 检测到暗黑模式 (HTML class)')
        return
      }

      // 然后检查本地存储
      const savedDarkMode = localStorage.getItem('darkMode')
      if (savedDarkMode !== null) {
        isDarkMode.value = savedDarkMode === 'true'
        console.log('ActivityHeatmap: 从本地存储获取暗黑模式设置:', isDarkMode.value)
        return
      }

      // 最后检查系统偏好
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        isDarkMode.value = true
        console.log('ActivityHeatmap: 检测到系统暗黑模式偏好')
        return
      }

      console.log('ActivityHeatmap: 使用默认亮色模式')
    }

    // 监听暗黑模式变化
    const setupDarkModeListener = () => {
      // 监听HTML元素的class变化
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.attributeName === 'class') {
            const hasDarkClass = document.documentElement.classList.contains('dark')
            if (isDarkMode.value !== hasDarkClass) {
              console.log('ActivityHeatmap: 暗黑模式变化 (HTML class):', hasDarkClass)
              isDarkMode.value = hasDarkClass
            }
          }
        })
      })

      observer.observe(document.documentElement, { attributes: true })

      // 监听系统偏好变化
      if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
          // 只有在没有本地设置的情况下才使用系统偏好
          if (localStorage.getItem('darkMode') === null) {
            console.log('ActivityHeatmap: 系统暗黑模式偏好变化:', e.matches)
            isDarkMode.value = e.matches
          }
        })
      }
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
      console.log('ActivityHeatmap: 处理传入的活动数据', props.activityData);

      if (props.activityData && props.activityData.length > 0) {
        console.log('ActivityHeatmap: 使用传入的数据，长度:', props.activityData.length);

        // 设置日期范围
        const dates = props.activityData.map(item => item.date).sort();
        startDate.value = dates[0];
        endDate.value = dates[dates.length - 1];

        console.log('ActivityHeatmap: 设置日期范围:', startDate.value, '至', endDate.value);

        // 更新统计数据
        updateStats(props.activityData);

        // 存储原始数据用于月度统计
        rawData.value = props.activityData;

        return props.activityData;
      }

      console.log('ActivityHeatmap: 没有传入数据，返回空数组');
      return [];
    }

    // 从后端获取活动热力图数据
    const fetchActivityHeatmap = async (params = {}) => {
      console.log('ActivityHeatmap: 开始获取活动热力图数据，参数:', params);

      // 只有在初始加载且没有指定活动类型时，才使用传入的数据
      if (props.activityData && props.activityData.length > 0 && !params.action_type) {
        // 如果有传入的数据，且没有指定活动类型，就使用传入的数据
        console.log('ActivityHeatmap: 使用传入的数据，跳过API请求');
        heatmapData.value = processActivityData();
        return;
      }

      loading.value = true;
      error.value = null;

      try {
        // 准备请求参数
        const requestParams = {
          days: params.days || 365,
          action_type: params.action_type || undefined,
          user_id: params.user_id || undefined
        };

        console.log('ActivityHeatmap: 请求参数:', JSON.stringify(requestParams));
        console.log('ActivityHeatmap: 当前选择的活动类型:', selectedActionType.value);

        // 使用 statsApi 的 getActivityHeatmap 方法
        const response = await statsApi.getActivityHeatmap(requestParams);
        console.log('ActivityHeatmap: API响应:', response);

        // 处理响应数据
        const responseData = response.data || response;

        // 根据 API 文档，响应格式应为 { values: [{ date, count }] }
        if (responseData && responseData.values && Array.isArray(responseData.values)) {
          console.log('ActivityHeatmap: 响应包含values数组，长度:', responseData.values.length);

          // 将数据设置到热力图
          heatmapData.value = responseData.values;

          // 设置日期范围
          if (responseData.values.length > 0) {
            const dates = responseData.values.map(item => item.date).sort();
            startDate.value = dates[0];
            endDate.value = dates[dates.length - 1];

            console.log('ActivityHeatmap: 设置日期范围:', startDate.value, '至', endDate.value);

            // 更新统计数据
            updateStats(responseData.values);

            // 存储原始数据用于月度统计
            rawData.value = responseData.values;
          } else {
            console.log('ActivityHeatmap: values数组为空');
            heatmapData.value = [];
          }
        } else {
          // 尝试处理其他可能的格式
          if (Array.isArray(responseData)) {
            console.log('ActivityHeatmap: 响应是数组格式，长度:', responseData.length);

            if (responseData.length > 0 && 'date' in responseData[0] && 'count' in responseData[0]) {
              console.log('ActivityHeatmap: 响应数组符合热力图格式');
              heatmapData.value = responseData;

              // 设置日期范围
              const dates = responseData.map(item => item.date).sort();
              startDate.value = dates[0];
              endDate.value = dates[dates.length - 1];

              // 更新统计数据
              updateStats(responseData);

              // 存储原始数据
              rawData.value = responseData;
            } else {
              console.warn('ActivityHeatmap: 响应数组不符合热力图格式');
              heatmapData.value = [];
            }
          } else {
            // 如果响应格式不符合预期，设置空数组
            console.warn('ActivityHeatmap: 响应数据格式不符合预期:', responseData);
            heatmapData.value = [];
          }
        }
      } catch (err) {
        console.error('ActivityHeatmap: 获取活动热力图数据失败:', err.message);
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
      let unit = '条'

      if (selectedActionType.value === 'article') {
        activityType = '文章'
      } else if (selectedActionType.value === 'comment') {
        activityType = '评论'
      } else if (selectedActionType.value === 'like') {
        activityType = '点赞'
      } else if (selectedActionType.value === 'memo') {
        activityType = '备忘录'
        unit = '篇'
      }

      return `${dateStr}: ${value.count} ${unit}${activityType}`
    }

    // 获取过滤器状态文本
    const getFilterStatusText = () => {
      if (!selectedActionType.value) {
        return '当前显示: 所有活动'
      }

      let typeText = selectedActionType.value

      if (selectedActionType.value === 'article') {
        typeText = '文章'
      } else if (selectedActionType.value === 'comment') {
        typeText = '评论'
      } else if (selectedActionType.value === 'like') {
        typeText = '点赞'
      } else if (selectedActionType.value === 'memo') {
        typeText = '备忘录'
      }

      return `当前显示: ${typeText} 类型`
    }




    // 监听活动类型变化
    watch(selectedActionType, (newValue, oldValue) => {
      console.log(`ActivityHeatmap: 活动类型变化 ${oldValue} -> ${newValue}`);
      if (newValue !== oldValue) {
        refreshData();
      }
    });

    // 监听天数变化
    watch(selectedDays, (newValue, oldValue) => {
      console.log(`ActivityHeatmap: 天数变化 ${oldValue} -> ${newValue}`);
      if (newValue !== oldValue) {
        refreshData();
      }
    });

    onMounted(() => {
      console.log('ActivityHeatmap: 组件挂载');

      // 初始化暗黑模式
      initDarkMode();

      // 设置暗黑模式监听器
      setupDarkModeListener();

      // 从 API 获取数据，使用默认过滤器参数
      refreshData();
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
      getFilterStatusText,
      isDarkMode,
      currentColorScheme,
      // 过滤器相关
      selectedDays,
      selectedActionType,
      refreshData,
      CalendarHeatmap
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
  transition: all 0.3s ease;
}

.p-6:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.dark .p-6 {
  background-color: #1f2937;
  border-color: #374151;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.dark .p-6:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

/* 热力图包装器样式 */
.heatmap-wrapper {
  overflow-x: auto;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-radius: 12px;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.dark .heatmap-wrapper {
  scrollbar-color: #475569 #1f2937;
}

/* 自定义滚动条 */
.heatmap-wrapper::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.heatmap-wrapper::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.dark .heatmap-wrapper::-webkit-scrollbar-track {
  background: #1f2937;
}

.heatmap-wrapper::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 3px;
}

.dark .heatmap-wrapper::-webkit-scrollbar-thumb {
  background-color: #475569;
}

/* 日历热力图样式 */
.calendar-heatmap {
  background-color: #fff;
  position: relative;
  padding: 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
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
  font-weight: 500;
}

.dark :deep(.vch__months) {
  color: #9ca3af;
}

:deep(.vch__days) {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.dark :deep(.vch__days) {
  color: #9ca3af;
}

:deep(.vch__legend) {
  display: none; /* 隐藏默认图例，使用我们自定义的图例 */
}

/* 热力图单元格样式 */
:deep(.vch__day) {
  transition: transform 0.2s ease;
}

:deep(.vch__day:hover) {
  transform: scale(1.2);
  z-index: 10;
}

/* 工具提示样式 */
:deep(.vch__tooltip) {
  background-color: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  padding: 8px 12px !important;
  font-size: 0.875rem !important;
  color: #1f2937 !important;
  backdrop-filter: blur(4px);
}

.dark :deep(.vch__tooltip) {
  background-color: rgba(31, 41, 55, 0.95) !important;
  border-color: #374151 !important;
  color: #f3f4f6 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}
</style>
