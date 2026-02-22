import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress'

const routes = [
  // ===== Public Pages =====
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/pages/Home.vue'),
        meta: { title: '首頁' },
      },
      {
        path: 'category/:slug',
        name: 'ProductList',
        component: () => import('@/pages/ProductList.vue'),
        meta: { title: '商品列表' },
      },
      {
        path: 'product/:slug',
        name: 'ProductDetail',
        component: () => import('@/pages/ProductDetail.vue'),
        meta: { title: '商品詳情' },
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('@/pages/Search.vue'),
        meta: { title: '搜尋結果' },
      },
      {
        path: 'brands',
        name: 'Brands',
        component: () => import('@/pages/Brands.vue'),
        meta: { title: '品牌列表' },
      },
      {
        path: 'brand/:slug',
        name: 'BrandDetail',
        component: () => import('@/pages/BrandDetail.vue'),
        meta: { title: '品牌專頁' },
      },
      {
        path: 'cart',
        name: 'Cart',
        component: () => import('@/pages/Cart.vue'),
        meta: { title: '購物車' },
      },
      {
        path: 'checkout',
        name: 'Checkout',
        component: () => import('@/pages/Checkout.vue'),
        meta: { title: '結帳', requiresAuth: true },
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('@/pages/About.vue'),
        meta: { title: '關於我們' },
      },
      {
        path: 'contact',
        name: 'Contact',
        component: () => import('@/pages/Contact.vue'),
        meta: { title: '聯絡我們' },
      },
      {
        path: 'faq',
        name: 'FAQ',
        component: () => import('@/pages/FAQ.vue'),
        meta: { title: '常見問題' },
      },
      {
        path: 'terms',
        name: 'Terms',
        component: () => import('@/pages/Terms.vue'),
        meta: { title: '服務條款' },
      },
      {
        path: 'privacy',
        name: 'Privacy',
        component: () => import('@/pages/Privacy.vue'),
        meta: { title: '隱私政策' },
      },
      {
        path: 'shipping',
        name: 'Shipping',
        component: () => import('@/pages/Shipping.vue'),
        meta: { title: '運送資訊' },
      },
      {
        path: 'returns',
        name: 'Returns',
        component: () => import('@/pages/ReturnsPolicy.vue'),
        meta: { title: '退換貨說明' },
      },
    ],
  },

  // ===== Auth Pages =====
  {
    path: '/login',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        name: 'Login',
        component: () => import('@/pages/auth/Login.vue'),
        meta: { title: '登入', guestOnly: true },
      },
    ],
  },
  {
    path: '/register',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        name: 'Register',
        component: () => import('@/pages/auth/Register.vue'),
        meta: { title: '註冊', guestOnly: true },
      },
    ],
  },
  {
    path: '/forgot-password',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        name: 'ForgotPassword',
        component: () => import('@/pages/auth/ForgotPassword.vue'),
        meta: { title: '忘記密碼', guestOnly: true },
      },
    ],
  },
  {
    path: '/reset-password',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        name: 'ResetPassword',
        component: () => import('@/pages/auth/ResetPassword.vue'),
        meta: { title: '重設密碼', guestOnly: true },
      },
    ],
  },

  // ===== Account Pages =====
  {
    path: '/account',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/account/profile',
      },
      {
        path: 'profile',
        name: 'AccountProfile',
        component: () => import('@/pages/account/Profile.vue'),
        meta: { title: '個人資料' },
      },
      {
        path: 'addresses',
        name: 'AccountAddresses',
        component: () => import('@/pages/account/Addresses.vue'),
        meta: { title: '我的地址' },
      },
      {
        path: 'orders',
        name: 'AccountOrders',
        component: () => import('@/pages/account/Orders.vue'),
        meta: { title: '訂單紀錄' },
      },
      {
        path: 'orders/:id',
        name: 'AccountOrderDetail',
        component: () => import('@/pages/account/OrderDetail.vue'),
        meta: { title: '訂單詳情' },
      },
      {
        path: 'returns',
        name: 'AccountReturns',
        component: () => import('@/pages/account/Returns.vue'),
        meta: { title: '退貨紀錄' },
      },
      {
        path: 'wishlist',
        name: 'AccountWishlist',
        component: () => import('@/pages/account/Wishlist.vue'),
        meta: { title: '願望清單' },
      },
      {
        path: 'points',
        name: 'AccountPoints',
        component: () => import('@/pages/account/Points.vue'),
        meta: { title: '回饋金' },
      },
      {
        path: 'credits',
        name: 'AccountCredits',
        component: () => import('@/pages/account/Credits.vue'),
        meta: { title: '購物金' },
      },
      {
        path: 'cards',
        name: 'AccountCards',
        component: () => import('@/pages/account/Cards.vue'),
        meta: { title: '我的信用卡' },
      },
    ],
  },

  // ===== Admin Pages =====
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/pages/admin/Dashboard.vue'),
        meta: { title: '管理儀表板' },
      },
      {
        path: 'products',
        name: 'AdminProducts',
        component: () => import('@/pages/admin/Products.vue'),
        meta: { title: '商品管理' },
      },
      {
        path: 'products/create',
        name: 'AdminProductCreate',
        component: () => import('@/pages/admin/ProductCreate.vue'),
        meta: { title: '新增商品' },
      },
      {
        path: 'products/:id/edit',
        name: 'AdminProductEdit',
        component: () => import('@/pages/admin/ProductEdit.vue'),
        meta: { title: '編輯商品' },
      },
      {
        path: 'categories',
        name: 'AdminCategories',
        component: () => import('@/pages/admin/Categories.vue'),
        meta: { title: '分類管理' },
      },
      {
        path: 'brands',
        name: 'AdminBrands',
        component: () => import('@/pages/admin/Brands.vue'),
        meta: { title: '品牌管理' },
      },
      {
        path: 'orders',
        name: 'AdminOrders',
        component: () => import('@/pages/admin/Orders.vue'),
        meta: { title: '訂單管理' },
      },
      {
        path: 'orders/:id',
        name: 'AdminOrderDetail',
        component: () => import('@/pages/admin/OrderDetail.vue'),
        meta: { title: '訂單詳情' },
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/pages/admin/Users.vue'),
        meta: { title: '會員管理' },
      },
      {
        path: 'promotions',
        name: 'AdminPromotions',
        component: () => import('@/pages/admin/Promotions.vue'),
        meta: { title: '促銷管理' },
      },
      {
        path: 'content',
        name: 'AdminContent',
        component: () => import('@/pages/admin/Content.vue'),
        meta: { title: '內容管理' },
      },
      {
        path: 'reports',
        name: 'AdminReports',
        component: () => import('@/pages/admin/Reports.vue'),
        meta: { title: '數據報表' },
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/pages/admin/Settings.vue'),
        meta: { title: '系統設定' },
      },
    ],
  },

  // ===== 404 =====
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFound.vue'),
    meta: { title: '頁面不存在' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    // Smooth scroll for anchor links
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0, behavior: 'smooth' }
  },
})

// NProgress configuration
NProgress.configure({ showSpinner: false, speed: 300, minimum: 0.2 })

// Navigation guards
router.beforeEach((to, from, next) => {
  // Only show progress bar for actual page changes
  if (to.path !== from.path) {
    NProgress.start()
  }

  // Set page title
  const baseTitle = 'Popular Food Shop'
  document.title = to.meta.title ? `${to.meta.title} | ${baseTitle}` : baseTitle

  // Auth check
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  if (to.meta.guestOnly && token && user) {
    next({ name: 'Home' })
    return
  }

  const adminRoles = ['admin', 'super_admin', 'superadmin', 'editor']
  if (to.meta.requiresAdmin && (!user || !adminRoles.includes(user.role))) {
    next({ name: 'Home' })
    return
  }

  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
