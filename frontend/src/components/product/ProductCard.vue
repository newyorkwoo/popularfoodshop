<template>
  <div class="group bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-300">
    <!-- Image -->
    <router-link :to="{ name: 'ProductDetail', params: { slug: product.slug } }" class="block relative aspect-square overflow-hidden bg-gray-100">
      <img
        :src="product.image || product.images?.[0] || 'https://placehold.co/400x400/f3f4f6/9ca3af?text=No+Image'"
        :alt="product.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        loading="lazy"
      />
      <!-- Badges -->
      <div class="absolute top-2 left-2 flex flex-col gap-1">
        <span v-if="product.isNew" class="px-2 py-0.5 bg-primary-600 text-white text-xs font-medium rounded">
          {{ $t('product.newArrival') }}
        </span>
        <span v-if="discountPercent > 0" class="px-2 py-0.5 bg-red-500 text-white text-xs font-medium rounded">
          -{{ discountPercent }}%
        </span>
      </div>
      <!-- Wishlist -->
      <button
        class="absolute top-2 right-2 p-2 bg-white/80 backdrop-blur rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white"
        @click.prevent="toggleWishlist"
      >
        <HeartIconSolid v-if="isWishlisted" class="w-5 h-5 text-red-500" />
        <HeartIcon v-else class="w-5 h-5 text-gray-600" />
      </button>
    </router-link>

    <!-- Info -->
    <div class="p-4">
      <!-- Brand -->
      <p v-if="product.brand" class="text-xs text-gray-500 uppercase tracking-wide mb-1">{{ product.brand }}</p>

      <!-- Name -->
      <router-link
        :to="{ name: 'ProductDetail', params: { slug: product.slug } }"
        class="block text-sm font-medium text-gray-900 line-clamp-2 hover:text-primary-600 transition-colors min-h-[2.5rem]"
      >
        {{ product.name }}
      </router-link>

      <!-- Price -->
      <div class="flex items-center gap-2 mt-2">
        <span class="text-lg font-bold" :class="product.salePrice ? 'text-red-600' : 'text-gray-900'">
          NT${{ (product.salePrice || product.price || 0).toLocaleString() }}
        </span>
        <span v-if="product.salePrice" class="text-sm text-gray-400 line-through">
          NT${{ (product.price || 0).toLocaleString() }}
        </span>
      </div>

      <!-- Rating -->
      <div v-if="product.rating" class="flex items-center gap-1 mt-2">
        <div class="flex">
          <StarIcon
            v-for="i in 5"
            :key="i"
            class="w-3.5 h-3.5"
            :class="i <= Math.round(product.rating) ? 'text-yellow-400' : 'text-gray-200'"
          />
        </div>
        <span class="text-xs text-gray-500">({{ product.reviewCount || 0 }})</span>
      </div>

      <!-- Add to cart -->
      <button
        class="w-full mt-3 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="product.inStock === false
          ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
          : 'bg-gray-900 text-white hover:bg-primary-600'"
        :disabled="product.inStock === false"
        @click="handleAddToCart"
      >
        {{ product.inStock === false ? $t('product.outOfStock') : $t('product.addToCart') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useUIStore } from '@/stores/ui'
import { HeartIcon, StarIcon } from '@heroicons/vue/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/vue/24/solid'

const props = defineProps({
  product: { type: Object, required: true },
})

const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const uiStore = useUIStore()

const discountPercent = computed(() => {
  if (!props.product.salePrice || !props.product.price) return 0
  return Math.round((1 - props.product.salePrice / props.product.price) * 100)
})

const isWishlisted = computed(() => wishlistStore.isInWishlist(props.product.id))

function toggleWishlist() {
  const added = wishlistStore.toggleWishlist(props.product)
  uiStore.showToast(
    added ? '已加入收藏' : '已移除收藏',
    added ? 'success' : 'info'
  )
}

function handleAddToCart() {
  const success = cartStore.addItem(props.product)
  if (success) {
    uiStore.showToast('已加入購物車', 'success')
  } else {
    uiStore.showToast('已達庫存上限', 'warning')
  }
}
</script>
