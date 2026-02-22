<template>
  <div>
    <!-- Hero Banner -->
    <section class="relative bg-linear-to-br from-primary-700 via-primary-600 to-primary-800 text-white overflow-hidden">
      <div class="container mx-auto px-4 py-20 md:py-28 relative z-10">
        <div class="max-w-2xl">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-white/15 backdrop-blur-sm rounded-full text-sm font-medium mb-6">
            <SparklesIcon class="w-4 h-4 text-amber-300" />
            新品上架優惠中
          </div>
          <h1 class="text-4xl md:text-6xl font-extrabold leading-tight mb-5">
            精選全球美味<br /><span class="text-gradient-warm">盡在人氣美食</span>
          </h1>
          <p class="text-lg text-primary-100/90 mb-10 leading-relaxed max-w-lg">
            從日本零食到手工巧克力，從健康穀物到有機食品，為您嚴選世界各地優質美食。
          </p>
          <div class="flex flex-wrap gap-4">
            <router-link
              to="/products"
              class="inline-flex items-center gap-2.5 px-8 py-3.5 bg-white text-primary-700 font-bold rounded-full hover:bg-primary-50 hover:shadow-xl hover:shadow-white/20 transition-all duration-300 text-sm"
            >
              {{ $t('home.heroCTA') }}
              <ArrowRightIcon class="w-4 h-4" />
            </router-link>
            <router-link
              to="/products?sort=newest"
              class="inline-flex items-center gap-2 px-8 py-3.5 bg-white/10 text-white font-semibold rounded-full hover:bg-white/20 backdrop-blur-sm transition-all duration-300 border border-white/20 text-sm"
            >
              探索新品
            </router-link>
          </div>
        </div>
      </div>
      <!-- Decorative elements -->
      <div class="absolute inset-0 opacity-[0.07]">
        <div class="absolute -right-20 -top-20 w-120 h-120 bg-white rounded-full animate-pulse-soft" />
        <div class="absolute -left-10 -bottom-10 w-80 h-80 bg-white rounded-full animate-pulse-soft" style="animation-delay: 1s" />
        <div class="absolute right-1/3 top-1/2 w-48 h-48 bg-white rounded-full animate-float" />
      </div>
    </section>

    <!-- Category Showcase -->
    <section class="container mx-auto px-4 py-14">
      <div class="text-center mb-10">
        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-2">熱門分類</h2>
        <p class="text-gray-500 text-sm">探索各種美味分類，找到您的最愛</p>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <router-link
          v-for="(cat, i) in categories"
          :key="cat.slug"
          :to="{ name: 'ProductList', params: { slug: cat.slug } }"
          class="group flex flex-col items-center p-5 bg-white rounded-2xl border border-gray-100 hover:border-primary-200 hover:shadow-lg hover:shadow-primary-100/50 transition-all duration-300 hover:-translate-y-1"
          :style="{ animationDelay: i * 50 + 'ms' }"
        >
          <span class="text-4xl mb-3 group-hover:scale-110 transition-transform duration-300">{{ cat.icon }}</span>
          <span class="text-sm font-semibold text-gray-700 group-hover:text-primary-600 transition-colors">{{ cat.name }}</span>
        </router-link>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="bg-gray-50/80 py-14">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-2xl md:text-3xl font-bold text-gray-900">{{ $t('home.featuredTitle') }}</h2>
            <p class="text-gray-500 text-sm mt-1">為您精心挑選的人氣商品</p>
          </div>
          <router-link to="/products" class="text-sm text-primary-600 hover:text-primary-700 font-semibold flex items-center gap-1.5 hover:gap-2.5 transition-all">
            {{ $t('common.viewAll') }}
            <ArrowRightIcon class="w-4 h-4" />
          </router-link>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
          <ProductCard v-for="product in featuredProducts" :key="product.id" :product="product" />
        </div>
      </div>
    </section>

    <!-- Promotional Banner -->
    <section class="container mx-auto px-4 py-14">
      <div class="grid md:grid-cols-2 gap-6">
        <div class="group relative bg-linear-to-br from-emerald-500 to-emerald-700 rounded-2xl p-8 md:p-10 text-white overflow-hidden hover:shadow-xl hover:shadow-emerald-500/20 transition-all duration-500">
          <h3 class="text-2xl md:text-3xl font-bold mb-2">有機食品專區</h3>
          <p class="text-emerald-100 mb-6 text-sm md:text-base">精選認證有機食品，吃得安心又健康</p>
          <router-link
            to="/products?category=organic-food"
            class="inline-flex items-center gap-2 px-6 py-2.5 bg-white text-emerald-700 font-semibold rounded-full hover:bg-emerald-50 transition-colors text-sm"
          >
            立即選購
            <ArrowRightIcon class="w-4 h-4" />
          </router-link>
          <div class="absolute -right-8 -bottom-8 w-44 h-44 bg-white/10 rounded-full group-hover:scale-125 transition-transform duration-500" />
          <div class="absolute right-12 bottom-12 w-20 h-20 bg-white/5 rounded-full group-hover:scale-150 transition-transform duration-700" />
        </div>
        <div class="group relative bg-linear-to-br from-amber-500 to-orange-600 rounded-2xl p-8 md:p-10 text-white overflow-hidden hover:shadow-xl hover:shadow-amber-500/20 transition-all duration-500">
          <h3 class="text-2xl md:text-3xl font-bold mb-2">日本零食祭</h3>
          <p class="text-amber-100 mb-6 text-sm md:text-base">直送日本人氣零食，限時優惠中</p>
          <router-link
            to="/products?category=japanese-snacks"
            class="inline-flex items-center gap-2 px-6 py-2.5 bg-white text-amber-700 font-semibold rounded-full hover:bg-amber-50 transition-colors text-sm"
          >
            立即選購
            <ArrowRightIcon class="w-4 h-4" />
          </router-link>
          <div class="absolute -right-8 -bottom-8 w-44 h-44 bg-white/10 rounded-full group-hover:scale-125 transition-transform duration-500" />
          <div class="absolute right-12 bottom-12 w-20 h-20 bg-white/5 rounded-full group-hover:scale-150 transition-transform duration-700" />
        </div>
      </div>
    </section>

    <!-- New Arrivals -->
    <section class="container mx-auto px-4 py-14">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl md:text-3xl font-bold text-gray-900">新品上架</h2>
          <p class="text-gray-500 text-sm mt-1">最新到貨的優質好物</p>
        </div>
        <router-link to="/products?sort=newest" class="text-sm text-primary-600 hover:text-primary-700 font-semibold flex items-center gap-1.5 hover:gap-2.5 transition-all">
          {{ $t('common.viewAll') }}
          <ArrowRightIcon class="w-4 h-4" />
        </router-link>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
        <ProductCard v-for="product in newProducts" :key="product.id" :product="product" />
      </div>
    </section>

    <!-- Trust Badges -->
    <section class="bg-gray-900 text-white py-14 relative overflow-hidden">
      <div class="container mx-auto px-4 relative z-10">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 text-center">
          <div class="flex flex-col items-center group">
            <div class="w-16 h-16 bg-primary-500/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-primary-500/30 transition-colors">
              <ShieldCheckIcon class="w-8 h-8 text-primary-400" />
            </div>
            <h3 class="font-bold text-lg mb-1.5">{{ $t('home.trustAuth') }}</h3>
            <p class="text-sm text-gray-400 leading-relaxed">{{ $t('home.trustAuthDesc') }}</p>
          </div>
          <div class="flex flex-col items-center group">
            <div class="w-16 h-16 bg-primary-500/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-primary-500/30 transition-colors">
              <SparklesIcon class="w-8 h-8 text-primary-400" />
            </div>
            <h3 class="font-bold text-lg mb-1.5">{{ $t('home.trustQuality') }}</h3>
            <p class="text-sm text-gray-400 leading-relaxed">{{ $t('home.trustQualityDesc') }}</p>
          </div>
          <div class="flex flex-col items-center group">
            <div class="w-16 h-16 bg-primary-500/20 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-primary-500/30 transition-colors">
              <TruckIcon class="w-8 h-8 text-primary-400" />
            </div>
            <h3 class="font-bold text-lg mb-1.5">{{ $t('home.trustShipping') }}</h3>
            <p class="text-sm text-gray-400 leading-relaxed">{{ $t('home.trustShippingDesc') }}</p>
          </div>
        </div>
      </div>
      <!-- Decorative -->
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-1/4 w-72 h-72 bg-primary-500/5 rounded-full blur-3xl"></div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ProductCard from '@/components/product/ProductCard.vue'
import { useAdminProductStore } from '@/stores/adminProduct'
import {
  ArrowRightIcon,
  ShieldCheckIcon,
  SparklesIcon,
  TruckIcon,
} from '@heroicons/vue/24/outline'

const adminProductStore = useAdminProductStore()

const archivedIds = computed(() => new Set(
  adminProductStore.products
    .filter(p => p.status === 'archived')
    .map(p => p.id)
))

const categories = [
  { name: '人氣零食', slug: 'popular-snacks', icon: '🍿' },
  { name: '精選茶品', slug: 'fine-tea', icon: '🍵' },
  { name: '進口巧克力', slug: 'imported-chocolate', icon: '🍫' },
  { name: '健康穀物', slug: 'healthy-grains', icon: '🌾' },
  { name: '有機食品', slug: 'organic-food', icon: '🥬' },
  { name: '日本零食', slug: 'japanese-snacks', icon: '🍘' },
  { name: '手工餅乾', slug: 'handmade-cookies', icon: '🍪' },
  { name: '果乾蜜餞', slug: 'dried-fruits', icon: '🥭' },
  { name: '飲品', slug: 'beverages', icon: '🧃' },
  { name: '調味料', slug: 'seasonings', icon: '🧂' },
]

// Mock data for demo — replaced by API call later
const allFeatured = [
  { id: 1, name: '日本北海道白色戀人巧克力餅乾 24入', slug: 'shiroi-koibito-24', brand: 'ISHIYA', price: 680, salePrice: 580, image: 'https://placehold.co/400x400/FFF3E0/E65100?text=白色戀人', rating: 4.8, reviewCount: 256, isNew: false, inStock: true },
  { id: 2, name: '有機台灣高山烏龍茶 150g', slug: 'organic-oolong-tea', brand: '茶山房', price: 450, image: 'https://placehold.co/400x400/E8F5E9/2E7D32?text=烏龍茶', rating: 4.9, reviewCount: 189, isNew: true, inStock: true },
  { id: 3, name: '比利時Godiva 經典松露巧克力禮盒', slug: 'godiva-truffle-box', brand: 'GODIVA', price: 1280, salePrice: 999, image: 'https://placehold.co/400x400/F3E5F5/7B1FA2?text=GODIVA', rating: 4.7, reviewCount: 142, isNew: false, inStock: true },
  { id: 4, name: '日本卡樂比薯條三兄弟 10袋入', slug: 'calbee-jagabee-10', brand: 'Calbee', price: 320, image: 'https://placehold.co/400x400/FFFDE7/F57F17?text=卡樂比', rating: 4.6, reviewCount: 328, isNew: false, inStock: true },
  { id: 5, name: '澳洲有機藜麥 500g', slug: 'organic-quinoa-500', brand: 'Nature First', price: 380, salePrice: 299, image: 'https://placehold.co/400x400/FFF8E1/FF8F00?text=藜麥', rating: 4.5, reviewCount: 87, isNew: false, inStock: true },
]

const allNewProducts = [
  { id: 6, name: '法國La Mère Poulard 奶油餅乾禮盒', slug: 'la-mere-poulard-cookies', brand: 'La Mère Poulard', price: 520, image: 'https://placehold.co/400x400/FBE9E7/BF360C?text=法式餅乾', rating: 4.4, reviewCount: 56, isNew: true, inStock: true },
  { id: 7, name: '台灣小農手作芒果乾 200g', slug: 'handmade-mango-dried', brand: '在地好味', price: 280, image: 'https://placehold.co/400x400/FFF3E0/E65100?text=芒果乾', rating: 4.8, reviewCount: 201, isNew: true, inStock: true },
  { id: 8, name: '日本伊藤園抹茶拿鐵 隨身包30入', slug: 'itoen-matcha-latte-30', brand: '伊藤園', price: 450, salePrice: 399, image: 'https://placehold.co/400x400/E8F5E9/1B5E20?text=抹茶拿鐵', rating: 4.6, reviewCount: 178, isNew: true, inStock: true },
  { id: 9, name: '韓國CJ 韓式辣椒醬 500g', slug: 'cj-gochujang-500', brand: 'CJ', price: 199, image: 'https://placehold.co/400x400/FFEBEE/C62828?text=辣椒醬', rating: 4.3, reviewCount: 92, isNew: true, inStock: true },
  { id: 10, name: '義大利Lavazza 經典中焙咖啡豆 250g', slug: 'lavazza-classico-250', brand: 'Lavazza', price: 380, image: 'https://placehold.co/400x400/EFEBE9/4E342E?text=Lavazza', rating: 4.7, reviewCount: 134, isNew: true, inStock: true },
]

// Filter out archived products
const featuredProducts = computed(() => allFeatured.filter(p => !archivedIds.value.has(p.id)))
const newProducts = computed(() => allNewProducts.filter(p => !archivedIds.value.has(p.id)))
</script>
