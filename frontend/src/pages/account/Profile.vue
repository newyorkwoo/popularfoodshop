<template>
  <div>
    <h2 class="text-xl font-bold text-gray-900 mb-6">個人資料</h2>
    <form @submit.prevent="handleSave" class="space-y-6 max-w-lg">
      <div class="flex items-center gap-4 mb-6">
        <div class="w-20 h-20 rounded-full bg-primary-100 flex items-center justify-center text-2xl font-bold text-primary-600">
          {{ authStore.user?.lastName?.charAt(0) || 'U' }}
        </div>
        <div>
          <p class="font-medium text-gray-900">{{ authStore.fullName }}</p>
          <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <BaseInput v-model="form.lastName" label="姓氏" required />
        <BaseInput v-model="form.firstName" label="名字" required />
      </div>
      <BaseInput v-model="form.email" label="電子郵件" type="email" required disabled />
      <BaseInput v-model="form.phone" label="電話" />

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">性別</label>
        <div class="flex gap-4">
          <label class="flex items-center gap-2 text-sm"><input type="radio" v-model="form.gender" value="male" class="accent-primary-600" /> 男</label>
          <label class="flex items-center gap-2 text-sm"><input type="radio" v-model="form.gender" value="female" class="accent-primary-600" /> 女</label>
          <label class="flex items-center gap-2 text-sm"><input type="radio" v-model="form.gender" value="other" class="accent-primary-600" /> 其他</label>
        </div>
      </div>

      <BaseInput v-model="form.birthday" label="生日" type="date" />

      <BaseButton type="submit" :loading="saving">儲存變更</BaseButton>
    </form>

    <!-- Change Password -->
    <div class="mt-12 pt-8 border-t max-w-lg">
      <h3 class="text-lg font-bold text-gray-900 mb-4">變更密碼</h3>
      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <BaseInput v-model="pwForm.currentPassword" label="目前密碼" type="password" required />
        <BaseInput v-model="pwForm.newPassword" label="新密碼" type="password" required hint="至少 8 個字元" />
        <BaseInput v-model="pwForm.confirmPassword" label="確認新密碼" type="password" required :error="pwError" />
        <BaseButton type="submit" variant="outline" :loading="pwSaving">更新密碼</BaseButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const authStore = useAuthStore()
const uiStore = useUIStore()
const saving = ref(false)
const pwSaving = ref(false)
const pwError = ref('')

const form = reactive({ lastName: '', firstName: '', email: '', phone: '', gender: '', birthday: '' })
const pwForm = reactive({ currentPassword: '', newPassword: '', confirmPassword: '' })

onMounted(() => {
  if (authStore.user) {
    Object.assign(form, {
      lastName: authStore.user.lastName || '', firstName: authStore.user.firstName || '',
      email: authStore.user.email || '', phone: authStore.user.phone || '',
      gender: authStore.user.gender || '', birthday: authStore.user.birthday || '',
    })
  }
})

async function handleSave() {
  saving.value = true
  try {
    await authStore.updateProfile(form)
    uiStore.showToast('個人資料已更新', 'success')
  } catch { /* store handles */ } finally { saving.value = false }
}

async function handleChangePassword() {
  pwError.value = ''
  if (pwForm.newPassword.length < 8) { pwError.value = '密碼至少 8 個字元'; return }
  if (pwForm.newPassword !== pwForm.confirmPassword) { pwError.value = '密碼不一致'; return }
  pwSaving.value = true
  try {
    await authStore.changePassword(pwForm)
    uiStore.showToast('密碼已更新', 'success')
    Object.assign(pwForm, { currentPassword: '', newPassword: '', confirmPassword: '' })
  } catch { /* store handles */ } finally { pwSaving.value = false }
}
</script>
