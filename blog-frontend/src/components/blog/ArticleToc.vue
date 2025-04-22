<template>
  <div class="article-toc bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 sticky top-4">
    <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">目录</h3>
    <div v-if="headings && headings.length > 0" class="space-y-2">
      <a
        v-for="(heading, index) in headings"
        :key="index"
        :href="`#${heading.id}`"
        :class="[
          'block py-1 border-l-2 pl-3 transition-colors duration-200 hover:text-secondary dark:hover:text-dark-secondary',
          heading.level === 2 ? 'font-medium border-gray-300 dark:border-gray-600' : 'text-sm ml-4 border-gray-200 dark:border-gray-700',
          activeHeading === heading.id ? 'border-secondary dark:border-dark-secondary text-secondary dark:text-dark-secondary font-medium' : 'text-gray-600 dark:text-gray-400'
        ]"
        :data-index="index"
        :data-heading-index="heading.index"
        :data-heading-id="heading.id"
        @click.prevent="scrollToHeading(heading.id, heading.index)"
      >
        <span class="flex items-center mt-2">
          <span class="toc-bullet mr-2 w-1.5 h-1.5 rounded-full" :class="activeHeading === heading.id ? 'bg-secondary dark:bg-dark-secondary' : 'bg-gray-400 dark:bg-gray-500'"></span>
          {{ heading.text }}
        </span>
      </a>
    </div>
    <div v-else class="text-gray-500 dark:text-gray-400 text-sm italic">
      无目录内容
    </div>
  </div>  <!-- 标签云 -->
  <tag-cloud class="mt-6" />
  
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { format } from 'date-fns'
// 直接导入组件，避免循环引用
import TagCloud from '../blog/TagCloud.vue'

// 定义属性
const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

// 使用 shallowRef 而不是 ref，减少响应式处理的开销
const headings = shallowRef([])
const activeHeading = shallowRef('')

// 添加组件挂载状态跟踪
const isComponentMounted = ref(false)

// 解析内容中的标题
const parseHeadings = () => {
  // 如果组件已经卸载，不执行操作
  if (!isComponentMounted.value) {
    console.log('解析标题时，组件已卸载，取消操作')
    return
  }

  try {
    // 如果内容为空，直接返回
    if (!props.content || props.content.trim() === '') {
      headings.value = []
      return
    }

    console.log('开始解析标题，内容长度:', props.content.length)

    // 先尝试从 DOM 中直接获取标题元素
    const articleContent = document.querySelector('.prose')
    if (articleContent) {
      console.log('找到文章内容元素')
      const domHeadings = articleContent.querySelectorAll('h1, h2, h3, h4, h5, h6')

      if (domHeadings.length > 0) {
        console.log(`从 DOM 中找到 ${domHeadings.length} 个标题元素`)
        const parsedHeadings = []

        domHeadings.forEach((heading, index) => {
          try {
            const text = heading.textContent.trim()
            const level = parseInt(heading.tagName.substring(1))
            const id = heading.id || ''

            console.log(`标题 ${index + 1}: 文本="${text}", 级别=${level}, ID="${id}"`)

            if (text && id) {
              parsedHeadings.push({
                id,
                text,
                level,
                index: index + 1
              })
            } else if (text) {
              // 如果标题没有 ID，生成一个
              let baseId = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '')

              // 如果 baseId 为空，使用备用的 ID
              if (!baseId) {
                baseId = `heading-${index + 1}`
                console.log(`标题文本生成的 ID 为空，使用备用 ID: ${baseId}`)
              }

              parsedHeadings.push({
                id: baseId,
                text,
                level,
                index: index + 1
              })
              console.log(`标题没有 ID，生成了 ID="${baseId}"`)

              // 尝试设置标题的 ID
              try {
                heading.id = baseId
                console.log(`设置了标题元素的 ID: ${baseId}`)
              } catch (e) {
                console.error('设置标题 ID 时出错:', e)
              }
            }
          } catch (error) {
            console.error(`解析标题 ${index + 1} 时出错:`, error)
          }
        })

        // 更新标题数组
        headings.value = parsedHeadings
        console.log('从 DOM 解析的标题:', parsedHeadings)
        return
      } else {
        console.log('从 DOM 中没有找到标题元素，尝试使用正则表达式解析')
      }
    } else {
      console.log('没有找到文章内容元素，尝试使用正则表达式解析')
    }

    // 使用正则表达式匹配标题
    const regex = /<h([1-6])[^>]*?(id=["']([^"']+)["'])?[^>]*>(.*?)<\/h\1>/gi
    const matches = [...props.content.matchAll(regex)]

    console.log(`正则表达式匹配到 ${matches.length} 个标题`)

    if (matches.length === 0) {
      headings.value = []
      return
    }

    // 创建一个映射来跟踪标题文本和计数器
    const headingTextCounters = {}
    const parsedHeadings = []

    matches.forEach((match, idx) => {
      try {
        const level = parseInt(match[1])
        const extractedId = match[3] // 从正则表达式中提取 ID
        const text = match[4].replace(/<[^>]*>/g, '').trim()

        console.log(`标题 ${idx + 1}: 文本="${text}", 级别=${level}, 提取的ID="${extractedId || '无'}"`)

        if (!text) return

        // 更新标题计数器
        if (!headingTextCounters[text]) {
          headingTextCounters[text] = 1
        } else {
          headingTextCounters[text]++
        }

        // 生成基本ID
        let baseId = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '')

        // 如果 baseId 为空，使用备用的 ID
        if (!baseId) {
          baseId = `heading-${idx + 1}`
          console.log(`标题文本生成的 ID 为空，使用备用 ID: ${baseId}`)
        }

        // 生成唯一ID
        let id = extractedId || baseId
        if (!extractedId && headingTextCounters[text] > 1) {
          id = `${baseId}-${headingTextCounters[text]}`
        }

        // 确保 ID 不为空
        if (!id) {
          id = `heading-${idx + 1}-${Date.now()}`
          console.log(`生成的 ID 仍然为空，使用备用 ID: ${id}`)
        }

        console.log(`最终生成的ID="${id}"`)

        // 尝试设置文章中对应标题的 ID
        try {
          // 获取所有标题元素
          const headingElements = document.querySelectorAll(`.prose h${level}`)
          let headingElement = null

          // 遍历标题元素，查找包含指定文本的元素
          for (const element of headingElements) {
            if (element.textContent.trim() === text) {
              headingElement = element
              break
            }
          }

          if (headingElement && !headingElement.id) {
            headingElement.id = id
            console.log(`设置了文章中标题元素的 ID: ${id}`)
          }
        } catch (e) {
          console.error('设置文章中标题 ID 时出错:', e)
        }


        // 添加到标题数组
        parsedHeadings.push({
          id,
          text,
          level,
          index: headingTextCounters[text]
        })
      } catch (error) {
        console.error('解析标题时出错:', error)
      }
    })

    // 更新标题数组
    headings.value = parsedHeadings
  } catch (error) {
    console.error('解析标题时出错:', error)
    headings.value = []
  }
}

// 滚动到指定标题
const scrollToHeading = (id, headingIndex) => {
  console.log(`尝试滚动到标题，ID="${id}"`)

  // 如果 ID 为空，使用第一个标题
  if (!id) {
    console.log('标题 ID 为空，尝试使用第一个标题')
    const firstHeading = document.querySelector('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')
    if (firstHeading) {
      if (firstHeading.id) {
        id = firstHeading.id
        console.log(`使用第一个标题的 ID: ${id}`)
      } else {
        // 如果第一个标题没有 ID，给它设置一个
        id = `heading-first-${Date.now()}`
        firstHeading.id = id
        console.log(`给第一个标题设置 ID: ${id}`)
      }
    } else {
      console.log('没有找到任何标题元素')
      return
    }
  }

  // 如果组件已经卸载，不执行操作
  if (!isComponentMounted.value) {
    console.log('滚动到标题时，组件已卸载，取消操作')
    return
  }

  // 先尝试直接通过ID查找元素
  let element = document.getElementById(id)
  if (element) {
    console.log(`通过 getElementById 找到标题元素，标签名=${element.tagName}`)
  }

  // 如果没找到，尝试通过选择器查找
  if (!element) {
    const selector = `.prose h1[id="${id}"], .prose h2[id="${id}"], .prose h3[id="${id}"], .prose h4[id="${id}"], .prose h5[id="${id}"], .prose h6[id="${id}"]`
    console.log(`尝试使用选择器查找：${selector}`)
    element = document.querySelector(selector)

    if (element) {
      console.log(`通过选择器找到标题元素，标签名=${element.tagName}`)
    }
  }

  // 如果还是没找到，尝试更宽松的选择器
  if (!element) {
    const allHeadings = document.querySelectorAll('.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6')
    console.log(`文章中共有 ${allHeadings.length} 个标题元素`)

    // 输出所有标题的 ID
    allHeadings.forEach((heading, idx) => {
      console.log(`标题 ${idx + 1}: ID="${heading.id}", 文本="${heading.textContent.trim()}"`)
    })

    // 尝试模糊匹配
    for (const heading of allHeadings) {
      if (heading.id && (heading.id.includes(id) || id.includes(heading.id))) {
        element = heading
        console.log(`通过模糊匹配找到标题元素，标签名=${element.tagName}, ID="${element.id}"`)
        break
      }
    }

    // 如果还是没找到，使用第一个标题
    if (!element && allHeadings.length > 0) {
      element = allHeadings[0]
      console.log(`没有找到匹配的标题，使用第一个标题，标签名=${element.tagName}, ID="${element.id}"`)
    }
  }

  // 如果找到了元素，滚动到它
  if (element) {
    // 计算元素的位置
    const rect = element.getBoundingClientRect()
    const absoluteElementTop = rect.top + window.pageYOffset

    // 计算偏移量，使标题位于页面中间位置
    // 获取视口高度
    const viewportHeight = window.innerHeight
    // 计算偏移量，使标题位于视口中间偏上的位置
    const offset = viewportHeight * 0.2 // 视口高度的20%

    // 滚动到元素位置减去偏移量
    window.scrollTo({
      top: absoluteElementTop - offset,
      behavior: 'smooth'
    })

    // 更新当前活动标题
    activeHeading.value = id

    // 添加高亮效果
    element.classList.add('highlight-heading')

    // 2秒后移除高亮效果
    setTimeout(() => {
      if (isComponentMounted.value) {
        element.classList.remove('highlight-heading')
      }
    }, 2000)
  } else {
    console.error(`无法找到标题元素: ${id}`)
  }
}

// 监听滚动事件，更新当前活动标题
const handleScroll = () => {
  // 如果组件已经卸载，不执行操作
  if (!isComponentMounted.value) {
    return
  }

  // 使用局部变量保存当前的挂载状态
  const isMounted = isComponentMounted.value

  // 使用 requestAnimationFrame 确保在下一帧渲染时执行
  if (handleScroll.rafId) {
    cancelAnimationFrame(handleScroll.rafId)
  }

  handleScroll.rafId = requestAnimationFrame(() => {
    // 再次检查组件是否已卸载
    if (!isMounted) {
      return
    }

    try {
      if (headings.value.length === 0) return

      // 获取所有标题元素
      const headingElements = []
      for (const heading of headings.value) {
        const element = document.getElementById(heading.id)
        if (element) {
          headingElements.push({
            id: heading.id,
            element
          })
        }
      }

      if (headingElements.length === 0) return

      // 获取当前滚动位置
      const scrollPosition = window.scrollY + 120 // 添加偏移量，考虑导航栏高度

      // 默认选择第一个标题
      let activeId = headingElements[0].id

      // 按照元素在页面中的位置排序
      const sortedHeadings = [...headingElements].sort((a, b) => {
        const aTop = a.element.getBoundingClientRect().top + window.scrollY
        const bTop = b.element.getBoundingClientRect().top + window.scrollY
        return aTop - bTop
      })

      // 遍历所有标题，找到当前滚动位置对应的标题
      for (let i = 0; i < sortedHeadings.length; i++) {
        const currentHeading = sortedHeadings[i]
        const nextHeading = sortedHeadings[i + 1]

        // 获取元素当前位置
        const headingTop = currentHeading.element.getBoundingClientRect().top + window.scrollY - 10
        const headingBottom = nextHeading ?
          nextHeading.element.getBoundingClientRect().top + window.scrollY :
          document.body.scrollHeight

        if (scrollPosition >= headingTop && scrollPosition < headingBottom) {
          activeId = currentHeading.id
          break
        }
      }

      // 更新活动标题，只在变化时更新
      if (activeId !== activeHeading.value) {
        activeHeading.value = activeId
      }
    } catch (error) {
      console.error('处理滚动事件时出错:', error)
    }
  })
}

// 监听内容变化
watch(() => props.content, () => {
  // 如果组件已经卸载，不执行操作
  if (!isComponentMounted.value) {
    return
  }

  if (props.content) {
    parseHeadings()
  }
})

// 组件挂载时
onMounted(() => {
  console.log('目录组件挂载')
  isComponentMounted.value = true

  // 等待一小段时间，确保文章内容已经渲染
  setTimeout(() => {
    if (isComponentMounted.value) {
      console.log('延迟解析标题')
      if (props.content) {
        parseHeadings()
      }

      // 尝试处理 URL 中的锚点
      const hash = window.location.hash
      if (hash && hash.length > 1) {
        const id = hash.substring(1)
        console.log(`检测到 URL 中的锚点: ${id}`)
        setTimeout(() => {
          if (isComponentMounted.value) {
            scrollToHeading(id, 0)
          }
        }, 500)
      }
    }
  }, 500)

  // 添加滚动事件监听
  window.addEventListener('scroll', handleScroll)
})

// 组件卸载时
onUnmounted(() => {
  isComponentMounted.value = false

  // 移除滚动事件监听
  window.removeEventListener('scroll', handleScroll)

  // 清除 requestAnimationFrame
  if (handleScroll.rafId) {
    cancelAnimationFrame(handleScroll.rafId)
  }

  // 清除引用
  headings.value = []
  activeHeading.value = ''
})
</script>

<style scoped>
:root {
  --color-secondary-rgb: 59, 130, 246; /* 蓝色的RGB值 */
  --color-secondary: #3b82f6;
}

.article-toc {
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  scrollbar-width: thin;
  min-height: 400px;
}

.article-toc::-webkit-scrollbar {
  width: 4px;
}

.article-toc::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.article-toc::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.article-toc::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.toc-bullet {
  transition: background-color 0.2s;
}

/* 添加目录项悬停效果 */
.article-toc a:hover {
  background-color: rgba(var(--color-secondary-rgb), 0.05);
  border-radius: 0.25rem;
}

/* 标题高亮效果 */
@keyframes highlight-pulse {
  0% {
    background-color: rgba(var(--color-secondary-rgb), 0.1);
  }
  50% {
    background-color: rgba(var(--color-secondary-rgb), 0.2);
  }
  100% {
    background-color: rgba(var(--color-secondary-rgb), 0.1);
  }
}

.highlight-heading {
  animation: highlight-pulse 1s ease-in-out 2;
  border-left: 3px solid var(--color-secondary);
  padding-left: 10px;
  transition: all 0.3s ease;
}

/* 暗黑模式下的高亮效果 */
.dark .highlight-heading {
  border-left-color: var(--color-dark-secondary);
}
</style>
