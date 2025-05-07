<template>
  <div class="memo-input bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden transition-all duration-300"
       :class="{ 'expanded': isExpanded }">
    <!-- 文件选择器 -->
    <div v-if="showFileSelector" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-auto">
        <div class="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-medium">选择图片</h3>
          <button @click="showFileSelector = false" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-4">
          <FileSelector
            file-type="image"
            @close="showFileSelector = false"
            @select="handleFileSelected"
          />
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="p-4">
      <!-- 简洁模式 -->
      <div v-if="!isExpanded" class="flex items-center">
        <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mr-3 flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-500 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
        </div>
        <input
          ref="quickInput"
          type="text"
          v-model="quickText"
          @focus="expandInput"
          class="w-full px-3 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-transparent dark:text-gray-200 text-sm"
          placeholder="记录一下此刻的想法..."
        />
      </div>

      <!-- 展开模式 -->
      <div v-else>
        <!-- 内容输入 -->
        <textarea
          ref="contentInput"
          v-model="formData.content"
          rows="3"
          class="w-full px-3 py-2 mb-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-transparent dark:text-gray-200 text-sm resize-none"
          placeholder="记录一下此刻的想法..."
        ></textarea>

        <!-- 工具栏 -->
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-1">
            <!-- 标签按钮 -->
            <button
              @click="insertTag"
              class="p-1.5 text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title="添加标签"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </button>

            <!-- 图片按钮 -->
            <button
              @click="openFileSelector"
              class="p-1.5 text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title="添加图片"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </button>

            <!-- 私密按钮 -->
            <button
              @click="formData.is_encrypted = !formData.is_encrypted"
              class="p-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              :class="formData.is_encrypted ? 'text-yellow-500 dark:text-yellow-400' : 'text-gray-400 dark:text-gray-500 hover:text-yellow-500 dark:hover:text-yellow-400'"
              title="设为私密"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </button>

            <!-- 标题按钮 -->
            <button
              @click="showTitleInput = !showTitleInput"
              class="p-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              :class="showTitleInput ? 'text-blue-500 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500 hover:text-blue-500 dark:hover:text-blue-400'"
              title="添加标题"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </button>
          </div>

          <div class="flex items-center space-x-2">
            <!-- 取消按钮 -->
            <button
              @click="collapseInput"
              class="px-2 py-1 text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
            >
              取消
            </button>

            <!-- 发布按钮 -->
            <button
              @click="submitMemo"
              :disabled="isSubmitting || !isValid"
              class="px-3 py-1 text-xs text-white bg-blue-500 hover:bg-blue-600 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isSubmitting">发布中...</span>
              <span v-else>发布</span>
            </button>
          </div>
        </div>

        <!-- 标题输入 (可选) -->
        <div v-if="showTitleInput" class="mt-3">
          <input
            ref="titleInput"
            v-model="formData.title"
            type="text"
            class="w-full px-3 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-transparent dark:text-gray-200 text-sm"
            placeholder="标题 (可选)"
          />
        </div>

        <!-- 密码输入 (如果是私密) -->
        <div v-if="formData.is_encrypted" class="mt-3 p-2 bg-gray-50 dark:bg-gray-900 rounded-md border border-gray-200 dark:border-gray-700">
          <div class="flex items-center">
            <div class="flex-grow">
              <input
                v-model="formData.password"
                type="password"
                class="w-full px-2 py-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 dark:focus:ring-blue-600 focus:border-transparent dark:text-gray-200 text-xs"
                placeholder="设置访问密码"
                :required="formData.is_encrypted"
              />
            </div>
            <div class="ml-2 text-xs text-gray-500 dark:text-gray-400">
              私密
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue';
import { filesApi } from '@/api';
import FileSelector from '@/components/admin/FileSelector.vue';

// 组件状态
const isExpanded = ref(false);
const quickText = ref('');
const isSubmitting = ref(false);
const showTitleInput = ref(false);
const showFileSelector = ref(false);

// 表单数据
const formData = ref({
  title: '',
  content: '',
  is_encrypted: false,
  password: ''
});

// 输入框引用
const quickInput = ref(null);
const titleInput = ref(null);
const contentInput = ref(null);

// 表单验证
const isValid = computed(() => {
  if (isExpanded.value) {
    // 展开模式下，内容必填
    if (!formData.value.content.trim()) return false;

    // 如果是加密模式，密码必填
    if (formData.value.is_encrypted && !formData.value.password) return false;

    return true;
  }

  // 简洁模式下，快速输入必填
  return quickText.value.trim() !== '';
});

// 展开输入框
const expandInput = async () => {
  // 如果已经有快速输入的内容，转移到内容框
  if (quickText.value) {
    formData.value.content = quickText.value;
    quickText.value = '';
  }

  isExpanded.value = true;

  // 等待DOM更新后聚焦
  await nextTick();
  if (titleInput.value) {
    titleInput.value.focus();
  }
};

// 收起输入框
const collapseInput = () => {
  isExpanded.value = false;
  resetForm();
};

// 重置表单
const resetForm = () => {
  formData.value = {
    title: '',
    content: '',
    is_encrypted: false,
    password: ''
  };
  quickText.value = '';
  showTitleInput.value = false;
};

// 提交备忘录
const emit = defineEmits(['submit', 'error']);

const submitMemo = async () => {
  if (!isValid.value) return;

  try {
    isSubmitting.value = true;

    // 如果是简洁模式，使用快速输入作为内容
    if (!isExpanded.value) {
      formData.value.content = quickText.value.trim();

      // 确保内容不为空
      if (!formData.value.content) {
        console.error('内容不能为空');
        emit('error', '请输入内容后再发布');
        isSubmitting.value = false;
        return;
      }

      // 提取第一行或第一句话作为标题
      const firstLine = formData.value.content.split(/[\n\r]/)[0];
      const firstSentence = firstLine.split(/[.。!！?？]/)[0];

      // 如果没有有效的第一句话，则标题留空
      if (!firstSentence || firstSentence.trim() === '') {
        formData.value.title = '';
      } else {
        // 检查内容是否包含标签标记 (#)
        if (formData.value.content.includes('#')) {
          const tagMatch = formData.value.content.match(/#([^\s#]+)/);
          if (tagMatch && tagMatch[1]) {
            // 将标签添加到标题中，但不作为整个标题
            // 如果第一句话太长，截取合适长度
            if (firstSentence.length > 15) {
              formData.value.title = firstSentence.substring(0, 15) + '... #' + tagMatch[1];
            } else {
              formData.value.title = firstSentence + ' #' + tagMatch[1];
            }
          } else {
            // 使用第一句话作为标题
            if (firstSentence.length > 20) {
              formData.value.title = firstSentence.substring(0, 20) + '...';
            } else {
              formData.value.title = firstSentence;
            }
          }
        } else {
          // 使用第一句话作为标题
          if (firstSentence.length > 20) {
            formData.value.title = firstSentence.substring(0, 20) + '...';
          } else {
            formData.value.title = firstSentence;
          }
        }
      }
    } else if (!formData.value.title) {
      // 如果展开模式下没有标题
      // 确保内容不为空
      if (!formData.value.content || formData.value.content.trim() === '') {
        console.error('内容不能为空');
        emit('error', '请输入内容后再发布');
        isSubmitting.value = false;
        return;
      }

      // 在展开模式下，如果用户明确留空标题，则保持为空
      formData.value.title = '';
    }

    // 标题可以为空，不设置默认值

    if (!formData.value.content || formData.value.content.trim() === '') {
      console.error('内容不能为空');
      emit('error', '请输入内容后再发布');
      isSubmitting.value = false;
      return;
    }

    // 如果内容只有空格、换行符等，也视为空内容
    if (formData.value.content.trim().length === 0) {
      console.error('内容不能只包含空格或换行符');
      emit('error', '请输入有效内容后再发布');
      isSubmitting.value = false;
      return;
    }

    // 提交表单
    await emit('submit', { ...formData.value });

    // 重置表单
    resetForm();
    collapseInput();
  } catch (error) {
    console.error('提交备忘录失败:', error);
  } finally {
    isSubmitting.value = false;
  }
};

// 打开文件选择器
const openFileSelector = () => {
  showFileSelector.value = true;
};

// 处理文件选择
const handleFileSelected = (file) => {
  if (file && file.url) {
    // 在光标位置插入图片Markdown
    const imageMarkdown = `![${file.original_filename || '图片'}](${file.url})\n`;

    if (isExpanded.value) {
      // 如果是展开模式，插入到内容中
      const textarea = contentInput.value;
      const startPos = textarea.selectionStart;
      const endPos = textarea.selectionEnd;

      formData.value.content =
        formData.value.content.substring(0, startPos) +
        imageMarkdown +
        formData.value.content.substring(endPos);

      // 设置光标位置
      nextTick(() => {
        textarea.focus();
        const newCursorPos = startPos + imageMarkdown.length;
        textarea.setSelectionRange(newCursorPos, newCursorPos);
      });
    } else {
      // 如果是简洁模式，先展开，然后插入
      expandInput().then(() => {
        formData.value.content += imageMarkdown;

        // 设置光标位置
        nextTick(() => {
          const textarea = contentInput.value;
          textarea.focus();
          const pos = formData.value.content.length;
          textarea.setSelectionRange(pos, pos);
        });
      });
    }
  }

  // 关闭文件选择器
  showFileSelector.value = false;
};

// 插入标签
const insertTag = () => {
  const tagText = ' #标签 ';

  if (isExpanded.value) {
    // 如果是展开模式，插入到内容中
    const textarea = contentInput.value;
    const startPos = textarea.selectionStart;
    const endPos = textarea.selectionEnd;

    formData.value.content =
      formData.value.content.substring(0, startPos) +
      tagText +
      formData.value.content.substring(endPos);

    // 设置光标位置并选中"标签"文本以便用户可以直接替换
    nextTick(() => {
      textarea.focus();
      const tagStart = startPos + 2; // 跳过空格和#
      const tagEnd = tagStart + 2; // "标签"的长度
      textarea.setSelectionRange(tagStart, tagEnd);
    });
  } else {
    // 如果是简洁模式，先展开，然后插入
    expandInput().then(() => {
      formData.value.content += tagText;

      // 设置光标位置并选中"标签"文本
      nextTick(() => {
        const textarea = contentInput.value;
        textarea.focus();
        const tagStart = formData.value.content.length - 3; // 跳过空格和#
        const tagEnd = formData.value.content.length - 1; // 跳过结尾空格
        textarea.setSelectionRange(tagStart, tagEnd);
      });
    });
  }
};
</script>

<style scoped>
.expanded {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 添加过渡效果 */
input, textarea {
  transition: all 0.2s ease;
}

/* 暗黑模式下的表单元素聚焦效果 */
:global(.dark) input:focus,
:global(.dark) textarea:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.5);
}
</style>
