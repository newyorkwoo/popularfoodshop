<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900">收貨地址</h2>
      <BaseButton size="sm" @click="openForm()">
        <PlusIcon class="w-4 h-4 mr-1" /> 新增地址
      </BaseButton>
    </div>

    <div v-if="addresses.length" class="grid md:grid-cols-2 gap-4">
      <div v-for="addr in addresses" :key="addr.id" class="border rounded-xl p-5 relative" :class="addr.isDefault ? 'border-primary-500 bg-primary-50' : 'border-gray-200'">
        <span v-if="addr.isDefault" class="absolute top-3 right-3 text-xs bg-primary-600 text-white px-2 py-0.5 rounded-full">預設</span>
        <p class="font-medium text-gray-900">{{ addr.name }}</p>
        <p class="text-sm text-gray-500 mt-1">{{ addr.phone }}</p>
        <p class="text-sm text-gray-600 mt-2">{{ addr.zipCode }} {{ addr.city }}{{ addr.district }}{{ addr.address }}</p>
        <div class="flex gap-3 mt-4">
          <button @click="openForm(addr)" class="text-sm text-primary-600 hover:underline">編輯</button>
          <button v-if="!addr.isDefault" @click="setDefault(addr.id)" class="text-sm text-gray-500 hover:underline">設為預設</button>
          <button @click="remove(addr.id)" class="text-sm text-red-500 hover:underline">刪除</button>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-12 text-gray-500">尚無收貨地址</div>

    <!-- Address Form Modal -->
    <BaseModal :visible="showModal" @close="showModal = false" :title="editId ? '編輯地址' : '新增地址'">
      <form @submit.prevent="handleSave" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <BaseInput v-model="form.name" label="收件人" required />
          <BaseInput v-model="form.phone" label="電話" required />
        </div>
        <div class="grid grid-cols-3 gap-4">
          <BaseInput v-model="form.zipCode" label="郵遞區號" />
          <BaseInput v-model="form.city" label="縣市" required />
          <BaseInput v-model="form.district" label="區域" required />
        </div>
        <BaseInput v-model="form.address" label="詳細地址" required />
        <label class="flex items-center gap-2 text-sm">
          <input type="checkbox" v-model="form.isDefault" class="accent-primary-600" /> 設為預設地址
        </label>
        <div class="flex justify-end gap-3 pt-2">
          <BaseButton variant="outline" @click="showModal = false">取消</BaseButton>
          <BaseButton type="submit" :loading="saving">儲存</BaseButton>
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

const showModal = ref(false)
const editId = ref(null)
const saving = ref(false)
const form = reactive({ name: '', phone: '', zipCode: '', city: '', district: '', address: '', isDefault: false })

const addresses = ref([
  { id: 1, name: '王小明', phone: '0912-345-678', zipCode: '106', city: '台北市', district: '大安區', address: '美食路 123 號 5 樓', isDefault: true },
  { id: 2, name: '王小明', phone: '0912-345-678', zipCode: '400', city: '台中市', district: '中區', address: '台灣大道一段 456 號', isDefault: false },
])

function openForm(addr = null) {
  if (addr) {
    editId.value = addr.id
    Object.assign(form, addr)
  } else {
    editId.value = null
    Object.assign(form, { name: '', phone: '', zipCode: '', city: '', district: '', address: '', isDefault: false })
  }
  showModal.value = true
}

async function handleSave() {
  saving.value = true
  await new Promise(r => setTimeout(r, 500))
  if (editId.value) {
    const idx = addresses.value.findIndex(a => a.id === editId.value)
    if (idx >= 0) addresses.value[idx] = { ...form, id: editId.value }
  } else {
    addresses.value.push({ ...form, id: Date.now() })
  }
  if (form.isDefault) {
    addresses.value.forEach(a => { a.isDefault = a.id === (editId.value || addresses.value[addresses.value.length - 1].id) })
  }
  saving.value = false
  showModal.value = false
}

function setDefault(id) { addresses.value.forEach(a => { a.isDefault = a.id === id }) }
function remove(id) { addresses.value = addresses.value.filter(a => a.id !== id) }
</script>
