<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">儀表板</h2>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="stat in stats" :key="stat.label" class="bg-white border border-gray-200 rounded-xl p-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="stat.bg">
            <component :is="stat.icon" class="w-5 h-5" :class="stat.color" />
          </div>
          <div>
            <p class="text-sm text-gray-500">{{ stat.label }}</p>
            <p class="text-xl font-bold text-gray-900">{{ stat.value }}</p>
          </div>
        </div>
        <p class="text-xs mt-2" :class="stat.trend > 0 ? 'text-green-600' : 'text-red-500'">
          {{ stat.trend > 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}% 較上月
        </p>
      </div>
    </div>

    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Recent Orders -->
      <div class="bg-white border border-gray-200 rounded-xl">
        <div class="flex items-center justify-between p-5 border-b">
          <h3 class="font-bold text-gray-900">最新訂單</h3>
          <router-link to="/orders" class="text-sm text-primary-600 hover:underline">查看全部</router-link>
        </div>
        <div class="divide-y">
          <div v-for="order in recentOrders" :key="order.id" class="flex items-center justify-between px-5 py-3">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ order.orderNumber }}</p>
              <p class="text-xs text-gray-500">{{ order.customer }} · {{ order.date }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium">NT${{ order.total.toLocaleString() }}</p>
              <span class="text-xs px-2 py-0.5 rounded-full" :class="orderStatusClass(order.status)">{{ order.statusLabel }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Products -->
      <div class="bg-white border border-gray-200 rounded-xl">
        <div class="flex items-center justify-between p-5 border-b">
          <h3 class="font-bold text-gray-900">熱銷商品</h3>
          <router-link to="/products" class="text-sm text-primary-600 hover:underline">查看全部</router-link>
        </div>
        <div class="divide-y">
          <div v-for="(p, i) in topProducts" :key="p.id" class="flex items-center gap-3 px-5 py-3">
            <span class="text-sm font-bold text-gray-400 w-5">{{ i + 1 }}</span>
            <img :src="p.image" class="w-10 h-10 rounded-lg object-cover bg-gray-100" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ p.name }}</p>
              <p class="text-xs text-gray-500">{{ p.sold }} 件已售</p>
            </div>
            <p class="text-sm font-medium">NT${{ p.revenue.toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  CurrencyDollarIcon, ShoppingCartIcon, UsersIcon, CubeIcon,
} from '@heroicons/vue/24/outline'
import { useAdminOrderStore } from '@/stores/adminOrder'

const orderStore = useAdminOrderStore()

const statusLabels = { pending: '待付款', processing: '處理中', shipped: '已出貨', completed: '已完成', cancelled: '已取消' }

/* ---- computed from real orders ---- */
const validOrders = computed(() => orderStore.orders.filter(o => o.status !== 'cancelled'))
const totalRevenue = computed(() => validOrders.value.reduce((s, o) => s + o.total, 0))
const orderCount = computed(() => validOrders.value.length)

const stats = computed(() => [
  { label: '本月營收', value: `NT$${totalRevenue.value.toLocaleString()}`, icon: CurrencyDollarIcon, bg: 'bg-green-100', color: 'text-green-600', trend: 12.5 },
  { label: '訂單數量', value: String(orderCount.value), icon: ShoppingCartIcon, bg: 'bg-blue-100', color: 'text-blue-600', trend: 8.3 },
  { label: '新增會員', value: '42', icon: UsersIcon, bg: 'bg-purple-100', color: 'text-purple-600', trend: -2.1 },
  { label: '商品數量', value: '30', icon: CubeIcon, bg: 'bg-orange-100', color: 'text-orange-600', trend: 5.0 },
])

/* ---- recent orders (latest 5) ---- */
const recentOrders = computed(() => {
  const sorted = [...orderStore.orders].sort((a, b) => b.date.localeCompare(a.date) || b.id - a.id)
  return sorted.slice(0, 5).map(o => ({
    id: o.id,
    orderNumber: o.orderNumber,
    customer: o.customer,
    date: o.date,
    total: o.total,
    status: o.status,
    statusLabel: statusLabels[o.status] || o.status,
  }))
})

/* ---- top products aggregated from order items ---- */
const topProducts = computed(() => {
  const map = {}
  validOrders.value.forEach(o => {
    o.items.forEach(item => {
      const key = item.name
      if (!map[key]) map[key] = { name: key, sold: 0, revenue: 0, image: item.image }
      map[key].sold += item.quantity
      map[key].revenue += item.price * item.quantity
    })
  })
  return Object.values(map).sort((a, b) => b.revenue - a.revenue).slice(0, 5).map((p, i) => ({ ...p, id: i + 1 }))
})

function orderStatusClass(s) {
  return {
    pending: 'bg-yellow-100 text-yellow-700', processing: 'bg-blue-100 text-blue-700',
    shipped: 'bg-indigo-100 text-indigo-700', completed: 'bg-green-100 text-green-700',
  }[s] || 'bg-gray-100 text-gray-700'
}
</script>
