<template>
  <transition name="slide-right">
    <div v-if="uiStore.cartDrawerOpen" class="fixed inset-0 z-50">
      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="uiStore.toggleCartDrawer(false)" />

      <!-- Drawer -->
      <div class="absolute inset-y-0 right-0 w-104 max-w-[92vw] bg-white shadow-2xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between px-5 h-16 border-b border-gray-100 bg-gray-50/80">
          <h2 class="text-lg font-bold text-gray-900 flex items-center gap-2">
            <ShoppingBagIcon class="w-5 h-5 text-primary-600" />
            {{ $t('cart.title') }}
            <span class="text-sm font-normal text-gray-400">({{ cartStore.itemCount }})</span>
          </h2>
          <button @click="uiStore.toggleCartDrawer(false)" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <!-- Free shipping progress -->
        <div v-if="cartStore.items.length > 0 && cartStore.freeShippingRemaining > 0" class="px-5 py-3.5 bg-amber-50/80 border-b border-amber-100">
          <p class="text-sm text-amber-700 mb-2">
            再消費 <strong class="text-amber-900">NT${{ cartStore.freeShippingRemaining }}</strong> 即享免運費！
          </p>
          <div class="h-2 bg-amber-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-linear-to-r from-amber-400 to-amber-500 rounded-full transition-all duration-500 ease-out"
              :style="{ width: cartStore.freeShippingProgress + '%' }"
            />
          </div>
        </div>
        <div v-else-if="cartStore.items.length > 0 && cartStore.freeShippingRemaining <= 0" class="px-5 py-3 bg-green-50 border-b border-green-100">
          <p class="text-sm text-green-700 font-medium flex items-center gap-1.5">
            <span>🎉</span> 已達免運門檻！
          </p>
        </div>

        <!-- Items -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="cartStore.items.length === 0" class="flex flex-col items-center justify-center h-full text-gray-400 px-4">
            <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <ShoppingBagIcon class="w-10 h-10 text-gray-300" />
            </div>
            <p class="text-lg font-medium text-gray-500">{{ $t('cart.empty') }}</p>
            <p class="text-sm text-gray-400 mt-1">開始選購您喜歡的商品吧</p>
            <router-link
              to="/products"
              class="mt-6 px-6 py-2.5 bg-primary-600 text-white text-sm font-medium rounded-xl hover:bg-primary-500 transition-all hover:shadow-lg hover:shadow-primary-600/25"
              @click="uiStore.toggleCartDrawer(false)"
            >
              {{ $t('cart.continueShopping') }}
            </router-link>
          </div>

          <ul v-else class="divide-y divide-gray-50">
            <li v-for="item in cartStore.items" :key="`${item.productId}-${item.variantId}`" class="flex gap-3 p-4 hover:bg-gray-50/50 transition-colors">
              <!-- Image -->
              <router-link
                :to="{ name: 'ProductDetail', params: { slug: item.slug } }"
                class="shrink-0 w-20 h-20 bg-gray-50 rounded-xl overflow-hidden border border-gray-100"
                @click="uiStore.toggleCartDrawer(false)"
              >
                <img
                  :src="item.image || 'https://placehold.co/160x160/f3f4f6/9ca3af?text=No+Image'"
                  :alt="item.name"
                  class="w-full h-full object-cover"
                />
              </router-link>

              <!-- Info -->
              <div class="flex-1 min-w-0">
                <router-link
                  :to="{ name: 'ProductDetail', params: { slug: item.slug } }"
                  class="text-sm font-semibold text-gray-800 hover:text-primary-600 line-clamp-2 transition-colors"
                  @click="uiStore.toggleCartDrawer(false)"
                >
                  {{ item.name }}
                </router-link>
                <p v-if="item.variant" class="text-[11px] text-gray-400 mt-0.5">{{ item.variant.name }}: {{ item.variant.value }}</p>
                <div class="flex items-center justify-between mt-2">
                  <div class="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                    <button
                      class="px-2.5 py-1 text-gray-500 hover:text-gray-900 hover:bg-gray-100 text-sm transition-colors"
                      @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity - 1)"
                    >−</button>
                    <span class="px-2.5 text-sm font-medium text-gray-900 min-w-8 text-center bg-gray-50">{{ item.quantity }}</span>
                    <button
                      class="px-2.5 py-1 text-gray-500 hover:text-gray-900 hover:bg-gray-100 text-sm transition-colors"
                      @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity + 1)"
                    >+</button>
                  </div>
                  <p class="text-sm font-bold text-gray-900">
                    NT${{ ((item.salePrice || item.price) * item.quantity).toLocaleString() }}
                  </p>
                </div>
              </div>

              <!-- Remove -->
              <button
                class="self-start text-gray-300 hover:text-red-500 p-1 transition-colors"
                @click="cartStore.removeItem(item.productId, item.variantId)"
              >
                <TrashIcon class="w-4 h-4" />
              </button>
            </li>
          </ul>
        </div>

        <!-- Footer -->
        <div v-if="cartStore.items.length > 0" class="border-t border-gray-100 p-5 space-y-3 bg-gray-50/50">
          <div class="flex justify-between text-sm">
            <span class="text-gray-500">{{ $t('cart.subtotal') }}</span>
            <span class="font-medium text-gray-900">NT${{ cartStore.subtotal.toLocaleString() }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-500">{{ $t('cart.shipping') }}</span>
            <span class="font-semibold" :class="cartStore.shippingFee === 0 ? 'text-green-600' : 'text-gray-900'">
              {{ cartStore.shippingFee === 0 ? $t('cart.freeShipping') : `NT$${cartStore.shippingFee}` }}
            </span>
          </div>
          <div class="flex justify-between text-lg font-bold pt-3 border-t border-gray-200">
            <span>{{ $t('cart.total') }}</span>
            <span class="text-primary-600">NT${{ cartStore.total.toLocaleString() }}</span>
          </div>
          <div class="space-y-2.5 pt-1">
            <router-link
              to="/cart"
              class="block w-full text-center py-3 bg-white text-gray-900 font-semibold rounded-xl border border-gray-200 hover:bg-gray-50 transition-all text-sm"
              @click="uiStore.toggleCartDrawer(false)"
            >
              {{ $t('cart.title') }}
            </router-link>
            <router-link
              to="/checkout"
              class="block w-full text-center py-3 bg-primary-600 text-white font-semibold rounded-xl hover:bg-primary-500 hover:shadow-lg hover:shadow-primary-600/25 transition-all text-sm"
              @click="uiStore.toggleCartDrawer(false)"
            >
              {{ $t('cart.checkout') }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useUIStore } from '@/stores/ui'
import { XMarkIcon, ShoppingBagIcon, TrashIcon } from '@heroicons/vue/24/outline'

const cartStore = useCartStore()
const uiStore = useUIStore()
</script>

<style scoped>
.slide-right-enter-active,
.slide-right-leave-active {
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-right-enter-active > div:last-child,
.slide-right-leave-active > div:last-child {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-right-enter-from,
.slide-right-leave-to {
  opacity: 0;
}
.slide-right-enter-from > div:last-child,
.slide-right-leave-to > div:last-child {
  transform: translateX(100%);
}
</style>
