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
        <router-link to="/" class="text-lg font-bold text-blue-400">
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
          :class="isActive(item.to) ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
        >
          <component :is="item.icon" class="w-5 h-5" />
          {{ item.label }}
        </router-link>
      </nav>
      <!-- Security badge -->
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700 space-y-2">
        <div class="flex items-center gap-2 text-xs text-gray-500">
          <ShieldCheckIcon class="w-4 h-4" />
          <span>獨立管理系統 v1.0</span>
        </div>
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
          <span class="text-xs px-2 py-0.5 rounded-full font-medium"
            :class="roleBadgeClass"
          >
            {{ roleLabel }}
          </span>
          <span class="text-sm text-gray-600">{{ authStore.fullName || '管理員' }}</span>
          <button @click="authStore.logout()" class="text-sm text-red-600 hover:text-red-800 font-medium">
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
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminAuthStore } from '@/stores/auth'
import {
  Bars3Icon,
  XMarkIcon,
  ShieldCheckIcon,
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
const authStore = useAdminAuthStore()
const sidebarOpen = ref(false)

const menuItems = [
  { to: '/', label: '儀表板', icon: HomeIcon },
  { to: '/products', label: '商品管理', icon: ShoppingBagIcon },
  { to: '/categories', label: '分類管理', icon: TagIcon },
  { to: '/brands', label: '品牌管理', icon: BuildingStorefrontIcon },
  { to: '/orders', label: '訂單管理', icon: ClipboardDocumentListIcon },
  { to: '/users', label: '會員管理', icon: UsersIcon },
  { to: '/promotions', label: '促銷活動', icon: GiftIcon },
  { to: '/content', label: '內容管理', icon: DocumentTextIcon },
  { to: '/reports', label: '報表分析', icon: ChartBarIcon },
  { to: '/settings', label: '系統設定', icon: Cog6ToothIcon },
]

const roleLabel = computed(() => {
  const labels = { super_admin: '超級管理員', admin: '管理員', editor: '編輯' }
  return labels[authStore.userRole] || authStore.userRole
})

const roleBadgeClass = computed(() => {
  const classes = {
    super_admin: 'bg-red-100 text-red-700',
    admin: 'bg-blue-100 text-blue-700',
    editor: 'bg-green-100 text-green-700',
  }
  return classes[authStore.userRole] || 'bg-gray-100 text-gray-700'
})

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>
