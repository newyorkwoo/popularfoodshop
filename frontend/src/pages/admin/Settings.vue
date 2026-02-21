<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">系統設定</h2>

    <div class="space-y-6 max-w-2xl">
      <!-- Store Info -->
      <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <h3 class="font-bold text-gray-900">商店資訊</h3>
        <BaseInput v-model="settings.storeName" label="商店名稱" />
        <BaseInput v-model="settings.email" label="客服信箱" type="email" />
        <BaseInput v-model="settings.phone" label="客服電話" />
        <BaseInput v-model="settings.address" label="地址" />
        <BaseButton size="sm" @click="store.save()">儲存</BaseButton>
      </div>

      <!-- Shipping -->
      <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <h3 class="font-bold text-gray-900">運費設定</h3>
        <BaseInput v-model.number="settings.freeShippingThreshold" label="免運門檻 (NT$)" type="number" />
        <BaseInput v-model.number="settings.normalShipping" label="常溫運費 (NT$)" type="number" />
        <BaseInput v-model.number="settings.coldShipping" label="冷藏/冷凍運費 (NT$)" type="number" />
        <BaseInput v-model.number="settings.convenienceShipping" label="超商取貨運費 (NT$)" type="number" />
        <BaseButton size="sm" @click="store.save()">儲存</BaseButton>
      </div>

      <!-- Payment -->
      <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <h3 class="font-bold text-gray-900">付款方式</h3>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="settings.creditCard" class="accent-primary-600" /> 信用卡</label>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="settings.linePay" class="accent-primary-600" /> LINE Pay</label>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="settings.cod" class="accent-primary-600" /> 貨到付款</label>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="settings.bankTransfer" class="accent-primary-600" /> 銀行轉帳</label>
        <BaseButton size="sm" @click="store.save()">儲存</BaseButton>
      </div>

      <!-- Points -->
      <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <h3 class="font-bold text-gray-900">點數設定</h3>
        <BaseInput v-model.number="settings.pointRate" label="消費 NT$1 獲得點數" type="number" />
        <BaseInput v-model.number="settings.pointValue" label="每點折抵金額 (NT$)" type="number" step="0.1" />
        <BaseInput v-model.number="settings.pointExpiry" label="點數有效期限 (天)" type="number" />
        <BaseButton size="sm" @click="store.save()">儲存</BaseButton>
      </div>

      <!-- Notification -->
      <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
        <h3 class="font-bold text-gray-900">通知設定</h3>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="settings.orderNotify" class="accent-primary-600" /> 新訂單通知</label>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="settings.lowStockNotify" class="accent-primary-600" /> 庫存不足通知</label>
        <BaseInput v-model.number="settings.lowStockThreshold" label="庫存警示門檻" type="number" />
        <BaseButton size="sm" @click="store.save()">儲存</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAdminSettingsStore } from '@/stores/adminSettings'

const store = useAdminSettingsStore()
const { settings } = storeToRefs(store)
</script>
