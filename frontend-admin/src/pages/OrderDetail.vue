<template>
  <div>
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/orders" class="text-gray-400 hover:text-gray-600"><ArrowLeftIcon class="w-5 h-5" /></router-link>
      <h2 class="text-2xl font-bold text-gray-900">訂單詳情</h2>
    </div>

    <div v-if="order" class="grid lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <!-- Items -->
        <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
          <div class="px-5 py-3 bg-gray-50 font-medium text-sm text-gray-700">訂單商品</div>
          <div v-for="item in order.items" :key="item.id" class="flex items-center gap-4 px-5 py-4 border-t">
            <img :src="item.image" class="w-14 h-14 rounded-lg object-cover bg-gray-100" />
            <div class="flex-1"><p class="font-medium text-gray-900 text-sm">{{ item.name }}</p><p class="text-xs text-gray-500">SKU: {{ item.sku }}</p></div>
            <p class="text-sm text-gray-500">x{{ item.quantity }}</p>
            <p class="text-sm font-medium">NT${{ (item.price * item.quantity).toLocaleString() }}</p>
          </div>
        </div>

        <!-- Shipping -->
        <div class="bg-white border border-gray-200 rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">收貨資訊</h3>
          <div class="text-sm text-gray-600 space-y-1">
            <p>{{ order.shipping.name }} / {{ order.shipping.phone }}</p>
            <p>{{ order.shipping.address }}</p>
            <p class="text-gray-400">配送方式：{{ order.shipping.method }}</p>
          </div>
        </div>

        <!-- Notes -->
        <div class="bg-white border border-gray-200 rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">管理備註</h3>
          <textarea v-model="adminNote" rows="3" class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" placeholder="新增內部備註..."></textarea>
          <BaseButton size="sm" class="mt-2" variant="outline" @click="saveNote">儲存備註</BaseButton>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <div class="bg-white border border-gray-200 rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">訂單狀態</h3>
          <p class="text-sm text-gray-500 mb-2">訂單編號：{{ order.orderNumber }}</p>
          <p class="text-sm text-gray-500 mb-4">下單時間：{{ order.date }}</p>
          <select v-model="selectedStatus" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm mb-3">
            <option value="pending">待付款</option><option value="processing">處理中</option>
            <option value="shipped">已出貨</option><option value="completed">已完成</option>
            <option value="cancelled">已取消</option>
          </select>
          <BaseButton class="w-full" size="sm" @click="updateStatus">更新狀態</BaseButton>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">付款明細</h3>
          <div class="text-sm space-y-2">
            <div class="flex justify-between"><span class="text-gray-500">商品小計</span><span>NT${{ order.subtotal.toLocaleString() }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">運費</span><span>NT${{ order.shippingFee.toLocaleString() }}</span></div>
            <div class="flex justify-between font-bold pt-2 border-t"><span>合計</span><span class="text-primary-600">NT${{ order.total.toLocaleString() }}</span></div>
            <p class="text-gray-400 mt-2">付款方式：{{ order.paymentMethod }}</p>
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-3">客戶資訊</h3>
          <p class="text-sm text-gray-600">{{ order.customer.name }}</p>
          <p class="text-sm text-gray-500">{{ order.customer.email }}</p>
          <p class="text-sm text-gray-500">{{ order.customer.phone }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAdminOrderStore } from '@/stores/adminOrder'

const route = useRoute()
const store = useAdminOrderStore()
const adminNote = ref('')
const selectedStatus = ref('')

const order = computed(() => {
  const o = store.getOrder(route.params.id)
  if (!o) return null
  return {
    ...o,
    customer: o.customerInfo || { name: o.customer, email: '', phone: '' },
  }
})

onMounted(() => {
  if (order.value) {
    adminNote.value = order.value.adminNote || ''
    selectedStatus.value = order.value.status
  }
})

function saveNote() {
  store.updateNote(route.params.id, adminNote.value)
}

function updateStatus() {
  store.updateStatus(route.params.id, selectedStatus.value)
}
</script>
