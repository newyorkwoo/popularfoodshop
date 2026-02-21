<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('auth.loginTitle') }}</h2>
    <p class="text-sm text-gray-500 mb-6">{{ $t('auth.loginSubtitle') }}</p>

    <form @submit.prevent="handleLogin" class="space-y-4">
      <BaseInput v-model="form.email" :label="$t('auth.email')" type="email" required :error="errors.email" />
      <BaseInput v-model="form.password" :label="$t('auth.password')" type="password" required :error="errors.password" />

      <div class="flex items-center justify-between">
        <label class="flex items-center gap-2 text-sm text-gray-600">
          <input type="checkbox" v-model="form.rememberMe" class="accent-primary-600 rounded" />
          {{ $t('auth.rememberMe') }}
        </label>
        <router-link to="/forgot-password" class="text-sm text-primary-600 hover:text-primary-700">
          {{ $t('auth.forgotPassword') }}
        </router-link>
      </div>

      <BaseButton type="submit" class="w-full" size="lg" :loading="authStore.loading">
        {{ $t('auth.loginBtn') }}
      </BaseButton>
    </form>

    <div class="mt-6 text-center">
      <p class="text-sm text-gray-500">
        {{ $t('auth.noAccount') }}
        <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-medium">{{ $t('auth.registerBtn') }}</router-link>
      </p>
    </div>

    <!-- Social login -->
    <div class="mt-6">
      <div class="relative">
        <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-gray-200"></div></div>
        <div class="relative flex justify-center text-xs"><span class="px-2 bg-white text-gray-500">{{ $t('auth.orContinueWith') }}</span></div>
      </div>
      <div class="mt-4 grid grid-cols-2 gap-3">
        <button class="flex items-center justify-center gap-2 px-4 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700">
          <svg class="w-5 h-5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
          Google
        </button>
        <button class="flex items-center justify-center gap-2 px-4 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm font-medium text-gray-700">
          <svg class="w-5 h-5" fill="#06C755" viewBox="0 0 24 24"><path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/></svg>
          LINE
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

const errors = reactive({
  email: '',
  password: '',
})

async function handleLogin() {
  errors.email = ''
  errors.password = ''

  if (!form.email) { errors.email = '請輸入電子郵件'; return }
  if (!form.password) { errors.password = '請輸入密碼'; return }

  try {
    await authStore.login({ email: form.email, password: form.password })
    router.push('/')
  } catch {
    // error handled in store
  }
}
</script>
