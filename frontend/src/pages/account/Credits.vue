<template>
  <div>
    <h2 class="text-xl font-bold text-gray-900 mb-6">購物金</h2>

    <div class="bg-linear-to-r from-primary-500 to-orange-500 rounded-2xl p-6 text-white mb-8">
      <p class="text-sm opacity-80">可用購物金</p>
      <p class="text-3xl font-black mt-1">NT${{ credits.toLocaleString() }}</p>
    </div>

    <h3 class="font-bold text-gray-900 mb-4">購物金紀錄</h3>
    <div v-if="records.length" class="space-y-3">
      <div v-for="r in records" :key="r.id" class="flex items-center justify-between border-b border-gray-100 pb-3">
        <div>
          <p class="text-sm font-medium text-gray-900">{{ r.description }}</p>
          <p class="text-xs text-gray-400">{{ r.date }}</p>
        </div>
        <span class="font-bold" :class="r.amount > 0 ? 'text-green-600' : 'text-red-500'">
          {{ r.amount > 0 ? '+' : '' }}NT${{ r.amount.toLocaleString() }}
        </span>
      </div>
    </div>
    <div v-else class="text-center py-12 text-gray-500">暫無紀錄</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const credits = ref(500)
const records = ref([
  { id: 1, description: '會員註冊贈送', amount: 200, date: '2025-01-01' },
  { id: 2, description: '訂單 PFS20250101001 回饋', amount: 300, date: '2025-01-15' },
])
</script>
