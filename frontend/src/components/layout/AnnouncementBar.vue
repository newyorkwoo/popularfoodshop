<template>
  <transition name="slide-up">
    <div v-if="visible" class="relative bg-linear-to-r from-primary-600 via-primary-500 to-amber-500 text-white text-center text-sm py-2.5 px-4 overflow-hidden">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute -left-4 top-0 w-20 h-20 bg-white rounded-full blur-2xl" />
        <div class="absolute right-1/4 -top-2 w-16 h-16 bg-white rounded-full blur-2xl" />
      </div>
      <p class="relative flex items-center justify-center gap-2 font-medium">
        <SparklesIcon class="w-4 h-4 animate-pulse-soft" />
        {{ $t('home.announcement') }}
        <SparklesIcon class="w-4 h-4 animate-pulse-soft" />
      </p>
      <button
        class="absolute right-3 top-1/2 -translate-y-1/2 text-white/70 hover:text-white transition-colors"
        @click="visible = false"
      >
        <XMarkIcon class="w-4 h-4" />
      </button>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { XMarkIcon, SparklesIcon } from '@heroicons/vue/24/outline'

const visible = ref(true)
</script>
