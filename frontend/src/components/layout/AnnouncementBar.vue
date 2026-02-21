<template>
  <div v-if="visible" class="bg-primary-600 text-white text-center text-sm py-2 px-4 relative">
    <p>{{ $t('home.announcement') }}</p>
    <button
      class="absolute right-3 top-1/2 -translate-y-1/2 text-white/70 hover:text-white"
      @click="visible = false"
    >
      <XMarkIcon class="w-4 h-4" />
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const visible = ref(true)
</script>
