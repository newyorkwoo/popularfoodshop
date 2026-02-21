<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-2">忘記密碼</h2>
    <p class="text-sm text-gray-500 mb-6">輸入您的電子郵件，我們將發送重設密碼連結。</p>

    <div v-if="sent" class="text-center space-y-4">
      <div class="w-16 h-16 mx-auto rounded-full bg-green-100 flex items-center justify-center">
        <EnvelopeIcon class="w-8 h-8 text-green-600" />
      </div>
      <p class="text-gray-700">重設密碼連結已發送至<br><strong>{{ form.email }}</strong></p>
      <p class="text-sm text-gray-500">若未收到請檢查垃圾郵件資料夾</p>
      <BaseButton variant="outline" class="w-full" @click="sent = false">重新發送</BaseButton>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="space-y-4">
      <BaseInput v-model="form.email" label="電子郵件" type="email" required :error="error" />
      <BaseButton type="submit" class="w-full" size="lg" :loading="loading">發送重設連結</BaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-gray-500">
      <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">返回登入</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { EnvelopeIcon } from '@heroicons/vue/24/outline'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const authStore = useAuthStore()
const form = reactive({ email: '' })
const error = ref('')
const loading = ref(false)
const sent = ref(false)

async function handleSubmit() {
  error.value = ''
  if (!form.email) { error.value = '請輸入電子郵件'; return }
  loading.value = true
  try {
    await authStore.forgotPassword(form.email)
    sent.value = true
  } catch {
    error.value = '發送失敗，請稍後再試'
  } finally {
    loading.value = false
  }
}
</script>
