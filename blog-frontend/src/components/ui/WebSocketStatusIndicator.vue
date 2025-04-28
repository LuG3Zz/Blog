<template>
  <div
    class="websocket-status-indicator"
    :class="[statusClass, { 'expanded': isExpanded }]"
    @mouseenter="isExpanded = true"
    @mouseleave="isExpanded = false"
    @click="handleClick"
  >
    <div class="status-icon" :title="statusText">
      <div class="icon-inner" :class="statusClass"></div>
    </div>
    <div class="status-text" v-if="isExpanded">
      <div class="status-info">
        <span class="status-label">WebSocket:</span>
        <span class="status-value" :class="statusClass">{{ statusText }}</span>
      </div>
      <div class="status-actions">
        <span v-if="showReconnectButton" class="reconnect-button" @click.stop="reconnect">重连</span>
        <span v-else-if="status === WebSocketStatus.OPEN" class="disconnect-button" @click.stop="disconnect">断开</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { WebSocketStatus, WebSocketStatusText, useWebSocket } from '@/services/websocket-new';

// 状态指示器是否展开
const isExpanded = ref(false);

// 获取WebSocket状态
const { status, connect, disconnect } = useWebSocket();

// 计算状态文本
const statusText = computed(() => {
  return WebSocketStatusText[status.value] || '未知状态';
});

// 计算状态类名
const statusClass = computed(() => {
  switch (status.value) {
    case WebSocketStatus.CONNECTING:
      return 'connecting';
    case WebSocketStatus.OPEN:
      return 'connected';
    case WebSocketStatus.CLOSING:
      return 'closing';
    case WebSocketStatus.CLOSED:
      return 'disconnected';
    default:
      return 'unknown';
  }
});

// 是否显示重连按钮
const showReconnectButton = computed(() => {
  return status.value === WebSocketStatus.CLOSED;
});

// 处理点击事件
const handleClick = () => {
  isExpanded.value = !isExpanded.value;
};

// 重新连接
const reconnect = () => {
  connect();
};

// 组件卸载时断开连接
onUnmounted(() => {
  disconnect();
});
</script>

<style scoped>
.websocket-status-indicator {
  position: fixed;
  bottom: 20px;
  left: 20px; /* 从右下角改为左下角 */
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 6px;
  z-index: 1000;
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.dark .websocket-status-indicator {
  background-color: rgba(30, 30, 30, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.status-icon {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.1);
}

.icon-inner {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.status-text {
  margin-left: 8px;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  max-width: 0;
  transition: max-width 0.3s ease, opacity 0.3s ease;
  opacity: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.expanded .status-text {
  max-width: 200px;
  opacity: 1;
  margin-right: 8px;
}

.status-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-label {
  color: #6b7280;
  font-weight: 500;
}

.status-value {
  font-weight: 600;
}

.status-value.connected {
  color: #10b981;
}

.status-value.connecting {
  color: #f59e0b;
}

.status-value.disconnected {
  color: #ef4444;
}

.status-value.closing {
  color: #6b7280;
}

.status-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

/* 状态颜色 */
.connected .icon-inner {
  background-color: #10b981; /* 绿色 */
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
}

.connecting .icon-inner {
  background-color: #f59e0b; /* 黄色 */
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
  animation: pulse 1.5s infinite;
}

.disconnected .icon-inner {
  background-color: #ef4444; /* 红色 */
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
}

.closing .icon-inner {
  background-color: #6b7280; /* 灰色 */
  box-shadow: 0 0 8px rgba(107, 114, 128, 0.6);
}

.unknown .icon-inner {
  background-color: #8b5cf6; /* 紫色 */
  box-shadow: 0 0 8px rgba(139, 92, 246, 0.6);
}

.reconnect-button, .disconnect-button {
  padding: 2px 6px;
  color: white;
  border-radius: 4px;
  font-size: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.reconnect-button {
  background-color: #3b82f6;
}

.reconnect-button:hover {
  background-color: #2563eb;
}

.disconnect-button {
  background-color: #6b7280;
}

.disconnect-button:hover {
  background-color: #4b5563;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
  100% {
    transform: scale(0.8);
    opacity: 0.8;
  }
}

/* 响应式调整 */
@media (max-width: 640px) {
  .websocket-status-indicator {
    bottom: 10px;
    left: 10px; /* 从右下角改为左下角 */
  }
}
</style>
