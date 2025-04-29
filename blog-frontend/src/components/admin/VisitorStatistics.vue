<template>
  <div class="visitor-statistics">
    <div class="mb-4 flex justify-between items-center">
      <div>
        <h2 class="text-xl font-bold text-gray-800 dark:text-gray-200">访客统计</h2>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
          <i class="fas fa-chart-line text-blue-500 mr-1"></i>
          基于WebSocket连接收集的访客数据统计
          <span class="ml-2 text-xs text-gray-400 dark:text-gray-500">
            <i class="fas fa-clock text-yellow-500 mr-1"></i>
            匿名用户同IP 30分钟内只记录一次；已登录用户按IP和用户ID组合记录
          </span>
        </p>
      </div>

      <!-- 时间范围选择 -->
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600 dark:text-gray-400">统计范围:</span>
        <select
          v-model="days"
          class="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-md text-sm"
          @change="fetchStatistics"
        >
          <option :value="7">最近7天</option>
          <option :value="30">最近30天</option>
          <option :value="90">最近3个月</option>
          <option :value="180">最近6个月</option>
          <option :value="365">最近1年</option>
        </select>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="py-20 flex justify-center">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else>
      <!-- 概览卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-500 dark:text-blue-300 mr-4">
              <i class="fas fa-eye text-xl"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">总访问量</p>
              <p class="text-2xl font-bold text-gray-800 dark:text-gray-200">{{ statistics.total_visits }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100 dark:bg-green-900 text-green-500 dark:text-green-300 mr-4">
              <i class="fas fa-users text-xl"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">独立访客</p>
              <p class="text-2xl font-bold text-gray-800 dark:text-gray-200">{{ statistics.unique_visitors }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-purple-100 dark:bg-purple-900 text-purple-500 dark:text-purple-300 mr-4">
              <i class="fas fa-mobile-alt text-xl"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">移动设备</p>
              <p class="text-2xl font-bold text-gray-800 dark:text-gray-200">{{ statistics.mobile_visits }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-yellow-100 dark:bg-yellow-900 text-yellow-500 dark:text-yellow-300 mr-4">
              <i class="fas fa-robot text-xl"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">爬虫访问</p>
              <p class="text-2xl font-bold text-gray-800 dark:text-gray-200">{{ statistics.bot_visits }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- 访问趋势图 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">访问趋势</h3>
          <div class="h-64">
            <canvas v-if="statistics.recent_trend && statistics.recent_trend.length > 0" ref="trendChart"></canvas>
            <div v-else class="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
              暂无趋势数据
            </div>
          </div>
        </div>

        <!-- 地区分布图 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">地区分布</h3>
          <div class="h-64">
            <canvas v-if="statistics.top_regions && statistics.top_regions.length > 0" ref="regionChart"></canvas>
            <div v-else class="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
              暂无地区数据
            </div>
          </div>
        </div>
      </div>

      <!-- 热门页面 -->
      <div class="grid grid-cols-1 gap-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">热门页面</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    页面路径
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    访问量
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    占比
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="(page, index) in statistics.top_pages" :key="index" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="text-sm text-gray-900 dark:text-gray-100 max-w-xs truncate" :title="page.path">
                      {{ page.path }}
                    </div>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="text-sm text-gray-900 dark:text-gray-100">{{ page.count }}</div>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="text-sm text-gray-900 dark:text-gray-100">
                      {{ ((page.count / statistics.total_visits) * 100).toFixed(2) }}%
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue';
import { visitorApi } from '@/api';
import { Chart, registerables } from 'chart.js';
import message from '@/utils/message';

// 注册所有 Chart.js 组件
Chart.register(...registerables);

export default {
  name: 'VisitorStatistics',
  setup() {
    // 状态
    const statistics = ref({
      total_visits: 0,
      unique_visitors: 0,
      mobile_visits: 0,
      bot_visits: 0,
      top_pages: [],
      top_regions: [],
      recent_trend: []
    });
    const loading = ref(false);
    const days = ref(30);

    // 图表引用
    const trendChart = ref(null);
    const regionChart = ref(null);

    // 图表实例
    let trendChartInstance = null;
    let regionChartInstance = null;

    // 方法
    const fetchStatistics = async () => {
      loading.value = true;
      try {
        const response = await visitorApi.getVisitorStatistics({ days: days.value });
        statistics.value = response;

        // 更新图表
        updateCharts();
      } catch (error) {
        console.error('获取访客统计信息失败:', error);
        message.error('获取访客统计信息失败');
      } finally {
        loading.value = false;
      }
    };

    const updateCharts = () => {
      // 使用 nextTick 确保 DOM 已更新
      nextTick(() => {
        // 添加一个小延迟，确保 DOM 完全渲染
        setTimeout(() => {
          // 检查 canvas 元素是否存在
          if (trendChart.value && regionChart.value) {
            // 更新趋势图
            updateTrendChart();

            // 更新地区分布图
            updateRegionChart();
          } else {
            console.warn('Canvas 元素尚未准备好，稍后重试');
            // 再次尝试更新图表
            setTimeout(updateCharts, 100);
          }
        }, 50);
      });
    };

    const updateTrendChart = () => {
      if (trendChartInstance) {
        trendChartInstance.destroy();
      }

      // 确保 canvas 元素存在
      if (!trendChart.value) {
        console.warn('趋势图 canvas 元素不存在');
        return;
      }

      const ctx = trendChart.value.getContext('2d');

      // 准备数据
      const labels = statistics.value.recent_trend.map(item => item.date);
      const data = statistics.value.recent_trend.map(item => item.count);

      // 创建图表
      trendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '访问量',
            data: data,
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          }
        }
      });
    };

    const updateRegionChart = () => {
      if (regionChartInstance) {
        regionChartInstance.destroy();
      }

      // 确保 canvas 元素存在
      if (!regionChart.value) {
        console.warn('地区分布图 canvas 元素不存在');
        return;
      }

      const ctx = regionChart.value.getContext('2d');

      // 准备数据
      const labels = statistics.value.top_regions.map(item => item.region);
      const data = statistics.value.top_regions.map(item => item.count);

      // 创建图表
      regionChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: [
              'rgba(59, 130, 246, 0.8)',
              'rgba(16, 185, 129, 0.8)',
              'rgba(245, 158, 11, 0.8)',
              'rgba(239, 68, 68, 0.8)',
              'rgba(139, 92, 246, 0.8)',
              'rgba(236, 72, 153, 0.8)',
              'rgba(75, 85, 99, 0.8)',
              'rgba(14, 165, 233, 0.8)',
              'rgba(168, 85, 247, 0.8)',
              'rgba(234, 179, 8, 0.8)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                boxWidth: 12,
                padding: 10
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(2);
                  return `${label}: ${value} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
    };

    // 生命周期钩子
    onMounted(() => {
      // 在组件挂载后获取统计数据
      nextTick(() => {
        // 确保 DOM 已完全渲染
        setTimeout(() => {
          fetchStatistics();
        }, 100);
      });
    });

    onUnmounted(() => {
      // 销毁图表实例
      if (trendChartInstance) {
        trendChartInstance.destroy();
      }

      if (regionChartInstance) {
        regionChartInstance.destroy();
      }
    });

    // 监听天数变化
    watch(() => days.value, () => {
      fetchStatistics();
    });

    return {
      statistics,
      loading,
      days,
      trendChart,
      regionChart,
      fetchStatistics
    };
  }
};
</script>
