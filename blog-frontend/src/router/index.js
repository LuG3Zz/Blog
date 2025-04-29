import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores'
import { isAdmin } from '@/utils/permission'

// 使用懒加载方式导入视图组件
const Home = () => import('../views/layout/Home.vue')
const Login = () => import('../views/auth/Login.vue')
const Admin = () => import('../views/admin/Admin.vue')
const Dashboard = () => import('../views/admin/Dashboard.vue')
const ArticleManage = () => import('../views/admin/ArticleManage.vue')
const ArticleEdit = () => import('../views/admin/ArticleEdit.vue')
const CategoryManage = () => import('../views/admin/CategoryManage.vue')
const TagManage = () => import('../views/admin/TagManage.vue')
const UserManage = () => import('../views/admin/UserManage.vue')
const CommentManagement = () => import('../views/admin/CommentManagement.vue')
const ActivityManage = () => import('../views/admin/ActivityManage.vue')
const NotificationManage = () => import('../views/admin/NotificationManage.vue')
const AboutManage = () => import('../views/admin/AboutManage.vue')
const FileManager = () => import('../views/admin/FileManager.vue')
const VisitorManagement = () => import('../views/admin/VisitorManagement.vue')

// 导入 UI 组件
import { UnauthorizedAccess } from '../components/ui'
const UserProfile = () => import('../views/user/UserProfile.vue')
const ArticleDetail = () => import('../views/blog/ArticleDetail.vue')
const ArticleList = () => import('../views/blog/ArticleList.vue')
const CategoryList = () => import('../views/blog/CategoryList.vue')
const TagList = () => import('../views/blog/TagList.vue')
const Search = () => import('../views/search/Search.vue')
const NotFound = () => import('../views/error/NotFound.vue')
const About = () => import('../views/about/About.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },

  {
    path: '/articles',
    name: 'ArticleList',
    component: ArticleList,
    meta: { requiresAuth: false }
  },
  {
    path: '/categories',
    name: 'CategoryList',
    component: CategoryList,
    meta: { requiresAuth: false }
  },
  {
    path: '/tags/:id',
    name: 'TagList',
    component: TagList,
    meta: { requiresAuth: false }
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetail,
    meta: { requiresAuth: false }
  },
  {
    path: '/search',
    name: 'Search',
    component: Search,
    meta: { requiresAuth: false }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: UnauthorizedAccess,
    meta: { requiresAuth: false }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'articles',
        name: 'ArticleManage',
        component: ArticleManage
      },
      {
        path: 'articles/edit',
        name: 'ArticleEdit',
        component: ArticleEdit
      },
      {
        path: 'categories',
        name: 'CategoryManage',
        component: CategoryManage
      },
      {
        path: 'tags',
        name: 'TagManage',
        component: TagManage
      },
      {
        path: 'users',
        name: 'UserManage',
        component: UserManage
      },
      {
        path: 'comments',
        name: 'CommentManagement',
        component: CommentManagement
      },
      {
        path: 'activities',
        name: 'ActivityManage',
        component: ActivityManage
      },
      {
        path: 'notifications',
        name: 'NotificationManage',
        component: NotificationManage
      },
      {
        path: 'about',
        name: 'AboutManage',
        component: AboutManage
      },
      {
        path: 'files',
        name: 'FileManager',
        component: FileManager,
        meta: {
          requiresAuth: true,
          title: '文件管理'
        }
      },
      {
        path: 'visitors',
        name: 'VisitorManagement',
        component: VisitorManagement,
        meta: {
          requiresAuth: true,
          title: '访客记录'
        }
      }
    ]
  },
  {
    path: '/user/:id',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局路由守卫
router.beforeEach(async (to, from, next) => {
  try {
    // 使用Pinia状态管理
    const userStore = useUserStore()

    // 使用状态管理模块检查登录状态
    const isLoggedIn = userStore.isLoggedIn

    // 如果访问登录页且已登录，重定向到首页
    if (to.path === '/login' && isLoggedIn) {
      next('/')
      return
    }

    // 检查路由是否需要认证
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!isLoggedIn) {
        // 如果本地有 token 但状态不是登录状态，尝试验证 token
        if (localStorage.getItem('token')) {
          const validToken = await userStore.checkLoginStatus()
          if (validToken) {
            // 检查是否需要管理员权限
            if (to.matched.some(record => record.meta.requiresAdmin)) {
              if (!isAdmin(userStore.userInfo)) {
                // 非管理员访问管理页面，重定向到未授权页面
                next({ path: '/unauthorized' })
                return
              }
            }
            next()
            return
          }
        }

        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
        return
      } else {
        // 已登录，检查是否需要管理员权限
        if (to.matched.some(record => record.meta.requiresAdmin)) {
          if (!isAdmin(userStore.userInfo)) {
            // 非管理员访问管理页面，重定向到未授权页面
            next({ path: '/unauthorized' })
            return
          }
        }
      }
    }

    next()
  } catch (error) {
    console.error('路由守卫错误:', error)
    next('/login')
  }
})

export default router
