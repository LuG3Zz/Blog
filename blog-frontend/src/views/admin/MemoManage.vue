<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-200">备忘录管理</h1>
      <GradientButton @click="showCreateForm = true">
        <div class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          创建备忘录
        </div>
      </GradientButton>
    </div>

    <!-- 备忘录列表 -->
    <MemoListComponent
      ref="memoListRef"
      @create="showCreateForm = true"
      @edit="handleEdit"
      @delete="handleDelete"
      @view="handleView"
    />

    <!-- 创建/编辑备忘录表单对话框 -->
    <div v-if="showCreateForm || showEditForm" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="w-full max-w-2xl">
        <MemoForm
          :initial-data="currentMemo"
          :is-edit="showEditForm"
          @submit="handleSubmit"
          @cancel="closeForm"
        />
      </div>
    </div>

    <!-- 备忘录详情对话框 -->
    <div v-if="showViewDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-2xl mx-4 transform transition-all">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
            {{ currentMemo.title }}
          </h3>
          <button
            @click="showViewDialog = false"
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="mb-4 text-sm text-gray-500 dark:text-gray-400">
          创建于: {{ formatDate(currentMemo.created_at) }}
          <span v-if="currentMemo.updated_at !== currentMemo.created_at">
            | 更新于: {{ formatDate(currentMemo.updated_at) }}
          </span>
        </div>

        <div class="border-t border-gray-200 dark:border-gray-700 pt-4 mb-4">
          <div v-if="currentMemo.is_encrypted && !decryptedContent" class="flex flex-col items-center justify-center py-8">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 dark:text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <p class="text-gray-500 dark:text-gray-400 text-center mb-4">此备忘录已加密</p>
            <button
              @click="openPasswordDialog"
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors"
            >
              输入密码查看
            </button>
          </div>
          <div v-else class="prose dark:prose-invert max-w-none">
            {{ decryptedContent || currentMemo.content }}
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="handleEdit(currentMemo)"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            编辑
          </button>
          <button
            @click="showViewDialog = false"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            关闭
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            确认删除
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            您确定要删除备忘录 "{{ currentMemo.title }}" 吗？此操作无法撤销。
          </p>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteDialog = false"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button
            @click="confirmDelete"
            :disabled="isDeleting"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isDeleting">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 密码对话框 -->
    <PasswordDialog
      v-if="showPasswordDialog"
      :memo-id="currentMemo.id"
      @close="showPasswordDialog = false"
      @verify-success="handlePasswordVerified"
    />
  </div>
</template>

<script>
import { ref } from 'vue';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { memoApi } from '@/api';
import { MemoList as MemoListComponent, MemoForm, PasswordDialog } from '@/components/memo';
import { GradientButton } from '@/components/ui';
import useToast from '@/composables/useToast';

export default {
  name: 'MemoManage',
  components: {
    MemoListComponent,
    MemoForm,
    PasswordDialog,
    GradientButton
  },
  setup() {

// 组件状态
const memoListRef = ref(null);
const showCreateForm = ref(false);
const showEditForm = ref(false);
const showViewDialog = ref(false);
const showDeleteDialog = ref(false);
const showPasswordDialog = ref(false);
const currentMemo = ref({});
const decryptedContent = ref('');
const isDeleting = ref(false);

// 使用消息提示
const toast = useToast;

// 格式化日期
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return format(date, 'yyyy年MM月dd日 HH:mm', { locale: zhCN });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return dateString;
  }
};

// 关闭表单
const closeForm = () => {
  showCreateForm.value = false;
  showEditForm.value = false;
  currentMemo.value = {};
};

// 处理创建/编辑表单提交
const handleSubmit = async (formData) => {
  try {
    if (showEditForm.value) {
      // 更新备忘录
      await memoApi.updateMemo(currentMemo.value.id, formData);
      toast.showToast('备忘录更新成功', 'success');
    } else {
      // 创建备忘录
      await memoApi.createMemo(formData);
      toast.showToast('备忘录创建成功', 'success');
    }

    // 关闭表单并刷新列表
    closeForm();
    memoListRef.value.fetchMemos();
  } catch (error) {
    console.error('保存备忘录失败:', error);
    toast.showToast(error.message || '保存备忘录失败', 'error');
  }
};

// 处理编辑
const handleEdit = (memo) => {
  currentMemo.value = { ...memo };

  // 如果是加密备忘录，需要先验证密码
  if (memo.is_encrypted && !decryptedContent.value) {
    // 设置一个标志，表示验证密码是为了编辑
    currentMemo.value.editAfterVerify = true;
    // 打开密码验证对话框
    showPasswordDialog.value = true;
  } else {
    // 非加密备忘录或已解密，直接打开编辑表单
    showEditForm.value = true;
    showCreateForm.value = false;
    showViewDialog.value = false;
  }
};

// 处理查看
const handleView = (memo) => {
  currentMemo.value = { ...memo };
  decryptedContent.value = '';
  showViewDialog.value = true;
};

// 处理删除
const handleDelete = (memo) => {
  currentMemo.value = { ...memo };
  showDeleteDialog.value = true;
};

// 确认删除
const confirmDelete = async () => {
  isDeleting.value = true;

  try {
    await memoApi.deleteMemo(currentMemo.value.id);
    toast.showToast('备忘录删除成功', 'success');
    showDeleteDialog.value = false;
    memoListRef.value.fetchMemos();
  } catch (error) {
    console.error('删除备忘录失败:', error);
    toast.showToast(error.message || '删除备忘录失败', 'error');
  } finally {
    isDeleting.value = false;
  }
};

// 打开密码对话框
const openPasswordDialog = () => {
  showPasswordDialog.value = true;
};

// 处理密码验证成功
const handlePasswordVerified = (content) => {
  decryptedContent.value = content;
  showPasswordDialog.value = false;

  // 如果是为了编辑而验证密码
  if (currentMemo.value && currentMemo.value.editAfterVerify) {
    // 将解密后的内容添加到当前备忘录对象
    currentMemo.value.content = content;
    // 清除编辑标志
    delete currentMemo.value.editAfterVerify;
    // 打开编辑表单
    showEditForm.value = true;
    showCreateForm.value = false;
    showViewDialog.value = false;
  }
};

return {
  memoListRef,
  showCreateForm,
  showEditForm,
  showViewDialog,
  showDeleteDialog,
  showPasswordDialog,
  currentMemo,
  decryptedContent,
  isDeleting,
  formatDate,
  closeForm,
  handleSubmit,
  handleEdit,
  handleView,
  handleDelete,
  confirmDelete,
  openPasswordDialog,
  handlePasswordVerified
};
}
};
</script>
