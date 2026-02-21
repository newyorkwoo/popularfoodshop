<template>
  <header class="sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
    <!-- Top bar -->
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Mobile menu button -->
        <button class="lg:hidden p-2 text-gray-600 hover:text-gray-900" @click="uiStore.toggleMobileMenu(true)">
          <Bars3Icon class="w-6 h-6" />
        </button>

        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2 shrink-0">
          <span class="text-2xl">🍜</span>
          <span class="text-xl font-bold text-gray-900 hidden sm:inline">人氣美食商店</span>
        </router-link>

        <!-- Search bar (desktop) -->
        <div class="hidden lg:flex flex-1 max-w-xl mx-8">
          <div class="relative w-full">
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="$t('common.search')"
              class="w-full pl-10 pr-4 py-2.5 rounded-full border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-colors text-sm"
              @keyup.enter="handleSearch"
            />
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
        </div>

        <!-- Right actions -->
        <div class="flex items-center gap-2 sm:gap-4">
          <!-- Mobile search toggle -->
          <button class="lg:hidden p-2 text-gray-600 hover:text-gray-900" @click="uiStore.toggleSearch(true)">
            <MagnifyingGlassIcon class="w-6 h-6" />
          </button>

          <!-- Wishlist -->
          <router-link
            to="/account/wishlist"
            class="relative p-2 text-gray-600 hover:text-primary-600 transition-colors"
          >
            <HeartIcon class="w-6 h-6" />
            <span
              v-if="wishlistStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full"
            >
              {{ wishlistStore.itemCount }}
            </span>
          </router-link>

          <!-- Account -->
          <div class="relative" v-if="authStore.isAuthenticated">
            <button
              class="p-2 text-gray-600 hover:text-primary-600 transition-colors"
              @click="accountMenuOpen = !accountMenuOpen"
            >
              <UserIcon class="w-6 h-6" />
            </button>
            <transition name="fade">
              <div
                v-if="accountMenuOpen"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
                @mouseleave="accountMenuOpen = false"
              >
                <div class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ authStore.fullName }}</p>
                  <p class="text-xs text-gray-500">{{ authStore.user?.email }}</p>
                </div>
                <router-link to="/account" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="accountMenuOpen = false">
                  {{ $t('account.profile') }}
                </router-link>
                <router-link to="/account/orders" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="accountMenuOpen = false">
                  {{ $t('account.orders') }}
                </router-link>
                <router-link v-if="authStore.isAdmin" to="/admin" class="block px-4 py-2 text-sm text-primary-600 hover:bg-gray-50" @click="accountMenuOpen = false">
                  管理後台
                </router-link>
                <button
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-50"
                  @click="authStore.logout(); accountMenuOpen = false"
                >
                  {{ $t('common.logout') }}
                </button>
              </div>
            </transition>
          </div>
          <router-link v-else to="/login" class="p-2 text-gray-600 hover:text-primary-600 transition-colors">
            <UserIcon class="w-6 h-6" />
          </router-link>

          <!-- Cart -->
          <button
            class="relative p-2 text-gray-600 hover:text-primary-600 transition-colors"
            @click="uiStore.toggleCartDrawer(true)"
          >
            <ShoppingBagIcon class="w-6 h-6" />
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-primary-600 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full"
            >
              {{ cartStore.itemCount }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Category navigation (desktop) -->
    <nav class="hidden lg:block border-t border-gray-100">
      <div class="container mx-auto px-4">
        <ul class="flex items-center gap-6 h-10 text-sm">
          <li v-for="cat in navCategories" :key="cat.slug">
            <router-link
              :to="{ name: 'ProductList', params: { slug: cat.slug } }"
              class="text-gray-700 hover:text-primary-600 transition-colors font-medium"
            >
              {{ cat.name }}
            </router-link>
          </li>
          <li>
            <router-link to="/brands" class="text-gray-700 hover:text-primary-600 transition-colors font-medium">
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
              class="w-full pl-10 pr-4 py-3 rounded-full border border-gray-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 text-sm"
              @keyup.enter="handleSearch"
            />
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
          <button class="text-gray-600 font-medium text-sm" @click="uiStore.toggleSearch(false)">
            {{ $t('common.cancel') }}
          </button>
        </div>
      </div>
    </transition>

    <MobileMenu />
  </header>
</template>

<script setup>
import { ref } from 'vue'
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

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'Search', query: { q: searchQuery.value.trim() } })
    uiStore.toggleSearch(false)
    searchQuery.value = ''
  }
}
</script>
