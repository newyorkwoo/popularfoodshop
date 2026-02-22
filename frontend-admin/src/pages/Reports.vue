<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">報表分析</h2>

    <!-- Period Select -->
    <div class="flex gap-2 mb-6">
      <button v-for="p in periods" :key="p.value" @click="activePeriod = p.value"
        class="px-4 py-2 rounded-lg text-sm font-medium transition"
        :class="activePeriod === p.value ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'">
        {{ p.label }}
      </button>
    </div>

    <!-- Revenue Summary -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="s in summary" :key="s.label" class="bg-white border border-gray-200 rounded-xl p-5">
        <p class="text-sm text-gray-500">{{ s.label }}</p>
        <p class="text-xl font-bold text-gray-900 mt-1">{{ s.value }}</p>
        <p class="text-xs mt-1" :class="s.trend > 0 ? 'text-green-600' : 'text-red-500'">{{ s.trend > 0 ? '↑' : '↓' }} {{ Math.abs(s.trend) }}%</p>
      </div>
    </div>

    <!-- Placeholder Chart -->
    <div class="bg-white border border-gray-200 rounded-xl p-6 mb-6">
      <h3 class="font-bold text-gray-900 mb-4">營收趨勢</h3>
      <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center text-gray-400">
        <p>📊 圖表區域（整合 Chart.js 後顯示）</p>
      </div>
    </div>

    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Top Categories -->
      <div class="bg-white border border-gray-200 rounded-xl p-6">
        <h3 class="font-bold text-gray-900 mb-4">分類銷售排行</h3>
        <div class="space-y-3">
          <div v-for="c in topCategories" :key="c.name" class="flex items-center gap-3">
            <span class="text-lg">{{ c.icon }}</span>
            <div class="flex-1">
              <div class="flex justify-between text-sm mb-1"><span>{{ c.name }}</span><span class="font-medium">NT${{ c.revenue.toLocaleString() }}</span></div>
              <div class="w-full bg-gray-100 rounded-full h-2"><div class="bg-primary-500 rounded-full h-2" :style="{ width: c.percent + '%' }"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white border border-gray-200 rounded-xl p-6">
        <h3 class="font-bold text-gray-900 mb-4">近期活動</h3>
        <div class="space-y-4">
          <div v-for="a in activities" :key="a.id" class="flex gap-3 text-sm">
            <div class="w-2 h-2 rounded-full mt-1.5 flex-shrink-0" :class="a.color"></div>
            <div><p class="text-gray-700">{{ a.text }}</p><p class="text-xs text-gray-400">{{ a.time }}</p></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAdminOrderStore } from '@/stores/adminOrder'

const store = useAdminOrderStore()
const activePeriod = ref('month')
const periods = [{ label: '今日', value: 'today' }, { label: '本週', value: 'week' }, { label: '本月', value: 'month' }, { label: '本季', value: 'quarter' }]

/* ---- helpers ---- */
const statusLabels = { pending: '待付款', processing: '處理中', shipped: '已出貨', completed: '已完成', cancelled: '已取消' }

const validOrders = computed(() => store.orders.filter(o => o.status !== 'cancelled'))

const totalRevenue = computed(() => validOrders.value.reduce((s, o) => s + o.total, 0))
const orderCount = computed(() => validOrders.value.length)
const avgOrder = computed(() => orderCount.value ? Math.round(totalRevenue.value / orderCount.value) : 0)

const summary = computed(() => [
  { label: '總營收', value: `NT$${totalRevenue.value.toLocaleString()}`, trend: 12.5 },
  { label: '訂單數', value: String(orderCount.value), trend: 8.3 },
  { label: '平均客單價', value: `NT$${avgOrder.value.toLocaleString()}`, trend: 3.7 },
  { label: '轉換率', value: '3.2%', trend: -0.5 },
])

/* ---- category breakdown from order items ---- */
const categoryIcons = { '肉品海鮮': '🥩', '調味醬料': '🫙', '茶葉飲品': '🍵', '乳製品': '🧀', '零食點心': '🍪' }

const topCategories = computed(() => {
  const map = {}
  validOrders.value.forEach(o => {
    o.items.forEach(item => {
      const cat = item.category || '其他'
      if (!map[cat]) map[cat] = 0
      map[cat] += item.price * item.quantity
    })
  })
  const sorted = Object.entries(map).sort((a, b) => b[1] - a[1])
  const max = sorted.length ? sorted[0][1] : 1
  return sorted.map(([name, revenue]) => ({
    name,
    icon: categoryIcons[name] || '📦',
    revenue,
    percent: Math.round((revenue / max) * 100),
  }))
})

/* ---- recent activity derived from orders ---- */
const activities = computed(() => {
  const acts = []
  const sorted = [...store.orders].sort((a, b) => b.date.localeCompare(a.date))
  sorted.slice(0, 5).forEach(o => {
    const label = statusLabels[o.status] || o.status
    const colors = {
      pending: 'bg-yellow-500', processing: 'bg-blue-500', shipped: 'bg-indigo-500',
      completed: 'bg-green-500', cancelled: 'bg-gray-400',
    }
    acts.push({
      id: o.id,
      text: `訂單 ${o.orderNumber}（${o.customer}）${label}，金額 NT$${o.total.toLocaleString()}`,
      time: o.date,
      color: colors[o.status] || 'bg-gray-500',
    })
  })
  return acts
})
</script>
