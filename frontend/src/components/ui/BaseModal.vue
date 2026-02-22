<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="modelValue" class="fixed inset-0 z-60 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="closeOnBackdrop && close()" />

        <!-- Modal -->
        <div
          :class="[
            'relative bg-white rounded-2xl shadow-2xl w-full max-h-[90vh] flex flex-col',
            sizeClasses,
          ]"
        >
          <!-- Header -->
          <div v-if="title || $slots.header" class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <slot name="header">
              <h3 class="text-lg font-bold text-gray-900">{{ title }}</h3>
            </slot>
            <button v-if="closable" @click="close" class="p-1.5 text-gray-400 hover:text-gray-600 rounded-xl hover:bg-gray-100 transition-all">
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>

          <!-- Body -->
          <div class="flex-1 overflow-y-auto px-6 py-4">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-100 bg-gray-50/50 rounded-b-2xl">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { computed, watch } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: '' },
  size: { type: String, default: 'md' },
  closable: { type: Boolean, default: true },
  closeOnBackdrop: { type: Boolean, default: true },
})

const emit = defineEmits(['update:modelValue', 'close'])

const sizeClasses = computed(() => {
  const map = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-[95vw]',
  }
  return map[props.size] || map.md
})

function close() {
  emit('update:modelValue', false)
  emit('close')
}

watch(() => props.modelValue, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})
</script>

<style scoped>
.modal-enter-active {
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.modal-enter-active > div:last-child {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
}
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-leave-active > div:last-child {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from > div:last-child {
  transform: scale(0.92) translateY(10px);
  opacity: 0;
}
.modal-leave-to > div:last-child {
  transform: scale(0.95);
  opacity: 0;
}
</style>
