<template>
  <transition name="slide-left">
    <div v-if="uiStore.mobileMenuOpen" class="fixed inset-0 z-50 lg:hidden">
      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="uiStore.toggleMobileMenu(false)" />

      <!-- Panel -->
      <div class="absolute inset-y-0 left-0 w-80 max-w-[85vw] bg-white shadow-2xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between h-16 px-5 border-b border-gray-100 bg-gray-50/80">
          <span class="text-lg font-bold text-gray-900">🍜 人氣美食商店</span>
          <button @click="uiStore.toggleMobileMenu(false)" class="p-2 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-xl transition-all">
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- User info -->
        <div v-if="authStore.isAuthenticated" class="px-5 py-3 bg-gray-50/60 border-b border-gray-100">
          <p class="font-medium text-gray-900">{{ authStore.fullName }}</p>
          <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 overflow-y-auto py-4">
          <div class="px-4 mb-2">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">{{ $t('nav.allCategories') }}</p>
          </div>
          <router-link
            v-for="cat in categories"
            :key="cat.slug"
            :to="{ name: 'ProductList', params: { slug: cat.slug } }"
            class="block px-5 py-2.5 text-sm text-gray-600 hover:bg-primary-50 hover:text-primary-600 hover:pl-6 transition-all"
            @click="uiStore.toggleMobileMenu(false)"
          >
            {{ cat.name }}
          </router-link>

          <div class="border-t border-gray-100 my-3" />

          <router-link
            to="/brands"
            class="block px-5 py-2.5 text-sm text-gray-600 hover:bg-primary-50 hover:text-primary-600 hover:pl-6 transition-all"
            @click="uiStore.toggleMobileMenu(false)"
          >
            {{ $t('nav.brands') }}
          </router-link>

          <div v-if="authStore.isAuthenticated" class="border-t border-gray-200 my-3">
            <router-link
              to="/account"
              class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50"
              @click="uiStore.toggleMobileMenu(false)"
            >
              {{ $t('account.profile') }}
            </router-link>
            <router-link
              to="/account/orders"
              class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50"
              @click="uiStore.toggleMobileMenu(false)"
            >
              {{ $t('account.orders') }}
            </router-link>
            <router-link
              to="/account/wishlist"
              class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50"
              @click="uiStore.toggleMobileMenu(false)"
            >
              {{ $t('account.wishlist') }}
            </router-link>
          </div>
        </nav>

        <!-- Footer actions -->
        <div class="border-t border-gray-100 p-5 space-y-2.5">
          <template v-if="authStore.isAuthenticated">
            <button
              class="block w-full py-2.5 text-sm font-semibold text-red-600 border border-red-200 rounded-xl hover:bg-red-50 transition-colors"
              @click="authStore.logout(); uiStore.toggleMobileMenu(false)"
            >
              {{ $t('common.logout') }}
            </button>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="block w-full text-center py-2.5 text-sm font-semibold text-white bg-primary-600 rounded-xl hover:bg-primary-500 hover:shadow-lg hover:shadow-primary-600/25 transition-all"
              @click="uiStore.toggleMobileMenu(false)"
            >
              {{ $t('common.login') }}
            </router-link>
            <router-link
              to="/register"
              class="block w-full text-center py-2.5 text-sm font-semibold text-primary-600 border-2 border-primary-600 rounded-xl hover:bg-primary-50 transition-colors"
              @click="uiStore.toggleMobileMenu(false)"
            >
              {{ $t('common.register') }}
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const { t } = useI18n()
const authStore = useAuthStore()
const uiStore = useUIStore()

const categories = [
  { name: t('nav.popularSnacks'), slug: 'popular-snacks' },
  { name: t('nav.fineTea'), slug: 'fine-tea' },
  { name: t('nav.importedChocolate'), slug: 'imported-chocolate' },
  { name: t('nav.healthyGrains'), slug: 'healthy-grains' },
  { name: t('nav.organicFood'), slug: 'organic-food' },
  { name: t('nav.japaneseSnacks'), slug: 'japanese-snacks' },
  { name: t('nav.handmadeCookies'), slug: 'handmade-cookies' },
  { name: t('nav.driedFruits'), slug: 'dried-fruits' },
  { name: t('nav.beverages'), slug: 'beverages' },
  { name: t('nav.seasonings'), slug: 'seasonings' },
]
</script>

<style scoped>
.slide-left-enter-active,
.slide-left-leave-active {
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-left-enter-active > div:last-child,
.slide-left-leave-active > div:last-child {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-left-enter-from,
.slide-left-leave-to {
  opacity: 0;
}
.slide-left-enter-from > div:last-child,
.slide-left-leave-to > div:last-child {
  transform: translateX(-100%);
}
</style>
