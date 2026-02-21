<template>
  <div>
    <h2 class="text-xl font-bold text-gray-900 mb-6">退換貨申請</h2>

    <div v-if="returns.length" class="space-y-4">
      <div v-for="r in returns" :key="r.id" class="border border-gray-200 rounded-xl p-5">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm text-gray-500">申請編號：{{ r.returnNumber }}</span>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-medium"
            :class="{ 'bg-yellow-100 text-yellow-700': r.status === 'pending', 'bg-blue-100 text-blue-700': r.status === 'processing', 'bg-green-100 text-green-700': r.status === 'completed', 'bg-red-100 text-red-700': r.status === 'rejected' }">
            {{ { pending: '審核中', processing: '處理中', completed: '已完成', rejected: '已拒絕' }[r.status] }}
          </span>
        </div>
        <div class="flex items-center gap-4">
          <img :src="r.product.image" class="w-16 h-16 rounded-lg object-cover bg-gray-100" />
          <div>
            <p class="font-medium text-gray-900">{{ r.product.name }}</p>
            <p class="text-sm text-gray-500">原因：{{ r.reason }}</p>
            <p class="text-xs text-gray-400 mt-1">申請日期：{{ r.date }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p>目前沒有退換貨申請</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const returns = ref([
  {
    id: 1, returnNumber: 'RET20250120001', status: 'processing', date: '2025-01-20',
    reason: '商品到貨時已損壞',
    product: { name: '法國手工果醬三入組', image: 'https://placehold.co/100x100/FEF2F2/DC2626?text=果醬' },
  },
])
</script>
