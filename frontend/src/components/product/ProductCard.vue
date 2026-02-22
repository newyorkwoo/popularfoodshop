<template>
  <div class="group bg-white rounded-2xl border border-gray-100 overflow-hidden card-hover transition-all duration-300">
    <!-- Image -->
    <router-link :to="{ name: 'ProductDetail', params: { slug: product.slug } }" class="block relative aspect-square overflow-hidden bg-gray-50">
      <img
        :src="product.image || product.images?.[0] || 'https://placehold.co/400x400/f3f4f6/9ca3af?text=No+Image'"
        :alt="product.name"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
        loading="lazy"
      />
      <!-- Hover overlay -->
      <div class="absolute inset-0 bg-linear-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      <!-- Badges -->
      <div class="absolute top-3 left-3 flex flex-col gap-1.5">
        <span v-if="product.isNew" class="px-2.5 py-1 bg-primary-600 text-white text-[11px] font-semibold rounded-lg shadow-sm badge-shine">
          {{ $t('product.newArrival') }}
        </span>
        <span v-if="discountPercent > 0" class="px-2.5 py-1 bg-red-500 text-white text-[11px] font-semibold rounded-lg shadow-sm">
          -{{ discountPercent }}%
        </span>
      </div>
      <!-- Wishlist -->
      <button
        class="absolute top-3 right-3 p-2 bg-white/90 backdrop-blur-sm rounded-full shadow-md opacity-0 group-hover:opacity-100 transition-all duration-300 hover:bg-white hover:scale-110 active:scale-95"
        @click.prevent="toggleWishlist"
      >
        <HeartIconSolid v-if="isWishlisted" class="w-5 h-5 text-red-500" />
        <HeartIcon v-else class="w-5 h-5 text-gray-500" />
      </button>
    </router-link>

    <!-- Info -->
    <div class="p-4">
      <!-- Brand -->
      <p v-if="product.brand" class="text-[11px] text-gray-400 uppercase tracking-wider font-medium mb-1.5">{{ product.brand }}</p>

      <!-- Name -->
      <router-link
        :to="{ name: 'ProductDetail', params: { slug: product.slug } }"
        class="block text-sm font-semibold text-gray-800 line-clamp-2 hover:text-primary-600 transition-colors min-h-10"
      >
        {{ product.name }}
      </router-link>

      <!-- Price -->
      <div class="flex items-baseline gap-2 mt-2.5">
        <span class="text-lg font-bold" :class="product.salePrice ? 'text-red-600' : 'text-gray-900'">
          NT${{ (product.salePrice || product.price || 0).toLocaleString() }}
        </span>
        <span v-if="product.salePrice" class="text-xs text-gray-400 line-through">
          NT${{ (product.price || 0).toLocaleString() }}
        </span>
      </div>

      <!-- Rating -->
      <div v-if="product.rating" class="flex items-center gap-1.5 mt-2">
        <div class="flex gap-0.5">
          <StarIcon
            v-for="i in 5"
            :key="i"
            class="w-3.5 h-3.5"
            :class="i <= Math.round(product.rating) ? 'text-amber-400 fill-amber-400' : 'text-gray-200'"
          />
        </div>
        <span class="text-[11px] text-gray-400">({{ product.reviewCount || 0 }})</span>
      </div>

      <!-- Add to cart -->
      <button
        class="w-full mt-4 py-2.5 text-sm font-semibold rounded-xl transition-all duration-300"
        :class="product.inStock === false
          ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
          : 'bg-gray-900 text-white hover:bg-primary-600 hover:shadow-lg hover:shadow-primary-600/25 active:scale-[0.98]'"
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
