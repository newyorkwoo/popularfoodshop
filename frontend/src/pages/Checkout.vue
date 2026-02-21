<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ $t('checkout.title') }}</h1>

    <!-- Steps -->
    <div class="flex items-center justify-center mb-10">
      <template v-for="(s, i) in steps" :key="s.key">
        <div class="flex items-center gap-2">
          <span
            class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
            :class="checkoutStore.step > i + 1 ? 'bg-primary-600 text-white' : checkoutStore.step === i + 1 ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-500'"
          >
            <CheckIcon v-if="checkoutStore.step > i + 1" class="w-4 h-4" />
            <span v-else>{{ i + 1 }}</span>
          </span>
          <span class="text-sm font-medium" :class="checkoutStore.step >= i + 1 ? 'text-gray-900' : 'text-gray-400'">{{ s.label }}</span>
        </div>
        <div v-if="i < steps.length - 1" class="w-12 h-0.5 mx-2" :class="checkoutStore.step > i + 1 ? 'bg-primary-600' : 'bg-gray-200'" />
      </template>
    </div>

    <div class="grid lg:grid-cols-3 gap-8">
      <!-- Forms -->
      <div class="lg:col-span-2">
        <!-- Step 1: Shipping -->
        <div v-if="checkoutStore.step === 1" class="bg-white rounded-xl border border-gray-200 p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">{{ $t('checkout.shippingInfo') }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <BaseInput v-model="checkoutStore.shippingInfo.lastName" :label="$t('auth.lastName')" required />
            <BaseInput v-model="checkoutStore.shippingInfo.firstName" :label="$t('auth.firstName')" required />
            <BaseInput v-model="checkoutStore.shippingInfo.email" :label="$t('auth.email')" type="email" class="col-span-2" required />
            <BaseInput v-model="checkoutStore.shippingInfo.phone" :label="$t('auth.phone')" class="col-span-2" required />
          </div>

          <h3 class="text-base font-semibold text-gray-900 mt-6 mb-3">{{ $t('checkout.deliveryMethod') }}</h3>
          <div class="grid grid-cols-2 gap-3 mb-4">
            <label
              v-for="method in deliveryMethods"
              :key="method.value"
              class="flex items-center gap-3 p-3 border rounded-lg cursor-pointer transition-colors"
              :class="checkoutStore.deliveryMethod === method.value ? 'border-primary-600 bg-primary-50' : 'border-gray-300'"
            >
              <input type="radio" :value="method.value" v-model="checkoutStore.deliveryMethod" class="accent-primary-600" />
              <div>
                <p class="text-sm font-medium text-gray-900">{{ method.label }}</p>
                <p class="text-xs text-gray-500">{{ method.desc }}</p>
              </div>
            </label>
          </div>

          <template v-if="checkoutStore.deliveryMethod === 'home'">
            <div class="grid grid-cols-2 gap-4">
              <BaseInput v-model="checkoutStore.shippingInfo.postalCode" label="郵遞區號" required />
              <BaseInput v-model="checkoutStore.shippingInfo.city" label="縣市" required />
              <BaseInput v-model="checkoutStore.shippingInfo.district" label="區域" required />
              <BaseInput v-model="checkoutStore.shippingInfo.address" label="地址" class="col-span-2" required />
            </div>
          </template>

          <BaseInput v-model="checkoutStore.shippingInfo.notes" label="備註" class="mt-4" />

          <div class="flex justify-end mt-6">
            <BaseButton @click="checkoutStore.nextStep()" :disabled="!checkoutStore.isShippingValid">
              {{ $t('common.next') }}
            </BaseButton>
          </div>
        </div>

        <!-- Step 2: Payment -->
        <div v-if="checkoutStore.step === 2" class="bg-white rounded-xl border border-gray-200 p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">{{ $t('checkout.paymentMethod') }}</h2>
          <div class="space-y-3">
            <label
              v-for="method in paymentMethods"
              :key="method.value"
              class="flex items-center gap-3 p-4 border rounded-lg cursor-pointer transition-colors"
              :class="checkoutStore.paymentMethod === method.value ? 'border-primary-600 bg-primary-50' : 'border-gray-300'"
            >
              <input type="radio" :value="method.value" v-model="checkoutStore.paymentMethod" class="accent-primary-600" />
              <span class="text-2xl">{{ method.icon }}</span>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ method.label }}</p>
                <p class="text-xs text-gray-500">{{ method.desc }}</p>
              </div>
            </label>
          </div>
          <div class="flex justify-between mt-6">
            <BaseButton variant="ghost" @click="checkoutStore.prevStep()">{{ $t('common.back') }}</BaseButton>
            <BaseButton @click="checkoutStore.nextStep()">{{ $t('common.next') }}</BaseButton>
          </div>
        </div>

        <!-- Step 3: Review -->
        <div v-if="checkoutStore.step === 3" class="bg-white rounded-xl border border-gray-200 p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">{{ $t('checkout.orderReview') }}</h2>
          <div class="space-y-4">
            <div v-for="item in checkoutStore.orderSummary.items" :key="item.productId" class="flex items-center gap-3 py-2 border-b border-gray-100 last:border-0">
              <div class="w-12 h-12 bg-gray-100 rounded-lg overflow-hidden shrink-0">
                <img :src="item.image || 'https://placehold.co/100x100'" :alt="item.name" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-900 line-clamp-1">{{ item.name }}</p>
                <p class="text-xs text-gray-500">x {{ item.quantity }}</p>
              </div>
              <p class="text-sm font-medium text-gray-900">NT${{ ((item.salePrice || item.price) * item.quantity).toLocaleString() }}</p>
            </div>
          </div>
          <div class="flex justify-between mt-6">
            <BaseButton variant="ghost" @click="checkoutStore.prevStep()">{{ $t('common.back') }}</BaseButton>
            <BaseButton :loading="checkoutStore.loading" @click="handlePlaceOrder">
              {{ $t('checkout.placeOrder') }}
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Summary sidebar -->
      <div class="lg:col-span-1">
        <div class="sticky top-24 bg-white rounded-xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-4">訂單摘要</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('cart.subtotal') }}</span>
              <span>NT${{ checkoutStore.orderSummary.subtotal.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">{{ $t('cart.shipping') }}</span>
              <span>{{ checkoutStore.orderSummary.shipping === 0 ? $t('cart.freeShipping') : `NT$${checkoutStore.orderSummary.shipping}` }}</span>
            </div>
            <div v-if="checkoutStore.orderSummary.discount > 0" class="flex justify-between">
              <span class="text-gray-600">{{ $t('cart.discount') }}</span>
              <span class="text-red-600">-NT${{ checkoutStore.orderSummary.discount.toLocaleString() }}</span>
            </div>
          </div>
          <div class="flex justify-between font-bold text-lg pt-3 mt-3 border-t border-gray-200">
            <span>{{ $t('cart.total') }}</span>
            <span class="text-primary-600">NT${{ checkoutStore.orderSummary.total.toLocaleString() }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCheckoutStore } from '@/stores/checkout'
import { useCartStore } from '@/stores/cart'
import { useUIStore } from '@/stores/ui'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { CheckIcon } from '@heroicons/vue/24/solid'

const router = useRouter()
const checkoutStore = useCheckoutStore()
const cartStore = useCartStore()
const uiStore = useUIStore()

const steps = [
  { key: 'shipping', label: '收件資訊' },
  { key: 'payment', label: '付款方式' },
  { key: 'review', label: '確認訂單' },
]

const deliveryMethods = [
  { value: 'home', label: '宅配到府', desc: '1-3 個工作天' },
  { value: 'convenience', label: '超商取貨', desc: '2-4 個工作天' },
]

const paymentMethods = [
  { value: 'credit_card', label: '信用卡', desc: 'Visa / Mastercard / JCB', icon: '💳' },
  { value: 'line_pay', label: 'LINE Pay', desc: '使用 LINE Pay 付款', icon: '💚' },
  { value: 'cod', label: '貨到付款', desc: '宅配到府時現金付款', icon: '💵' },
]

async function handlePlaceOrder() {
  try {
    const orderId = await checkoutStore.placeOrder()
    uiStore.showToast('訂單已成立！', 'success')
    checkoutStore.reset()
    router.push({ name: 'OrderDetail', params: { id: orderId } })
  } catch {
    uiStore.showToast('下單失敗，請稍後再試', 'error')
  }
}

onMounted(() => {
  if (cartStore.items.length === 0) {
    router.push({ name: 'Cart' })
  }
  checkoutStore.reset()
})
</script>
