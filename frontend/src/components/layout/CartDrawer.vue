<template>
  <transition name="slide-right">
    <div v-if="uiStore.cartDrawerOpen" class="fixed inset-0 z-50">
      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/50" @click="uiStore.toggleCartDrawer(false)" />

      <!-- Drawer -->
      <div class="absolute inset-y-0 right-0 w-96 max-w-[90vw] bg-white shadow-xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between px-4 h-16 border-b border-gray-200">
          <h2 class="text-lg font-bold text-gray-900">{{ $t('cart.title') }} ({{ cartStore.itemCount }})</h2>
          <button @click="uiStore.toggleCartDrawer(false)" class="p-2 text-gray-500 hover:text-gray-700">
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Free shipping progress -->
        <div v-if="cartStore.items.length > 0 && cartStore.freeShippingRemaining > 0" class="px-4 py-3 bg-secondary-50 border-b">
          <p class="text-sm text-secondary-700 mb-1">
            再消費 <strong>NT${{ cartStore.freeShippingRemaining }}</strong> 即享免運費！
          </p>
          <div class="h-1.5 bg-secondary-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-secondary-500 rounded-full transition-all duration-300"
              :style="{ width: cartStore.freeShippingProgress + '%' }"
            />
          </div>
        </div>

        <!-- Items -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="cartStore.items.length === 0" class="flex flex-col items-center justify-center h-full text-gray-400">
            <ShoppingBagIcon class="w-16 h-16 mb-4" />
            <p class="text-lg">{{ $t('cart.empty') }}</p>
            <router-link
              to="/products"
              class="mt-4 text-sm text-primary-600 hover:text-primary-700 font-medium"
              @click="uiStore.toggleCartDrawer(false)"
            >
              {{ $t('cart.continueShopping') }}
            </router-link>
          </div>

          <ul v-else class="divide-y divide-gray-100">
            <li v-for="item in cartStore.items" :key="`${item.productId}-${item.variantId}`" class="flex gap-3 p-4">
              <!-- Image -->
              <router-link
                :to="{ name: 'ProductDetail', params: { slug: item.slug } }"
                class="shrink-0 w-20 h-20 bg-gray-100 rounded-lg overflow-hidden"
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
                  class="text-sm font-medium text-gray-900 hover:text-primary-600 line-clamp-2"
                  @click="uiStore.toggleCartDrawer(false)"
                >
                  {{ item.name }}
                </router-link>
                <p v-if="item.variant" class="text-xs text-gray-500 mt-0.5">{{ item.variant.name }}: {{ item.variant.value }}</p>
                <div class="flex items-center justify-between mt-2">
                  <div class="flex items-center border border-gray-300 rounded-lg">
                    <button
                      class="px-2 py-1 text-gray-600 hover:text-gray-900 text-sm"
                      @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity - 1)"
                    >−</button>
                    <span class="px-2 text-sm text-gray-900 min-w-[2rem] text-center">{{ item.quantity }}</span>
                    <button
                      class="px-2 py-1 text-gray-600 hover:text-gray-900 text-sm"
                      @click="cartStore.updateQuantity(item.productId, item.variantId, item.quantity + 1)"
                    >+</button>
                  </div>
                  <p class="text-sm font-semibold text-gray-900">
                    NT${{ ((item.salePrice || item.price) * item.quantity).toLocaleString() }}
                  </p>
                </div>
              </div>

              <!-- Remove -->
              <button
                class="self-start text-gray-400 hover:text-red-500 p-1"
                @click="cartStore.removeItem(item.productId, item.variantId)"
              >
                <TrashIcon class="w-4 h-4" />
              </button>
            </li>
          </ul>
        </div>

        <!-- Footer -->
        <div v-if="cartStore.items.length > 0" class="border-t border-gray-200 p-4 space-y-3">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">{{ $t('cart.subtotal') }}</span>
            <span class="font-medium text-gray-900">NT${{ cartStore.subtotal.toLocaleString() }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">{{ $t('cart.shipping') }}</span>
            <span class="font-medium" :class="cartStore.shippingFee === 0 ? 'text-secondary-600' : 'text-gray-900'">
              {{ cartStore.shippingFee === 0 ? $t('cart.freeShipping') : `NT$${cartStore.shippingFee}` }}
            </span>
          </div>
          <div class="flex justify-between text-base font-bold pt-2 border-t border-gray-100">
            <span>{{ $t('cart.total') }}</span>
            <span class="text-primary-600">NT${{ cartStore.total.toLocaleString() }}</span>
          </div>
          <router-link
            to="/cart"
            class="block w-full text-center py-3 bg-gray-900 text-white font-medium rounded-lg hover:bg-gray-800 transition-colors"
            @click="uiStore.toggleCartDrawer(false)"
          >
            {{ $t('cart.title') }}
          </router-link>
          <router-link
            to="/checkout"
            class="block w-full text-center py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
            @click="uiStore.toggleCartDrawer(false)"
          >
            {{ $t('cart.checkout') }}
          </router-link>
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
  transition: opacity 0.3s ease;
}
.slide-right-enter-active > div:last-child,
.slide-right-leave-active > div:last-child {
  transition: transform 0.3s ease;
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
