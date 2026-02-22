<template>
    <div class="max-w-7xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">品牌專區</h1>

      <!-- Brand Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <router-link
          v-for="brand in brands"
          :key="brand.id"
          :to="`/brand/${brand.slug}`"
          class="group bg-white border border-gray-200 rounded-xl p-6 text-center hover:shadow-lg hover:border-primary-300 transition"
        >
          <div class="w-20 h-20 mx-auto mb-4 bg-gray-50 rounded-full flex items-center justify-center overflow-hidden">
            <img :src="brand.logo" :alt="brand.name" class="w-14 h-14 object-contain" />
          </div>
          <h3 class="font-semibold text-gray-900 group-hover:text-primary-600 transition">{{ brand.name }}</h3>
          <p class="text-xs text-gray-500 mt-1">{{ brand.productCount }} 項商品</p>
        </router-link>
      </div>
    </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { getProductsByBrand, loadProductStatus } from '@/data/products'

const statusReady = ref(false)

const brandList = [
  { id: 1, name: '和牛專門店', slug: 'wagyu-shop', logo: 'https://placehold.co/100x100/FFF3E0/EA580C?text=和牛' },
  { id: 2, name: '地中海莊園', slug: 'mediterranean', logo: 'https://placehold.co/100x100/F0FDF4/16A34A?text=地中海' },
  { id: 3, name: '台灣茶莊', slug: 'taiwan-tea', logo: 'https://placehold.co/100x100/ECFDF5/059669?text=茶莊' },
  { id: 4, name: '法國甜品屋', slug: 'french-sweets', logo: 'https://placehold.co/100x100/FEF2F2/DC2626?text=法國' },
  { id: 5, name: '北海道牧場', slug: 'hokkaido-farm', logo: 'https://placehold.co/100x100/EFF6FF/2563EB?text=北海道' },
  { id: 6, name: '義式美食', slug: 'italian-food', logo: 'https://placehold.co/100x100/F5F3FF/7C3AED?text=義式' },
  { id: 7, name: '有機農場', slug: 'organic-farm', logo: 'https://placehold.co/100x100/F0FDF4/15803D?text=有機' },
  { id: 8, name: '韓國美味', slug: 'korean-taste', logo: 'https://placehold.co/100x100/FEF9C3/CA8A04?text=韓國' },
  { id: 9, name: '泰式料理', slug: 'thai-cuisine', logo: 'https://placehold.co/100x100/FFF7ED/EA580C?text=泰式' },
  { id: 10, name: '德國工藝', slug: 'german-craft', logo: 'https://placehold.co/100x100/F1F5F9/475569?text=德國' },
]

// Compute real product counts from the shared catalog
const brands = computed(() =>
  brandList.map(b => ({
    ...b,
    productCount: getProductsByBrand(b.slug).length,
  }))
)

onMounted(async () => {
  await loadProductStatus()
  statusReady.value = true
})
</script>
