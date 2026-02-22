<template>
  <component
    :is="tag"
    :class="[baseClasses, sizeClasses, variantClasses, { 'opacity-50 cursor-not-allowed': disabled || loading }]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  tag: { type: String, default: 'button' },
})

const baseClasses = 'inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 active:scale-[0.97]'

const sizeClasses = computed(() => {
  const map = {
    xs: 'px-2.5 py-1 text-xs',
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-6 py-3 text-base',
    xl: 'px-8 py-3.5 text-lg',
  }
  return map[props.size] || map.md
})

const variantClasses = computed(() => {
  const map = {
    primary: 'bg-primary-600 text-white hover:bg-primary-500 hover:shadow-lg hover:shadow-primary-600/25 focus:ring-primary-500',
    secondary: 'bg-gray-900 text-white hover:bg-gray-800 hover:shadow-lg focus:ring-gray-500',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-500 hover:shadow-lg hover:shadow-red-600/25 focus:ring-red-500',
    success: 'bg-green-600 text-white hover:bg-green-500 hover:shadow-lg hover:shadow-green-600/25 focus:ring-green-500',
  }
  return map[props.variant] || map.primary
})
</script>
