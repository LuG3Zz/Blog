<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6 dark:text-white">用户管理</h1>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold dark:text-gray-200">用户列表</h2>
        <button
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          @click="showAddModal = true"
        >
          添加用户
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">用户信息</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">角色</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">邮箱</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">注册时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="user in users" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ user.id }}</td>

              <!-- 用户信息列 -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 border-2 border-white dark:border-gray-600 shadow-sm hover:shadow-md transition-all duration-300 hover:scale-110">
                    <img v-if="user.avatar" :src="user.avatar" alt="用户头像" class="h-10 w-10 object-cover" />
                    <div v-else class="h-10 w-10 flex items-center justify-center bg-gradient-to-br from-blue-400 to-purple-500 dark:from-blue-600 dark:to-purple-700">
                      <span class="text-sm font-bold text-white">{{ user.username.charAt(0).toUpperCase() }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ user.username }}</div>
                    <div v-if="user.bio" class="text-xs text-gray-500 dark:text-gray-400 truncate max-w-xs">{{ user.bio }}</div>
                  </div>
                </div>
              </td>

              <!-- 角色列 -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="{
                    'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': user.role === 'admin',
                    'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200': user.role === 'editor',
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': user.role === 'user',
                    'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300': !user.role
                  }"
                >
                  {{ getRoleName(user.role) }}
                </span>
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ user.email }}</td>

              <!-- 注册时间列 -->
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ formatDate(user.created_at) }}
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                <button
                  class="text-blue-500 hover:text-blue-700 mr-3"
                  @click="editUser(user)"
                >
                  编辑
                </button>
                <button
                  class="text-green-500 hover:text-green-700 mr-3"
                  @click="viewProfile(user.id)"
                >
                  查看资料
                </button>
                <button
                  class="text-red-500 hover:text-red-700"
                  @click="deleteUser(user.id)"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加/编辑用户模态框 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAddModal = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4 dark:text-white">{{ isEditing ? '编辑用户' : '添加用户' }}</h3>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">用户名</label>
          <input
            v-model="currentUser.username"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="输入用户名"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">邮箱</label>
          <input
            v-model="currentUser.email"
            type="email"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="输入邮箱"
          />
        </div>

        <div class="flex justify-end space-x-3">
          <button
            class="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors"
            @click="showAddModal = false"
          >
            取消
          </button>
          <button
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            @click="saveUser"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import { useRouter } from 'vue-router'

export default {
  name: 'UserManage',
  setup() {
    const router = useRouter()
    const users = ref([])
    const showAddModal = ref(false)
    const isEditing = ref(false)
    const currentUser = ref({ id: null, username: '', email: '' })

    // 获取用户列表
    const fetchUsers = async () => {
      try {
        users.value = await adminApi.getUsers()
      } catch (error) {
        console.error('获取用户列表失败:', error)
      }
    }

    // 初始化数据
    onMounted(() => {
      fetchUsers()
    })

    const editUser = (user) => {
      currentUser.value = { ...user }
      isEditing.value = true
      showAddModal.value = true
    }

    const deleteUser = async (id) => {
      try {
        await adminApi.deleteUser(id)
        // 更新本地列表
        users.value = users.value.filter(u => u.id !== id)
      } catch (error) {
        console.error('删除用户失败:', error)
      }
    }

    const saveUser = async () => {
      try {
        if (isEditing.value) {
          // 更新用户
          const updatedUser = await adminApi.updateUser(currentUser.value.id, {
            username: currentUser.value.username,
            email: currentUser.value.email
          })

          // 更新本地列表
          const index = users.value.findIndex(u => u.id === currentUser.value.id)
          if (index !== -1) {
            users.value[index] = updatedUser
          }
        } else {
          // 创建新用户
          const newUser = await adminApi.createUser({
            username: currentUser.value.username,
            email: currentUser.value.email
          })

          // 添加到本地列表
          users.value.push(newUser)
        }

        showAddModal.value = false
        currentUser.value = { id: null, username: '', email: '' }
        isEditing.value = false
      } catch (error) {
        console.error('保存用户失败:', error)
      }
    }

    // 查看用户资料
    const viewProfile = (userId) => {
      router.push(`/user/${userId}`)
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      try {
        return new Date(dateString).toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
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
      return roleMap[role] || '普通用户'
    }

    return {
      users,
      showAddModal,
      isEditing,
      currentUser,
      editUser,
      deleteUser,
      saveUser,
      viewProfile,
      formatDate,
      getRoleName
    }
  }
}
</script>

<style scoped>
/* 用户头像样式 */
.rounded-full {
  position: relative;
  z-index: 10;
}

.rounded-full:hover {
  z-index: 20;
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
}

/* 表格行悬停效果 */
tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  background-color: rgba(243, 244, 246, 0.5);
}

.dark tbody tr:hover {
  background-color: rgba(55, 65, 81, 0.5);
}
</style>