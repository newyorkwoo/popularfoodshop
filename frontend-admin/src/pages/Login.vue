<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="text-4xl mb-2">🍜</div>
        <h1 class="text-2xl font-bold text-white">管理後台</h1>
        <p class="text-gray-400 text-sm mt-1">Popular Food Shop Administration</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-xl shadow-2xl p-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">管理員登入</h2>

        <!-- Error message -->
        <div v-if="authStore.error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ authStore.error }}</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              autocomplete="email"
              placeholder="admin@popularfoodshop.com"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              密碼
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="請輸入密碼"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors pr-10"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <EyeIcon v-if="!showPassword" class="w-5 h-5" />
                <EyeSlashIcon v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <svg v-if="authStore.loading" class="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {{ authStore.loading ? '登入中...' : '登入' }}
          </button>
        </form>

        <!-- Security notice -->
        <div class="mt-6 pt-4 border-t border-gray-100">
          <div class="flex items-start gap-2 text-xs text-gray-400">
            <ShieldCheckIcon class="w-4 h-4 mt-0.5 shrink-0" />
            <span>此為管理員專用登入頁面，僅限授權人員使用。所有登入行為皆會被記錄。</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminAuthStore } from '@/stores/auth'
import { EyeIcon, EyeSlashIcon, ShieldCheckIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAdminAuthStore()

const form = reactive({
  email: '',
  password: '',
})
const showPassword = ref(false)

async function handleLogin() {
  authStore.clearError()
  try {
    await authStore.login(form)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch {
    // error handled by store
  }
}
</script>
