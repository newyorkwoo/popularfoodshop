<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm text-gray-500 mb-6">
      <router-link to="/" class="hover:text-primary-600">{{ $t('common.home') }}</router-link>
      <span>/</span>
      <span class="text-gray-900">商品列表</span>
    </nav>

    <div class="flex gap-8">
      <!-- Sidebar Filters (desktop) -->
      <aside class="hidden lg:block w-64 shrink-0">
        <div class="sticky top-24 space-y-6">
          <!-- Categories -->
          <div>
            <h3 class="font-semibold text-gray-900 mb-3">{{ $t('product.filterCategory') }}</h3>
            <ul class="space-y-2">
              <li v-for="cat in categories" :key="cat.slug">
                <button
                  class="text-sm transition-colors"
                  :class="productStore.filters.category === cat.slug ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-gray-900'"
                  @click="toggleFilter('category', cat.slug)"
                >
                  {{ cat.name }}
                </button>
              </li>
            </ul>
          </div>

          <!-- Price range -->
          <div>
            <h3 class="font-semibold text-gray-900 mb-3">{{ $t('product.filterPrice') }}</h3>
            <ul class="space-y-2">
              <li v-for="range in priceRanges" :key="range.label">
                <button
                  class="text-sm text-gray-600 hover:text-gray-900 transition-colors"
                  @click="setPrice(range.min, range.max)"
                >
                  {{ range.label }}
                </button>
              </li>
            </ul>
          </div>

          <!-- Clear filters -->
          <button
            v-if="productStore.activeFiltersCount > 0"
            class="text-sm text-red-600 hover:text-red-700 font-medium"
            @click="productStore.clearFilters()"
          >
            清除所有篩選 ({{ productStore.activeFiltersCount }})
          </button>
        </div>
      </aside>

      <!-- Main content -->
      <div class="flex-1 min-w-0">
        <!-- Toolbar -->
        <div class="flex items-center justify-between mb-6">
          <p class="text-sm text-gray-500">
            共 <span class="font-medium text-gray-900">{{ productStore.pagination.total }}</span> 件商品
          </p>
          <div class="flex items-center gap-3">
            <!-- Mobile filter toggle -->
            <button class="lg:hidden flex items-center gap-1 text-sm text-gray-700 border rounded-lg px-3 py-2" @click="showMobileFilters = true">
              <FunnelIcon class="w-4 h-4" />
              篩選
            </button>
            <!-- Sort -->
            <select
              v-model="productStore.filters.sort"
              class="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:border-primary-500 focus:ring-1 focus:ring-primary-200"
              @change="loadProducts"
            >
              <option value="newest">{{ $t('product.sortNewest') }}</option>
              <option value="best-selling">{{ $t('product.sortBestSelling') }}</option>
              <option value="price-asc">{{ $t('product.sortPriceAsc') }}</option>
              <option value="price-desc">{{ $t('product.sortPriceDesc') }}</option>
              <option value="discount">{{ $t('product.sortDiscount') }}</option>
            </select>
          </div>
        </div>

        <!-- Product grid -->
        <div v-if="productStore.loading" class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
          <div v-for="i in 12" :key="i" class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <BaseSkeleton width="100%" height="250px" shape="rect" />
            <div class="p-4 space-y-2">
              <BaseSkeleton width="60%" height="14px" />
              <BaseSkeleton width="90%" height="14px" />
              <BaseSkeleton width="40%" height="20px" />
            </div>
          </div>
        </div>

        <div v-else-if="productStore.products.length === 0" class="text-center py-20">
          <MagnifyingGlassIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p class="text-lg text-gray-500">{{ $t('common.noResults') }}</p>
        </div>

        <div v-else class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
          <ProductCard v-for="product in productStore.products" :key="product.id" :product="product" />
        </div>

        <!-- Pagination -->
        <div v-if="productStore.pagination.totalPages > 1" class="mt-10">
          <BasePagination
            :model-value="productStore.pagination.page"
            :total-pages="productStore.pagination.totalPages"
            @update:model-value="changePage"
          />
        </div>
      </div>
    </div>

    <!-- Mobile Filter Drawer -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showMobileFilters" class="fixed inset-0 bg-black/50 z-50 lg:hidden" @click="showMobileFilters = false" />
      </Transition>
      <Transition name="slide-left">
        <div v-if="showMobileFilters" class="fixed inset-y-0 right-0 w-80 max-w-full bg-white z-50 shadow-2xl lg:hidden overflow-y-auto">
          <div class="flex items-center justify-between p-4 border-b border-gray-200">
            <h3 class="text-lg font-bold text-gray-900">篩選條件</h3>
            <button class="p-2 text-gray-500 hover:text-gray-700" @click="showMobileFilters = false">
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          <div class="p-4 space-y-6">
            <!-- Categories -->
            <div>
              <h4 class="font-semibold text-gray-900 mb-3">{{ $t('product.filterCategory') }}</h4>
              <ul class="space-y-2">
                <li v-for="cat in categories" :key="cat.slug">
                  <button
                    class="text-sm transition-colors w-full text-left py-1"
                    :class="productStore.filters.category === cat.slug ? 'text-primary-600 font-medium' : 'text-gray-600 hover:text-gray-900'"
                    @click="toggleFilter('category', cat.slug); showMobileFilters = false"
                  >
                    {{ cat.name }}
                  </button>
                </li>
              </ul>
            </div>

            <!-- Price range -->
            <div>
              <h4 class="font-semibold text-gray-900 mb-3">{{ $t('product.filterPrice') }}</h4>
              <ul class="space-y-2">
                <li v-for="range in priceRanges" :key="range.label">
                  <button
                    class="text-sm text-gray-600 hover:text-gray-900 transition-colors w-full text-left py-1"
                    @click="setPrice(range.min, range.max); showMobileFilters = false"
                  >
                    {{ range.label }}
                  </button>
                </li>
              </ul>
            </div>

            <!-- Clear filters -->
            <button
              v-if="productStore.activeFiltersCount > 0"
              class="w-full text-sm text-red-600 hover:text-red-700 font-medium text-center py-2 border border-red-200 rounded-lg"
              @click="productStore.clearFilters(); showMobileFilters = false; loadProducts()"
            >
              清除所有篩選 ({{ productStore.activeFiltersCount }})
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/product'
import { allProducts } from '@/data/products'
import { useAdminProductStore } from '@/stores/adminProduct'
import ProductCard from '@/components/product/ProductCard.vue'
import BasePagination from '@/components/ui/BasePagination.vue'
import BaseSkeleton from '@/components/ui/BaseSkeleton.vue'
import { FunnelIcon, MagnifyingGlassIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const adminProductStore = useAdminProductStore()
const showMobileFilters = ref(false)

const categories = [
  { name: '人氣零食', slug: 'popular-snacks' },
  { name: '精選茶品', slug: 'fine-tea' },
  { name: '進口巧克力', slug: 'imported-chocolate' },
  { name: '健康穀物', slug: 'healthy-grains' },
  { name: '有機食品', slug: 'organic-food' },
  { name: '日本零食', slug: 'japanese-snacks' },
  { name: '手工餅乾', slug: 'handmade-cookies' },
  { name: '果乾蜜餞', slug: 'dried-fruits' },
  { name: '飲品', slug: 'beverages' },
  { name: '調味料', slug: 'seasonings' },
]

const priceRanges = [
  { label: 'NT$100 以下', min: 0, max: 100 },
  { label: 'NT$100 - $300', min: 100, max: 300 },
  { label: 'NT$300 - $500', min: 300, max: 500 },
  { label: 'NT$500 - $1,000', min: 500, max: 1000 },
  { label: 'NT$1,000 以上', min: 1000, max: null },
]

function toggleFilter(key, value) {
  if (productStore.filters[key] === value) {
    productStore.setFilter(key, null)
  } else {
    productStore.setFilter(key, value)
  }
  loadProducts()
}

function setPrice(min, max) {
  productStore.setFilter('priceMin', min)
  productStore.setFilter('priceMax', max)
  loadProducts()
}

function changePage(page) {
  productStore.setPage(page)
  loadProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function loadProducts() {
  productStore.loading = true

  // Start with full catalog, excluding archived products
  const archivedIds = new Set(
    adminProductStore.products
      .filter(p => p.status === 'archived')
      .map(p => p.id)
  )
  let filtered = allProducts.filter(p => !archivedIds.has(p.id))

  // Category filter
  const categoryFilter = productStore.filters.category
  if (categoryFilter) {
    filtered = filtered.filter(p => p.category === categoryFilter)
  }

  // Price filter
  const priceMin = productStore.filters.priceMin
  const priceMax = productStore.filters.priceMax
  if (priceMin != null) {
    filtered = filtered.filter(p => (p.salePrice || p.price) >= priceMin)
  }
  if (priceMax != null) {
    filtered = filtered.filter(p => (p.salePrice || p.price) <= priceMax)
  }

  // Sort
  const sort = productStore.filters.sort
  if (sort === 'price-asc') {
    filtered.sort((a, b) => (a.salePrice || a.price) - (b.salePrice || b.price))
  } else if (sort === 'price-desc') {
    filtered.sort((a, b) => (b.salePrice || b.price) - (a.salePrice || a.price))
  } else if (sort === 'popular') {
    filtered.sort((a, b) => b.reviewCount - a.reviewCount)
  } else if (sort === 'rating') {
    filtered.sort((a, b) => b.rating - a.rating)
  }
  // 'newest' keeps the default order from the catalog

  productStore.products = filtered
  productStore.pagination = {
    page: 1,
    perPage: 24,
    total: filtered.length,
    totalPages: Math.max(1, Math.ceil(filtered.length / 24)),
  }
  productStore.loading = false
}

onMounted(() => {
  // Use route param slug as initial category filter
  const slug = route.params.slug
  if (slug) {
    productStore.setFilter('category', slug)
  }
  if (route.query.sort) {
    productStore.setFilter('sort', route.query.sort)
  }
  loadProducts()
})

watch(() => route.params.slug, (slug) => {
  if (slug) {
    productStore.setFilter('category', slug)
  } else {
    productStore.setFilter('category', null)
  }
  loadProducts()
})
</script>
