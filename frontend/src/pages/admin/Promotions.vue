<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">促銷活動</h2>
      <BaseButton size="sm" @click="openForm()"><PlusIcon class="w-4 h-4 mr-1" /> 新增活動</BaseButton>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50"><tr>
          <th class="px-4 py-3 text-left font-medium text-gray-600">活動名稱</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">類型</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">折扣碼</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">折扣</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">期間</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">使用次數</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">狀態</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">操作</th>
        </tr></thead>
        <tbody class="divide-y">
          <tr v-for="p in promotions" :key="p.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-900">{{ p.name }}</td>
            <td class="px-4 py-3 text-gray-600">{{ p.type }}</td>
            <td class="px-4 py-3"><code class="bg-gray-100 px-2 py-0.5 rounded text-xs">{{ p.code }}</code></td>
            <td class="px-4 py-3 text-gray-600">{{ p.discount }}</td>
            <td class="px-4 py-3 text-xs text-gray-500">{{ p.startDate }}<br>~ {{ p.endDate }}</td>
            <td class="px-4 py-3 text-gray-600">{{ p.used }} / {{ p.limit }}</td>
            <td class="px-4 py-3"><span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="p.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">{{ p.active ? '進行中' : '已結束' }}</span></td>
            <td class="px-4 py-3">
              <button @click="openForm(p)" class="text-primary-600 hover:underline text-xs mr-3">編輯</button>
              <button @click="remove(p.id)" class="text-red-500 hover:underline text-xs">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <BaseModal v-model="showModal" :title="editId ? '編輯活動' : '新增活動'" size="lg">
      <form @submit.prevent="handleSave" class="space-y-4">
        <BaseInput v-model="form.name" label="活動名稱" required />
        <div class="grid grid-cols-2 gap-4">
          <div><label class="block text-sm font-medium text-gray-700 mb-1">類型</label>
            <select v-model="form.type" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option>百分比折扣</option><option>固定金額折扣</option><option>免運費</option>
            </select></div>
          <BaseInput v-model="form.code" label="折扣碼" required />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <BaseInput v-model="form.discount" label="折扣值" required />
          <BaseInput v-model.number="form.limit" label="使用上限" type="number" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <BaseInput v-model="form.startDate" label="開始日期" type="date" required />
          <BaseInput v-model="form.endDate" label="結束日期" type="date" required />
        </div>
        <BaseInput v-model.number="form.minAmount" label="最低消費金額 (NT$)" type="number" />
        <div class="flex justify-end gap-3 pt-2">
          <BaseButton variant="outline" @click="showModal = false">取消</BaseButton>
          <BaseButton type="submit">儲存</BaseButton>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { PlusIcon } from '@heroicons/vue/24/outline'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import { useAdminPromotionStore } from '@/stores/adminPromotion'

const store = useAdminPromotionStore()
const { promotions } = storeToRefs(store)
const showModal = ref(false)
const editId = ref(null)
const form = reactive({ name: '', type: '百分比折扣', code: '', discount: '', limit: 100, startDate: '', endDate: '', minAmount: 0 })

function openForm(p = null) {
  if (p) { editId.value = p.id; Object.assign(form, p) }
  else { editId.value = null; Object.assign(form, { name: '', type: '百分比折扣', code: '', discount: '', limit: 100, startDate: '', endDate: '', minAmount: 0 }) }
  showModal.value = true
}
function handleSave() {
  if (editId.value) {
    store.updatePromotion(editId.value, { ...form })
  } else {
    store.createPromotion({ ...form })
  }
  showModal.value = false
}
function remove(id) { store.deletePromotion(id) }
</script>
