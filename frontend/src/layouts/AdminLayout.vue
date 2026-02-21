<template>
  <div class="min-h-screen flex bg-gray-100">
    <!-- Sidebar -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-30 w-64 bg-gray-900 text-white transform transition-transform duration-300 lg:translate-x-0 lg:static lg:inset-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="flex items-center justify-between h-16 px-6 border-b border-gray-700">
        <router-link to="/admin" class="text-lg font-bold text-primary-400">
          🍜 管理後台
        </router-link>
        <button class="lg:hidden text-gray-400 hover:text-white" @click="sidebarOpen = false">
          <XMarkIcon class="w-6 h-6" />
        </button>
      </div>
      <nav class="mt-4 px-3 space-y-1">
        <router-link
          v-for="item in menuItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="isActive(item.to) ? 'bg-primary-600 text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
        >
          <component :is="item.icon" class="w-5 h-5" />
          {{ item.label }}
        </router-link>
      </nav>
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700">
        <router-link to="/" class="flex items-center gap-2 text-sm text-gray-400 hover:text-white">
          <ArrowLeftIcon class="w-4 h-4" />
          返回前台
        </router-link>
      </div>
    </aside>

    <!-- Overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-20 bg-black/50 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Main -->
    <div class="flex-1 flex flex-col min-w-0">
      <header class="sticky top-0 z-10 flex items-center h-16 px-4 bg-white border-b border-gray-200 shadow-sm">
        <button class="lg:hidden mr-4 text-gray-600 hover:text-gray-900" @click="sidebarOpen = true">
          <Bars3Icon class="w-6 h-6" />
        </button>
        <div class="flex-1" />
        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-600">{{ authStore.fullName || '管理員' }}</span>
          <button @click="authStore.logout()" class="text-sm text-red-600 hover:text-red-800">
            登出
          </button>
        </div>
      </header>
      <main class="flex-1 p-6 overflow-auto">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  Bars3Icon,
  XMarkIcon,
  ArrowLeftIcon,
  HomeIcon,
  ShoppingBagIcon,
  TagIcon,
  BuildingStorefrontIcon,
  ClipboardDocumentListIcon,
  UsersIcon,
  GiftIcon,
  DocumentTextIcon,
  ChartBarIcon,
  Cog6ToothIcon,
} from '@heroicons/vue/24/outline'

const route = useRoute()
const authStore = useAuthStore()
const sidebarOpen = ref(false)

const menuItems = [
  { to: '/admin', label: '儀表板', icon: HomeIcon },
  { to: '/admin/products', label: '商品管理', icon: ShoppingBagIcon },
  { to: '/admin/categories', label: '分類管理', icon: TagIcon },
  { to: '/admin/brands', label: '品牌管理', icon: BuildingStorefrontIcon },
  { to: '/admin/orders', label: '訂單管理', icon: ClipboardDocumentListIcon },
  { to: '/admin/users', label: '會員管理', icon: UsersIcon },
  { to: '/admin/promotions', label: '促銷活動', icon: GiftIcon },
  { to: '/admin/content', label: '內容管理', icon: DocumentTextIcon },
  { to: '/admin/reports', label: '報表分析', icon: ChartBarIcon },
  { to: '/admin/settings', label: '系統設定', icon: Cog6ToothIcon },
]

function isActive(path) {
  if (path === '/admin') return route.path === '/admin'
  return route.path.startsWith(path)
}
</script>
