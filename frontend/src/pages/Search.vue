<template>
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Search Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-2">
          搜尋結果：<span class="text-primary-600">「{{ query }}」</span>
        </h1>
        <p class="text-gray-500">共找到 {{ filteredProducts.length }} 項商品</p>
      </div>

      <!-- Search Input -->
      <div class="relative mb-8 max-w-xl">
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          v-model="searchInput"
          @keyup.enter="doSearch"
          type="text"
          placeholder="搜尋商品名稱、品牌..."
          class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>

      <!-- Results -->
      <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <BaseSkeleton v-for="i in 8" :key="i" shape="rect" height="320px" />
      </div>
      <div v-else-if="filteredProducts.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <ProductCard v-for="p in filteredProducts" :key="p.id" :product="p" />
      </div>
      <div v-else class="text-center py-20">
        <MagnifyingGlassIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-700 mb-2">找不到相關商品</h3>
        <p class="text-gray-500 mb-6">請嘗試不同的關鍵字</p>
        <router-link to="/products" class="text-primary-600 hover:underline font-medium">瀏覽所有商品</router-link>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import ProductCard from '@/components/product/ProductCard.vue'
import BaseSkeleton from '@/components/ui/BaseSkeleton.vue'
import { searchProducts, loadProductStatus } from '@/data/products'

const route = useRoute()
const router = useRouter()

const query = computed(() => route.query.q || '')
const searchInput = ref(query.value)
const loading = ref(false)

const filteredProducts = computed(() => {
  return searchProducts(query.value)
})

function doSearch() {
  if (searchInput.value.trim()) {
    router.push({ path: '/search', query: { q: searchInput.value.trim() } })
  }
}

watch(query, (v) => { searchInput.value = v })

onMounted(async () => {
  await loadProductStatus()
  loading.value = true
  setTimeout(() => { loading.value = false }, 500)
})
</script>
