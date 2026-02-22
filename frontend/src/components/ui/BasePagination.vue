<template>
  <nav class="flex items-center justify-center gap-1" aria-label="Pagination">
    <button
      class="p-2 rounded-xl text-gray-400 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
      :disabled="modelValue <= 1"
      @click="emit('update:modelValue', modelValue - 1)"
    >
      <ChevronLeftIcon class="w-5 h-5" />
    </button>

    <template v-for="page in visiblePages">
      <span v-if="page === '...'" :key="'dots-' + page" class="px-2 text-gray-300 select-none">…</span>
      <button
        v-else
        :key="page"
        class="w-10 h-10 rounded-xl text-sm font-semibold transition-all"
        :class="page === modelValue ? 'bg-primary-600 text-white shadow-md shadow-primary-600/25' : 'text-gray-600 hover:bg-gray-100'"
        @click="emit('update:modelValue', page)"
      >
        {{ page }}
      </button>
    </template>

    <button
      class="p-2 rounded-xl text-gray-400 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
      :disabled="modelValue >= totalPages"
      @click="emit('update:modelValue', modelValue + 1)"
    >
      <ChevronRightIcon class="w-5 h-5" />
    </button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  siblingCount: { type: Number, default: 1 },
})

const emit = defineEmits(['update:modelValue'])

const visiblePages = computed(() => {
  const total = props.totalPages
  const current = props.modelValue
  const siblings = props.siblingCount

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const left = Math.max(current - siblings, 2)
  const right = Math.min(current + siblings, total - 1)
  const pages = [1]

  if (left > 2) pages.push('...')
  for (let i = left; i <= right; i++) pages.push(i)
  if (right < total - 1) pages.push('...')
  pages.push(total)

  return pages
})
</script>
