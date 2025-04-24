import { onUnmounted } from 'vue'

/**
 * 创建DOM观察器，监听文章内容变化
 * @param {Object} options 配置选项
 * @returns {Object} 包含DOM观察相关方法的对象
 */
export function useDomObserver(options = {}) {
  const { 
    isComponentMounted, 
    setupHeadingClickHandlers, 
    processCodeBlocks, 
    extractArticleHeadings 
  } = options
  
  let observer = null
  let debounceTimer = null

  /**
   * 设置DOM观察器
   */
  const setupObserver = () => {
    // 监听文章内容容器
    const contentContainer = document.querySelector('.prose')
    if (!contentContainer) return

    // 创建观察器
    observer = new MutationObserver((mutations) => {
      if (!isComponentMounted.value) return

      // 检查是否有相关的变化
      const hasRelevantChanges = mutations.some(mutation => {
        // 只处理添加标题元素的变化
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          for (const node of mutation.addedNodes) {
            if (node.nodeType === Node.ELEMENT_NODE) {
              // 检查是否是标题元素或包含标题元素
              if (node.tagName && /^H[1-6]$/.test(node.tagName) ||
                  node.querySelector && node.querySelector('h1, h2, h3, h4, h5, h6')) {
                return true
              }
            }
          }
        }
        return false
      })

      // 如果有相关变化，使用防抖处理
      if (hasRelevantChanges) {
        // 清除之前的定时器
        if (debounceTimer) {
          clearTimeout(debounceTimer)
        }

        // 设置新的定时器，延迟执行
        const currentIsMounted = isComponentMounted.value
        debounceTimer = setTimeout(() => {
          if (!currentIsMounted) return

          // 更新标题点击处理器
          setupHeadingClickHandlers()

          // 处理代码块
          processCodeBlocks()

          // 同时更新标题列表
          extractArticleHeadings()
        }, 500)
      }
    })

    // 使用更精细的配置，减少不必要的触发
    observer.observe(contentContainer, {
      childList: true,  // 监听子元素的添加和删除
      subtree: true,    // 监听所有后代元素
      attributes: false, // 不监听属性变化
      characterData: false // 不监听文本变化
    })
  }

  /**
   * 清理资源
   */
  const cleanup = () => {
    // 断开观察者连接
    if (observer) {
      observer.disconnect()
      observer = null
    }

    // 清除定时器
    if (debounceTimer) {
      clearTimeout(debounceTimer)
      debounceTimer = null
    }
  }

  // 组件卸载时清理资源
  onUnmounted(cleanup)

  return {
    setupObserver,
    cleanup
  }
}
