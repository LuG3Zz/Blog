<template>
  <div class="relative my-6 overflow-hidden rounded-lg shadow-md bg-gray-50 dark:bg-gray-800">
    <!-- 代码语言标签和复制按钮 -->
    <div class="flex items-center justify-between px-4 py-2 text-xs font-mono text-gray-500 bg-gray-100 dark:bg-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600">
      <!-- 语言标签 -->
      <span class="font-medium">{{ languageLabel }}</span>
      
      <!-- 复制按钮 -->
      <button 
        @click="copyCode" 
        class="flex items-center px-2 py-1 transition-colors rounded hover:bg-gray-200 dark:hover:bg-gray-600"
        :class="{ 'text-green-500': copied }"
      >
        <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <span>{{ copied ? '已复制' : '复制' }}</span>
      </button>
    </div>
    
    <!-- 代码内容 -->
    <div class="overflow-x-auto" ref="codeContainer">
      <pre class="p-4 text-sm leading-relaxed" :class="[`language-${language}`]"><code :class="[`language-${language}`]" ref="codeElement"><slot></slot></code></pre>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick } from 'vue';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
// 导入常用语言
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-css';
import 'prismjs/components/prism-scss';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-cpp';
import 'prismjs/components/prism-csharp';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-markdown';
import 'prismjs/components/prism-yaml';
import 'prismjs/components/prism-sql';
import 'prismjs/components/prism-go';
import 'prismjs/components/prism-rust';
import 'prismjs/components/prism-php';
import 'prismjs/components/prism-ruby';

export default {
  name: 'CodeBlock',
  props: {
    language: {
      type: String,
      default: 'javascript'
    },
    code: {
      type: String,
      default: ''
    },
    lineNumbers: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const codeElement = ref(null);
    const codeContainer = ref(null);
    const copied = ref(false);
    
    // 语言显示标签
    const languageLabel = computed(() => {
      const langMap = {
        'js': 'JavaScript',
        'javascript': 'JavaScript',
        'ts': 'TypeScript',
        'typescript': 'TypeScript',
        'html': 'HTML',
        'css': 'CSS',
        'scss': 'SCSS',
        'sass': 'Sass',
        'python': 'Python',
        'py': 'Python',
        'java': 'Java',
        'c': 'C',
        'cpp': 'C++',
        'csharp': 'C#',
        'cs': 'C#',
        'go': 'Go',
        'rust': 'Rust',
        'php': 'PHP',
        'ruby': 'Ruby',
        'bash': 'Bash',
        'sh': 'Shell',
        'json': 'JSON',
        'md': 'Markdown',
        'markdown': 'Markdown',
        'yaml': 'YAML',
        'yml': 'YAML',
        'sql': 'SQL',
        'xml': 'XML',
        'none': '纯文本'
      };
      
      return langMap[props.language.toLowerCase()] || props.language;
    });
    
    // 复制代码功能
    const copyCode = async () => {
      try {
        // 获取代码内容
        const code = props.code || (codeElement.value ? codeElement.value.textContent : '');
        
        // 复制到剪贴板
        await navigator.clipboard.writeText(code);
        
        // 显示复制成功状态
        copied.value = true;
        
        // 2秒后重置状态
        setTimeout(() => {
          copied.value = false;
        }, 2000);
      } catch (err) {
        console.error('复制失败:', err);
      }
    };
    
    // 添加行号
    const addLineNumbers = () => {
      if (!props.lineNumbers || !codeElement.value) return;
      
      const codeLines = codeElement.value.innerHTML.split('\n');
      let numberedCode = '';
      
      codeLines.forEach((line, index) => {
        const lineNumber = index + 1;
        numberedCode += `<div class="code-line relative">
          <span class="line-number select-none text-gray-400 dark:text-gray-500 text-xs mr-4 inline-block w-8 text-right">${lineNumber}</span>
          <span class="line-content">${line}</span>
        </div>`;
      });
      
      codeElement.value.innerHTML = numberedCode;
    };
    
    // 组件挂载后高亮代码
    onMounted(async () => {
      // 等待下一个DOM更新周期
      await nextTick();
      
      if (codeElement.value) {
        // 如果有传入的代码，使用它
        if (props.code) {
          codeElement.value.textContent = props.code;
        }
        
        // 应用Prism高亮
        Prism.highlightElement(codeElement.value);
        
        // 添加行号
        if (props.lineNumbers) {
          addLineNumbers();
        }
      }
    });
    
    return {
      codeElement,
      codeContainer,
      copied,
      copyCode,
      languageLabel
    };
  }
};
</script>

<style scoped>
/* 行号样式 */
:deep(.code-line) {
  display: block;
  position: relative;
  min-height: 1.5em;
  line-height: 1.5;
}

:deep(.line-number) {
  opacity: 0.5;
  user-select: none;
}

:deep(.line-content) {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

/* 代码行悬停效果 */
:deep(.code-line:hover) {
  background-color: rgba(0, 0, 0, 0.05);
}

.dark :deep(.code-line:hover) {
  background-color: rgba(255, 255, 255, 0.05);
}
</style>
