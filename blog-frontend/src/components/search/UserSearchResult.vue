<template>
  <div class="user-search-result bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
    <div class="p-4 md:p-6">
      <div class="flex items-center">
        <!-- 用户头像 -->
        <div class="flex-shrink-0 mr-4">
          <router-link :to="`/user/${user.id}`" class="block">
            <div class="user-avatar w-16 h-16 rounded-full overflow-hidden border border-gray-200 dark:border-gray-600 hover:border-secondary dark:hover:border-dark-secondary transition-all duration-300 shadow-md">
              <template v-if="user.avatar">
                <img
                  :src="user.avatar"
                  :alt="user.username"
                  class="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
                  @error="handleAvatarError"
                />
              </template>
              <div
                v-else
                class="w-full h-full bg-gradient-to-br from-secondary to-blue-500 dark:from-dark-secondary dark:to-blue-700 text-primary dark:text-dark-primary flex items-center justify-center font-bold text-xl"
              >
                {{ user.username.charAt(0).toUpperCase() }}
              </div>
            </div>
          </router-link>
        </div>

        <!-- 用户信息 -->
        <div class="flex-grow">
          <router-link :to="`/user/${user.id}`" class="block">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white hover:text-secondary dark:hover:text-dark-secondary transition-colors">
              {{ user.username }}
            </h3>
          </router-link>

          <div class="flex items-center mt-1">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 mr-2">
              {{ getRoleName(user.role) }}
            </span>
            <span class="text-sm text-gray-500 dark:text-gray-400">
              加入于 {{ formatDate(user.created_at) }}
            </span>
          </div>

          <p v-if="user.bio" class="mt-2 text-sm text-gray-600 dark:text-gray-300">
            {{ user.bio }}
          </p>
          <p v-else class="mt-2 text-sm text-gray-500 dark:text-gray-400 italic">
            该用户暂无个人简介
          </p>
        </div>

        <!-- 查看按钮 -->
        <div class="ml-4">
          <router-link
            :to="`/user/${user.id}`"
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary dark:bg-dark-secondary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-secondary dark:focus:ring-dark-secondary"
          >
            查看资料
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { format, parseISO } from 'date-fns'

export default {
  name: 'UserSearchResult',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  setup() {
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      try {
        return format(parseISO(dateString), 'yyyy-MM-dd')
      } catch (e) {
        console.error('日期格式化错误:', e)
        return dateString
      }
    }

    // 获取角色名称
    const getRoleName = (role) => {
      const roleMap = {
        'admin': '管理员',
        'editor': '编辑',
        'author': '作者',
        'user': '用户'
      }
      return roleMap[role] || '用户'
    }

    // 处理头像加载错误
    const handleAvatarError = (event) => {
      // 移除图片，显示默认头像
      const parent = event.target.parentNode
      if (parent) {
        parent.removeChild(event.target)
      }
    }

    return {
      formatDate,
      getRoleName,
      handleAvatarError
    }
  }
}
</script>

<style scoped>
/* 用户头像样式 */
.user-avatar {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.user-avatar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.user-avatar:hover::before {
  opacity: 1;
}

.user-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}

.user-avatar img {
  transition: transform 0.5s ease;
}

.user-avatar:hover img {
  transform: scale(1.15);
}

/* 搜索结果卡片样式 */
.user-search-result {
  transition: all 0.3s ease;
}

.user-search-result:hover {
  transform: translateY(-2px);
}
</style>
