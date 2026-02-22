<template>
  <div class="fixed top-4 right-4 z-100 space-y-2.5 pointer-events-none">
    <transition-group name="toast">
      <div
        v-for="toast in uiStore.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-xl backdrop-blur-sm min-w-75 max-w-sm"
        :class="toastClasses(toast.type)"
      >
        <component :is="toastIcon(toast.type)" class="w-5 h-5 shrink-0" />
        <p class="text-sm font-semibold flex-1">{{ toast.message }}</p>
        <button @click="uiStore.removeToast(toast.id)" class="shrink-0 opacity-40 hover:opacity-100 transition-opacity">
          <XMarkIcon class="w-4 h-4" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useUIStore } from '@/stores/ui'
import {
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
} from '@heroicons/vue/24/solid'

const uiStore = useUIStore()

function toastClasses(type) {
  const map = {
    success: 'bg-green-50/95 text-green-800 border border-green-200/80',
    error: 'bg-red-50/95 text-red-800 border border-red-200/80',
    warning: 'bg-amber-50/95 text-amber-800 border border-amber-200/80',
    info: 'bg-blue-50/95 text-blue-800 border border-blue-200/80',
  }
  return map[type] || map.info
}

function toastIcon(type) {
  const map = {
    success: CheckCircleIcon,
    error: XCircleIcon,
    warning: ExclamationTriangleIcon,
    info: InformationCircleIcon,
  }
  return map[type] || map.info
}
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-leave-active {
  transition: all 0.25s ease-in;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100px) scale(0.95);
}
.toast-move {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
