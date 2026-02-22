import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'

// Dev-mode mock accounts (admin roles only)
const MOCK_ADMIN_ACCOUNTS = [
  {
    email: 'admin@popularfoodshop.com',
    password: 'Admin@123456',
    user: { id: 1, email: 'admin@popularfoodshop.com', firstName: '管理員', lastName: '系統', role: 'super_admin', phone: '' },
  },
  {
    email: 'editor@popularfoodshop.com',
    password: 'Editor@123456',
    user: { id: 2, email: 'editor@popularfoodshop.com', firstName: '編輯', lastName: '內容', role: 'editor', phone: '' },
  },
]

export const useAdminAuthStore = defineStore('adminAuth', () => {
  const router = useRouter()

  // State — uses admin-prefixed localStorage keys (isolated from consumer)
  const user = ref(null)
  const token = ref(localStorage.getItem('admin_token') || null)
  const refreshToken = ref(localStorage.getItem('admin_refresh_token') || null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const fullName = computed(() => {
    if (!user.value) return ''
    return `${user.value.lastName || ''}${user.value.firstName || ''}`
  })
  const userRole = computed(() => user.value?.role || '')

  // Mock login for dev mode
  function mockLogin(credentials) {
    const account = MOCK_ADMIN_ACCOUNTS.find(
      (a) => a.email === credentials.email && a.password === credentials.password,
    )
    if (!account) return null
    return {
      access_token: `dev-admin-token-${account.user.id}`,
      refresh_token: `dev-admin-refresh-${account.user.id}`,
      user: account.user,
    }
  }

  // Actions
  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      // Dev mode mock login
      if (import.meta.env.DEV) {
        const mockData = mockLogin(credentials)
        if (mockData) {
          setTokens(mockData)
          user.value = mockData.user
          localStorage.setItem('admin_user', JSON.stringify(mockData.user))
          return mockData
        }
      }

      const response = await authService.login(credentials)
      const data = response.data?.data || response.data
      setTokens(data)
      await fetchUser()
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.response?.data?.message || '登入失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return

    // Dev mode mock token
    if (import.meta.env.DEV && token.value.startsWith('dev-admin-token-')) {
      const stored = localStorage.getItem('admin_user')
      if (stored) {
        user.value = JSON.parse(stored)
      } else {
        clearAuth()
      }
      return
    }

    try {
      const response = await authService.getProfile()
      const data = response.data?.data || response.data
      user.value = data
      localStorage.setItem('admin_user', JSON.stringify(data))
    } catch (err) {
      if (err.response?.status === 401 || !err.response) {
        clearAuth()
      }
    }
  }

  function setTokens(data) {
    token.value = data.access_token
    refreshToken.value = data.refresh_token
    localStorage.setItem('admin_token', data.access_token)
    localStorage.setItem('admin_refresh_token', data.refresh_token)
  }

  async function refreshAccessToken() {
    try {
      const response = await authService.refreshToken(refreshToken.value)
      const data = response.data?.data || response.data
      setTokens(data)
      return data.access_token
    } catch {
      await logout()
      return null
    }
  }

  function clearAuth() {
    user.value = null
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_refresh_token')
    localStorage.removeItem('admin_user')
  }

  async function logout() {
    try {
      if (token.value && !token.value.startsWith('dev-admin-token-')) {
        await authService.logout()
      }
    } catch {
      // ignore logout errors
    } finally {
      clearAuth()
      router.push({ name: 'AdminLogin' })
    }
  }

  function clearError() {
    error.value = null
  }

  // Initialize
  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    refreshToken,
    loading,
    error,
    isAuthenticated,
    fullName,
    userRole,
    login,
    fetchUser,
    refreshAccessToken,
    logout,
    clearError,
  }
})
