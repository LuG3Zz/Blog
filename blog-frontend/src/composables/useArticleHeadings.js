import { ref, onUnmounted } from 'vue'

/**
 * 处理文章标题和目录
 * @returns {Object} 包含标题相关方法和状态的对象
 */
export function useArticleHeadings() {
  const articleHeadings = ref([])
  const isComponentMounted = ref(true)
  const rafIds = []

  /**
   * 提取文章中的标题
   */
  const extractArticleHeadings = () => {
    if (!isComponentMounted.value) return

    try {
      // 查找所有标题元素
      const headingElements = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')

      if (headingElements.length === 0) {
        console.log('没有找到标题元素')
        return
      }

      // 清空现有标题列表
      articleHeadings.value = []

      // 提取标题信息
      headingElements.forEach((heading) => {
        const id = heading.id || heading.getAttribute('data-id')
        if (!id) return

        const level = parseInt(heading.tagName.substring(1)) // 从 'H1', 'H2' 等提取数字
        const text = heading.textContent.trim()

        articleHeadings.value.push({
          id,
          level,
          text
        })
      })

      // 强制触发响应式更新
      articleHeadings.value = [...articleHeadings.value]
    } catch (error) {
      console.error('提取文章标题时出错:', error)
    }
  }

  /**
   * 设置标题点击事件处理
   */
  const setupHeadingClickHandlers = () => {
    if (!isComponentMounted.value) return

    const id = requestAnimationFrame(() => {
      if (!isComponentMounted.value) return
      
      try {
        // 查找所有标题元素
        const headings = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')

        if (headings.length === 0) return

        // 为每个标题处理 ID 和类
        headings.forEach((heading, idx) => {
          // 添加 heading-anchor 类
          if (!heading.classList.contains('heading-anchor')) {
            heading.classList.add('heading-anchor')
          }

          // 处理 ID
          if (!heading.id) {
            const text = heading.textContent.trim()
            if (text) {
              // 获取标题索引
              const index = parseInt(heading.getAttribute('data-heading-index') || '0')

              // 生成基本ID
              let baseId = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '')

              // 如果 baseId 为空，使用备用的 ID
              if (!baseId) {
                baseId = `heading-${idx + 1}`
              }

              // 如果有索引，使用索引生成ID
              let id = index > 1 ? `${baseId}-${index}` : baseId

              // 检查是否已存在相同ID的元素
              let counter = index || 1
              while (document.getElementById(id)) {
                counter++
                id = `${baseId}-${counter}`
              }

              // 确保 ID 不为空
              if (!id) {
                id = `heading-${idx + 1}-${Date.now()}`
              }

              heading.id = id
              heading.setAttribute('data-id', id)

              // 确保标题有索引属性
              if (!heading.hasAttribute('data-heading-index')) {
                heading.setAttribute('data-heading-index', counter.toString())
              }
            }
          } else if (!heading.hasAttribute('data-id')) {
            heading.setAttribute('data-id', heading.id)
          }

          // 检查是否已添加点击事件
          if (heading.getAttribute('data-click-handler') !== 'true') {
            const id = heading.getAttribute('data-id') || heading.id
            if (id) {
              // 创建点击处理函数
              const clickHandler = function(event) {
                // 更新 URL 但不触发页面滚动
                history.pushState(null, null, `#${id}`)

                // 计算元素的位置
                const rect = heading.getBoundingClientRect()
                const absoluteElementTop = rect.top + window.pageYOffset

                // 计算偏移量，使标题位于页面中间位置
                const viewportHeight = window.innerHeight
                const offset = viewportHeight * 0.2 // 视口高度的20%

                // 滚动到元素位置减去偏移量
                window.scrollTo({
                  top: absoluteElementTop - offset,
                  behavior: 'smooth'
                })

                // 添加高亮效果
                heading.classList.add('highlight-heading')
                setTimeout(() => {
                  if (document.body.contains(heading)) {
                    heading.classList.remove('highlight-heading')
                  }
                }, 2000)

                // 阻止事件冒泡
                event.stopPropagation()
              }

              // 存储处理函数引用
              heading._clickHandler = clickHandler

              // 添加点击事件
              heading.addEventListener('click', clickHandler)

              // 标记已添加点击事件
              heading.setAttribute('data-click-handler', 'true')
            }
          }
        })
      } catch (error) {
        console.error('设置标题点击处理器时出错:', error)
      }
    })

    // 将 ID 添加到 rafIds 数组中
    if (id) {
      rafIds.push(id)
    }
  }

  /**
   * 清理资源
   */
  const cleanup = () => {
    isComponentMounted.value = false
    
    // 清理所有 requestAnimationFrame
    rafIds.forEach(id => {
      cancelAnimationFrame(id)
    })
    
    try {
      // 清除所有标题元素的点击事件
      const headings = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')
      headings.forEach(heading => {
        // 移除所有事件监听器
        heading.replaceWith(heading.cloneNode(true))
      })
    } catch (error) {
      console.error('清除标题点击处理器时出错:', error)
    }
  }

  // 组件卸载时清理资源
  onUnmounted(cleanup)

  return {
    articleHeadings,
    extractArticleHeadings,
    setupHeadingClickHandlers,
    cleanup,
    isComponentMounted
  }
}
