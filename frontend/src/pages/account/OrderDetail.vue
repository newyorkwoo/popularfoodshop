<template>
  <div>
    <router-link to="/account/orders" class="text-sm text-primary-600 hover:underline mb-4 inline-flex items-center gap-1">
      <ArrowLeftIcon class="w-4 h-4" /> 返回訂單列表
    </router-link>

    <div class="mt-4 space-y-6">
      <!-- Order Header -->
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-xl font-bold text-gray-900">訂單 {{ order.orderNumber }}</h2>
          <p class="text-sm text-gray-500 mt-1">下單時間：{{ order.date }}</p>
        </div>
        <span class="px-3 py-1 rounded-full text-sm font-medium" :class="statusClass">{{ statusLabel }}</span>
      </div>

      <!-- Progress -->
      <div class="flex items-center gap-0">
        <div v-for="(step, i) in progressSteps" :key="i" class="flex items-center" :class="i < progressSteps.length - 1 ? 'flex-1' : ''">
          <div class="flex flex-col items-center">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
              :class="i <= currentStep ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-400'">{{ i + 1 }}</div>
            <span class="text-xs mt-1" :class="i <= currentStep ? 'text-primary-600' : 'text-gray-400'">{{ step }}</span>
          </div>
          <div v-if="i < progressSteps.length - 1" class="flex-1 h-0.5 mx-2" :class="i < currentStep ? 'bg-primary-600' : 'bg-gray-200'"></div>
        </div>
      </div>

      <!-- Items -->
      <div class="border rounded-xl overflow-hidden">
        <div class="px-5 py-3 bg-gray-50 text-sm font-medium text-gray-700">訂單商品</div>
        <div v-for="item in order.items" :key="item.id" class="flex items-center gap-4 px-5 py-4 border-t">
          <img :src="item.image" class="w-20 h-20 rounded-lg object-cover bg-gray-100" />
          <div class="flex-1">
            <p class="font-medium text-gray-900">{{ item.name }}</p>
            <p class="text-sm text-gray-500">NT${{ item.price.toLocaleString() }} x {{ item.quantity }}</p>
          </div>
          <p class="font-medium">NT${{ (item.price * item.quantity).toLocaleString() }}</p>
        </div>
      </div>

      <!-- Summary + Shipping -->
      <div class="grid md:grid-cols-2 gap-6">
        <div class="border rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">收貨資訊</h3>
          <p class="text-sm text-gray-600">{{ order.shipping.name }}</p>
          <p class="text-sm text-gray-600">{{ order.shipping.phone }}</p>
          <p class="text-sm text-gray-600 mt-1">{{ order.shipping.address }}</p>
        </div>
        <div class="border rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">付款明細</h3>
          <div class="text-sm space-y-2">
            <div class="flex justify-between"><span class="text-gray-500">商品小計</span><span>NT${{ order.subtotal.toLocaleString() }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">運費</span><span>NT${{ order.shippingFee.toLocaleString() }}</span></div>
            <div v-if="order.discount" class="flex justify-between"><span class="text-gray-500">折扣</span><span class="text-red-500">-NT${{ order.discount.toLocaleString() }}</span></div>
            <div class="flex justify-between font-bold pt-2 border-t"><span>合計</span><span class="text-primary-600">NT${{ order.total.toLocaleString() }}</span></div>
            <p class="text-gray-500 mt-2">付款方式：{{ order.paymentMethod }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'

const progressSteps = ['訂單成立', '付款完成', '商品出貨', '配送完成']
const order = {
  id: 1, orderNumber: 'PFS20250101001', date: '2025-01-15 14:30', status: 'shipped',
  items: [
    { id: 1, name: '日本A5和牛火鍋片', quantity: 2, price: 1280, image: 'https://placehold.co/100x100/FFF3E0/EA580C?text=和牛' },
  ],
  shipping: { name: '王小明', phone: '0912-345-678', address: '台北市大安區美食路 123 號 5 樓' },
  subtotal: 2560, shippingFee: 0, discount: 0, total: 2560, paymentMethod: '信用卡',
}

const currentStep = computed(() => {
  return { pending: 0, processing: 1, shipped: 2, completed: 3, cancelled: -1 }[order.status] ?? 0
})
const statusLabel = computed(() => ({ pending: '待付款', processing: '處理中', shipped: '已出貨', completed: '已完成', cancelled: '已取消' }[order.status]))
const statusClass = computed(() => ({
  pending: 'bg-yellow-100 text-yellow-700', processing: 'bg-blue-100 text-blue-700',
  shipped: 'bg-indigo-100 text-indigo-700', completed: 'bg-green-100 text-green-700',
  cancelled: 'bg-gray-100 text-gray-500',
}[order.status]))
</script>
