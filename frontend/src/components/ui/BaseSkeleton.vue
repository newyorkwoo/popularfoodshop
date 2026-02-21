<template>
  <div :class="['animate-pulse rounded', shapeClasses]" :style="customStyle">
    <div class="bg-gray-200 rounded w-full h-full" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '1rem' },
  shape: { type: String, default: 'rect' }, // rect, circle, text
})

const shapeClasses = computed(() => {
  if (props.shape === 'circle') return 'rounded-full'
  if (props.shape === 'text') return 'rounded'
  return 'rounded-lg'
})

const customStyle = computed(() => ({
  width: props.width,
  height: props.height,
}))
</script>
