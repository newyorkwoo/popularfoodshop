<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900">付款方式</h2>
      <BaseButton size="sm" @click="showAdd = true"><PlusIcon class="w-4 h-4 mr-1" /> 新增信用卡</BaseButton>
    </div>

    <div v-if="cards.length" class="grid md:grid-cols-2 gap-4">
      <div v-for="card in cards" :key="card.id" class="border rounded-xl p-5 relative"
        :class="card.isDefault ? 'border-primary-500 bg-primary-50' : 'border-gray-200'">
        <span v-if="card.isDefault" class="absolute top-3 right-3 text-xs bg-primary-600 text-white px-2 py-0.5 rounded-full">預設</span>
        <div class="flex items-center gap-3 mb-3">
          <span class="text-2xl">{{ cardIcon(card.brand) }}</span>
          <div>
            <p class="font-medium text-gray-900">{{ card.brand }} •••• {{ card.last4 }}</p>
            <p class="text-xs text-gray-500">到期 {{ card.expiry }}</p>
          </div>
        </div>
        <div class="flex gap-3">
          <button v-if="!card.isDefault" @click="setDefault(card.id)" class="text-sm text-primary-600 hover:underline">設為預設</button>
          <button @click="removeCard(card.id)" class="text-sm text-red-500 hover:underline">移除</button>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-16 text-gray-500">尚未綁定任何信用卡</div>

    <BaseModal :visible="showAdd" @close="showAdd = false" title="新增信用卡">
      <form @submit.prevent="addCard" class="space-y-4">
        <BaseInput v-model="newCard.number" label="卡號" placeholder="0000 0000 0000 0000" required />
        <div class="grid grid-cols-2 gap-4">
          <BaseInput v-model="newCard.expiry" label="到期日" placeholder="MM/YY" required />
          <BaseInput v-model="newCard.cvc" label="CVC" placeholder="123" required />
        </div>
        <BaseInput v-model="newCard.name" label="持卡人姓名" required />
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" v-model="newCard.isDefault" class="accent-primary-600" /> 設為預設</label>
        <div class="flex justify-end gap-3 pt-2">
          <BaseButton variant="outline" @click="showAdd = false">取消</BaseButton>
          <BaseButton type="submit">新增</BaseButton>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'

const showAdd = ref(false)
const newCard = reactive({ number: '', expiry: '', cvc: '', name: '', isDefault: false })

const cards = ref([
  { id: 1, brand: 'Visa', last4: '4242', expiry: '12/27', isDefault: true },
  { id: 2, brand: 'Mastercard', last4: '8888', expiry: '06/26', isDefault: false },
])

function cardIcon(brand) {
  return { Visa: '💳', Mastercard: '💳', JCB: '💳' }[brand] || '💳'
}
function setDefault(id) { cards.value.forEach(c => { c.isDefault = c.id === id }) }
function removeCard(id) { cards.value = cards.value.filter(c => c.id !== id) }
function addCard() {
  const last4 = newCard.number.replace(/\s/g, '').slice(-4)
  cards.value.push({ id: Date.now(), brand: 'Visa', last4, expiry: newCard.expiry, isDefault: newCard.isDefault })
  if (newCard.isDefault) cards.value.forEach(c => { c.isDefault = c.last4 === last4 })
  Object.assign(newCard, { number: '', expiry: '', cvc: '', name: '', isDefault: false })
  showAdd.value = false
}
</script>
