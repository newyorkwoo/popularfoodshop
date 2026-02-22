import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress'
import { useAdminAuthStore } from '@/stores/auth'

const routes = [
  // ===== Admin Login =====
  {
    path: '/login',
    name: 'AdminLogin',
    component: () => import('@/pages/Login.vue'),
    meta: { title: '管理員登入', guestOnly: true },
  },

  // ===== Admin Panel =====
  {
    path: '/',
    component: () => import('@/components/layout/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/pages/Dashboard.vue'),
        meta: { title: '儀表板' },
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/pages/Products.vue'),
        meta: { title: '商品管理' },
      },
      {
        path: 'products/create',
        name: 'ProductCreate',
        component: () => import('@/pages/ProductCreate.vue'),
        meta: { title: '新增商品' },
      },
      {
        path: 'products/:id/edit',
        name: 'ProductEdit',
        component: () => import('@/pages/ProductEdit.vue'),
        meta: { title: '編輯商品' },
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/pages/Categories.vue'),
        meta: { title: '分類管理' },
      },
      {
        path: 'brands',
        name: 'Brands',
        component: () => import('@/pages/Brands.vue'),
        meta: { title: '品牌管理' },
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/pages/Orders.vue'),
        meta: { title: '訂單管理' },
      },
      {
        path: 'orders/:id',
        name: 'OrderDetail',
        component: () => import('@/pages/OrderDetail.vue'),
        meta: { title: '訂單詳情' },
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/pages/Users.vue'),
        meta: { title: '會員管理' },
      },
      {
        path: 'promotions',
        name: 'Promotions',
        component: () => import('@/pages/Promotions.vue'),
        meta: { title: '促銷管理' },
      },
      {
        path: 'content',
        name: 'Content',
        component: () => import('@/pages/Content.vue'),
        meta: { title: '內容管理' },
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/pages/Reports.vue'),
        meta: { title: '報表分析' },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/pages/Settings.vue'),
        meta: { title: '系統設定' },
      },
    ],
  },

  // ===== 404 =====
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// NProgress
NProgress.configure({ showSpinner: false, speed: 300, minimum: 0.2 })

// Navigation guard
router.beforeEach(async (to, from, next) => {
  if (to.path !== from.path) NProgress.start()

  const baseTitle = '管理後台 | Popular Food Shop'
  document.title = to.meta.title ? `${to.meta.title} - ${baseTitle}` : baseTitle

  const authStore = useAdminAuthStore()

  // Load user if token exists but user not loaded
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser()
  }

  const isAuthenticated = authStore.isAuthenticated

  // Require auth
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
    return
  }

  // Guest only (login page)
  if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }

  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
