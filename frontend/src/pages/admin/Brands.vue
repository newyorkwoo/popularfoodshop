<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">品牌管理</h2>
      <BaseButton size="sm" @click="openForm()"><PlusIcon class="w-4 h-4 mr-1" /> 新增品牌</BaseButton>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50"><tr>
          <th class="px-4 py-3 text-left font-medium text-gray-600">品牌</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">代稱</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">商品數</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">狀態</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">操作</th>
        </tr></thead>
        <tbody class="divide-y">
          <tr v-for="b in brands" :key="b.id" class="hover:bg-gray-50">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <img :src="b.logo" class="w-8 h-8 rounded-full object-cover bg-gray-100" />
                <span class="font-medium text-gray-900">{{ b.name }}</span>
              </div>
            </td>
            <td class="px-4 py-3 text-gray-500">{{ b.slug }}</td>
            <td class="px-4 py-3 text-gray-600">{{ b.productCount }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="b.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">
                {{ b.active ? '啟用' : '停用' }}
              </span>
            </td>
            <td class="px-4 py-3">
              <button @click="openForm(b)" class="text-primary-600 hover:underline text-xs mr-3">編輯</button>
              <button @click="store.toggleActive(b.id)" class="text-xs" :class="b.active ? 'text-red-500' : 'text-green-600'">{{ b.active ? '停用' : '啟用' }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <BaseModal v-model="showModal" :title="editId ? '編輯品牌' : '新增品牌'">
      <form @submit.prevent="handleSave" class="space-y-4">
        <BaseInput v-model="form.name" label="品牌名稱" required />
        <BaseInput v-model="form.slug" label="代稱 (slug)" required />
        <div><label class="block text-sm font-medium text-gray-700 mb-1">品牌簡介</label>
          <textarea v-model="form.description" rows="3" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm"></textarea></div>
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
import { useAdminBrandStore } from '@/stores/adminBrand'

const store = useAdminBrandStore()
const { brands } = storeToRefs(store)
const showModal = ref(false)
const editId = ref(null)
const form = reactive({ name: '', slug: '', description: '' })

function openForm(b = null) {
  if (b) { editId.value = b.id; Object.assign(form, b) }
  else { editId.value = null; Object.assign(form, { name: '', slug: '', description: '' }) }
  showModal.value = true
}
function handleSave() {
  if (editId.value) {
    store.updateBrand(editId.value, { ...form })
  } else {
    store.createBrand({ ...form })
  }
  showModal.value = false
}
</script>
