import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores'
import { isAdmin, isSuperAdmin, isEditor } from '@/utils/permission'

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
const SiteSettingsManage = () => import('../views/admin/SiteSettingsManage.vue')
// 静态导入备忘录管理组件，避免动态导入问题
import MemoManage from '../views/admin/MemoManage.vue'
// 使用同步导入方式
import SubscriptionManage from '../views/admin/SubscriptionManage.vue'

// 导入 UI 组件
import { UnauthorizedAccess } from '../components/ui'
const UserProfile = () => import('../views/user/UserProfile.vue')
const ArticleDetail = () => import('../views/blog/ArticleDetail.vue')
const ArticleList = () => import('../views/blog/ArticleList.vue')
const CategoryList = () => import('../views/blog/CategoryList.vue')
const CategoryDetail = () => import('../views/blog/CategoryDetail.vue')
const TagList = () => import('../views/blog/TagList.vue')
const Search = () => import('../views/search/Search.vue')
const NotFound = () => import('../views/error/NotFound.vue')
const About = () => import('../views/about/About.vue')
const Unsubscribe = () => import('../views/blog/Unsubscribe.vue')
// 静态导入备忘录组件，避免动态导入问题
import MemoList from '../views/memo/MemoList.vue'
import MemoDetail from '../views/memo/MemoDetail.vue'
import MemoExplore from '../views/memo/MemoExplore.vue'
import MemoArchive from '../views/memo/MemoArchive.vue'

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
    path: '/categories/:id',
    name: 'CategoryDetail',
    component: CategoryDetail,
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
    path: '/unsubscribe',
    name: 'Unsubscribe',
    component: Unsubscribe,
    meta: { requiresAuth: false }
  },
  {
    path: '/memos',
    name: 'MemoList',
    component: MemoList,
    meta: { requiresAuth: false }
  },
  {
    path: '/memos/explore',
    name: 'MemoExplore',
    component: MemoExplore,
    meta: { requiresAuth: false }
  },
  {
    path: '/memos/archive',
    name: 'MemoArchive',
    component: MemoArchive,
    meta: { requiresAuth: false }
  },
  {
    path: '/memos/:id',
    name: 'MemoDetail',
    component: MemoDetail,
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
        component: Dashboard,
        meta: { requiresAuth: true, requiresAdmin: true } // 所有后台用户都可访问
      },
      {
        path: 'articles',
        name: 'ArticleManage',
        component: ArticleManage,
        meta: { requiresAuth: true, requiresAdmin: true, allowEditor: true } // 编辑可访问
      },
      {
        path: 'articles/edit',
        name: 'ArticleEdit',
        component: ArticleEdit,
        meta: { requiresAuth: true, requiresAdmin: true, allowEditor: true } // 编辑可访问
      },
      {
        path: 'categories',
        name: 'CategoryManage',
        component: CategoryManage,
        meta: { requiresAuth: true, requiresAdmin: true, allowEditor: true } // 编辑可访问
      },
      {
        path: 'tags',
        name: 'TagManage',
        component: TagManage,
        meta: { requiresAuth: true, requiresAdmin: true, allowEditor: true } // 编辑可访问
      },
      {
        path: 'users',
        name: 'UserManage',
        component: UserManage,
        meta: { requiresAuth: true, requiresSuperAdmin: true } // 只有超级管理员可访问
      },
      {
        path: 'comments',
        name: 'CommentManagement',
        component: CommentManagement,
        meta: { requiresAuth: true, requiresAdmin: true, allowEditor: true } // 编辑可访问
      },
      {
        path: 'activities',
        name: 'ActivityManage',
        component: ActivityManage,
        meta: { requiresAuth: true, requiresSuperAdmin: true } // 只有超级管理员可访问
      },
      {
        path: 'notifications',
        name: 'NotificationManage',
        component: NotificationManage,
        meta: { requiresAuth: true, requiresSuperAdmin: true } // 只有超级管理员可访问
      },
      {
        path: 'about',
        name: 'AboutManage',
        component: AboutManage,
        meta: { requiresAuth: true, requiresSuperAdmin: true } // 只有超级管理员可访问
      },
      {
        path: 'files',
        name: 'FileManager',
        component: FileManager,
        meta: {
          requiresAuth: true,
          requiresAdmin: true,
          allowEditor: true, // 编辑可访问
          title: '文件管理'
        }
      },
      {
        path: 'visitors',
        name: 'VisitorManagement',
        component: VisitorManagement,
        meta: {
          requiresAuth: true,
          requiresSuperAdmin: true, // 只有超级管理员可访问
          title: '访客记录'
        }
      },
      {
        path: 'settings',
        name: 'SiteSettingsManage',
        component: SiteSettingsManage,
        meta: {
          requiresAuth: true,
          requiresSuperAdmin: true, // 只有超级管理员可访问
          title: '系统设置'
        }
      },
      {
        path: 'subscriptions',
        name: 'SubscriptionManage',
        component: SubscriptionManage,
        meta: {
          requiresAuth: true,
          requiresSuperAdmin: true, // 只有超级管理员可访问
          title: '订阅管理'
        }
      },
      {
        path: 'memos',
        name: 'MemoManage',
        component: MemoManage,
        meta: {
          requiresAuth: true,
          requiresAdmin: true,
          allowEditor: true, // 编辑可访问
          title: '备忘录管理'
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
            // 检查权限
            if (!checkRoutePermission(to, userStore.userInfo)) {
              // 权限不足，重定向到未授权页面
              next({ path: '/unauthorized' })
              return
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
        // 已登录，检查权限
        if (!checkRoutePermission(to, userStore.userInfo)) {
          // 权限不足，重定向到未授权页面
          next({ path: '/unauthorized' })
          return
        }
      }
    }

    next()
  } catch (error) {
    console.error('路由守卫错误:', error)
    next('/login')
  }
})

/**
 * 检查用户是否有权限访问路由
 * @param {Route} route - 路由对象
 * @param {Object} userInfo - 用户信息
 * @returns {boolean} 是否有权限
 */
function checkRoutePermission(route, userInfo) {
  // 检查路由是否需要超级管理员权限
  if (route.matched.some(record => record.meta.requiresSuperAdmin)) {
    return isSuperAdmin(userInfo)
  }

  // 检查路由是否需要管理员权限
  if (route.matched.some(record => record.meta.requiresAdmin)) {
    // 如果是超级管理员，直接允许访问
    if (isSuperAdmin(userInfo)) {
      return true
    }

    // 检查是否允许编辑访问
    const allowEditor = route.matched.some(record => record.meta.allowEditor)
    if (allowEditor && isEditor(userInfo)) {
      return true
    }

    // 其他情况，需要管理员权限
    return isAdmin(userInfo)
  }

  return true
}

export default router
