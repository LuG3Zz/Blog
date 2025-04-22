<template>
  <div class="comment-section mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
    <div class="mb-6">
      <h3 class="text-xl font-bold text-gray-800 dark:text-gray-200 flex items-center justify-between">
        评论区 <span class="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">({{ comments.length }})</span>
        <button
          @click="toggleSort"
          class="px-3 py-1 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-lg text-sm hover:bg-opacity-90 transition-colors"
        >
          {{ sortOrder === 'desc' ? '最新↑' : '最早↓' }}
        </button>
      </h3>
      <div v-if="articleTitle" class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        文章: {{ articleTitle }}
      </div>
    </div>

    <!-- 评论列表 -->
    <div v-if="comments.length > 0" class="space-y-6 mb-8">
      <div v-for="comment in comments" :key="comment.id" class="comment bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
        <div class="flex items-start">
          <div class="flex-shrink-0 mr-3">
            <!-- 用户头像 -->
            <div
              @click="navigateToUserProfile(comment.user?.id)"
              class="w-10 h-10 rounded-full overflow-hidden border-2 border-gray-200 dark:border-gray-600 cursor-pointer hover:border-secondary dark:hover:border-dark-secondary transition-colors flex items-center justify-center"
            >
              <img
                v-if="comment.user?.avatar"
                :src="comment.user.avatar"
                :alt="comment.user?.username || '用户头像'"
                class="w-10 h-10 object-cover object-center rounded-full"
                style="max-width: 40px; max-height: 40px;"
              />
              <div
                v-else
                class="w-full h-full bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary flex items-center justify-center font-bold"
              >
                {{ getAvatarInitial(comment) }}
              </div>
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <!-- 用户名和角色 -->
                <div class="flex items-center">
                  <h4
                    @click="comment.user?.id ? navigateToUserProfile(comment.user.id) : null"
                    :class="{
                      'font-medium text-gray-800 dark:text-gray-200 hover:text-secondary dark:hover:text-dark-secondary cursor-pointer transition-colors': comment.user?.id,
                      'font-medium text-gray-800 dark:text-gray-200': !comment.user?.id
                    }"
                  >
                    <template v-if="comment.user?.username">
                      {{ comment.user.username }}
                    </template>
                    <template v-else-if="comment.anonymous_name">
                      {{ comment.anonymous_name }} <span class="text-xs text-gray-500 dark:text-gray-400">(匿名)</span>
                    </template>
                    <template v-else-if="comment.commenter_name">
                      {{ comment.commenter_name }}
                    </template>
                    <template v-else-if="comment.ip_region">
                      {{ comment.ip_region + '网友' }}
                    </template>
                    <template v-else>
                      匿名用户
                    </template>
                  </h4>
                  <span
                    v-if="comment.user?.role"
                    class="ml-2 px-2 py-0.5 text-xs rounded-full"
                    :class="{
                      'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': comment.user.role === 'admin',
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': comment.user.role === 'editor',
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': comment.user.role === 'user'
                    }"
                  >
                    {{ getRoleName(comment.user.role) }}
                  </span>
                </div>
                <!-- IP地区 -->
                <p v-if="comment.ip_region" class="text-xs text-gray-500 dark:text-gray-400">{{ comment.ip_region }}</p>
              </div>
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ comment.date }}</span>
            </div>
            <!-- 评论内容 -->
            <p class="mt-2 text-gray-700 dark:text-gray-300">{{ comment.content }}</p>
            <!-- 评论操作 -->
            <div class="mt-2 flex items-center space-x-4">
              <button
                @click="likeComment(comment.id)"
                :class="{
                  'text-red-500 dark:text-red-400': comment.liked_by_me,
                  'text-sm text-gray-500 dark:text-gray-400 hover:text-red-500 dark:hover:text-red-400': !comment.liked_by_me
                }"
                class="flex items-center px-2 py-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" :stroke-width="comment.liked_by_me ? 2.5 : 2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                </svg>
                <span :class="{'font-medium': comment.liked_by_me}">{{ comment.like_count || 0 }}</span>
              </button>
              <button @click="replyToComment(comment.id)" class="text-sm text-gray-500 dark:text-gray-400 hover:text-secondary dark:hover:text-dark-secondary flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                </svg>
                回复
              </button>
              <!-- 如果是当前用户的评论，显示编辑和删除按钮 -->
              <div v-if="isCurrentUserComment(comment)" class="flex items-center space-x-2">
                <button @click="editComment(comment)" class="text-sm text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  编辑
                </button>
                <button @click="deleteComment(comment.id)" class="text-sm text-gray-500 dark:text-gray-400 hover:text-red-500 dark:hover:text-red-400 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  删除
                </button>
              </div>
            </div>

            <!-- 回复列表 -->
            <div v-if="comment.replies && comment.replies.length > 0" class="mt-4 pl-4 border-l-2 border-gray-200 dark:border-gray-600 space-y-3">
              <div v-for="reply in comment.replies" :key="reply.id" class="reply">
                <div class="flex items-start">
                  <div class="flex-shrink-0 mr-2">
                    <div
                      @click="navigateToUserProfile(reply.user?.id)"
                      class="w-8 h-8 rounded-full overflow-hidden border-2 border-gray-200 dark:border-gray-600 cursor-pointer hover:border-secondary dark:hover:border-dark-secondary transition-colors flex items-center justify-center"
                    >
                      <img
                        v-if="reply.user?.avatar"
                        :src="reply.user.avatar"
                        :alt="reply.user?.username || '用户头像'"
                        class="w-8 h-8 object-cover object-center rounded-full"
                        style="max-width: 32px; max-height: 32px;"
                      />
                      <div
                        v-else
                        class="w-full h-full bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary flex items-center justify-center font-bold text-xs"
                      >
                        {{ getAvatarInitial(reply) }}
                      </div>
                    </div>
                  </div>
                  <div class="flex-grow">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <h5
                          @click="reply.user?.id ? navigateToUserProfile(reply.user.id) : null"
                          :class="{
                            'text-sm font-medium text-gray-800 dark:text-gray-200 hover:text-secondary dark:hover:text-dark-secondary cursor-pointer transition-colors': reply.user?.id,
                            'text-sm font-medium text-gray-800 dark:text-gray-200': !reply.user?.id
                          }"
                        >
                          <template v-if="reply.user?.username">
                            {{ reply.user.username }}
                          </template>
                          <template v-else-if="reply.anonymous_name">
                            {{ reply.anonymous_name }} <span class="text-xs text-gray-500 dark:text-gray-400">(匿名)</span>
                          </template>
                          <template v-else-if="reply.commenter_name">
                            {{ reply.commenter_name }}
                          </template>
                          <template v-else-if="reply.ip_region">
                            {{ reply.ip_region + '网友' }}
                          </template>
                          <template v-else>
                            匿名用户
                          </template>
                        </h5>
                        <span
                          v-if="reply.user?.role"
                          class="ml-2 px-1.5 py-0.5 text-xs rounded-full"
                          :class="{
                            'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': reply.user.role === 'admin',
                            'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': reply.user.role === 'editor',
                            'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': reply.user.role === 'user'
                          }"
                        >
                          {{ getRoleName(reply.user.role) }}
                        </span>
                      </div>
                      <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(reply.created_at) }}</span>
                    </div>
                    <p class="text-sm text-gray-700 dark:text-gray-300 mt-1">{{ reply.content }}</p>
                    <div class="mt-1 flex items-center space-x-2">
                      <button
                        @click="likeComment(reply.id)"
                        :class="{
                          'text-red-500 dark:text-red-400': reply.liked_by_me,
                          'text-xs text-gray-500 dark:text-gray-400 hover:text-red-500 dark:hover:text-red-400': !reply.liked_by_me
                        }"
                        class="flex items-center px-1.5 py-0.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" :stroke-width="reply.liked_by_me ? 2.5 : 2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                        </svg>
                        <span :class="{'font-medium': reply.liked_by_me}">{{ reply.like_count || 0 }}</span>
                      </button>
                      <button
                        @click="replyToComment(reply.id)"
                        class="text-xs text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 flex items-center"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                        </svg>
                        回复
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- 无评论状态 -->
    <div v-else class="text-center py-8">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
      <p class="mt-4 text-gray-600 dark:text-gray-400">暂无评论，成为第一个评论的人吧！</p>
    </div>

    <!-- 评论表单 -->
    <div class="mt-6">
      <form @submit.prevent="submitComment">
        <div class="mb-4">
          <div class="flex justify-between items-center mb-2">
            <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300">评论内容</label>
            <div v-if="newComment.parentId" class="flex items-center text-sm text-blue-500 dark:text-blue-400">
              <span>回复中</span>
              <button
                @click="cancelReply"
                class="ml-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                title="取消回复"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          <textarea
            id="content"
            v-model="newComment.content"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-secondary dark:focus:ring-dark-secondary focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="请输入您的评论内容"
            required
          ></textarea>
        </div>

        <!-- 匿名评论表单字段 -->
        <div v-if="!isLoggedIn" class="mb-4">
          <label for="anonymousName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">显示名称</label>
          <input
            id="anonymousName"
            v-model="newComment.anonymousName"
            type="text"
            maxlength="50"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-secondary dark:focus:ring-dark-secondary focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="请输入您的显示名称"
            required
          />
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">匿名评论可能需要审核后才能显示</p>
        </div>

        <div class="flex justify-between items-center">
          <div v-if="!isLoggedIn" class="text-sm text-gray-500 dark:text-gray-400">
            <router-link to="/login" class="text-blue-500 hover:underline">登录</router-link> 后发表评论无需审核
          </div>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-6 py-2 bg-secondary dark:bg-dark-secondary text-primary dark:text-dark-primary rounded-lg hover:bg-gray-800 dark:hover:bg-gray-300 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 ml-auto"
          >
            <svg v-if="isSubmitting" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isSubmitting ? '提交中...' : (editingComment ? '更新评论' : '提交评论') }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { commentApi, userApi } from '../../api'
import message from '../../utils/message'
import { useRouter } from 'vue-router'

export default {
  name: 'CommentSection',
  props: {
    postId: {
      type: [Number, String],
      required: true,
      validator: function(value) {
        // 确保值可以被转换为有效的整数
        const num = parseInt(value)
        return !isNaN(num) && num > 0
      }
    },
    articleTitle: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const router = useRouter()
    const comments = ref([])
    const newComment = ref({ content: '', anonymousName: '', parentId: null })
    const isSubmitting = ref(false)
    const sortOrder = ref('desc') // 默认降序，最新的在前
    const currentUserId = ref(localStorage.getItem('userId'))
    const editingComment = ref(null)

    // 检查用户是否已登录
    const isLoggedIn = computed(() => {
      return !!localStorage.getItem('token')
    })

    // 导航到登录页面
    const navigateToLogin = () => {
      router.push('/login?redirect=' + encodeURIComponent(window.location.pathname))
    }

    // 获取评论
    const loadComments = async () => {
      try {
        const response = await commentApi.fetchComments(props.postId, {
          parentOnly: true // 只获取主评论，不包括回复
        })

        // 处理评论数据
        if (response && response.items) {
          // 将评论数据转换为所需格式
          const processedComments = response.items.map(c => ({
            ...c,
            date: formatDate(c.created_at),
            // 如果有用户信息，保留原样，否则使用 IP 地区
            user: c.user || null,
            // 确保点赞状态存在
            liked_by_me: c.liked_by_me || false,
            // 确保回复中的点赞状态也存在
            replies: c.replies ? c.replies.map(r => ({
              ...r,
              liked_by_me: r.liked_by_me || false
            })) : []
          }))

          comments.value = processedComments
        } else {
          comments.value = []
        }
      } catch (error) {
        console.error('获取评论失败:', error)
        message.error('获取评论失败')
      }
    }

    // 提交评论
    const submitComment = async () => {
      // 检查评论内容
      if (!newComment.value.content?.trim()) {
        message.error('请填写评论内容');
        return;
      }

      // 检查匿名用户名称
      const token = localStorage.getItem('token');
      if (!token && !newComment.value.anonymousName?.trim()) {
        message.error('请填写显示名称或登录后再发表评论');
        return;
      }

      isSubmitting.value = true;
      try {
        // 如果是编辑现有评论
        if (editingComment.value) {
          const updatedComment = await commentApi.updateComment(
            editingComment.value.id,
            newComment.value.content
          )

          // 更新评论列表中的评论
          const index = comments.value.findIndex(c => c.id === editingComment.value.id)
          if (index !== -1) {
            comments.value[index] = {
              ...comments.value[index],
              content: updatedComment.content,
              updated_at: updatedComment.updated_at,
              date: formatDate(updatedComment.updated_at)
            }
          }

          editingComment.value = null
          message.success('评论更新成功')
        } else {
          // 创建新评论
          let data;
          if (token) {
            // 登录用户发表评论
            console.log('发送登录用户评论数据:', {
              articleId: parseInt(props.postId),
              content: newComment.value.content
            });
            data = await commentApi.createComment(
              props.postId,
              newComment.value.content,
              newComment.value.parentId
            )
          } else {
            // 匿名用户发表评论
            console.log('发送匿名评论数据:', {
              articleId: parseInt(props.postId),
              content: newComment.value.content,
              anonymousName: newComment.value.anonymousName
            });
            data = await commentApi.createComment(
              props.postId,
              newComment.value.content,
              newComment.value.parentId, // 父评论ID
              newComment.value.anonymousName
            )
          }

          if (data.is_approved === false) {
            message.info('评论已提交，需要审核后才能显示');
            // 清空输入框
            newComment.value.content = '';
            newComment.value.parentId = null;
            if (!token) newComment.value.anonymousName = '';
            return;
          }

          // 将新评论添加到列表开头
          comments.value.unshift({
            ...data,
            date: formatDate(data.created_at)
          })

          message.success('评论成功')
        }

        // 清空输入框
        newComment.value.content = '';
        newComment.value.parentId = null;
        if (!token) newComment.value.anonymousName = '';
      } catch (error) {
        console.error('评论提交失败:', error)

        // 显示更详细的错误信息
        if (error.response && error.response.data) {
          console.error('错误响应数据:', error.response.data);

          // 如果有详细的错误信息，显示给用户
          if (error.response.data.detail) {
            const detail = error.response.data.detail;
            if (Array.isArray(detail) && detail.length > 0) {
              // 如果是数组形式的错误详情
              const firstError = detail[0];
              message.error(`评论提交失败: ${firstError.msg || '未知错误'}`);
            } else if (typeof detail === 'string') {
              message.error(`评论提交失败: ${detail}`);
            } else {
              message.error('评论提交失败，请检查输入');
            }
            return;
          }
        }

        // 默认错误消息
        message.error('评论提交失败，请稍后重试');
      } finally {
        isSubmitting.value = false;
      }
    }

    // 切换排序方法
    const toggleSort = () => {
      sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
      comments.value.sort((a, b) => {
        const dateA = new Date(a.created_at + 'Z')
        const dateB = new Date(b.created_at + 'Z')
        return sortOrder.value === 'desc' ? dateB - dateA : dateA - dateB
      })
    }

    onMounted(loadComments)

    // 点赞评论
    const likeComment = async (commentId) => {
      try {
        const result = await commentApi.likeComment(commentId)
        // 更新评论的点赞数
        const updateComment = (comments, id, result) => {
          const comment = comments.find(c => c.id === id)
          if (comment) {
            comment.like_count = result.like_count
            // 更新点赞状态
            comment.liked_by_me = result.liked_by_me || false
            return true
          }
          return false
        }

        // 先在主评论列表中查找
        let found = updateComment(comments.value, commentId, result)

        // 如果没找到，在回复中查找
        if (!found) {
          for (const comment of comments.value) {
            if (comment.replies && comment.replies.length > 0) {
              found = updateComment(comment.replies, commentId, result)
              if (found) break
            }
          }
        }

        // 根据API文档，可能会返回点赞状态的消息
        message.success(result.message || '点赞成功')
      } catch (error) {
        console.error('点赞失败:', error)
        message.error(error.message || '点赞失败，请稍后重试')
      }
    }

    // 回复评论
    const replyToComment = (commentId) => {
      const comment = comments.value.find(c => c.id === commentId)
      if (comment) {
        let displayName = '用户';

        if (comment.user?.username) {
          displayName = comment.user.username;
        } else if (comment.anonymous_name) {
          displayName = comment.anonymous_name;
        } else if (comment.commenter_name) {
          displayName = comment.commenter_name;
        } else if (comment.ip_region) {
          displayName = comment.ip_region + '网友';
        }

        newComment.value.content = `@${displayName} `;
        // 聚焦到评论输入框
        document.getElementById('content').focus();

        // 设置父评论 ID
        newComment.value.parentId = commentId;
      }
    }

    // 取消回复
    const cancelReply = () => {
      newComment.value.parentId = null;
      // 清除引用的用户名
      newComment.value.content = newComment.value.content.replace(/^@[^\s]+ /, '');
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return new Date(dateString + 'Z').toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        console.error('日期格式化错误:', error)
        return dateString
      }
    }

    // 获取角色名称
    const getRoleName = (role) => {
      const roleMap = {
        'admin': '管理员',
        'editor': '编辑',
        'user': '用户'
      }
      return roleMap[role] || role
    }

    // 判断是否是当前用户的评论
    const isCurrentUserComment = (comment) => {
      return currentUserId.value && comment.user && comment.user.id === parseInt(currentUserId.value)
    }

    // 获取头像首字母
    const getAvatarInitial = (comment) => {
      if (comment.user?.username) {
        return comment.user.username.charAt(0).toUpperCase()
      } else if (comment.anonymous_name) {
        return comment.anonymous_name.charAt(0).toUpperCase()
      } else if (comment.commenter_name) {
        return comment.commenter_name.charAt(0).toUpperCase()
      } else if (comment.ip_region) {
        return comment.ip_region.charAt(0).toUpperCase()
      }
      return 'U'
    }

    // 导航到用户资料页
    const navigateToUserProfile = (userId) => {
      if (!userId) return
      router.push(`/user/${userId}`)
    }

    // 编辑评论
    const editComment = (comment) => {
      editingComment.value = { ...comment }
      newComment.value.content = comment.content
      document.getElementById('content').focus()
    }

    // 删除评论
    const deleteComment = async (commentId) => {
      try {
        await commentApi.deleteComment(commentId)
        comments.value = comments.value.filter(c => c.id !== commentId)
        message.success('评论删除成功')
      } catch (error) {
        message.error('评论删除失败')
      }
    }

    return {
      comments,
      newComment,
      submitComment,
      likeComment,
      replyToComment,
      isSubmitting,
      sortOrder,
      toggleSort,
      formatDate,
      getRoleName,
      isCurrentUserComment,
      navigateToUserProfile,
      navigateToLogin,
      isLoggedIn,
      editComment,
      deleteComment,
      getAvatarInitial,
      cancelReply
    }
  }
}
</script>
