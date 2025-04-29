<template>
  <div class="space-y-6">
    <div class="flex flex-col space-y-4 md:space-y-0 md:flex-row md:items-center md:justify-between">
      <div class="flex items-center">
        <h1 class="text-2xl font-semibold text-gray-800 dark:text-white">评论管理</h1>
        <!-- 显示当前文章标题（如果有） -->
        <div v-if="currentArticleTitle" class="ml-4 px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm">
          文章: {{ currentArticleTitle }}
          <button @click="clearArticleFilter" class="ml-2 text-blue-600 dark:text-blue-300 hover:text-blue-800 dark:hover:text-blue-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <select
          v-model="filterStatus"
          class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
        >
          <option value="all">全部评论</option>
          <option value="pending">待审核</option>
          <option value="approved">已通过</option>
        </select>
        <button
          @click="refreshComments"
          class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          title="刷新"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 p-4 rounded-md">
      {{ error }}
      <button @click="refreshComments" class="ml-2 underline">重试</button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-700 dark:border-gray-300"></div>
    </div>

    <!-- 评论列表 -->
    <div v-if="!loading && comments.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">评论内容</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">用户</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">文章</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">时间</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">点赞</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">状态</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="comment in comments" :key="comment.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <td class="px-6 py-4 whitespace-normal">
              <div class="text-sm text-gray-900 dark:text-gray-100 line-clamp-2">{{ comment.content }}</div>
              <div v-if="comment.parent_id" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                回复: {{ getParentContent(comment) }}
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                  <span v-if="!comment.user?.avatar" class="text-xs font-medium text-gray-700 dark:text-gray-300">{{ (comment.user?.username || comment.anonymous_name || comment.commenter_name || 'U').charAt(0).toUpperCase() }}</span>
                  <img v-else :src="comment.user.avatar" alt="" class="h-8 w-8 rounded-full">
                </div>
                <div class="ml-3">
                  <div class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    <template v-if="comment.user">
                      {{ comment.user.username }}
                    </template>
                    <template v-else-if="comment.anonymous_name">
                      {{ comment.anonymous_name }} <span class="text-xs text-gray-500 dark:text-gray-400">(匿名)</span>
                    </template>
                    <template v-else>
                      {{ comment.commenter_name || '匿名用户' }}
                    </template>
                  </div>
                  <div v-if="comment.ip_region" class="text-xs text-gray-500 dark:text-gray-400">
                    {{ comment.ip_region }}
                  </div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900 dark:text-gray-100 line-clamp-1">{{ comment.article_title || '未知文章' }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(comment.created_at) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <svg v-if="comment.like_count > 0" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-red-500 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                </svg>
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ comment.like_count || 0 }}</span>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full"
                :class="{
                  'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200': !comment.is_approved,
                  'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': comment.is_approved
                }">
                {{ getStatusText(comment.is_approved) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex space-x-2">
                <button
                  @click="viewCommentDetail(comment)"
                  class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                  title="查看详情"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
                <button
                  v-if="!comment.is_approved"
                  @click="approveComment(comment.id)"
                  class="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                  title="通过"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
                <button
                  v-if="!comment.is_approved"
                  @click="confirmDeleteComment(comment.id)"
                  class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                  title="拒绝（删除）"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
                <button
                  @click="confirmDeleteComment(comment.id)"
                  class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                  title="删除"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页 -->
      <div class="bg-white dark:bg-gray-800 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            :class="{
              'bg-gray-300 dark:bg-gray-700 cursor-not-allowed': currentPage === 1,
              'bg-secondary hover:bg-opacity-90 dark:bg-dark-secondary dark:hover:bg-opacity-90': currentPage !== 1
            }"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200"
          >
            上一页
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            :class="{
              'bg-gray-300 dark:bg-gray-700 cursor-not-allowed': currentPage === totalPages,
              'bg-secondary hover:bg-opacity-90 dark:bg-dark-secondary dark:hover:bg-opacity-90': currentPage !== totalPages
            }"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200"
          >
            下一页
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              显示第 <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> 至 <span class="font-medium">{{ Math.min(currentPage * pageSize, totalComments) }}</span> 条，共 <span class="font-medium">{{ totalComments }}</span> 条
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                :class="{ 'cursor-not-allowed': currentPage === 1 }"
              >
                <span class="sr-only">上一页</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <template v-for="page in paginationRange" :key="page">
                <button
                  v-if="page !== '...'"
                  @click="goToPage(page)"
                  :class="{
                    'z-10 bg-secondary text-white dark:bg-dark-secondary': page === currentPage,
                    'bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700': page !== currentPage
                  }"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium"
                >
                  {{ page }}
                </button>
                <span
                  v-else
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                  ...
                </span>
              </template>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                :class="{ 'cursor-not-allowed': currentPage === totalPages }"
              >
                <span class="sr-only">下一页</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- 无数据提示 -->
    <div v-if="!loading && comments.length === 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400">暂无评论数据</p>
    </div>

    <!-- 评论详情弹窗 -->
    <div v-if="showDetailModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">评论详情</h3>
            <button @click="showDetailModal = false" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <div class="flex items-center mb-2">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center mr-3">
                  <span v-if="!selectedComment?.user?.avatar" class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ getCommentInitial(selectedComment) }}</span>
                  <img v-else :src="selectedComment.user.avatar" alt="" class="h-10 w-10 rounded-full">
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    <template v-if="selectedComment?.user">
                      {{ selectedComment.user.username }}
                    </template>
                    <template v-else-if="selectedComment?.anonymous_name">
                      {{ selectedComment.anonymous_name }} <span class="text-xs text-gray-500 dark:text-gray-400">(匿名)</span>
                    </template>
                    <template v-else>
                      {{ selectedComment?.commenter_name || '未知用户' }}
                    </template>
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(selectedComment?.created_at) }}</div>
                  <div v-if="selectedComment?.ip_region" class="text-xs text-gray-500 dark:text-gray-400">{{ selectedComment.ip_region }}</div>
                </div>
              </div>
              <div class="mt-2 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p class="text-gray-800 dark:text-gray-200 whitespace-pre-wrap">{{ selectedComment?.content }}</p>
                <div v-if="selectedComment?.like_count > 0" class="mt-2 flex items-center text-sm text-gray-500 dark:text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                  </svg>
                  <span>{{ selectedComment.like_count }} 人点赞</span>
                </div>
              </div>
            </div>
            <div v-if="selectedComment?.parent_id" class="border-t border-gray-200 dark:border-gray-700 pt-4">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">回复的评论：</h4>
              <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p class="text-gray-800 dark:text-gray-200 whitespace-pre-wrap">{{ selectedComment?.parent?.content || '原评论内容不可用' }}</p>
              </div>
            </div>
            <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">文章信息：</h4>
              <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p class="text-gray-800 dark:text-gray-200 font-medium">{{ selectedComment?.article?.title || '未知文章' }}</p>
                <router-link
                  v-if="selectedComment?.article?.id"
                  :to="`/article/${selectedComment.article.id}`"
                  target="_blank"
                  class="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 mt-2 inline-block"
                >
                  查看文章
                </router-link>
              </div>
            </div>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button
              v-if="selectedComment && !selectedComment.is_approved"
              @click="approveComment(selectedComment.id, true)"
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              通过
            </button>
            <button
              v-if="selectedComment && !selectedComment.is_approved"
              @click="confirmDeleteComment(selectedComment.id, true)"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              拒绝（删除）
            </button>
            <button
              @click="confirmDeleteComment(selectedComment.id, true)"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              删除
            </button>
            <button
              @click="showDetailModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 确认删除弹窗 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">确认删除</h3>
            <button @click="showDeleteModal = false" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p class="text-gray-700 dark:text-gray-300 mb-6">确定要删除这条评论吗？此操作无法撤销。</p>
          <div class="flex justify-end space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              取消
            </button>
            <button
              @click="deleteComment()"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              确认删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { commentApi } from '@/api'
import message from '@/utils/message.js'
import { formatDateTimeWithTimeZone } from '@/utils/date-utils'

export default {
  name: 'CommentManagement',
  setup() {
    const route = useRoute()
    const router = useRouter()

    // 状态变量
    const comments = ref([])
    const loading = ref(true)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalComments = ref(0)
    const totalPages = ref(1)
    const filterStatus = ref('all')
    const showDetailModal = ref(false)
    const showDeleteModal = ref(false)
    const selectedComment = ref(null)
    const commentToDelete = ref(null)
    const fromDetailModal = ref(false)

    // 文章筛选相关
    const currentArticleId = ref(null)
    const currentArticleTitle = ref('')

    // 计算属性
    const paginationRange = computed(() => {
      const range = []
      const maxVisiblePages = 5

      if (totalPages.value <= maxVisiblePages) {
        // 如果总页数小于等于最大可见页数，显示所有页码
        for (let i = 1; i <= totalPages.value; i++) {
          range.push(i)
        }
      } else {
        // 总是显示第一页
        range.push(1)

        // 计算中间页码的起始和结束
        let start = Math.max(2, currentPage.value - 1)
        let end = Math.min(totalPages.value - 1, currentPage.value + 1)

        // 如果当前页接近开始，调整结束页
        if (currentPage.value <= 3) {
          end = Math.min(totalPages.value - 1, maxVisiblePages - 1)
        }

        // 如果当前页接近结束，调整开始页
        if (currentPage.value >= totalPages.value - 2) {
          start = Math.max(2, totalPages.value - maxVisiblePages + 2)
        }

        // 添加省略号
        if (start > 2) {
          range.push('...')
        }

        // 添加中间页码
        for (let i = start; i <= end; i++) {
          range.push(i)
        }

        // 添加省略号
        if (end < totalPages.value - 1) {
          range.push('...')
        }

        // 总是显示最后一页
        range.push(totalPages.value)
      }

      return range
    })

    // 获取评论列表
    const fetchComments = async () => {
      loading.value = true
      error.value = null

      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value
        }

        let response

        // 如果有文章ID筛选，优先获取指定文章的评论
        if (currentArticleId.value) {
          try {
            // 使用文章评论接口
            // 确保使用正确的 API 路径
            response = await commentApi.fetchComments(currentArticleId.value, params)
            // 如果需要按状态筛选，在前端进行过滤
            if (filterStatus.value !== 'all') {
              const isApproved = filterStatus.value === 'approved'
              response.items = response.items.filter(comment => comment.is_approved === isApproved)
              // 更新总数
              response.total = response.items.length
              response.pages = Math.ceil(response.total / params.page_size) || 1
            }
          } catch (err) {
            console.error(`获取文章 ${currentArticleId.value} 的评论失败:`, err)
            // 如果获取失败，返回空数组
            response = {
              items: [],
              total: 0,
              page: currentPage.value,
              page_size: pageSize.value,
              pages: 1
            }
          }
        } else {
          // 使用获取所有评论的API
          const approvedOnly = filterStatus.value === 'approved' ? true :
                              filterStatus.value === 'pending' ? false : null;

          // 确保使用正确的 API 路径
          response = await commentApi.fetchAllComments({
            page: currentPage.value,
            pageSize: pageSize.value,
            approvedOnly: approvedOnly
          })
        }

        // 根据新的API响应格式处理数据
        comments.value = response.items || []
        totalComments.value = response.total || 0
        totalPages.value = response.pages || Math.ceil(totalComments.value / pageSize.value) || 1
      } catch (err) {
        console.error('获取评论列表失败:', err)
        error.value = err.message || '获取评论列表失败'
        message.error('获取评论列表失败')
      } finally {
        loading.value = false
      }
    }

    // 刷新评论列表
    const refreshComments = () => {
      fetchComments()
    }

    // 分页相关方法
    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    const goToPage = (page) => {
      currentPage.value = page
    }

    // 获取父评论内容
    const getParentContent = (comment) => {
      if (!comment.parent) return '原评论不可见'
      return comment.parent.content ? (comment.parent.content.length > 30 ? comment.parent.content.substring(0, 30) + '...' : comment.parent.content) : '原评论不可见'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知时间'
      try {
        // 使用自定义日期工具函数，将UTC时间转换为本地时间
        return formatDateTimeWithTimeZone(dateString)
      } catch (error) {
        console.error('日期格式化错误:', error)
        return '日期格式错误'
      }
    }

    // 获取状态文本
    const getStatusText = (isApproved) => {
      if (isApproved === true) return '已通过'
      if (isApproved === false) return '待审核'
      return '未知状态'
    }

    // 获取评论用户首字母
    const getCommentInitial = (comment) => {
      if (!comment) return 'U'

      // 确保安全获取字符
      const safeGetChar = (str) => {
        if (!str || typeof str !== 'string' || str.length === 0) return 'U'
        return str.charAt(0).toUpperCase()
      }

      if (comment.user?.username) {
        return safeGetChar(comment.user.username)
      } else if (comment.anonymous_name) {
        return safeGetChar(comment.anonymous_name)
      } else if (comment.commenter_name) {
        return safeGetChar(comment.commenter_name)
      } else if (comment.ip_region) {
        return safeGetChar(comment.ip_region)
      }
      return 'U'
    }

    // 查看评论详情
    const viewCommentDetail = (comment) => {
      selectedComment.value = comment
      showDetailModal.value = true
    }

    // 通过评论
    const approveComment = async (commentId, fromDetail = false) => {
      try {
        // 使用API文档中的路径
        await commentApi.approveComment(commentId)
        message.success('评论已通过')

        // 更新评论状态
        const index = comments.value.findIndex(c => c.id === commentId)
        if (index !== -1) {
          comments.value[index].is_approved = true
        }

        // 如果是从详情弹窗操作的，更新选中的评论
        if (fromDetail && selectedComment.value && selectedComment.value.id === commentId) {
          selectedComment.value.is_approved = true
        }
      } catch (err) {
        console.error('通过评论失败:', err)
        message.error(err.message || '通过评论失败')
      }
    }

    // 注意：由于API文档中没有提供拒绝评论的接口，我们已经将拒绝按钮改为直接调用confirmDeleteComment函数

    // 确认删除评论
    const confirmDeleteComment = (commentId, fromDetail = false) => {
      commentToDelete.value = commentId
      fromDetailModal.value = fromDetail
      showDeleteModal.value = true
    }

    // 删除评论
    const deleteComment = async () => {
      if (!commentToDelete.value) return

      try {
        // 使用API文档中的路径
        await commentApi.deleteComment(commentToDelete.value)
        message.success('评论已删除')

        // 从列表中移除评论
        comments.value = comments.value.filter(c => c.id !== commentToDelete.value)

        // 关闭弹窗
        showDeleteModal.value = false

        // 如果是从详情弹窗操作的，关闭详情弹窗
        if (fromDetailModal.value) {
          showDetailModal.value = false
        }

        // 重置状态
        commentToDelete.value = null
        fromDetailModal.value = false
      } catch (err) {
        console.error('删除评论失败:', err)
        message.error(err.message || '删除评论失败')
        showDeleteModal.value = false
      }
    }

    // 监听筛选条件变化，重置页码并重新获取数据
    watch(filterStatus, () => {
      currentPage.value = 1
      fetchComments()
    })

    // 监听页码变化，重新获取数据
    watch(currentPage, () => {
      fetchComments()
    })

    // 清除文章筛选
    const clearArticleFilter = () => {
      currentArticleId.value = null
      currentArticleTitle.value = ''
      // 移除URL参数
      router.replace({ path: '/admin/comments' })
      // 重新加载评论
      fetchComments()
    }

    // 组件挂载时获取评论列表
    onMounted(() => {
      // 检查URL参数中是否有文章ID和标题
      if (route.query.articleId) {
        currentArticleId.value = route.query.articleId
        currentArticleTitle.value = route.query.articleTitle || `文章 #${route.query.articleId}`
      }

      fetchComments()
    })

    return {
      comments,
      loading,
      error,
      currentPage,
      pageSize,
      totalComments,
      totalPages,
      filterStatus,
      paginationRange,
      showDetailModal,
      showDeleteModal,
      selectedComment,
      currentArticleTitle,
      refreshComments,
      prevPage,
      nextPage,
      goToPage,
      getParentContent,
      formatDate,
      getStatusText,
      getCommentInitial,
      viewCommentDetail,
      approveComment,
      confirmDeleteComment,
      deleteComment,
      clearArticleFilter
    }
  }
}
</script>