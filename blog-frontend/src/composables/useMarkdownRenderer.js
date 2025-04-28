import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import markdownItKatex from 'markdown-it-katex'

// 添加脚注支持
const footnote = (md) => {
  // 匹配脚注引用 [^1]
  const footnoteRefRegex = /\[\^([^\]]+)\]/g;
  // 匹配脚注定义 [^1]: 脚注内容
  const footnoteDefRegex = /^\[\^([^\]]+)\]:\s+(.*(?:\n+(?:\s{4}|\t).+)*)/gm;

  // 存储脚注
  const footnotes = {};

  // 修改渲染器的 render 方法
  const originalRender = md.render;

  md.render = function(src) {
    // 清空脚注
    Object.keys(footnotes).forEach(key => delete footnotes[key]);

    // 提取脚注定义
    let match;
    while ((match = footnoteDefRegex.exec(src)) !== null) {
      const id = match[1];
      const content = match[2].replace(/^\s{4}/gm, ''); // 移除缩进
      footnotes[id] = content;
    }

    // 替换脚注引用
    let html = originalRender.call(this, src);

    // 如果有脚注，添加脚注区域
    if (Object.keys(footnotes).length > 0) {
      let footnotesHtml = '<div class="footnotes"><hr><ol>';

      Object.keys(footnotes).forEach((id, index) => {
        footnotesHtml += `<li id="fn-${id}"><p>${footnotes[id]} <a href="#fnref-${id}" class="footnote-backref">↩</a></p></li>`;
      });

      footnotesHtml += '</ol></div>';
      html += footnotesHtml;
    }

    return html;
  };

  // 修改内联规则，处理脚注引用
  md.inline.ruler.after('emphasis', 'footnote_ref', function(state, silent) {
    const start = state.pos;
    const max = state.posMax;

    if (start + 3 > max) return false;
    if (state.src.charCodeAt(start) !== 0x5B/* [ */) return false;
    if (state.src.charCodeAt(start + 1) !== 0x5E/* ^ */) return false;

    let pos = start + 2;
    let id = '';

    // 收集脚注ID
    while (pos < max && state.src.charCodeAt(pos) !== 0x5D/* ] */) {
      id += state.src.charAt(pos);
      pos++;
    }

    // 没有找到结束的 ]
    if (pos === max || id.length === 0) return false;

    // 不渲染，只前进
    if (silent) {
      state.pos = pos + 1;
      return true;
    }

    // 渲染脚注引用
    state.pos = pos + 1;

    const token = state.push('footnote_ref', '', 0);
    token.content = id;
    token.meta = { id };

    return true;
  });

  // 添加脚注引用的渲染规则
  md.renderer.rules.footnote_ref = function(tokens, idx) {
    const id = tokens[idx].meta.id;
    return `<sup id="fnref-${id}"><a href="#fn-${id}" class="footnote-ref">[${id}]</a></sup>`;
  };
}
// 添加任务列表支持
const taskLists = (md) => {
  // 匹配任务列表项 [ ], [x], [X]
  const taskListRegex = /^\[([ xX])\]\s+/;

  // 修改列表项渲染
  const originalListItemRender = md.renderer.rules.list_item_open || function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
  };

  md.renderer.rules.list_item_open = function(tokens, idx, options, env, self) {
    const token = tokens[idx];
    const nextToken = tokens[idx + 1];

    // 检查是否是任务列表项
    if (nextToken && nextToken.type === 'inline' && nextToken.content.match(taskListRegex)) {
      // 添加任务列表类
      token.attrSet('class', (token.attrGet('class') || '') + ' task-list-item');

      // 修改内容，将 [ ] 或 [x] 替换为复选框
      const match = nextToken.content.match(taskListRegex);
      const checked = match[1] !== ' ';

      // 替换内容
      nextToken.content = nextToken.content.replace(
        taskListRegex,
        `<input type="checkbox" class="task-list-item-checkbox" ${checked ? 'checked' : ''} disabled> `
      );

      // 将父列表标记为任务列表
      let parentToken = null;
      for (let i = idx - 1; i >= 0; i--) {
        if (tokens[i].type === 'bullet_list_open' || tokens[i].type === 'ordered_list_open') {
          parentToken = tokens[i];
          break;
        }
      }

      if (parentToken) {
        parentToken.attrSet('class', (parentToken.attrGet('class') || '') + ' task-list');
      }
    }

    return originalListItemRender(tokens, idx, options, env, self);
  };
}

/**
 * 创建并配置Markdown渲染器
 * @returns {Object} 包含渲染函数和Markdown实例的对象
 */
export function useMarkdownRenderer() {
  // 创建markdown-it实例
  const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true,
    highlight: function (str, lang) {
      // 返回空字符串，因为我们将使用自定义的代码块组件
      return '';
    }
  })

  // 使用 KaTeX 插件渲染数学公式
  md.use(markdownItKatex, {
    throwOnError: false,
    errorColor: '#cc0000',
    output: 'html',  // 使用 HTML 输出模式
    macros: {  // 自定义宏
      '\\RR': '\\mathbb{R}',
      '\\NN': '\\mathbb{N}',
      '\\ZZ': '\\mathbb{Z}'
    },
    strict: false  // 非严格模式，允许更多语法
  })

  // 添加自动生成标题ID的功能
  md.use(function(md) {
    // 创建一个映射来跟踪标题文本和计数器
    const headingCounters = {};

    const originalHeadingOpen = md.renderer.rules.heading_open || function(tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };

    md.renderer.rules.heading_open = function(tokens, idx, options, env, self) {
      const token = tokens[idx];
      const nextToken = tokens[idx + 1];
      if (nextToken && nextToken.type === 'inline' && nextToken.content) {
        // 生成基本ID：将标题文本转换为小写，替换空格为连字符，移除非单词字符
        const text = nextToken.content;
        let baseId = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w\-]/g, '');

        // 如果 baseId 为空，使用备用的 ID
        if (!baseId) {
          const headingLevel = token.tag.substring(1); // 例如，从 'h1' 中提取 '1'
          baseId = `heading-${headingLevel}-${idx}`;
        }

        // 检查是否已经有相同文本的标题，如果有，增加计数器
        if (!headingCounters[text]) {
          headingCounters[text] = 0;
        }
        headingCounters[text]++;

        // 如果是第一个出现的标题，使用基本ID，否则添加计数器
        let uniqueId;
        if (headingCounters[text] === 1) {
          uniqueId = baseId;
        } else {
          uniqueId = `${baseId}-${headingCounters[text]}`;
        }

        // 确保 ID 不为空
        if (!uniqueId) {
          uniqueId = `heading-${idx}-${Date.now()}`;
        }

        // 设置标题ID和数据属性
        token.attrSet('id', uniqueId);
        token.attrSet('data-heading-text', text);
        token.attrSet('data-heading-index', headingCounters[text].toString());
      }
      return originalHeadingOpen(tokens, idx, options, env, self);
    };
  })

  // 添加标题点击跳转功能
  md.use(function(md) {
    const originalHeadingRender = md.renderer.rules.heading_close || function(tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };

    md.renderer.rules.heading_close = function(tokens, idx, options, env, self) {
      // 不使用内联脚本，而是添加一个特殊的类
      const token = tokens[idx - 2]; // heading_open token
      if (token && token.tag && token.tag.match(/^h[1-6]$/)) {
        const id = token.attrs && token.attrs.find(attr => attr[0] === 'id');
        if (id && id[1]) {
          // 在标题开始标签上添加类，用于样式和脚本选择
          token.attrSet('class', (token.attrGet('class') || '') + ' heading-anchor');
          token.attrSet('data-id', id[1]);
        }
      }
      return originalHeadingRender(tokens, idx, options, env, self);
    };
  })

  // 增强列表渲染
  md.use(function(md) {
    // 增强无序列表开始标签
    const originalBulletListOpen = md.renderer.rules.bullet_list_open || function(tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };

    md.renderer.rules.bullet_list_open = function(tokens, idx, options, env, self) {
      const token = tokens[idx];
      token.attrSet('class', (token.attrGet('class') || '') + ' md-list md-bullet-list');
      return originalBulletListOpen(tokens, idx, options, env, self);
    };

    // 增强有序列表开始标签
    const originalOrderedListOpen = md.renderer.rules.ordered_list_open || function(tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };

    md.renderer.rules.ordered_list_open = function(tokens, idx, options, env, self) {
      const token = tokens[idx];
      token.attrSet('class', (token.attrGet('class') || '') + ' md-list md-ordered-list');
      return originalOrderedListOpen(tokens, idx, options, env, self);
    };

    // 增强列表项开始标签
    const originalListItemOpen = md.renderer.rules.list_item_open || function(tokens, idx, options, env, self) {
      return self.renderToken(tokens, idx, options);
    };

    md.renderer.rules.list_item_open = function(tokens, idx, options, env, self) {
      const token = tokens[idx];
      token.attrSet('class', (token.attrGet('class') || '') + ' md-list-item');
      return originalListItemOpen(tokens, idx, options, env, self);
    };
  })

  // 添加任务列表支持
  md.use(taskLists)

  // 添加脚注支持
  md.use(footnote)

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
   * 计算阅读时间
   * @param {String} content 文章内容
   * @returns {Number} 阅读时间（分钟）
   */
  const calculateReadingTime = (content) => {
    if (!content) return 0
    const wordsPerMinute = 200 // 假设平均阅读速度为每分钟200字
    const wordCount = content.length
    return Math.ceil(wordCount / wordsPerMinute)
  }

  return {
    md,
    renderMarkdown,
    calculateReadingTime
  }
}
