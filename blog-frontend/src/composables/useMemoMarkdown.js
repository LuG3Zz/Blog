import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import markdownItTaskLists from 'markdown-it-task-lists'

/**
 * 创建并配置备忘录Markdown渲染器
 * @returns {Object} 包含渲染函数的对象
 */
export function useMemoMarkdown() {
  // 创建markdown-it实例
  const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true,
    breaks: true, // 自动将换行符转换为 <br>
  })

  // 使用任务列表插件
  md.use(markdownItTaskLists)

  // 增强图片渲染
  const defaultImageRenderer = md.renderer.rules.image || function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };

  md.renderer.rules.image = function(tokens, idx, options, env, self) {
    const token = tokens[idx];
    // 添加响应式类
    token.attrSet('class', 'max-w-full rounded-md my-2');
    return defaultImageRenderer(tokens, idx, options, env, self);
  };

  /**
   * 渲染Markdown内容
   * @param {String} content Markdown内容
   * @returns {String} 渲染后的HTML
   */
  const renderMarkdown = (content) => {
    if (!content) return ''

    // 渲染Markdown内容
    let html = md.render(content)

    return html
  }

  /**
   * 计算属性：格式化后的内容
   * @param {String} content 原始内容
   * @returns {String} 渲染后的HTML
   */
  const createFormattedContent = (content) => {
    return computed(() => {
      if (!content.value) return '';
      
      // 确保内容是字符串
      const contentStr = typeof content.value === 'string' 
        ? content.value 
        : String(content.value);
      
      return renderMarkdown(contentStr);
    });
  }

  return {
    md,
    renderMarkdown,
    createFormattedContent
  }
}
