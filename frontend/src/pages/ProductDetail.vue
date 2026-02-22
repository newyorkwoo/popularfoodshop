<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm text-gray-400 mb-8">
      <router-link to="/" class="hover:text-primary-600 transition-colors">{{ $t('common.home') }}</router-link>
      <span class="text-gray-300">/</span>
      <router-link to="/products" class="hover:text-primary-600 transition-colors">商品列表</router-link>
      <span class="text-gray-300">/</span>
      <span class="text-gray-700 font-medium line-clamp-1">{{ product?.name || '...' }}</span>
    </nav>

    <!-- Loading -->
    <div v-if="loading" class="grid lg:grid-cols-2 gap-8">
      <BaseSkeleton width="100%" height="500px" />
      <div class="space-y-4">
        <BaseSkeleton width="60%" height="24px" />
        <BaseSkeleton width="90%" height="32px" />
        <BaseSkeleton width="40%" height="28px" />
        <BaseSkeleton width="100%" height="200px" />
      </div>
    </div>

    <!-- Archived / unavailable -->
    <div v-else-if="product && isArchived" class="text-center py-20">
      <h2 class="text-xl font-bold text-gray-700 mb-2">此商品已下架</h2>
      <p class="text-gray-500 mb-6">很抱歉，此商品目前無法購買。</p>
      <router-link to="/products" class="text-primary-600 hover:underline font-medium">瀏覽其他商品</router-link>
    </div>

    <!-- Product -->
    <div v-else-if="product" class="grid lg:grid-cols-2 gap-8 lg:gap-12">
      <!-- Gallery -->
      <div class="space-y-4">
        <div class="aspect-square bg-gray-50 rounded-2xl overflow-hidden border border-gray-100 shadow-sm">
          <img
            :src="currentImage"
            :alt="product.name"
            class="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
          />
        </div>
        <div v-if="product.images?.length > 1" class="flex gap-2.5 overflow-x-auto pb-2">
          <button
            v-for="(img, i) in product.images"
            :key="i"
            class="w-20 h-20 shrink-0 rounded-xl overflow-hidden border-2 transition-all duration-200 hover:scale-105"
            :class="selectedImageIndex === i ? 'border-primary-600 ring-2 ring-primary-100' : 'border-gray-200 hover:border-gray-300'"
            @click="selectedImageIndex = i"
          >
            <img :src="img" :alt="`${product.name} ${i+1}`" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>

      <!-- Info -->
      <div>
        <p v-if="product.brand" class="text-sm text-gray-500 uppercase tracking-wide mb-1">{{ product.brand }}</p>
        <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>

        <!-- Rating -->
        <div v-if="product.rating" class="flex items-center gap-2.5 mb-5">
          <div class="flex gap-0.5">
            <StarIcon
              v-for="i in 5"
              :key="i"
              class="w-5 h-5"
              :class="i <= Math.round(product.rating) ? 'text-amber-400 fill-amber-400' : 'text-gray-200'"
            />
          </div>
          <span class="text-sm text-gray-500">{{ product.rating }} ({{ product.reviewCount }} 則評價)</span>
        </div>

        <!-- Price -->
        <div class="flex items-baseline gap-3 mb-6 bg-gray-50 rounded-xl px-5 py-4">
          <span class="text-3xl font-extrabold" :class="product.salePrice ? 'text-red-600' : 'text-gray-900'">
            NT${{ (product.salePrice || product.price).toLocaleString() }}
          </span>
          <span v-if="product.salePrice" class="text-lg text-gray-400 line-through">
            NT${{ product.price.toLocaleString() }}
          </span>
          <BaseBadge v-if="product.salePrice" variant="danger">
            省 NT${{ (product.price - product.salePrice).toLocaleString() }}
          </BaseBadge>
        </div>

        <!-- Stock status -->
        <div class="flex items-center gap-2 mb-6">
          <span
            class="w-2.5 h-2.5 rounded-full animate-pulse"
            :class="product.inStock !== false ? 'bg-green-500' : 'bg-red-500'"
          />
          <span class="text-sm font-medium" :class="product.inStock !== false ? 'text-green-700' : 'text-red-700'">
            {{ product.inStock !== false ? $t('product.inStock') : $t('product.outOfStock') }}
          </span>
        </div>

        <!-- Quantity -->
        <div class="flex items-center gap-4 mb-6">
          <span class="text-sm font-semibold text-gray-700">數量</span>
          <div class="flex items-center border border-gray-200 rounded-xl overflow-hidden">
            <button class="px-3.5 py-2.5 text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors" @click="quantity = Math.max(1, quantity - 1)">−</button>
            <input v-model.number="quantity" type="number" min="1" class="w-16 text-center border-x border-gray-200 py-2.5 text-sm font-medium bg-gray-50" />
            <button class="px-3.5 py-2.5 text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors" @click="quantity++">+</button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 mb-8">
          <BaseButton size="lg" class="flex-1" :disabled="product.inStock === false" @click="handleAddToCart">
            <ShoppingBagIcon class="w-5 h-5 mr-2" />
            {{ $t('product.addToCart') }}
          </BaseButton>
          <BaseButton variant="outline" size="lg" @click="handleToggleWishlist">
            <HeartIconSolid v-if="isWishlisted" class="w-5 h-5 text-red-500" />
            <HeartIcon v-else class="w-5 h-5" />
          </BaseButton>
        </div>

        <!-- Tabs -->
        <div class="border-t border-gray-100 mt-2">
          <div class="flex gap-1">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              class="py-3.5 px-4 text-sm font-semibold border-b-2 transition-all"
              :class="activeTab === tab.key ? 'border-primary-600 text-primary-600 bg-primary-50/50' : 'border-transparent text-gray-400 hover:text-gray-600 hover:bg-gray-50'"
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
            </button>
          </div>
          <div class="py-5">
            <div v-if="activeTab === 'description'" class="prose prose-sm max-w-none text-gray-600 leading-relaxed">
              <p>{{ product.description || '暫無商品描述。' }}</p>
            </div>
            <div v-else-if="activeTab === 'nutrition'" class="text-sm text-gray-600 leading-relaxed">
              <p>{{ product.nutrition || '暫無營養資訊。' }}</p>
            </div>
            <div v-else-if="activeTab === 'reviews'">
              <p class="text-sm text-gray-400">{{ $t('product.reviews') }}功能即將推出。</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Related products -->
    <section v-if="relatedProducts.length > 0" class="mt-20">
      <h2 class="text-2xl font-bold text-gray-900 mb-8">{{ $t('product.relatedProducts') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 md:gap-6">
        <ProductCard v-for="p in relatedProducts" :key="p.id" :product="p" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useUIStore } from '@/stores/ui'
import { getProductBySlug, getActiveProducts, loadProductStatus, getProductStatus } from '@/data/products'
import ProductCard from '@/components/product/ProductCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseSkeleton from '@/components/ui/BaseSkeleton.vue'
import { StarIcon, HeartIcon, ShoppingBagIcon } from '@heroicons/vue/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/vue/24/solid'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const uiStore = useUIStore()

const loading = ref(true)
const product = ref(null)
const quantity = ref(1)
const selectedImageIndex = ref(0)
const activeTab = ref('description')

const tabs = [
  { key: 'description', label: '商品描述' },
  { key: 'nutrition', label: '營養資訊' },
  { key: 'reviews', label: '商品評價' },
]

const currentImage = computed(() => {
  if (product.value?.images?.length) {
    return product.value.images[selectedImageIndex.value]
  }
  return product.value?.image || 'https://placehold.co/600x600/f3f4f6/9ca3af?text=No+Image'
})

const isWishlisted = computed(() => product.value && wishlistStore.isInWishlist(product.value.id))

const isArchived = computed(() => {
  if (!product.value) return false
  const s = getProductStatus()[String(product.value.id)]
  return s === 'archived'
})

const relatedProducts = ref([])

function handleAddToCart() {
  if (!product.value) return
  const success = cartStore.addItem(product.value, quantity.value)
  if (success) {
    uiStore.showToast('已加入購物車', 'success')
    uiStore.toggleCartDrawer(true)
  } else {
    uiStore.showToast('已達庫存上限', 'warning')
  }
}

function handleToggleWishlist() {
  if (!product.value) return
  const added = wishlistStore.toggleWishlist(product.value)
  uiStore.showToast(added ? '已加入收藏' : '已移除收藏', added ? 'success' : 'info')
}

async function loadProduct() {
  loading.value = true
  selectedImageIndex.value = 0
  quantity.value = 1
  try {
    // Look up product from shared catalog by slug
    const slug = route.params.slug
    const found = getProductBySlug(slug)
    if (found) {
      product.value = { ...found }
    } else {
      // Product not found — show 404
      router.replace({ name: 'NotFound', params: { pathMatch: ['product', slug] } })
      return
    }
    // Related products: pick up to 4 products that aren't the current one
    relatedProducts.value = getActiveProducts()
      .filter((p) => p.id !== product.value.id)
      .slice(0, 4)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadProductStatus()
  loadProduct()
})
watch(() => route.params.slug, loadProduct)
</script>
