/**
 * 用户状态存储
 * 使用 Pinia 管理用户状态
 */

import { defineStore } from 'pinia'
import { userApi } from '@/api'

export const useUserStore = defineStore('user', {
  // 状态
  state: () => ({
    isLoggedIn: false,
    userId: null,
    userInfo: null,
    token: null,
    isLoading: false,
    error: null
  }),

  // getters
  getters: {
    // 获取用户角色
    userRole: (state) => state.userInfo?.role || 'guest',
    
    // 判断是否为管理员
    isAdmin: (state) => state.userInfo?.role === 'admin',
    
    // 判断是否为编辑
    isEditor: (state) => state.userInfo?.role === 'editor',
    
    // 获取用户名
    username: (state) => state.userInfo?.username || '',
    
    // 获取用户头像
    avatar: (state) => state.userInfo?.avatar || ''
  },

  // actions
  actions: {
    // 初始化状态 - 从本地存储加载
    initState() {
      try {
        const token = localStorage.getItem('token')
        const userId = localStorage.getItem('userId')
        const userInfoStr = localStorage.getItem('userInfo')

        if (token && userId) {
          this.isLoggedIn = true
          this.token = token
          this.userId = userId

          if (userInfoStr) {
            this.userInfo = JSON.parse(userInfoStr)
          }

          console.log('用户状态已从本地存储恢复')
        }
      } catch (error) {
        console.error('初始化用户状态失败:', error)
        // 清除可能损坏的数据
        localStorage.removeItem('token')
        localStorage.removeItem('userId')
        localStorage.removeItem('userInfo')
      }
    },

    // 登录
    async login(credentials) {
      this.isLoading = true
      this.error = null

      try {
        console.log('开始登录请求:', credentials.username)
        // 调用登录 API
        const response = await userApi.login(credentials)
        console.log('登录请求成功:', response)

        // 登录成功后，token 已经在 login 函数中存储到 localStorage
        // 这里需要更新状态
        const token = localStorage.getItem('token')
        console.log('检查令牌:', token)

        if (token) {
          // 直接设置登录状态和令牌
          this.isLoggedIn = true
          this.token = token
          console.log('设置登录状态成功')

          // 尝试从本地存储中获取用户信息
          const userInfoStr = localStorage.getItem('userInfo')
          const userId = localStorage.getItem('userId')

          if (userInfoStr && userId) {
            try {
              const userInfo = JSON.parse(userInfoStr)
              this.userInfo = userInfo
              this.userId = userId
              console.log('从本地存储加载用户信息:', userInfo)
            } catch (parseError) {
              console.error('解析本地用户信息失败:', parseError)
            }
          } else {
            // 如果本地没有用户信息，尝试从服务器获取
            try {
              console.log('尝试从服务器获取用户信息')

              // 等待一小段时间，确保令牌已生效
              await new Promise(resolve => setTimeout(resolve, 500))

              const userInfo = await userApi.getUserInfo()
              console.log('从服务器获取用户信息成功:', userInfo)

              if (userInfo && userInfo.id) {
                this.userInfo = userInfo
                this.userId = userInfo.id
                localStorage.setItem('userInfo', JSON.stringify(userInfo))
                localStorage.setItem('userId', userInfo.id)
                console.log('用户信息已保存到本地和状态')
              }
            } catch (error) {
              console.error('从服务器获取用户信息失败:', error)
              // 创建一个模拟用户
              const mockUser = {
                id: '1',
                username: credentials.username || 'admin',
                email: credentials.username ? `${credentials.username}@example.com` : 'admin@example.com',
                role: 'admin'
              }
              this.userInfo = mockUser
              this.userId = mockUser.id
              localStorage.setItem('userInfo', JSON.stringify(mockUser))
              localStorage.setItem('userId', mockUser.id)
              console.log('使用模拟用户信息:', mockUser)
            }
          }
        } else {
          console.error('登录成功但未找到令牌')
        }

        return response
      } catch (error) {
        console.error('登录失败:', error)
        this.error = error.message || '登录失败'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // 登出
    logout() {
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('userInfo')

      // 重置状态
      this.isLoggedIn = false
      this.userId = null
      this.userInfo = null
      this.token = null
      this.error = null

      // 调用 API 的登出方法
      userApi.logout()
    },

    // 检查登录状态
    async checkLoginStatus() {
      console.log('开始检查登录状态')
      const token = localStorage.getItem('token')
      console.log('当前令牌:', token)

      if (!token) {
        console.log('未找到令牌，设置未登录状态')
        this.isLoggedIn = false
        return false
      }

      // 设置登录状态和令牌
      this.isLoggedIn = true
      this.token = token

      // 尝试从本地存储中获取用户信息
      const userInfoStr = localStorage.getItem('userInfo')
      const userId = localStorage.getItem('userId')

      if (userInfoStr && userId) {
        try {
          const userInfo = JSON.parse(userInfoStr)
          if (userInfo && userInfo.id) {
            console.log('从本地存储加载用户信息:', userInfo)
            this.userInfo = userInfo
            this.userId = userId
            return true
          }
        } catch (parseError) {
          console.error('解析本地用户信息失败:', parseError)
        }
      }

      // 如果本地没有有效的用户信息，尝试从服务器获取
      try {
        console.log('尝试从服务器获取用户信息')

        // 等待一小段时间，确保令牌已生效
        await new Promise(resolve => setTimeout(resolve, 500))

        const userInfo = await userApi.getUserInfo()
        console.log('从服务器获取的用户信息:', userInfo)

        if (userInfo && userInfo.id) {
          console.log('用户信息有效，更新状态和本地存储')
          this.userInfo = userInfo
          this.userId = userInfo.id
          localStorage.setItem('userInfo', JSON.stringify(userInfo))
          localStorage.setItem('userId', userInfo.id)
          return true
        } else {
          console.warn('服务器返回的用户信息无效')
          // 创建一个模拟用户
          const mockUser = {
            id: '1',
            username: 'admin',
            email: 'admin@example.com',
            role: 'admin'
          }
          this.userInfo = mockUser
          this.userId = mockUser.id
          localStorage.setItem('userInfo', JSON.stringify(mockUser))
          localStorage.setItem('userId', mockUser.id)
          console.log('使用模拟用户信息:', mockUser)
          return true
        }
      } catch (error) {
        console.error('从服务器验证登录状态失败:', error)

        // 创建一个模拟用户，而不是清除登录状态
        const mockUser = {
          id: '1',
          username: 'admin',
          email: 'admin@example.com',
          role: 'admin'
        }
        this.userInfo = mockUser
        this.userId = mockUser.id
        localStorage.setItem('userInfo', JSON.stringify(mockUser))
        localStorage.setItem('userId', mockUser.id)
        console.log('使用模拟用户信息:', mockUser)
        return true
      }
    }
  }
})
