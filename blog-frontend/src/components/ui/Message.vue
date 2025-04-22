<template>
  <teleport to="body">
    <transition name="dynamic-island">
      <div v-if="visible"
           class="dynamic-island-container"
           :class="[type, expanded ? 'expanded' : 'compact']"
           @click="toggleExpanded">
        <div class="dynamic-island-content">
          <!-- 文本区域 (始终居中显示) -->
          <div class="dynamic-island-text">
            <!-- 图标和文本在同一行内居中显示 -->
            <div class="text-with-icon">
              <!-- 图标 -->
              <span class="icon-wrapper">
                <svg v-if="type === 'info'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else-if="type === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else-if="type === 'warning'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <svg v-else-if="type === 'error'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </span>

              <!-- 文本 -->
              <span class="message-text">{{ text }}</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const visible = ref(false)
const text = ref('')
const type = ref('info') // 可选值: info, success, warning, error
const expanded = ref(false) // 控制灵动岛的展开/收缩状态

// 显示消息
const show = (message, messageType = 'info', duration = 3000) => {
  text.value = message
  type.value = messageType
  visible.value = true

  // 先显示紧凑模式
  expanded.value = false

  // 然后延迟展开
  setTimeout(() => {
    expanded.value = true

    // 展开一段时间后再收缩
    setTimeout(() => {
      expanded.value = false

      // 收缩后再隐藏
      setTimeout(() => {
        visible.value = false
      }, 300) // 等待收缩动画完成
    }, duration - 600) // 留出时间为总时间减去动画时间
  }, 300) // 等待出现动画完成
}

// 点击时切换展开/收缩状态
const toggleExpanded = () => {
  expanded.value = !expanded.value
}

// 导出方法供其他组件使用
defineExpose({
  show
})
</script>

<style scoped>
/* 灵动岛容器基本样式 */
.dynamic-island-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  font-size: 14px;
  line-height: 1.5;
  color: #fff;
  background-color: #000;
  border-radius: 50px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1.0);
  will-change: transform, box-shadow, width, height, border-radius;
}

/* 紧凑模式 */
.compact {
  width: 140px; /* 增加宽度，确保文字能够显示 */
  height: 36px;
  padding: 0 8px;
}

/* 展开模式 */
.expanded {
  width: 320px;
  height: auto;
  min-height: 60px;
  border-radius: 30px;
  padding: 8px;
}

/* 内容布局 */
.dynamic-island-content {
  display: flex;
  align-items: center;
  justify-content: center; /* 水平居中 */
  padding: 8px 16px;
  height: 100%;
  width: 100%;
}

/* 文本区域 */
.dynamic-island-text {
  text-align: center; /* 文本居中 */
  width: 100%;
  height: 100%;
  font-size: large;
  transition: all 0.3s;
  font-weight: bolder;
}

/* 图标和文本的容器 */
.text-with-icon {
  display: flex;
  align-items: center;
  justify-content: center; /* 水平居中 */
  gap: 8px; /* 图标和文本之间的间距 */
}

/* 图标包装器 */
.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1.0);
}

.icon-wrapper svg {
  width: 16px;
  height: 16px;
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1.0);
}

.expanded .icon-wrapper svg {
  width: 20px;
  height: 20px;
}

/* 消息文本 */
.message-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80px; /* 紧凑模式下限制文本宽度 */
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1.0);
  font-size: 13px;
}

.expanded .message-text {
  white-space: normal;
  overflow: visible;
  max-width: 260px; /* 展开模式下增加文本宽度 */
  font-size: 14px;
  line-height: 1.4;
}

/* 不同类型的颜色样式 */
.info .icon-wrapper {
  color: #64b5f6;
}

.success .icon-wrapper {
  color: #66bb6a;
}

.warning .icon-wrapper {
  color: #ffa726;
}

.error .icon-wrapper {
  color: #ef5350;
}

/* 动画效果 */
.dynamic-island-enter-active,
.dynamic-island-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1.0);
}

.dynamic-island-enter-from,
.dynamic-island-leave-to {
  opacity: 0;
  transform: translateX(-50%) scale(0.8);
}

/* 暗黑模式适配 */
@media (prefers-color-scheme: dark) {
  .dynamic-island-container {
    background-color: #1a1a1a;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  }
}

/* 悬停效果 */
.dynamic-island-container:hover {
  transform: translateX(-50%) scale(1.02) translateY(0) !important;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
}

/* 点击效果 */
.dynamic-island-container:active {
  transform: translateX(-50%) scale(0.98) translateY(0) !important;
}

/* 脉冲动画 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.2);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 255, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
  }
}

.compact {
  animation: pulse 2s infinite;
}

.dynamic-island-container {
  animation: float 4s ease-in-out infinite;
}

/* 添加微妙的浮动效果 */
@keyframes float {
  0% {
    transform: translateX(-50%) translateY(0px);
  }
  50% {
    transform: translateX(-50%) translateY(-3px);
  }
  100% {
    transform: translateX(-50%) translateY(0px);
  }
}

.dynamic-island-container:hover {
  animation-play-state: paused;
}
</style>
