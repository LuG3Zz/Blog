/**
 * 事件总线
 * 用于组件间通信
 */
import { reactive } from 'vue';

// 创建事件总线
export const eventBus = reactive({
  // 事件监听器
  listeners: {},

  // 添加事件监听器
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  },

  // 移除事件监听器
  off(event, callback) {
    if (!this.listeners[event]) return;
    if (!callback) {
      this.listeners[event] = [];
      return;
    }
    this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
  },

  // 触发事件
  emit(event, ...args) {
    console.log(`EventBus: 触发事件 ${event}，监听器数量: ${this.listeners[event]?.length || 0}`);
    if (!this.listeners[event]) {
      console.warn(`EventBus: 没有 ${event} 事件的监听器`);
      return;
    }
    this.listeners[event].forEach(callback => {
      try {
        callback(...args);
      } catch (error) {
        console.error(`EventBus: 执行 ${event} 事件的监听器时出错:`, error);
      }
    });
  }
});
