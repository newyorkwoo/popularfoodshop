<template>
    <div class="max-w-3xl mx-auto px-4 py-12">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">聯絡我們</h1>

      <div class="grid md:grid-cols-2 gap-10">
        <!-- Contact Form -->
        <div>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <BaseInput v-model="form.name" label="姓名" required />
            <BaseInput v-model="form.email" label="電子郵件" type="email" required />
            <BaseInput v-model="form.phone" label="電話" />
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">主旨</label>
              <select v-model="form.subject" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
                <option value="">請選擇</option>
                <option value="order">訂單問題</option>
                <option value="product">商品諮詢</option>
                <option value="return">退換貨</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">訊息內容 <span class="text-red-500">*</span></label>
              <textarea v-model="form.message" rows="5" required class="w-full border border-gray-300 rounded-lg px-3 py-2.5 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"></textarea>
            </div>
            <BaseButton type="submit" class="w-full" size="lg" :loading="loading">
              {{ sent ? '✓ 已送出' : '送出訊息' }}
            </BaseButton>
          </form>
        </div>

        <!-- Info -->
        <div class="space-y-6">
          <div class="bg-gray-50 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">客服資訊</h3>
            <div class="flex items-start gap-3">
              <EnvelopeIcon class="w-5 h-5 text-primary-600 mt-0.5" />
              <div><p class="text-sm font-medium text-gray-700">電子郵件</p><p class="text-sm text-gray-500">support@popularfoodshop.com</p></div>
            </div>
            <div class="flex items-start gap-3">
              <PhoneIcon class="w-5 h-5 text-primary-600 mt-0.5" />
              <div><p class="text-sm font-medium text-gray-700">客服電話</p><p class="text-sm text-gray-500">(02) 2345-6789</p></div>
            </div>
            <div class="flex items-start gap-3">
              <ClockIcon class="w-5 h-5 text-primary-600 mt-0.5" />
              <div><p class="text-sm font-medium text-gray-700">服務時間</p><p class="text-sm text-gray-500">週一至週五 9:00 - 18:00</p></div>
            </div>
            <div class="flex items-start gap-3">
              <MapPinIcon class="w-5 h-5 text-primary-600 mt-0.5" />
              <div><p class="text-sm font-medium text-gray-700">地址</p><p class="text-sm text-gray-500">台北市大安區美食路 123 號</p></div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { EnvelopeIcon, PhoneIcon, ClockIcon, MapPinIcon } from '@heroicons/vue/24/outline'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const form = reactive({ name: '', email: '', phone: '', subject: '', message: '' })
const loading = ref(false)
const sent = ref(false)

async function handleSubmit() {
  loading.value = true
  await new Promise(r => setTimeout(r, 1000))
  loading.value = false
  sent.value = true
}
</script>
