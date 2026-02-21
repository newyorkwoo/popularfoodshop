<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('auth.registerTitle') }}</h2>
    <p class="text-sm text-gray-500 mb-6">{{ $t('auth.registerSubtitle') }}</p>

    <form @submit.prevent="handleRegister" class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <BaseInput v-model="form.lastName" :label="$t('auth.lastName')" required :error="errors.lastName" />
        <BaseInput v-model="form.firstName" :label="$t('auth.firstName')" required :error="errors.firstName" />
      </div>
      <BaseInput v-model="form.email" :label="$t('auth.email')" type="email" required :error="errors.email" />
      <BaseInput v-model="form.phone" :label="$t('auth.phone')" :error="errors.phone" />
      <BaseInput v-model="form.password" :label="$t('auth.password')" type="password" required :error="errors.password" hint="至少 8 個字元" />
      <BaseInput v-model="form.confirmPassword" :label="$t('auth.confirmPassword')" type="password" required :error="errors.confirmPassword" />

      <label class="flex items-start gap-2 text-sm text-gray-600">
        <input type="checkbox" v-model="form.agreeTerms" class="accent-primary-600 mt-0.5" />
        <span>我同意<router-link to="/terms" class="text-primary-600 hover:underline">服務條款</router-link>與<router-link to="/privacy" class="text-primary-600 hover:underline">隱私政策</router-link></span>
      </label>

      <BaseButton type="submit" class="w-full" size="lg" :loading="authStore.loading" :disabled="!form.agreeTerms">
        {{ $t('auth.registerBtn') }}
      </BaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-gray-500">
      {{ $t('auth.hasAccount') }}
      <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">{{ $t('auth.loginBtn') }}</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  firstName: '', lastName: '', email: '', phone: '',
  password: '', confirmPassword: '', agreeTerms: false,
})
const errors = reactive({
  firstName: '', lastName: '', email: '', phone: '',
  password: '', confirmPassword: '',
})

async function handleRegister() {
  Object.keys(errors).forEach(k => errors[k] = '')
  if (!form.lastName) { errors.lastName = '請輸入姓氏'; return }
  if (!form.firstName) { errors.firstName = '請輸入名字'; return }
  if (!form.email) { errors.email = '請輸入電子郵件'; return }
  if (!form.password || form.password.length < 8) { errors.password = '密碼至少 8 個字元'; return }
  if (form.password !== form.confirmPassword) { errors.confirmPassword = '密碼不一致'; return }

  try {
    await authStore.register(form)
    router.push('/')
  } catch {
    // handled in store
  }
}
</script>
