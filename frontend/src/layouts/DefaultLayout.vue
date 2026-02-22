<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Global Loading Overlay -->
    <transition name="fade">
      <div v-if="uiStore.globalLoading" class="fixed inset-0 z-200 flex items-center justify-center bg-white/70 backdrop-blur-sm">
        <div class="flex flex-col items-center gap-3">
          <div class="w-10 h-10 border-3 border-primary-200 border-t-primary-600 rounded-full animate-spin" />
          <span class="text-sm text-gray-500 font-medium">載入中...</span>
        </div>
      </div>
    </transition>

    <AnnouncementBar />
    <AppHeader />
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
    <CartDrawer />
    <ToastContainer />

    <!-- Scroll to Top Button -->
    <transition name="scale">
      <button
        v-show="showScrollTop"
        @click="scrollToTop"
        class="fixed bottom-6 right-6 z-40 w-12 h-12 bg-primary-600 text-white rounded-full shadow-lg shadow-primary-600/30 hover:bg-primary-700 hover:shadow-xl hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center group"
        aria-label="回到頂部"
      >
        <ChevronUpIcon class="w-5 h-5 group-hover:animate-bounce" />
      </button>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUIStore } from '@/stores/ui'
import AnnouncementBar from '@/components/layout/AnnouncementBar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import CartDrawer from '@/components/layout/CartDrawer.vue'
import ToastContainer from '@/components/ui/ToastContainer.vue'
import { ChevronUpIcon } from '@heroicons/vue/24/outline'

const uiStore = useUIStore()
const showScrollTop = ref(false)

function handleScroll() {
  showScrollTop.value = window.scrollY > 400
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
