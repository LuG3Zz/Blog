<template>
  <div class="card my-6 overflow-hidden">
    <!-- 窗口工具栏 -->
    <div class="tools">
      <div class="circle">
        <span class="red box"></span>
      </div>
      <div class="circle">
        <span class="yellow box"></span>
      </div>
      <div class="circle">
        <span class="green box" @click="copyCode"></span>
      </div>
      <!-- 语言标签 -->
      <span class="language-label">{{ languageLabel }}</span>

      <!-- 复制成功提示 -->
      <span v-if="copied" class="copy-success">已复制</span>
    </div>

    <!-- 代码内容 -->
    <div class="card__content" ref="codeContainer">
      <!-- 行号 -->
      <div v-if="lineNumbers" class="line-numbers-wrapper">
        <div class="line-numbers">
          <div v-for="n in lineCount" :key="n" class="line-number">{{ n }}</div>
        </div>
      </div>

      <!-- 代码 -->
      <div class="code-wrapper mt-3.5 ml-3">
        <pre class="text-sm" :class="[`language-${language}`]"><code :class="[`language-${language}`]" ref="codeElement" v-html="highlightedCode"></code></pre>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick } from 'vue';
import hljs from '@/utils/highlight';

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

    // 我们不再需要这个函数，因为我们在模板中使用了单独的行号显示

    // 高亮后的代码
    const highlightedCode = computed(() => {
      if (!props.code) return '';

      try {
        let result;

        // 先尝试使用指定的语言
        try {
          if (props.language && props.language !== 'none') {
            result = hljs.highlight(props.code, { language: props.language });
            console.log('使用指定语言高亮成功:', props.language);
          } else {
            // 如果没有指定语言或语言为 none，使用自动检测
            result = hljs.highlightAuto(props.code);
            console.log('自动检测语言高亮成功，语言:', result.language);
          }
        } catch (e) {
          // 如果指定语言失败，回退到自动检测
          console.warn('指定语言高亮失败，尝试自动检测:', e);
          result = hljs.highlightAuto(props.code);
          console.log('自动检测语言高亮成功，语言:', result.language);
        }

        // 将高亮后的代码按行分割，并为每行添加包装器
        const lines = result.value.split('\n');
        const wrappedLines = lines.map(line =>
          `<div class="hljs-line">${line || '&nbsp;'}</div>`
        );

        return wrappedLines.join('');
      } catch (error) {
        console.error('应用代码高亮时出错:', error);
        // 如果高亮失败，返回原始代码
        return props.code;
      }
    });

    // 组件挂载后的处理
    onMounted(async () => {
      // 等待下一个DOM更新周期
      await nextTick();
      console.log('代码块组件挂载成功，语言:', props.language);
    });

    // 计算代码行数
    const lineCount = computed(() => {
      if (!props.code) return 0;
      // 如果代码以\n结尾，不计算最后一个空行
      const code = props.code.endsWith('\n') ? props.code.slice(0, -1) : props.code;
      return code.split('\n').length;
    });

    return {
      codeElement,
      codeContainer,
      copied,
      copyCode,
      languageLabel,
      lineCount,
      highlightedCode
    };
  }
};
</script>

<style>
/* macOS 窗口样式 */
.card {
  width: 100%;
  background-color: #f8f9fa;
  border-radius: 8px;
  z-index: 1;
  overflow: hidden;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 暗色模式下的卡片样式 */
.dark .card {
  background-color: #0d1117;
  border-color: #30363d;
  box-shadow: none;
}

.tools {
  display: flex;
  align-items: center;
  padding: 9px 12px;
  background-color: #f1f3f5;
  border-bottom: 1px solid #e9ecef;
}

.dark .tools {
  background-color: #161b22;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.circle {
  padding: 0 4px;
  cursor: pointer;
}

.box {
  display: inline-block;
  align-items: center;
  width: 10px;
  height: 10px;
  padding: 1px;
  border-radius: 50%;
}

.red {
  background-color: #ff605c;
}

.yellow {
  background-color: #ffbd44;
}

.green {
  background-color: #00ca4e;
}

.language-label {
  margin-left: 10px;
  font-size: 0.75rem;
  color: #495057;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

.dark .language-label {
  color: #e1e1e1;
}

.copy-button {
  margin-left: auto;
  display: flex;
  align-items: center;
  background-color: rgba(73, 80, 87, 0.1);
  border: none;
  border-radius: 4px;
  color: #495057;
  padding: 4px 8px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

.dark .copy-button {
  background-color: rgba(255, 255, 255, 0.1);
  color: #e1e1e1;
}

.copy-button:hover {
  background-color: rgba(73, 80, 87, 0.2);
}

.dark .copy-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.copy-button:active {
  transform: scale(0.95);
}

.copy-icon {
  width: 14px;
  height: 14px;
  margin-right: 4px;
  stroke: currentColor;
}

.copy-button span {
  line-height: 1;
}

.copy-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 202, 78, 0.5);
}

/* 复制成功状态 */
.copy-button.copied {
  color: #00ca4e;
  background-color: rgba(0, 202, 78, 0.2);
}

.card__content {
  display: flex;
  background-color: #f8f9fa;
  color: #212529;
  overflow-x: auto;
}

/* 暗色模式下的代码内容 */
.dark .card__content {
  background-color: #0d1117;
  color: #c9d1d9;
}

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

/* highlight.js样式增强 - 白天模式 */
:deep(.hljs-comment),
:deep(.hljs-quote) {
  color: #5c6370;
}

.dark :deep(.hljs-comment),
.dark :deep(.hljs-quote) {
  color: #8292a2;
}

:deep(.hljs-variable),
:deep(.hljs-template-variable),
:deep(.hljs-attribute),
:deep(.hljs-tag),
:deep(.hljs-name),
:deep(.hljs-regexp),
:deep(.hljs-link),
:deep(.hljs-name),
:deep(.hljs-selector-id),
:deep(.hljs-selector-class) {
  color: #e45649;
}

.dark :deep(.hljs-variable),
.dark :deep(.hljs-template-variable),
.dark :deep(.hljs-attribute),
.dark :deep(.hljs-tag),
.dark :deep(.hljs-name),
.dark :deep(.hljs-regexp),
.dark :deep(.hljs-link),
.dark :deep(.hljs-name),
.dark :deep(.hljs-selector-id),
.dark :deep(.hljs-selector-class) {
  color: #f92672;
}

:deep(.hljs-number),
:deep(.hljs-meta),
:deep(.hljs-built_in),
:deep(.hljs-builtin-name),
:deep(.hljs-literal),
:deep(.hljs-type),
:deep(.hljs-params) {
  color: #986801;
}

.dark :deep(.hljs-number),
.dark :deep(.hljs-meta),
.dark :deep(.hljs-built_in),
.dark :deep(.hljs-builtin-name),
.dark :deep(.hljs-literal),
.dark :deep(.hljs-type),
.dark :deep(.hljs-params) {
  color: #ae81ff;
}

:deep(.hljs-string),
:deep(.hljs-symbol),
:deep(.hljs-bullet) {
  color: #50a14f;
}

.dark :deep(.hljs-string),
.dark :deep(.hljs-symbol),
.dark :deep(.hljs-bullet) {
  color: #a6e22e;
}

:deep(.hljs-title),
:deep(.hljs-section) {
  color: #c18401;
}

.dark :deep(.hljs-title),
.dark :deep(.hljs-section) {
  color: #e6db74;
}

:deep(.hljs-keyword),
:deep(.hljs-selector-tag) {
  color: #a626a4;
}

.dark :deep(.hljs-keyword),
.dark :deep(.hljs-selector-tag) {
  color: #66d9ef;
}

:deep(.hljs-emphasis) {
  font-style: italic;
}

:deep(.hljs-strong) {
  font-weight: bold;
}

/* 代码块容器样式 - 白天模式 */
.code-block-container {
  display: flex;
  background-color: #f8f8f8;
  color: #383a42;
  overflow-x: auto;
}

/* 暗色模式下的代码块容器 */
.dark .code-block-container {
  background-color: #282c34;
  color: #abb2bf;
}

/* 行号容器样式 */
.line-numbers-wrapper {
  padding: 0.5rem 0;
  background-color: rgba(0, 0, 0, 0.03);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  user-select: none;
  display: flex;
  align-items: stretch;
}

.dark .line-numbers-wrapper {
  background-color: rgba(255, 255, 255, 0.03);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.line-numbers {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0.5rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #4d5566;
}

.dark .line-numbers {
  color: #4d5566;
}

.line-number {
  display: flex;
  align-items: flex-start; /* 与代码对齐上边缘 */
  justify-content: flex-end; /* 右对齐 */
  height: 1.5rem; /* 确保行高与代码行高一致 */
  min-width: 2rem;
  user-select: none;
  padding: 0;
  margin: 0;
  line-height: 1.5;
  color: #4d5566;
}

/* 代码容器 */
.code-wrapper {
  flex: 1;
  overflow-x: auto;
  display: flex;
  align-items: stretch;
}

.code-wrapper pre {
  margin: 0;
  padding: 0.5rem;
  background-color: transparent;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  width: 100%;
  color: #212529;
}

.dark .code-wrapper pre {
  color: #e1e1e1;
}

/* 确保代码行与行号对齐 */
.code-wrapper code {
  display: block;
  padding: 0;
  margin: 0;
  line-height: 1.5;
}

/* 确保代码内容中的每一行与行号对齐 */
.code-wrapper code .hljs-line {
  display: flex;
  align-items: flex-start; /* 与行号对齐上边缘 */
  min-height: 1.5rem;
  line-height: 1.5;
}

/* 如果没有行元素，为每一行添加垂直内边距 */
.code-wrapper code span {
  line-height: 1.5;
}
</style>
