<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ $t('cart.title') }}</h1>

    <div v-if="cartStore.items.length === 0" class="text-center py-20">
      <ShoppingBagIcon class="w-20 h-20 text-gray-300 mx-auto mb-4" />
      <p class="text-xl text-gray-500 mb-4">{{ $t('cart.empty') }}</p>
      <router-link to="/products" class="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium">
        {{ $t('cart.continueShopping') }}
      </router-link>
    </div>

    <div v-else class="grid lg:grid-cols-3 gap-8">
      <!-- Cart items -->
      <div class="lg:col-span-2">
        <!-- Free shipping bar -->
        <div v-if="cartStore.freeShippingRemaining > 0" class="mb-6 p-4 bg-secondary-50 rounded-xl">
          <p class="text-sm text-secondary-700 mb-2">
            再消費 <strong>NT${{ cartStore.freeShippingRemaining.toLocaleString() }}</strong> 即享免運費！
          </p>
          <div class="h-2 bg-secondary-200 rounded-full overflow-hidden">
            <div class="h-full bg-secondary-500 rounded-full transition-all duration-300" :style="{ width: cartStore.freeShippingProgress + '%' }" />
          </div>
        </div>
        <div v-else class="mb-6 p-4 bg-secondary-50 rounded-xl flex items-center gap-2">
          <CheckCircleIcon class="w-5 h-5 text-secondary-600" />
          <p class="text-sm text-secondary-700 font-medium">已達免運門檻！</p>
        </div>

        <div class="space-y-4">
          <div v-for="item in cartStore.items" :key="`${item.productId}-${item.variantId}`" class="flex gap-4 p-4 bg-white rounded-xl border border-gray-200">
            <router-link :to="{ name: 'ProductDetail', params: { slug: item.slug } }" class="shrink-0 w-24 h-24 bg-gray-100 rounded-lg overflow-hidden">
              <img :src="item.image || 'https://placehold.co/200x200/f3f4f6/9ca3af?text=No'" :alt="item.name" class="w-full h-full object-cover" />
            </router-link>
            <div class="flex-1 min-w-0">
              <router-link :to="{ name: 'ProductDetail', params: { slug: item.slug } }" class="text-sm font-medium text-gray-900 hover:text-primary-600 line-clamp-2">
                {{ item.name }}
              </router-link>
              <p v-if="item.variant" class="text-xs text-gray-500 mt-0.5">{{ item.variant.name }}: {{ item.variant.value }}</p>
              <div class="flex items-center justify-between mt-3">
                <div class="flex items-center border border-gray-300 rounded-lg">
                  <button class="px-3 py-1.5 text-gray-600 hover:text-gray-900" @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity - 1)">−</button>
                  <span class="px-3 py-1.5 text-sm text-gray-900 border-x border-gray-300 min-w-[3rem] text-center">{{ item.quantity }}</span>
                  <button class="px-3 py-1.5 text-gray-600 hover:text-gray-900" @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity + 1)">+</button>
                </div>
                <p class="text-base font-bold text-gray-900">NT${{ ((item.salePrice || item.price) * item.quantity).toLocaleString() }}</p>
              </div>
            </div>
            <button class="self-start p-2 text-gray-400 hover:text-red-500" @click="cartStore.removeItem(item.productId, item.variantId)">
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <!-- Order summary -->
      <div class="lg:col-span-1">
        <div class="sticky top-24 bg-white rounded-xl border border-gray-200 p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">訂單摘要</h2>

          <!-- Coupon -->
          <div class="flex gap-2 mb-4">
            <input v-model="couponInput" :placeholder="$t('cart.couponPlaceholder')" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:border-primary-500 focus:ring-1 focus:ring-primary-200" />
            <button class="px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800" @click="applyCoupon">
              {{ $t('cart.applyCoupon') }}
            </button>
          </div>

          <div class="space-y-3 pb-4 border-b border-gray-200">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">{{ $t('cart.subtotal') }}</span>
              <span class="text-gray-900">NT${{ cartStore.subtotal.toLocaleString() }}</span>
            </div>
            <div v-if="cartStore.discount > 0" class="flex justify-between text-sm">
              <span class="text-gray-600">{{ $t('cart.discount') }}</span>
              <span class="text-red-600">-NT${{ cartStore.discount.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">{{ $t('cart.shipping') }}</span>
              <span :class="cartStore.shippingFee === 0 ? 'text-secondary-600 font-medium' : 'text-gray-900'">
                {{ cartStore.shippingFee === 0 ? $t('cart.freeShipping') : `NT$${cartStore.shippingFee}` }}
              </span>
            </div>
          </div>

          <div class="flex justify-between pt-4 mb-6">
            <span class="text-lg font-bold text-gray-900">{{ $t('cart.total') }}</span>
            <span class="text-xl font-bold text-primary-600">NT${{ cartStore.total.toLocaleString() }}</span>
          </div>

          <router-link to="/checkout" class="block w-full text-center py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors">
            {{ $t('cart.checkout') }}
          </router-link>
          <router-link to="/products" class="block w-full text-center py-3 text-sm text-gray-600 hover:text-gray-900 mt-2">
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
