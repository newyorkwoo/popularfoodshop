<template>
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200/80 shadow-sm transition-shadow duration-300" :class="{ 'shadow-md': scrolled }">
    <!-- Top bar -->
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Mobile menu button -->
        <button class="lg:hidden p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors" @click="uiStore.toggleMobileMenu(true)">
          <Bars3Icon class="w-6 h-6" />
        </button>

        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2.5 shrink-0 group">
          <span class="text-2xl group-hover:animate-bounce transition-transform">🍜</span>
          <span class="text-xl font-bold text-gradient hidden sm:inline">人氣美食商店</span>
        </router-link>

        <!-- Search bar (desktop) -->
        <div class="hidden lg:flex flex-1 max-w-xl mx-8">
          <div class="relative w-full group">
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="$t('common.search')"
              class="w-full pl-11 pr-4 py-2.5 rounded-full bg-gray-50 border border-gray-200 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-100 transition-all text-sm placeholder-gray-400"
              @keyup.enter="handleSearch"
              @focus="searchFocused = true"
              @blur="searchFocused = false"
            />
            <MagnifyingGlassIcon class="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 transition-colors" :class="{ 'text-primary-500': searchFocused }" />
          </div>
        </div>

        <!-- Right actions -->
        <div class="flex items-center gap-1 sm:gap-2">
          <!-- Mobile search toggle -->
          <button class="lg:hidden p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all" @click="uiStore.toggleSearch(true)">
            <MagnifyingGlassIcon class="w-6 h-6" />
          </button>

          <!-- Wishlist -->
          <router-link
            to="/account/wishlist"
            class="relative p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all"
          >
            <HeartIcon class="w-6 h-6" />
            <span
              v-if="wishlistStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full ring-2 ring-white animate-bounce-in"
            >
              {{ wishlistStore.itemCount }}
            </span>
          </router-link>

          <!-- Account -->
          <div class="relative" v-if="authStore.isAuthenticated">
            <button
              class="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all"
              @click="accountMenuOpen = !accountMenuOpen"
            >
              <UserIcon class="w-6 h-6" />
            </button>
            <transition name="scale">
              <div
                v-if="accountMenuOpen"
                class="absolute right-0 mt-2 w-52 bg-white rounded-xl shadow-xl shadow-gray-200/50 border border-gray-100 py-1 z-50"
                @mouseleave="accountMenuOpen = false"
              >
                <div class="px-4 py-3 border-b border-gray-100 bg-gray-50/50 rounded-t-xl">
                  <p class="text-sm font-semibold text-gray-900">{{ authStore.fullName }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">{{ authStore.user?.email }}</p>
                </div>
                <router-link to="/account" class="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 hover:bg-primary-50 hover:text-primary-600 transition-colors" @click="accountMenuOpen = false">
                  {{ $t('account.profile') }}
                </router-link>
                <router-link to="/account/orders" class="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 hover:bg-primary-50 hover:text-primary-600 transition-colors" @click="accountMenuOpen = false">
                  {{ $t('account.orders') }}
                </router-link>
                <hr class="my-1 border-gray-100" />
                <button
                  class="w-full text-left flex items-center gap-2 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                  @click="authStore.logout(); accountMenuOpen = false"
                >
                  {{ $t('common.logout') }}
                </button>
              </div>
            </transition>
          </div>
          <router-link v-else to="/login" class="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all">
            <UserIcon class="w-6 h-6" />
          </router-link>

          <!-- Cart -->
          <button
            class="relative p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all"
            @click="uiStore.toggleCartDrawer(true)"
          >
            <ShoppingBagIcon class="w-6 h-6" />
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-primary-600 text-white text-[10px] font-bold w-5 h-5 flex items-center justify-center rounded-full ring-2 ring-white animate-bounce-in"
            >
              {{ cartStore.itemCount }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Category navigation (desktop) -->
    <nav class="hidden lg:block border-t border-gray-100/80">
      <div class="container mx-auto px-4">
        <ul class="flex items-center gap-1 h-11 text-sm">
          <li v-for="cat in navCategories" :key="cat.slug">
            <router-link
              :to="{ name: 'ProductList', params: { slug: cat.slug } }"
              class="px-3 py-1.5 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all font-medium text-[13px]"
            >
              {{ cat.name }}
            </router-link>
          </li>
          <li>
            <router-link to="/brands" class="px-3 py-1.5 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all font-medium text-[13px]">
              {{ $t('nav.brands') }}
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Mobile search overlay -->
    <transition name="slide-up">
      <div v-if="uiStore.searchOpen" class="fixed inset-0 z-50 bg-white p-4 lg:hidden">
        <div class="flex items-center gap-3">
          <div class="relative flex-1">
            <input
              ref="mobileSearchInput"
              v-model="searchQuery"
              type="text"
              :placeholder="$t('common.search')"
              class="w-full pl-11 pr-4 py-3 rounded-2xl bg-gray-50 border border-gray-200 focus:bg-white focus:border-primary-500 focus:ring-2 focus:ring-primary-100 text-sm"
              @keyup.enter="handleSearch"
            />
            <MagnifyingGlassIcon class="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
          <button class="text-gray-600 font-medium text-sm hover:text-primary-600" @click="uiStore.toggleSearch(false)">
            {{ $t('common.cancel') }}
          </button>
        </div>
      </div>
    </transition>

    <MobileMenu />
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useUIStore } from '@/stores/ui'
import MobileMenu from './MobileMenu.vue'
import {
  Bars3Icon,
  MagnifyingGlassIcon,
  HeartIcon,
  UserIcon,
  ShoppingBagIcon,
} from '@heroicons/vue/24/outline'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const uiStore = useUIStore()

const searchQuery = ref('')
const searchFocused = ref(false)
const scrolled = ref(false)
const accountMenuOpen = ref(false)

const navCategories = [
  { name: t('nav.popularSnacks'), slug: 'popular-snacks' },
  { name: t('nav.fineTea'), slug: 'fine-tea' },
  { name: t('nav.importedChocolate'), slug: 'imported-chocolate' },
  { name: t('nav.healthyGrains'), slug: 'healthy-grains' },
  { name: t('nav.organicFood'), slug: 'organic-food' },
  { name: t('nav.japaneseSnacks'), slug: 'japanese-snacks' },
  { name: t('nav.handmadeCookies'), slug: 'handmade-cookies' },
  { name: t('nav.driedFruits'), slug: 'dried-fruits' },
  { name: t('nav.beverages'), slug: 'beverages' },
]

function handleScroll() {
  scrolled.value = window.scrollY > 10
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'Search', query: { q: searchQuery.value.trim() } })
    uiStore.toggleSearch(false)
    searchQuery.value = ''
  }
}
</script>

<style scoped>
.scale-enter-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.scale-leave-active {
  transition: all 0.15s ease-in;
}
.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-4px);
}
.slide-up-enter-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-leave-active {
  transition: all 0.2s ease-in;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(100%);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(100%);
}
</style>
