<template>
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Brand Header -->
      <div class="flex items-center gap-6 mb-8 bg-white rounded-xl border border-gray-200 p-6">
        <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center overflow-hidden flex-shrink-0">
          <img :src="brand.logo" :alt="brand.name" class="w-16 h-16 object-contain" />
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">{{ brand.name }}</h1>
          <p class="text-gray-500 mt-1">{{ brand.description }}</p>
          <p class="text-sm text-gray-400 mt-2">{{ brand.productCount }} 項商品</p>
        </div>
      </div>

      <!-- Products -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>

      <div v-if="!isBrandActive" class="text-center py-20">
        <p class="text-gray-400 text-lg">此品牌目前暫停營業</p>
      </div>

      <div v-else-if="!products.length" class="text-center py-20">
        <p class="text-gray-500">此品牌尚無商品</p>
      </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '@/components/product/ProductCard.vue'
import { getProductsByBrand } from '@/data/products'
import { useAdminBrandStore } from '@/stores/adminBrand'
import { useAdminProductStore } from '@/stores/adminProduct'

const route = useRoute()
const adminBrandStore = useAdminBrandStore()
const adminProductStore = useAdminProductStore()

// Brand catalog with descriptions
const brandCatalog = {
  'wagyu-shop': { name: '和牛專門店', description: '嚴選日本A5等級和牛，產地直送，品質保證。', logo: 'https://placehold.co/100x100/FFF3E0/EA580C?text=和牛' },
  'mediterranean': { name: '地中海莊園', description: '來自地中海沿岸的頂級橄欖油與天然食材。', logo: 'https://placehold.co/100x100/F0FDF4/16A34A?text=地中海' },
  'taiwan-tea': { name: '台灣茶莊', description: '精選台灣高山茶園，傳承百年製茶工藝。', logo: 'https://placehold.co/100x100/ECFDF5/059669?text=茶莊' },
  'french-sweets': { name: '法國甜品屋', description: '法式經典甜點與手工餅乾，優雅的味覺饗宴。', logo: 'https://placehold.co/100x100/FEF2F2/DC2626?text=法國' },
  'hokkaido-farm': { name: '北海道牧場', description: '北海道純淨牧場直送，新鮮乳製品與甜點。', logo: 'https://placehold.co/100x100/EFF6FF/2563EB?text=北海道' },
  'italian-food': { name: '義式美食', description: '道地義大利食材，松露、起司與頂級橄欖油。', logo: 'https://placehold.co/100x100/F5F3FF/7C3AED?text=義式' },
  'organic-farm': { name: '有機農場', description: '通過有機認證的天然食品，吃得安心又健康。', logo: 'https://placehold.co/100x100/F0FDF4/15803D?text=有機' },
  'korean-taste': { name: '韓國美味', description: '正宗韓國調味料與零食，在家重現韓式風味。', logo: 'https://placehold.co/100x100/FEF9C3/CA8A04?text=韓國' },
  'thai-cuisine': { name: '泰式料理', description: '泰國道地香料與醬料，酸辣鮮香一次滿足。', logo: 'https://placehold.co/100x100/FFF7ED/EA580C?text=泰式' },
  'german-craft': { name: '德國工藝', description: '德國精工食品，啤酒、香腸與巧克力。', logo: 'https://placehold.co/100x100/F1F5F9/475569?text=德國' },
}

const slug = computed(() => route.params.slug)

const brandInfo = computed(() => brandCatalog[slug.value] || { name: slug.value, description: '', logo: 'https://placehold.co/100x100/F3F4F6/6B7280?text=Brand' })

// Check if this brand is disabled in admin
const isBrandActive = computed(() => {
  const adminBrand = adminBrandStore.brands.find(b => b.slug === slug.value)
  return adminBrand ? adminBrand.active : true
})

// If brand is disabled, show no products; otherwise filter out archived products
const products = computed(() => {
  if (!isBrandActive.value) return []
  const allBrandProducts = getProductsByBrand(slug.value)
  // Build a set of archived product IDs from admin store
  const archivedIds = new Set(
    adminProductStore.products
      .filter(p => p.status === 'archived')
      .map(p => p.id)
  )
  return allBrandProducts.filter(p => !archivedIds.has(p.id))
})

const brand = computed(() => ({
  ...brandInfo.value,
  slug: slug.value,
  productCount: products.value.length,
}))
</script>
