<template>
  <div>
    <h2 class="text-xl font-bold text-gray-900 mb-6">會員點數</h2>

    <div class="bg-linear-to-r from-yellow-400 to-orange-500 rounded-2xl p-6 text-white mb-8">
      <p class="text-sm opacity-80">可用點數</p>
      <p class="text-3xl font-black mt-1">{{ points.toLocaleString() }} 點</p>
      <p class="text-sm opacity-80 mt-2">等值 NT${{ Math.floor(points / 10).toLocaleString() }}（每 10 點折 NT$1）</p>
    </div>

    <h3 class="font-bold text-gray-900 mb-4">點數紀錄</h3>
    <div v-if="records.length" class="space-y-3">
      <div v-for="r in records" :key="r.id" class="flex items-center justify-between border-b border-gray-100 pb-3">
        <div>
          <p class="text-sm font-medium text-gray-900">{{ r.description }}</p>
          <p class="text-xs text-gray-400">{{ r.date }}<span v-if="r.expiry" class="ml-2 text-red-400">到期：{{ r.expiry }}</span></p>
        </div>
        <span class="font-bold" :class="r.amount > 0 ? 'text-green-600' : 'text-red-500'">
          {{ r.amount > 0 ? '+' : '' }}{{ r.amount.toLocaleString() }} 點
        </span>
      </div>
    </div>
    <div v-else class="text-center py-12 text-gray-500">暫無紀錄</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const points = ref(1250)
const records = ref([
  { id: 1, description: '訂單 PFS20250101001 獲得', amount: 500, date: '2025-01-15', expiry: '2026-01-15' },
  { id: 2, description: '訂單 PFS20250102002 獲得', amount: 350, date: '2025-01-20', expiry: '2026-01-20' },
  { id: 3, description: '每日簽到獎勵', amount: 100, date: '2025-01-22', expiry: '2026-01-22' },
  { id: 4, description: '新會員贈送', amount: 300, date: '2025-01-01', expiry: '2025-07-01' },
])
</script>
