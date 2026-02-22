<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">訂單管理</h2>

    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-3 mb-6">
      <input v-model="search" placeholder="搜尋訂單編號..." class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-52 focus:ring-2 focus:ring-primary-500" />
      <select v-model="filterStatus" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
        <option value="">所有狀態</option>
        <option value="pending">待付款</option>
        <option value="processing">處理中</option>
        <option value="shipped">已出貨</option>
        <option value="completed">已完成</option>
        <option value="cancelled">已取消</option>
      </select>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50"><tr>
          <th class="px-4 py-3 text-left font-medium text-gray-600">訂單編號</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">客戶</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">日期</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">金額</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">狀態</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">操作</th>
        </tr></thead>
        <tbody class="divide-y">
          <tr v-for="o in pagedOrders" :key="o.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-900">{{ o.orderNumber }}</td>
            <td class="px-4 py-3 text-gray-600">{{ o.customer }}</td>
            <td class="px-4 py-3 text-gray-500">{{ o.date }}</td>
            <td class="px-4 py-3 font-medium">NT${{ o.total.toLocaleString() }}</td>
            <td class="px-4 py-3">
              <select :value="o.status" @change="changeStatus(o, $event)" class="text-xs border rounded-lg px-2 py-1"
                :class="statusClass(o.status)">
                <option value="pending">待付款</option>
                <option value="processing">處理中</option>
                <option value="shipped">已出貨</option>
                <option value="completed">已完成</option>
                <option value="cancelled">已取消</option>
              </select>
            </td>
            <td class="px-4 py-3">
              <router-link :to="`/orders/${o.id}`" class="text-primary-600 hover:underline text-xs">查看詳情</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <BasePagination v-if="totalPages > 1" v-model="currentPage" :total-pages="totalPages" class="mt-6" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BasePagination from '@/components/ui/BasePagination.vue'
import { useAdminOrderStore } from '@/stores/adminOrder'

const store = useAdminOrderStore()
const search = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const perPage = 10

const filteredOrders = computed(() =>
  store.orders.filter(o => {
    if (search.value && !o.orderNumber.includes(search.value)) return false
    if (filterStatus.value && o.status !== filterStatus.value) return false
    return true
  })
)

const totalPages = computed(() => Math.max(1, Math.ceil(filteredOrders.value.length / perPage)))

const pagedOrders = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredOrders.value.slice(start, start + perPage)
})

function changeStatus(order, event) {
  store.updateStatus(order.id, event.target.value)
}

function statusClass(s) {
  return {
    pending: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    processing: 'bg-blue-50 text-blue-700 border-blue-200',
    shipped: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    completed: 'bg-green-50 text-green-700 border-green-200',
    cancelled: 'bg-gray-50 text-gray-500 border-gray-200',
  }[s] || ''
}
</script>
