<template>
  <div class="container mx-auto px-4 py-10">
    <h1 class="text-3xl font-extrabold text-gray-900 mb-8">{{ $t('cart.title') }}</h1>

    <div v-if="cartStore.items.length === 0" class="text-center py-24">
      <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-5">
        <ShoppingBagIcon class="w-12 h-12 text-gray-300" />
      </div>
      <p class="text-xl font-medium text-gray-500 mb-2">{{ $t('cart.empty') }}</p>
      <p class="text-sm text-gray-400 mb-6">開始選購您喜歡的商品吧</p>
      <router-link to="/products" class="inline-flex items-center gap-2 px-7 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-500 hover:shadow-lg hover:shadow-primary-600/25 font-semibold transition-all">
        {{ $t('cart.continueShopping') }}
      </router-link>
    </div>

    <div v-else class="grid lg:grid-cols-3 gap-8">
      <!-- Cart items -->
      <div class="lg:col-span-2">
        <!-- Free shipping bar -->
        <div v-if="cartStore.freeShippingRemaining > 0" class="mb-6 p-4 bg-amber-50 rounded-2xl border border-amber-100">
          <p class="text-sm text-amber-700 mb-2">
            再消費 <strong class="text-amber-900">NT${{ cartStore.freeShippingRemaining.toLocaleString() }}</strong> 即享免運費！
          </p>
          <div class="h-2 bg-amber-100 rounded-full overflow-hidden">
            <div class="h-full bg-linear-to-r from-amber-400 to-amber-500 rounded-full transition-all duration-500 ease-out" :style="{ width: cartStore.freeShippingProgress + '%' }" />
          </div>
        </div>
        <div v-else class="mb-6 p-4 bg-green-50 rounded-2xl border border-green-100 flex items-center gap-2">
          <CheckCircleIcon class="w-5 h-5 text-green-600" />
          <p class="text-sm text-green-700 font-semibold">🎉 已達免運門檻！</p>
        </div>

        <div class="space-y-4">
          <div v-for="item in cartStore.items" :key="`${item.productId}-${item.variantId}`" class="flex gap-4 p-5 bg-white rounded-2xl border border-gray-100 hover:shadow-md transition-shadow">
            <router-link :to="{ name: 'ProductDetail', params: { slug: item.slug } }" class="shrink-0 w-24 h-24 bg-gray-50 rounded-xl overflow-hidden border border-gray-100">
              <img :src="item.image || 'https://placehold.co/200x200/f3f4f6/9ca3af?text=No'" :alt="item.name" class="w-full h-full object-cover" />
            </router-link>
            <div class="flex-1 min-w-0">
              <router-link :to="{ name: 'ProductDetail', params: { slug: item.slug } }" class="text-sm font-semibold text-gray-800 hover:text-primary-600 line-clamp-2 transition-colors">
                {{ item.name }}
              </router-link>
              <p v-if="item.variant" class="text-xs text-gray-400 mt-0.5">{{ item.variant.name }}: {{ item.variant.value }}</p>
              <div class="flex items-center justify-between mt-3">
                <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden">
                  <button class="px-3 py-1.5 text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors" @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity - 1)">−</button>
                  <span class="px-3 py-1.5 text-sm font-medium text-gray-900 border-x border-gray-200 min-w-[3rem] text-center bg-gray-50">{{ item.quantity }}</span>
                  <button class="px-3 py-1.5 text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors" @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity + 1)">+</button>
                </div>
                <p class="text-base font-bold text-gray-900">NT${{ ((item.salePrice || item.price) * item.quantity).toLocaleString() }}</p>
              </div>
            </div>
            <button class="self-start p-2 text-gray-300 hover:text-red-500 transition-colors" @click="cartStore.removeItem(item.productId, item.variantId)">
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <!-- Order summary -->
      <div class="lg:col-span-1">
        <div class="sticky top-24 bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
          <h2 class="text-lg font-bold text-gray-900 mb-5">訂單摘要</h2>

          <!-- Coupon -->
          <div class="flex gap-2 mb-5">
            <input v-model="couponInput" :placeholder="$t('cart.couponPlaceholder')" class="flex-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:border-primary-500 focus:ring-2 focus:ring-primary-100 transition-all" />
            <button class="px-4 py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-xl hover:bg-gray-800 transition-colors" @click="applyCoupon">
              {{ $t('cart.applyCoupon') }}
            </button>
          </div>

          <div class="space-y-3.5 pb-5 border-b border-gray-100">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">{{ $t('cart.subtotal') }}</span>
              <span class="text-gray-900 font-medium">NT${{ cartStore.subtotal.toLocaleString() }}</span>
            </div>
            <div v-if="cartStore.discount > 0" class="flex justify-between text-sm">
              <span class="text-gray-500">{{ $t('cart.discount') }}</span>
              <span class="text-red-600 font-semibold">-NT${{ cartStore.discount.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">{{ $t('cart.shipping') }}</span>
              <span :class="cartStore.shippingFee === 0 ? 'text-green-600 font-semibold' : 'text-gray-900'">
                {{ cartStore.shippingFee === 0 ? $t('cart.freeShipping') : `NT$${cartStore.shippingFee}` }}
              </span>
            </div>
          </div>

          <div class="flex justify-between pt-5 mb-6">
            <span class="text-lg font-bold text-gray-900">{{ $t('cart.total') }}</span>
            <span class="text-2xl font-extrabold text-primary-600">NT${{ cartStore.total.toLocaleString() }}</span>
          </div>

          <router-link to="/checkout" class="block w-full text-center py-3.5 bg-primary-600 text-white font-bold rounded-xl hover:bg-primary-500 hover:shadow-lg hover:shadow-primary-600/25 transition-all">
            {{ $t('cart.checkout') }}
          </router-link>
          <router-link to="/products" class="block w-full text-center py-3 text-sm text-gray-500 hover:text-primary-600 mt-2 font-medium transition-colors">
            {{ $t('cart.continueShopping') }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useUIStore } from '@/stores/ui'
import { ShoppingBagIcon, TrashIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'

const cartStore = useCartStore()
const uiStore = useUIStore()
const couponInput = ref('')

async function applyCoupon() {
  if (!couponInput.value.trim()) return
  try {
    const result = await cartStore.applyCoupon(couponInput.value.trim())
    uiStore.showToast(`優惠券已套用：折扣 NT$${result.discount.toLocaleString()}`, 'success')
  } catch {
    uiStore.showToast('無效的優惠券代碼', 'error')
  }
}
</script>
