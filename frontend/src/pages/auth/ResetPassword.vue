<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">重設密碼</h2>
    <p class="text-sm text-gray-500 mb-6">請輸入新密碼</p>

    <div v-if="done" class="text-center space-y-4">
      <div class="w-16 h-16 mx-auto rounded-full bg-green-100 flex items-center justify-center">
        <CheckCircleIcon class="w-8 h-8 text-green-600" />
      </div>
      <p class="text-gray-700">密碼已成功重設！</p>
      <BaseButton class="w-full" @click="router.push('/login')">前往登入</BaseButton>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="space-y-4">
      <BaseInput v-model="form.password" label="新密碼" type="password" required :error="errors.password" hint="至少 8 個字元" />
      <BaseInput v-model="form.confirmPassword" label="確認新密碼" type="password" required :error="errors.confirmPassword" />
      <BaseButton type="submit" class="w-full" size="lg" :loading="loading">重設密碼</BaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-gray-500">
      <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">返回登入</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { CheckCircleIcon } from '@heroicons/vue/24/outline'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ password: '', confirmPassword: '' })
const errors = reactive({ password: '', confirmPassword: '' })
const loading = ref(false)
const done = ref(false)

async function handleSubmit() {
  Object.keys(errors).forEach(k => errors[k] = '')
  if (!form.password || form.password.length < 8) { errors.password = '密碼至少 8 個字元'; return }
  if (form.password !== form.confirmPassword) { errors.confirmPassword = '密碼不一致'; return }

  loading.value = true
  try {
    await authStore.resetPassword({ token: route.query.token, password: form.password })
    done.value = true
  } catch {
    errors.password = '重設失敗，連結可能已過期'
  } finally {
    loading.value = false
  }
}
</script>
