<template>
  <div class="fixed top-4 right-4 z-[100] space-y-2 pointer-events-none">
    <transition-group name="toast">
      <div
        v-for="toast in uiStore.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg min-w-[280px] max-w-sm"
        :class="toastClasses(toast.type)"
      >
        <component :is="toastIcon(toast.type)" class="w-5 h-5 shrink-0" />
        <p class="text-sm font-medium flex-1">{{ toast.message }}</p>
        <button @click="uiStore.removeToast(toast.id)" class="shrink-0 opacity-60 hover:opacity-100">
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
    success: 'bg-green-50 text-green-800 border border-green-200',
    error: 'bg-red-50 text-red-800 border border-red-200',
    warning: 'bg-yellow-50 text-yellow-800 border border-yellow-200',
    info: 'bg-blue-50 text-blue-800 border border-blue-200',
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
  transition: all 0.3s ease;
}
.toast-leave-active {
  transition: all 0.2s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100px);
}
.toast-move {
  transition: transform 0.3s ease;
}
</style>
