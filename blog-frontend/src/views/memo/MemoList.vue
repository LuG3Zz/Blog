<template>
  <div class="bg-gray-50 dark:bg-gray-900 min-h-screen flex flex-col">

    <!-- UseMemos风格的主布局 -->
    <div class="relative flex-1 flex">
      <!-- 遮罩层 - 仅在小屏幕上侧边栏可见时显示 -->
      <div
        v-if="sidebarVisible"
        @click="toggleSidebar"
        class="md:hidden fixed inset-0 bg-black bg-opacity-50 z-5 transition-opacity"
      ></div>

      <!-- 左侧边栏 - 固定 -->
      <div :class="['fixed left-0 top-[64px] bottom-0 z-10 sidebar-width border-r border-gray-200 dark:border-gray-700 shadow-lg transition-transform bg-white dark:bg-gray-800',
                   {'sidebar-visible': sidebarVisible}]">
        <MemoSidebar
          :tags="tagsList"
          :memos-dates="memosDates"
          :is-logged-in="isLoggedIn"
          @tag-selected="handleTagSelected"
          @date-selected="handleDateSelected"
          @create-memo="showCreateForm = true"
          @open-settings="openSettings"
          @search="handleSearch"
          @encrypted-filter="handleEncryptedFilter"
        />
      </div>

      <!-- 侧边栏切换按钮 - 在所有屏幕尺寸下显示 -->
      <button
        @click="toggleSidebar"
        class="fixed left-4 top-[80px] z-20 bg-blue-500 text-white rounded-full p-2 shadow-lg hover:bg-blue-600 transition-colors"
        :class="{'left-[250px]': sidebarVisible}"
      >
        <svg v-if="!sidebarVisible" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- 主内容区 - 可滚动，占据全宽 -->
      <div class="flex-1 overflow-y-auto pl-sidebar pr-4 py-6 scroll-smooth memo-content-area overflow-x-hidden" :class="{'pl-4': !sidebarVisible}" style="height: calc(100vh - 64px); margin-top: 0; padding-bottom: 100px;">
        <div class="max-w-2xl mx-auto">
          <!-- 页面标题 -->
          <div class="mb-6">
            <div class="flex justify-between items-center">
              <h1 class="text-xl font-medium text-gray-800 dark:text-gray-200">
                <span class="text-blue-500 dark:text-blue-400 mr-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </span>
                {{ selectedTag ? `#${selectedTag}` : (isLoggedIn ? '我的备忘录' : '备忘录') }}
              </h1>

              <!-- 筛选和搜索按钮 -->
              <div class="flex items-center space-x-2">
                <button class="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                  </svg>
                </button>
                <button class="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </div>
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {{ isLoggedIn ? '管理和创建您的个人备忘录' : '浏览公开备忘录或登录以创建您自己的备忘录' }}
            </p>
          </div>

          <!-- 快速输入框 -->
          <div v-if="isLoggedIn" class="mb-6 sticky top-0 z-10 pt-2 pb-4 bg-gray-50 dark:bg-gray-900">
            <QuickMemoInput
              @submit="handleQuickSubmit"
              @error="handleInputError"
            />
          </div>

          <!-- 备忘录列表 -->
          <MemoListComponent
            ref="memoListRef"
            :is-logged-in="isLoggedIn"
            :tag-filter="selectedTag"
            :date-filter="selectedDate"
            :encrypted-filter="isEncryptedFilterActive"
            @create="showCreateForm = true"
            @edit="handleEdit"
            @delete="handleDelete"
            @view="handleView"
            @tag-click="handleTagSelected"
            @data-updated="handleDataUpdated"
            @clear-search="clearSearch"
          />
        </div>
      </div>
    </div>

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
      :memo-id="isLoggedIn && currentMemo && userInfo && userInfo.id === currentMemo.user_id ? currentMemo.id : null"
      :local-verification="!isLoggedIn || !userInfo || (currentMemo && userInfo.id !== currentMemo.user_id)"
      :correct-password="currentMemo ? currentMemo.password : ''"
      :encrypted-content="currentMemo ? currentMemo.encryptedContent : ''"
      @close="showPasswordDialog = false"
      @verify-success="handlePasswordVerified"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { memoApi } from '@/api';
import { MemoList as MemoListComponent, MemoForm, PasswordDialog, QuickMemoInput, MemoSidebar } from '@/components/memo';
import { GradientButton } from '@/components/ui';
import { Navbar } from '@/components/layout';
import useToast from '@/composables/useToast';
import { useUserStore } from '@/stores';
import { formatDateTime } from '@/utils/date-utils';

export default {
  name: 'MemoListView',
  components: {
    MemoListComponent,
    MemoForm,
    PasswordDialog,
    GradientButton,
    Navbar,
    QuickMemoInput,
    MemoSidebar
  },
  setup() {
    // 获取用户状态
    const userStore = useUserStore();
    // 使用 storeToRefs 保持响应性
    const { isLoggedIn, userInfo } = storeToRefs(userStore);

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

    // 侧边栏状态
    const sidebarVisible = ref(window.innerWidth > 768); // 默认在大屏幕上显示

    // 切换侧边栏显示/隐藏
    const toggleSidebar = () => {
      sidebarVisible.value = !sidebarVisible.value;
    };

    // 标签相关
    const selectedTag = ref('');
    const tagsList = ref([]);

    // 日期相关
    const selectedDate = ref(null);
    const memosDates = ref([]);

    // 加密动态筛选
    const isEncryptedFilterActive = ref(false);

    // 搜索相关
    const searchQuery = ref('');

    // 处理搜索
    const handleSearch = async (query) => {
      searchQuery.value = query;

      // 清除标签和日期筛选
      selectedTag.value = '';
      selectedDate.value = null;

      if (query && query.trim() !== '') {
        try {
          // 显示加载状态
          if (memoListRef.value) {
            memoListRef.value.setLoading(true);
          }

          // 调用搜索API
          const results = await memoApi.searchMemos({
            q: query,
            skip: 0,
            limit: 100
          });

          // 更新备忘录列表
          if (memoListRef.value) {
            memoListRef.value.updateMemosDirectly(results, query);
          }
        } catch (error) {
          console.error('搜索备忘录失败:', error);
          toast.showToast(error.message || '搜索备忘录失败', 'error');
        } finally {
          // 隐藏加载状态
          if (memoListRef.value) {
            memoListRef.value.setLoading(false);
          }
        }
      } else {
        // 如果搜索关键词为空，重新获取所有备忘录
        if (memoListRef.value) {
          memoListRef.value.fetchMemos(true);
        }
      }
    };

    // 清除搜索
    const clearSearch = () => {
      searchQuery.value = '';
      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 最近的备忘录
    const recentMemos = ref([]);

    // 使用消息提示
    const toast = useToast;

    // 格式化日期
    const formatDate = (dateString) => {
      try {
        return formatDateTime(dateString, 'yyyy年MM月dd日 HH:mm');
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
        // 标题可以为空，不设置默认值

        if (!formData.content || formData.content.trim() === '') {
          toast.showToast('内容不能为空', 'error');
          return;
        }

        // 确保内容不超过后端限制
        if (formData.content.length > 10000) {
          toast.showToast('内容过长，请减少字数', 'error');
          return;
        }

        // 确保标题不超过后端限制
        if (formData.title.length > 100) {
          formData.title = formData.title.substring(0, 97) + '...';
        }

        console.log('MemoList视图接收到的表单数据:', {
          title: formData.title,
          content_length: formData.content ? formData.content.length : 0,
          is_encrypted: formData.is_encrypted,
          has_password: !!formData.password
        });

        if (showEditForm.value) {
          // 更新备忘录
          console.log(`准备更新备忘录 ${currentMemo.value.id}`);
          const response = await memoApi.updateMemo(currentMemo.value.id, {
            title: formData.title,
            content: formData.content,
            is_encrypted: formData.is_encrypted,
            password: formData.password
          });
          console.log('更新备忘录响应:', response);
          toast.showToast('备忘录更新成功', 'success');
        } else {
          // 创建备忘录
          console.log('准备创建新备忘录');
          const response = await memoApi.createMemo({
            title: formData.title,
            content: formData.content,
            is_encrypted: formData.is_encrypted,
            password: formData.password
          });
          console.log('创建备忘录响应:', response);
          toast.showToast('备忘录创建成功', 'success');
        }

        // 关闭表单并刷新列表
        closeForm();
        memoListRef.value.fetchMemos();

        // 刷新后更新故事栏
        setTimeout(() => {
          updateRecentMemos();
        }, 300);
      } catch (error) {
        console.error('保存备忘录失败:', error);
        if (error.response && error.response.data && error.response.data.detail) {
          toast.showToast(`保存失败: ${error.response.data.detail}`, 'error');
        } else {
          toast.showToast(error.message || '保存备忘录失败', 'error');
        }
      }
    };

    // 处理快速输入提交
    const handleQuickSubmit = async (formData) => {
      try {
        // 标题可以为空，不设置默认值

        if (!formData.content || formData.content.trim() === '') {
          toast.showToast('内容不能为空', 'error');
          return;
        }

        // 确保内容不超过后端限制
        if (formData.content.length > 10000) {
          toast.showToast('内容过长，请减少字数', 'error');
          return;
        }

        // 确保标题不超过后端限制
        if (formData.title.length > 100) {
          formData.title = formData.title.substring(0, 97) + '...';
        }

        console.log('快速输入提交的数据:', {
          title: formData.title,
          content_length: formData.content ? formData.content.length : 0,
          is_encrypted: formData.is_encrypted,
          has_password: !!formData.password
        });

        // 创建备忘录
        const response = await memoApi.createMemo({
          title: formData.title,
          content: formData.content,
          is_encrypted: formData.is_encrypted,
          password: formData.password
        });

        console.log('创建备忘录响应:', response);
        toast.showToast('动态发布成功', 'success');

        // 刷新列表
        memoListRef.value.fetchMemos();

        // 刷新后更新故事栏
        setTimeout(() => {
          updateRecentMemos();
        }, 300);
      } catch (error) {
        console.error('发布动态失败:', error);
        if (error.response && error.response.data && error.response.data.detail) {
          toast.showToast(`发布失败: ${error.response.data.detail}`, 'error');
        } else {
          toast.showToast(error.message || '发布动态失败', 'error');
        }
      }
    };

    // 处理编辑
    const handleEdit = (memo) => {
      // 检查用户是否已登录
      if (!isLoggedIn.value) {
        toast.showToast('请先登录后再编辑', 'warning');
        return;
      }

      // 检查userInfo是否存在
      if (!userInfo.value) {
        toast.showToast('无法获取用户信息，请重新登录', 'warning');
        return;
      }

      // 检查用户是否是备忘录的所有者
      if (userInfo.value.id !== memo.user_id) {
        toast.showToast('您无权编辑此备忘录', 'warning');
        return;
      }

      currentMemo.value = { ...memo };
      showEditForm.value = true;
      showCreateForm.value = false;
      showViewDialog.value = false;
    };

    // 处理查看
    const handleView = (memo) => {
      currentMemo.value = { ...memo };
      decryptedContent.value = '';
      showViewDialog.value = true;
    };

    // 处理删除
    const handleDelete = (memo) => {
      // 检查用户是否已登录
      if (!isLoggedIn.value) {
        toast.showToast('请先登录后再删除', 'warning');
        return;
      }

      // 检查userInfo是否存在
      if (!userInfo.value) {
        toast.showToast('无法获取用户信息，请重新登录', 'warning');
        return;
      }

      // 检查用户是否是备忘录的所有者
      if (userInfo.value.id !== memo.user_id) {
        toast.showToast('您无权删除此备忘录', 'warning');
        return;
      }

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
    };

    // 处理标签选择
    const handleTagSelected = (tag) => {
      selectedTag.value = tag;
      // 清除日期筛选和加密筛选
      selectedDate.value = null;
      isEncryptedFilterActive.value = false;
      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 处理加密动态筛选
    const handleEncryptedFilter = (isActive) => {
      isEncryptedFilterActive.value = isActive;

      // 清除标签和日期筛选
      if (isActive) {
        selectedTag.value = '';
        selectedDate.value = null;
      }

      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 处理日期选择
    const handleDateSelected = (date) => {
      selectedDate.value = date;
      // 清除标签筛选和加密筛选
      selectedTag.value = '';
      isEncryptedFilterActive.value = false;
      if (memoListRef.value) {
        memoListRef.value.fetchMemos(true);
      }
    };

    // 打开设置
    const openSettings = () => {
      // 这里可以实现设置功能，暂时只显示提示
      toast.showToast('设置功能即将推出', 'info');
    };

    // 处理输入错误
    const handleInputError = (errorMessage) => {
      toast.showToast(errorMessage, 'error');
    };

    // 处理数据更新
    const handleDataUpdated = (data) => {
      console.log('MemoList.handleDataUpdated 收到数据更新事件，数据长度:', data.length);
      // 提取标签
      extractTags();
    };

    // 提取标签并更新标签列表，同时收集备忘录日期
    const extractTags = () => {
      if (!memoListRef.value || !memoListRef.value.memos) return;

      const memos = memoListRef.value.memos;
      const tagsMap = new Map();
      const datesSet = new Set();

      console.log('提取标签，备忘录数量:', memos.length);

      // 从备忘录内容中提取标签，同时收集日期
      memos.forEach(memo => {
        // 提取标签
        if (memo.content) {
          // 检查内容是否包含标签标记 (#)
          if (memo.content.includes('#')) {
            const tagMatch = memo.content.match(/#([\u4e00-\u9fa5a-zA-Z0-9_-]+)/);
            if (tagMatch && tagMatch[1]) {
              const tagName = tagMatch[1];
              console.log('从内容中提取到标签:', tagName, '内容:', memo.content.substring(0, 30) + '...');

              // 只有成功提取到标签时才添加到标签映射中
              if (tagsMap.has(tagName)) {
                tagsMap.set(tagName, tagsMap.get(tagName) + 1);
              } else {
                tagsMap.set(tagName, 1);
              }
            } else {
              console.log('内容中有#但未匹配到有效标签，认为没有标签');
            }
          } else {
            console.log('内容中没有#，认为没有标签');
          }
        }

        // 收集日期，使用formatDateTime格式化
        if (memo.created_at) {
          const dateStr = formatDateTime(memo.created_at, 'yyyy-MM-dd');
          datesSet.add(dateStr);
        }
      });

      // 转换为数组格式
      tagsList.value = Array.from(tagsMap.entries()).map(([name, count]) => ({
        name,
        count
      })).sort((a, b) => b.count - a.count);

      console.log('提取的标签列表:', tagsList.value);

      // 更新日期列表
      memosDates.value = Array.from(datesSet);
      console.log('提取的日期列表:', memosDates.value);
    };

    // 监听备忘录列表组件的数据
    const updateRecentMemos = () => {
      if (memoListRef.value && memoListRef.value.memos) {
        console.log('updateRecentMemos: 备忘录数量', memoListRef.value.memos.length);
        // 获取最近的5个备忘录作为故事
        recentMemos.value = [...memoListRef.value.memos].slice(0, 5);

        // 提取标签
        extractTags();
      } else {
        console.log('updateRecentMemos: memoListRef 或 memos 不存在');
      }
    };

    // 组件挂载后获取数据
    onMounted(() => {
      console.log('MemoList 组件已挂载');
      // 初始化后更新故事栏和标签
      setTimeout(() => {
        updateRecentMemos();
      }, 500);

      // 添加一个额外的延迟调用，确保数据已加载
      setTimeout(() => {
        console.log('延迟 2 秒后再次尝试提取标签');
        if (memoListRef.value) {
          console.log('memoListRef 存在，尝试获取备忘录');
          if (memoListRef.value.memos && memoListRef.value.memos.length > 0) {
            console.log('找到备忘录数据，提取标签');
            extractTags();
          } else {
            console.log('备忘录数据不存在或为空，尝试获取数据');
            memoListRef.value.fetchMemos();
            setTimeout(extractTags, 500);
          }
        }
      }, 2000);
    });

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
      recentMemos,
      isLoggedIn,
      userInfo, // 使用解构出来的userInfo
      sidebarVisible,
      toggleSidebar,
      selectedTag,
      tagsList,
      selectedDate,
      memosDates,
      isEncryptedFilterActive,
      searchQuery,
      handleSearch,
      clearSearch,
      formatDate,
      closeForm,
      handleSubmit,
      handleQuickSubmit,
      handleEdit,
      handleView,
      handleDelete,
      confirmDelete,
      openPasswordDialog,
      handlePasswordVerified,
      updateRecentMemos,
      handleTagSelected,
      handleDateSelected,
      handleEncryptedFilter,
      openSettings,
      handleInputError,
      handleDataUpdated
    };
  }
};
</script>

<style scoped>
/* 添加页面过渡效果 */
.container {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 自定义滚动条 */
.scrollbar-thin {
  scrollbar-width: thin;
}

.scrollbar-thumb-gray-300::-webkit-scrollbar {
  height: 6px;
}

.scrollbar-thumb-gray-300::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thumb-gray-300::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 20px;
}

.dark .scrollbar-thumb-gray-600::-webkit-scrollbar-thumb {
  background-color: #4b5563;
}

/* 侧边栏宽度 */
.sidebar-width {
  width: 240px;
  min-width: 240px;
}

/* 内容区域左边距，与侧边栏宽度相同 */
.pl-sidebar {
  padding-left: 260px; /* 侧边栏宽度 + 额外间距 */
}

/* 侧边栏和内容区域的响应式设计 */
.sidebar-width {
  width: 240px;
  min-width: 240px;
  transform: translateX(0);
  transition: transform 0.3s ease, width 0.3s ease, min-width 0.3s ease;
}

/* 当侧边栏隐藏时 */
.sidebar-width:not(.sidebar-visible) {
  transform: translateX(-100%);
}

/* 内容区域在侧边栏隐藏时的样式 */
.pl-4 {
  padding-left: 1rem !important;
  transition: padding-left 0.3s ease;
}

/* 确保内容区域独立滚动 */
.memo-content-area {
  position: relative;
  overscroll-behavior: contain;
  overflow-y: auto !important;
  height: auto !important;
  min-height: calc(100vh - 64px) !important;
}

/* 侧边栏切换按钮过渡效果 */
button {
  transition: left 0.3s ease, background-color 0.2s ease;
}

/* 备忘录内容区域滚动条样式 */
.memo-content-area::-webkit-scrollbar {
  width: 6px;
}

.memo-content-area::-webkit-scrollbar-track {
  background: transparent;
}

.memo-content-area::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.memo-content-area::-webkit-scrollbar-thumb:hover {
  background-color: rgba(107, 114, 128, 0.7);
}

/* 确保内容区域可以独立滚动 */
.memo-content-area {
  overscroll-behavior: contain;
  overflow-y: auto !important;
  height: auto !important;
  min-height: calc(100vh - 64px) !important;
  padding-bottom: 100px !important;
}

/* 修复滚动问题 */
:deep(.infinite-scroll-container) {
  overflow-y: auto !important;
}

/* 确保根元素可以滚动 */
.min-h-screen {
  min-height: 100vh;
  height: auto;
  overflow-y: auto;
}
</style>
