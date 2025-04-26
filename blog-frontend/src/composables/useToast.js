/**
 * Toast 通知组合式函数
 * 提供简单的消息通知功能
 */
import { ref } from 'vue';

// 创建一个全局状态来存储 toast 消息
const toasts = ref([]);

export function useToast() {
  /**
   * 显示一个 toast 消息
   * @param {string} message - 要显示的消息
   * @param {string} type - 消息类型 (success, error, info, warning)
   * @param {number} duration - 消息显示时间 (毫秒)
   */
  const showToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    
    // 添加新的 toast
    toasts.value.push({
      id,
      message,
      type,
      show: true
    });
    
    // 设置定时器，在指定时间后移除 toast
    setTimeout(() => {
      const index = toasts.value.findIndex(toast => toast.id === id);
      if (index !== -1) {
        // 先设置 show 为 false，触发淡出动画
        toasts.value[index].show = false;
        
        // 然后在动画结束后移除 toast
        setTimeout(() => {
          toasts.value = toasts.value.filter(toast => toast.id !== id);
        }, 300);
      }
    }, duration);
  };
  
  return {
    toasts,
    showToast
  };
}

// 导出一个单例，以便在整个应用中共享 toast 状态
export default useToast();
