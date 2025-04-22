<template>
  <div 
    class="ai-summary-container absolute top-0 left-0 w-full h-full flex items-center justify-center pointer-events-none"
    :class="{ 'active': isVisible }"
  >
    <div class="ai-summary-content bg-black/60 text-white p-6 rounded-lg max-w-2xl pointer-events-auto">
      <div class="flex items-center mb-4">
        <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L4 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-.254.145a1 1 0 11-.992-1.736l.23-.132-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.58V12a1 1 0 11-2 0v-1.42l-1.246-.712a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.42l1.246.712a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.42V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z" clip-rule="evenodd" />
          </svg>
        </div>
        <h3 class="text-xl font-bold">AI 文章摘要</h3>
      </div>
      <p class="typewriter-text text-lg leading-relaxed" ref="textElement"></p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'

export default {
  name: 'AiSummary',
  props: {
    summary: {
      type: String,
      required: true
    },
    delay: {
      type: Number,
      default: 2000 // 延迟2秒后开始打字效果
    },
    typingSpeed: {
      type: Number,
      default: 50 // 每个字符的打字速度（毫秒）
    }
  },
  setup(props) {
    const textElement = ref(null)
    const isVisible = ref(false)
    let typingTimer = null

    // 打字机效果实现
    const typeText = () => {
      if (!textElement.value) return
      
      const text = props.summary
      let charIndex = 0
      isVisible.value = true

      // 清除之前的计时器
      if (typingTimer) clearInterval(typingTimer)
      
      // 清空文本内容
      textElement.value.textContent = ''
      
      // 设置打字效果计时器
      typingTimer = setInterval(() => {
        if (charIndex < text.length) {
          textElement.value.textContent += text.charAt(charIndex)
          charIndex++
        } else {
          clearInterval(typingTimer)
        }
      }, props.typingSpeed)
    }

    // 当组件挂载后，延迟启动打字效果
    onMounted(() => {
      setTimeout(() => {
        typeText()
      }, props.delay)
    })

    // 监听summary变化，重新启动打字效果
    watch(() => props.summary, (newSummary) => {
      if (newSummary) {
        setTimeout(() => {
          typeText()
        }, props.delay)
      }
    })

    return {
      textElement,
      isVisible
    }
  }
}
</script>

<style scoped>
.ai-summary-container {
  opacity: 0;
  transform: translateY(-20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.ai-summary-container.active {
  opacity: 1;
  transform: translateY(0);
}

.typewriter-text {
  border-right: 2px solid white;
  white-space: pre-wrap;
  overflow: hidden;
  animation: cursor-blink 0.7s step-end infinite;
}

@keyframes cursor-blink {
  from, to { border-color: transparent }
  50% { border-color: white; }
}
</style>
