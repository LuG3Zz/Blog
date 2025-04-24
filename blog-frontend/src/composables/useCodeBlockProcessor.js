import { h, createApp } from 'vue'

/**
 * 处理文章中的代码块
 * @param {Object} options 配置选项
 * @returns {Object} 包含代码块处理方法的对象
 */
export function useCodeBlockProcessor(options = {}) {
  const { CodeBlock, isComponentMounted } = options

  /**
   * 处理渲染后的内容中的代码块
   */
  const processCodeBlocks = () => {
    if (!isComponentMounted.value) return

    setTimeout(() => {
      try {
        // 查找所有代码块
        const codeBlocks = document.querySelectorAll('.prose pre code')
        if (codeBlocks.length === 0) return

        // 遍历每个代码块
        codeBlocks.forEach((codeBlock, index) => {
          // 获取代码块父元素
          const preElement = codeBlock.parentElement
          if (!preElement) return

          // 获取语言
          const classNames = codeBlock.className.split(' ')
          let language = 'none'
          for (const className of classNames) {
            if (className.startsWith('language-')) {
              language = className.replace('language-', '')
              break
            }
          }

          // 获取代码内容
          const code = codeBlock.textContent

          // 创建容器元素
          const containerElement = document.createElement('div')
          containerElement.className = 'code-block-wrapper'
          containerElement.id = `code-block-${index}`

          // 将容器插入到 pre 元素的父元素中
          preElement.parentElement.insertBefore(containerElement, preElement)

          // 创建并挂载 CodeBlock 组件
          try {
            const codeBlockInstance = h(CodeBlock, {
              language,
              code,
              lineNumbers: true
            })

            const app = createApp({
              render() {
                return codeBlockInstance
              }
            })

            app.mount(containerElement)

            // 移除原始的 pre 元素
            preElement.parentElement.removeChild(preElement)
          } catch (mountError) {
            console.error(`挂载代码块 ${index + 1} 时出错:`, mountError)
          }
        })
      } catch (error) {
        console.error('处理代码块时出错:', error)
      }
    }, 200) // 延迟执行，确保内容渲染完成
  }

  return {
    processCodeBlocks
  }
}
