<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm text-gray-500 mb-6">
      <router-link to="/" class="hover:text-primary-600">{{ $t('common.home') }}</router-link>
      <span>/</span>
      <router-link to="/products" class="hover:text-primary-600">商品列表</router-link>
      <span>/</span>
      <span class="text-gray-900 line-clamp-1">{{ product?.name || '...' }}</span>
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
        <div class="aspect-square bg-gray-100 rounded-2xl overflow-hidden">
          <img
            :src="currentImage"
            :alt="product.name"
            class="w-full h-full object-cover"
          />
        </div>
        <div v-if="product.images?.length > 1" class="flex gap-2 overflow-x-auto pb-2">
          <button
            v-for="(img, i) in product.images"
            :key="i"
            class="w-20 h-20 shrink-0 rounded-lg overflow-hidden border-2 transition-colors"
            :class="selectedImageIndex === i ? 'border-primary-600' : 'border-gray-200'"
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
        <div v-if="product.rating" class="flex items-center gap-2 mb-4">
          <div class="flex">
            <StarIcon
              v-for="i in 5"
              :key="i"
              class="w-5 h-5"
              :class="i <= Math.round(product.rating) ? 'text-yellow-400' : 'text-gray-200'"
            />
          </div>
          <span class="text-sm text-gray-600">{{ product.rating }} ({{ product.reviewCount }} 則評價)</span>
        </div>

        <!-- Price -->
        <div class="flex items-center gap-3 mb-6">
          <span class="text-3xl font-bold" :class="product.salePrice ? 'text-red-600' : 'text-gray-900'">
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
            class="w-2 h-2 rounded-full"
            :class="product.inStock !== false ? 'bg-green-500' : 'bg-red-500'"
          />
          <span class="text-sm" :class="product.inStock !== false ? 'text-green-700' : 'text-red-700'">
            {{ product.inStock !== false ? $t('product.inStock') : $t('product.outOfStock') }}
          </span>
        </div>

        <!-- Quantity -->
        <div class="flex items-center gap-4 mb-6">
          <span class="text-sm font-medium text-gray-700">數量</span>
          <div class="flex items-center border border-gray-300 rounded-lg">
            <button class="px-3 py-2 text-gray-600 hover:text-gray-900" @click="quantity = Math.max(1, quantity - 1)">−</button>
            <input v-model.number="quantity" type="number" min="1" class="w-16 text-center border-x border-gray-300 py-2 text-sm" />
            <button class="px-3 py-2 text-gray-600 hover:text-gray-900" @click="quantity++">+</button>
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
        <div class="border-t border-gray-200">
          <div class="flex gap-6 border-b border-gray-200">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              class="py-3 text-sm font-medium border-b-2 transition-colors"
              :class="activeTab === tab.key ? 'border-primary-600 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
            </button>
          </div>
          <div class="py-4">
            <div v-if="activeTab === 'description'" class="prose prose-sm max-w-none text-gray-600">
              <p>{{ product.description || '暫無商品描述。' }}</p>
            </div>
            <div v-else-if="activeTab === 'nutrition'" class="text-sm text-gray-600">
              <p>{{ product.nutrition || '暫無營養資訊。' }}</p>
            </div>
            <div v-else-if="activeTab === 'reviews'">
              <p class="text-sm text-gray-500">{{ $t('product.reviews') }}功能即將推出。</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Related products -->
    <section v-if="relatedProducts.length > 0" class="mt-16">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ $t('product.relatedProducts') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 md:gap-6">
        <ProductCard v-for="p in relatedProducts" :key="p.id" :product="p" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useUIStore } from '@/stores/ui'
import { useAdminProductStore } from '@/stores/adminProduct'
import { getProductBySlug, allProducts } from '@/data/products'
import ProductCard from '@/components/product/ProductCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseSkeleton from '@/components/ui/BaseSkeleton.vue'
import { StarIcon, HeartIcon, ShoppingBagIcon } from '@heroicons/vue/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/vue/24/solid'

const route = useRoute()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const uiStore = useUIStore()
const adminProductStore = useAdminProductStore()

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
  const adminP = adminProductStore.products.find(p => p.id === product.value.id)
  return adminP?.status === 'archived'
})

const archivedIds = computed(() => {
  return new Set(adminProductStore.products.filter(p => p.status === 'archived').map(p => p.id))
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
      // Fallback for unknown slugs
      product.value = {
        id: 999,
        name: slug?.replace(/-/g, ' ') || 'Sample Product',
        slug: slug,
        brand: 'Sample Brand',
        price: 580,
        salePrice: 480,
        image: 'https://placehold.co/600x600/FFF3E0/E65100?text=Product',
        images: [
          'https://placehold.co/600x600/FFF3E0/E65100?text=Image+1',
          'https://placehold.co/600x600/E8F5E9/2E7D32?text=Image+2',
          'https://placehold.co/600x600/E3F2FD/1565C0?text=Image+3',
        ],
        rating: 4.7,
        reviewCount: 128,
        inStock: true,
        description: '嚴選優質食材，遵循傳統工法製作，保留最純粹的美味。每一口都是對品質的堅持。',
        nutrition: '熱量：120kcal / 蛋白質：3g / 脂肪：5g / 碳水化合物：15g / 鈉：80mg',
        stock: 50,
      }
    }
    // Related products: pick up to 4 products that aren't the current one and not archived
    const archived = new Set(adminProductStore.products.filter(p => p.status === 'archived').map(p => p.id))
    relatedProducts.value = allProducts
      .filter((p) => p.id !== product.value.id && !archived.has(p.id))
      .slice(0, 4)
  } finally {
    loading.value = false
  }
}

onMounted(loadProduct)
watch(() => route.params.slug, loadProduct)
</script>
