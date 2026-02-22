<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">分類管理</h2>
      <BaseButton size="sm" @click="openForm()"><PlusIcon class="w-4 h-4 mr-1" /> 新增分類</BaseButton>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50"><tr>
          <th class="px-4 py-3 text-left font-medium text-gray-600">圖示</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">名稱</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">代稱</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">商品數</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">排序</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">操作</th>
        </tr></thead>
        <tbody class="divide-y">
          <tr v-for="cat in categories" :key="cat.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-2xl">{{ cat.icon }}</td>
            <td class="px-4 py-3 font-medium text-gray-900">{{ cat.name }}</td>
            <td class="px-4 py-3 text-gray-500">{{ cat.slug }}</td>
            <td class="px-4 py-3 text-gray-600">{{ cat.productCount }}</td>
            <td class="px-4 py-3 text-gray-600">{{ cat.sort }}</td>
            <td class="px-4 py-3">
              <button @click="openForm(cat)" class="text-primary-600 hover:underline text-xs mr-3">編輯</button>
              <button @click="remove(cat.id)" class="text-red-500 hover:underline text-xs">刪除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <BaseModal v-model="showModal" :title="editId ? '編輯分類' : '新增分類'">
      <form @submit.prevent="handleSave" class="space-y-4">
        <BaseInput v-model="form.name" label="分類名稱" required />
        <BaseInput v-model="form.slug" label="代稱 (slug)" required />
        <BaseInput v-model="form.icon" label="圖示 (emoji)" />
        <BaseInput v-model.number="form.sort" label="排序" type="number" />
        <div><label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
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
import { useAdminCategoryStore } from '@/stores/adminCategory'

const store = useAdminCategoryStore()
const { categories } = storeToRefs(store)
const showModal = ref(false)
const editId = ref(null)
const form = reactive({ name: '', slug: '', icon: '', sort: 0, description: '' })

function openForm(cat = null) {
  if (cat) { editId.value = cat.id; Object.assign(form, cat) }
  else { editId.value = null; Object.assign(form, { name: '', slug: '', icon: '', sort: store.categories.length + 1, description: '' }) }
  showModal.value = true
}

function handleSave() {
  if (editId.value) {
    store.updateCategory(editId.value, { ...form })
  } else {
    store.createCategory({ ...form })
  }
  showModal.value = false
}

function remove(id) { store.deleteCategory(id) }
</script>
