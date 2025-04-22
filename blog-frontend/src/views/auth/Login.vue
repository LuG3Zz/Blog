<template>
  <div class="min-h-screen flex items-center justify-center bg-primary dark:bg-dark-primary">
    <div class="wrapper">
      <label class="switch">
        <input type="checkbox" class="toggle" v-model="isSignup">
        <span class="slider"></span>
        <span class="card-side"></span>
        <div class="flip-card__inner">
          <!-- 登录表单 -->
          <div class="flip-card__front">
            <div class="title">登录</div>
            <form class="flip-card__form" @submit.prevent="handleLogin">
              <input
                class="flip-card__input"
                v-model="username"
                placeholder="用户名"
                :class="{ 'border-red-500': usernameError }"
              />
              <p v-if="usernameError" class="text-red-500 text-xs">{{ usernameError }}</p>

              <input
                class="flip-card__input"
                type="password"
                v-model="password"
                placeholder="密码"
                :class="{ 'border-red-500': passwordError }"
              />
              <p v-if="passwordError" class="text-red-500 text-xs">{{ passwordError }}</p>

              <div class="flex items-center w-full">
                <input
                  type="checkbox"
                  id="remember"
                  v-model="remember"
                  class="h-4 w-4 text-secondary dark:text-dark-secondary"
                />
                <label for="remember" class="ml-2 text-sm">记住我</label>
              </div>

              <button
                class="flip-card__btn"
                :disabled="isLoading"
                :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
              >
                {{ isLoading ? '登录中...' : '立即登录' }}
              </button>
            </form>
          </div>

          <!-- 注册表单 -->
          <div class="flip-card__back">
            <div class="title">注册</div>
            <form class="flip-card__form" @submit.prevent="handleSignup">
              <input
                class="flip-card__input"
                v-model="signupForm.username"
                placeholder="用户名"
                :class="{ 'border-red-500': signupErrors.username }"
              />
              <p v-if="signupErrors.username" class="text-red-500 text-xs">{{ signupErrors.username }}</p>

              <input
                class="flip-card__input"
                type="email"
                v-model="signupForm.email"
                placeholder="邮箱"
                :class="{ 'border-red-500': signupErrors.email }"
              />
              <p v-if="signupErrors.email" class="text-red-500 text-xs">{{ signupErrors.email }}</p>

              <input
                class="flip-card__input"
                type="password"
                v-model="signupForm.password"
                placeholder="密码"
                :class="{ 'border-red-500': signupErrors.password }"
              />
              <p v-if="signupErrors.password" class="text-red-500 text-xs">{{ signupErrors.password }}</p>

              <input
                class="flip-card__input"
                type="password"
                v-model="signupForm.confirmPassword"
                placeholder="确认密码"
                :class="{ 'border-red-500': signupErrors.confirmPassword }"
              />
              <p v-if="signupErrors.confirmPassword" class="text-red-500 text-xs">{{ signupErrors.confirmPassword }}</p>

              <button
                class="flip-card__btn"
                :disabled="isLoading"
                :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
              >
                {{ isLoading ? '注册中...' : '立即注册' }}
              </button>
            </form>
          </div>
        </div>
      </label>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '@/api'
import message from '@/utils/message'
import { userStore } from '@/store'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const isSignup = ref(false)
    const isLoading = ref(false)

    // 登录表单数据
    const username = ref('')
    const password = ref('')
    const remember = ref(false)
    const usernameError = ref('')
    const passwordError = ref('')

    // 注册表单数据
    const signupForm = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    const signupErrors = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    // 登录处理
    const handleLogin = async () => {
      // 重置错误信息
      usernameError.value = ''
      passwordError.value = ''

      // 表单验证
      let isValid = true
      if (!username.value) {
        usernameError.value = '请输入用户名'
        isValid = false
      }
      if (!password.value) {
        passwordError.value = '请输入密码'
        isValid = false
      }

      if (!isValid) return

      isLoading.value = true
      try {
        console.log('开始登录请求');
        // 使用状态管理模块的登录方法
        const response = await userStore.login({
          username: username.value,
          password: password.value
        })

        console.log('登录成功，响应数据:', response);

        // 确保登录状态已设置
        if (!userStore.state.isLoggedIn) {
          console.warn('登录成功但状态未更新，手动设置登录状态');
          // 手动设置登录状态
          await userStore.checkLoginStatus();
        }

        // 如果选择了记住我，保存用户名
        if (remember.value) {
          localStorage.setItem('username', username.value)
        } else {
          localStorage.removeItem('username')
        }

        message.success('登录成功')

        // 检查是否有重定向参数
        const redirectPath = router.currentRoute.value.query.redirect || '/admin'
        // 跳转到重定向路径或后台管理页面
        router.push(redirectPath)
      } catch (error) {
        console.error('登录失败:', error)
        message.error('登录失败: ' + (error.response?.data?.message || '用户名或密码错误'))
      } finally {
        isLoading.value = false
      }
    }

    // 注册处理
    const handleSignup = async () => {
      // 重置错误信息
      Object.keys(signupErrors).forEach(key => {
        signupErrors[key] = ''
      })

      // 表单验证
      let isValid = true
      if (!signupForm.username) {
        signupErrors.username = '请输入用户名'
        isValid = false
      }
      if (!signupForm.email) {
        signupErrors.email = '请输入邮箱'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(signupForm.email)) {
        signupErrors.email = '请输入有效的邮箱地址'
        isValid = false
      }
      if (!signupForm.password) {
        signupErrors.password = '请输入密码'
        isValid = false
      } else if (signupForm.password.length < 6) {
        signupErrors.password = '密码长度不能少于6个字符'
        isValid = false
      }
      if (!signupForm.confirmPassword) {
        signupErrors.confirmPassword = '请确认密码'
        isValid = false
      } else if (signupForm.password !== signupForm.confirmPassword) {
        signupErrors.confirmPassword = '两次输入的密码不一致'
        isValid = false
      }

      if (!isValid) return

      isLoading.value = true
      try {
        await userApi.register({
          username: signupForm.username,
          email: signupForm.email,
          password: signupForm.password
        })

        message.success('注册成功，请登录')

        // 切换到登录表单
        isSignup.value = false

        // 预填充用户名
        username.value = signupForm.username
      } catch (error) {
        console.error('注册失败:', error)
        message.error('注册失败: ' + (error.response?.data?.message || '注册失败，请稍后再试'))
      } finally {
        isLoading.value = false
      }
    }

    return {
      isSignup,
      isLoading,
      username,
      password,
      remember,
      usernameError,
      passwordError,
      signupForm,
      signupErrors,
      handleLogin,
      handleSignup
    }
  }
}
</script>

<style scoped>
.wrapper {
  --font-color: #323232;
  --font-color-sub: #666;
  --bg-color: #fff;
  --main-color: #323232;
  width: 400px;
  margin: 0 auto;
}

.switch {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 30px;
  width: 400px;
  height: 500px;
}

.card-side {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 60px;
  margin-top: -30px;
  z-index: 5;
}

.card-side::before {
  position: absolute;
  content: '登录';
  left: 30%;
  top: -30px;
  width: 60px;
  text-decoration: underline;
  color: var(--font-color);
  font-weight: 600;
  font-size: 16px;
  text-align: center;
  transform: translateX(-50%);
  z-index: 5;
}

.card-side::after {
  position: absolute;
  content: '注册';
  right: 30%;
  top: -30px;
  width: 60px;
  text-decoration: none;
  color: var(--font-color);
  font-weight: 600;
  font-size: 16px;
  text-align: center;
  transform: translateX(50%);
  z-index: 5;
}

.toggle {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  box-sizing: border-box;
  border-radius: 5px;
  border: 2px solid var(--main-color);
  box-shadow: 4px 4px var(--main-color);
  position: absolute;
  cursor: pointer;
  top: -40px;
  left: 50%;
  transform: translateX(-25px);
  width: 50px;
  height: 20px;
  background-color: var(--bg-color);
  transition: all 0.3s ease;
  z-index: 10;
}

.slider:before {
  box-sizing: border-box;
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  border: 2px solid var(--main-color);
  border-radius: 5px;
  left: 2px;
  bottom: 0px;
  background-color: var(--bg-color);
  box-shadow: 2px 2px var(--main-color);
  transition: 0.3s;
}

.toggle:checked + .slider {
  background-color: var(--bg-color);
  transform: translateX(-25px);
}

.toggle:checked + .slider:before {
  transform: translateX(30px);
}

.toggle:checked ~ .card-side::before {
  text-decoration: none;
  color: var(--font-color);
  font-weight: 600;
}

.toggle:checked ~ .card-side::after {
  text-decoration: underline;
}

.toggle:checked ~ .flip-card__inner {
  transform: rotateY(180deg);
}

.flip-card__inner {
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
  position: relative;
}

.flip-card__front, .flip-card__back {
  padding: 30px;
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 10px;
  border: 2px solid var(--main-color);
  box-shadow: 4px 4px var(--main-color);
  top: 0;
  left: 0;
}

.flip-card__front {
  background-color: var(--bg-color);
  transform: rotateY(0deg);
}

.flip-card__back {
  background-color: var(--bg-color);
  transform: rotateY(180deg);
}

.title {
  margin: 0 0 20px 0;
  font-size: 28px;
  font-weight: 900;
  text-align: center;
  color: var(--font-color);
}

.flip-card__form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  width: 100%;
}

.flip-card__input {
  margin: 5px 0;
  width: 100%;
  height: 40px;
  border-radius: 8px;
  border: 2px solid var(--main-color);
  background-color: var(--bg-color);
  box-shadow: 3px 3px var(--main-color);
  font-size: 15px;
  color: var(--font-color);
  padding: 5px 15px;
  outline: none;
  transition: all 0.3s ease;
}

.flip-card__input:focus {
  border: 2px solid #4f46e5;
  box-shadow: 3px 3px #4f46e5;
}

.flip-card__btn {
  margin: 20px 0 10px 0;
  width: 100%;
  height: 45px;
  border-radius: 8px;
  border: 2px solid var(--main-color);
  background-color: #4f46e5;
  box-shadow: 3px 3px var(--main-color);
  font-size: 17px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.flip-card__btn:hover {
  background-color: #4338ca;
  transform: translateY(-2px);
}

.flip-card__btn:active {
  transform: translateY(0);
  box-shadow: 2px 2px var(--main-color);
}

/* 暗黑模式适配 */
.dark .wrapper {
  --font-color: #e2e8f0;
  --font-color-sub: #94a3b8;
  --bg-color: #1e293b;
  --main-color: #cbd5e1;
}

.dark .flip-card__input {
  background-color: #334155;
  color: #e2e8f0;
}

.dark .flip-card__btn {
  background-color: #6366f1;
  color: #e2e8f0;
}

.dark .flip-card__btn:hover {
  background-color: #4f46e5;
}

.dark .slider {
  background-color: #334155;
}

.dark .slider:before {
  background-color: #1e293b;
}

/* 响应式调整 */
@media (max-width: 640px) {
  .wrapper {
    width: 90%;
    max-width: 360px;
  }

  .switch {
    width: 100%;
    height: 480px;
  }

  .card-side {
    padding: 0 40px;
  }

  .card-side::before {
    left: 25%;
  }

  .card-side::after {
    right: 25%;
  }
}
</style>
