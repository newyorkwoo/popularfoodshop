import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'

// Dev-mode mock accounts (matches backend seeds)
const MOCK_ACCOUNTS = [
  {
    email: 'user@example.com',
    password: 'User@123456',
    user: { id: 3, email: 'user@example.com', firstName: '會員', lastName: '測試', role: 'customer', phone: '0912345678' },
  },
]

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()

  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const fullName = computed(() => {
    if (!user.value) return ''
    return `${user.value.lastName || ''}${user.value.firstName || ''}`
  })

  // Mock login fallback for dev mode (when backend is unavailable)
  function mockLogin(credentials) {
    const account = MOCK_ACCOUNTS.find(
      (a) => a.email === credentials.email && a.password === credentials.password,
    )
    if (!account) return null
    return {
      accessToken: `dev-token-${account.user.id}`,
      refreshToken: `dev-refresh-${account.user.id}`,
      user: account.user,
    }
  }

  // Actions
  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      // In dev mode, try mock login first (backend may be unavailable)
      if (import.meta.env.DEV) {
        const mockData = mockLogin(credentials)
        if (mockData) {
          setTokens(mockData)
          user.value = mockData.user
          localStorage.setItem('user', JSON.stringify(mockData.user))
          return mockData
        }
      }
      const response = await authService.login(credentials)
      setTokens(response.data)
      await fetchUser()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '登入失敗，請檢查帳號密碼'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      const response = await authService.register(userData)
      setTokens(response.data)
      await fetchUser()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '註冊失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    // In dev mode with mock token, load user from localStorage
    if (import.meta.env.DEV && token.value.startsWith('dev-token-')) {
      const stored = localStorage.getItem('user')
      if (stored) {
        user.value = JSON.parse(stored)
      } else {
        // Token exists but no user data — clear stale token
        token.value = null
        refreshToken.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
      }
      return
    }
    try {
      const response = await authService.getProfile()
      user.value = response.data
    } catch (err) {
      // Backend unavailable or session invalid — clear stale auth
      if (err.response?.status === 401 || !err.response) {
        token.value = null
        refreshToken.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('user')
      }
    }
  }

  async function updateProfile(data) {
    loading.value = true
    try {
      const response = await authService.updateProfile(data)
      user.value = { ...user.value, ...response.data }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '更新失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function changePassword(data) {
    loading.value = true
    try {
      await authService.changePassword(data)
    } catch (err) {
      error.value = err.response?.data?.message || '密碼修改失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function forgotPassword(email) {
    loading.value = true
    try {
      await authService.forgotPassword(email)
    } catch (err) {
      error.value = err.response?.data?.message || '發送重設郵件失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function resetPassword(data) {
    loading.value = true
    try {
      await authService.resetPassword(data)
    } catch (err) {
      error.value = err.response?.data?.message || '重設密碼失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setTokens(data) {
    token.value = data.accessToken
    refreshToken.value = data.refreshToken
    localStorage.setItem('token', data.accessToken)
    localStorage.setItem('refreshToken', data.refreshToken)
  }

  async function refreshAccessToken() {
    try {
      const response = await authService.refreshToken(refreshToken.value)
      setTokens(response.data)
      return response.data.accessToken
    } catch {
      await logout()
      return null
    }
  }

  async function logout() {
    try {
      if (token.value) {
        await authService.logout()
      }
    } catch {
      // ignore logout errors
    } finally {
      user.value = null
      token.value = null
      refreshToken.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      router.push({ name: 'Home' })
    }
  }

  function clearError() {
    error.value = null
  }

  // Initialize: fetch user if token exists
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
    login,
    register,
    fetchUser,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    refreshAccessToken,
    logout,
    clearError,
  }
})
