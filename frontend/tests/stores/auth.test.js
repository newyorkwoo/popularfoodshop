/**
 * Tests for the Auth Pinia store
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

// Mock vue-router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}))

// Mock authService
vi.mock('@/services/authService', () => ({
  default: {
    login: vi.fn(),
    register: vi.fn(),
    getProfile: vi.fn(),
    updateProfile: vi.fn(),
    changePassword: vi.fn(),
    forgotPassword: vi.fn(),
    logout: vi.fn(),
  },
}))

describe('Auth Store', () => {
  let auth

  beforeEach(() => {
    setActivePinia(createPinia())
    auth = useAuthStore()
    vi.clearAllMocks()
  })

  // ── Initial State ──────────────────────────────────────────
  describe('initial state', () => {
    it('user is null', () => {
      expect(auth.user).toBeNull()
    })

    it('is not authenticated', () => {
      expect(auth.isAuthenticated).toBe(false)
    })

    it('is not loading', () => {
      expect(auth.loading).toBe(false)
    })

    it('fullName is empty', () => {
      expect(auth.fullName).toBe('')
    })
  })

  // ── Mock Login (Dev Mode) ─────────────────────────────────
  describe('login', () => {
    it('sets user and token on successful mock login', async () => {
      const result = await auth.login({
        email: 'user@example.com',
        password: 'User@123456',
      })
      expect(auth.user).not.toBeNull()
      expect(auth.user.email).toBe('user@example.com')
    })

    it('sets error on failed mock login and no backend', async () => {
      // With wrong credentials and no backend, it should throw
      const authService = await import('@/services/authService')
      authService.default.login.mockRejectedValue(new Error('fail'))

      await expect(
        auth.login({ email: 'wrong@test.com', password: 'WrongPass@1' })
      ).rejects.toThrow()
      expect(auth.error).toBeTruthy()
    })

    it('loading becomes false after login', async () => {
      await auth.login({
        email: 'user@example.com',
        password: 'User@123456',
      })
      expect(auth.loading).toBe(false)
    })
  })

  // ── Computed fullName ──────────────────────────────────────
  describe('fullName', () => {
    it('returns formatted full name', async () => {
      await auth.login({
        email: 'user@example.com',
        password: 'User@123456',
      })
      expect(auth.fullName).toContain('測試')
    })
  })

  // ── Logout ─────────────────────────────────────────────────
  describe('logout', () => {
    it('clears user and tokens', async () => {
      await auth.login({
        email: 'user@example.com',
        password: 'User@123456',
      })
      expect(auth.user).not.toBeNull()
      await auth.logout()
      expect(auth.user).toBeNull()
      expect(auth.isAuthenticated).toBe(false)
    })
  })
})
