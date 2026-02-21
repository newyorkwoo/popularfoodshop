<template>
  <div>
    <h2 class="text-xl font-bold text-gray-900 mb-6">我的收藏</h2>

    <div v-if="wishlistStore.items.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <ProductCard v-for="p in wishlistStore.items" :key="p.id" :product="p" />
    </div>
    <div v-else class="text-center py-16">
      <HeartIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-700 mb-2">收藏清單是空的</h3>
      <p class="text-gray-500 mb-6">將喜歡的商品加入收藏吧</p>
      <router-link to="/products" class="text-primary-600 hover:underline font-medium">瀏覽商品</router-link>
    </div>
  </div>
</template>

<script setup>
import { HeartIcon } from '@heroicons/vue/24/outline'
import { useWishlistStore } from '@/stores/wishlist'
import ProductCard from '@/components/product/ProductCard.vue'

const wishlistStore = useWishlistStore()
</script>
