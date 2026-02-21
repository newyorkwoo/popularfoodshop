<template>
  <div>
    <h2 class="text-xl font-bold text-gray-900 mb-6">我的訂單</h2>

    <!-- Status Tabs -->
    <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
      <button
        v-for="tab in tabs" :key="tab.value"
        @click="activeTab = tab.value"
        class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition"
        :class="activeTab === tab.value ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
      >{{ tab.label }}</button>
    </div>

    <!-- Orders -->
    <div v-if="filteredOrders.length" class="space-y-4">
      <div v-for="order in filteredOrders" :key="order.id" class="border border-gray-200 rounded-xl overflow-hidden">
        <div class="flex items-center justify-between px-5 py-3 bg-gray-50 text-sm">
          <div class="flex gap-6">
            <span>訂單編號：<strong>{{ order.orderNumber }}</strong></span>
            <span class="text-gray-500">{{ order.date }}</span>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-medium" :class="statusClass(order.status)">{{ statusLabel(order.status) }}</span>
        </div>
        <div class="p-5">
          <div v-for="item in order.items" :key="item.id" class="flex items-center gap-4 py-2">
            <img :src="item.image" class="w-16 h-16 rounded-lg object-cover bg-gray-100" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ item.name }}</p>
              <p class="text-xs text-gray-500">x{{ item.quantity }}</p>
            </div>
            <p class="text-sm font-medium">NT${{ item.price.toLocaleString() }}</p>
          </div>
        </div>
        <div class="flex items-center justify-between px-5 py-3 border-t bg-gray-50">
          <p class="text-sm">共 {{ order.items.length }} 件商品，合計 <strong class="text-primary-600">NT${{ order.total.toLocaleString() }}</strong></p>
          <router-link :to="`/account/orders/${order.id}`" class="text-sm text-primary-600 hover:underline font-medium">查看詳情</router-link>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-16 text-gray-500">
      <p>目前沒有{{ activeTab === 'all' ? '' : statusLabel(activeTab) }}訂單</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeTab = ref('all')
const tabs = [
  { label: '全部', value: 'all' },
  { label: '待付款', value: 'pending' },
  { label: '處理中', value: 'processing' },
  { label: '已出貨', value: 'shipped' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' },
]

const orders = ref([
  { id: 1, orderNumber: 'PFS20250101001', date: '2025-01-15', status: 'completed', total: 2560,
    items: [
      { id: 1, name: '日本A5和牛火鍋片', quantity: 2, price: 1280, image: 'https://placehold.co/100x100/FFF3E0/EA580C?text=和牛' },
    ],
  },
  { id: 2, orderNumber: 'PFS20250102002', date: '2025-01-20', status: 'shipped', total: 1570,
    items: [
      { id: 1, name: '有機冷壓初榨橄欖油', quantity: 1, price: 680, image: 'https://placehold.co/100x100/F0FDF4/16A34A?text=橄欖油' },
      { id: 2, name: '法國手工果醬三入組', quantity: 1, price: 890, image: 'https://placehold.co/100x100/FEF2F2/DC2626?text=果醬' },
    ],
  },
  { id: 3, orderNumber: 'PFS20250103003', date: '2025-01-22', status: 'pending', total: 950,
    items: [
      { id: 1, name: '義大利松露醬', quantity: 1, price: 950, image: 'https://placehold.co/100x100/F5F3FF/7C3AED?text=松露醬' },
    ],
  },
])

const filteredOrders = computed(() =>
  activeTab.value === 'all' ? orders.value : orders.value.filter(o => o.status === activeTab.value)
)

function statusLabel(s) {
  return { pending: '待付款', processing: '處理中', shipped: '已出貨', completed: '已完成', cancelled: '已取消' }[s] || s
}
function statusClass(s) {
  return {
    pending: 'bg-yellow-100 text-yellow-700',
    processing: 'bg-blue-100 text-blue-700',
    shipped: 'bg-indigo-100 text-indigo-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-gray-100 text-gray-500',
  }[s] || 'bg-gray-100 text-gray-700'
}
</script>
