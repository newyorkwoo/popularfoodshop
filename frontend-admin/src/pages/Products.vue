<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">商品管理</h2>
      <router-link to="/products/create" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition text-sm font-medium">
        + 新增商品
      </router-link>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-3 mb-6">
      <input v-model="search" placeholder="搜尋商品..." class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-60 focus:ring-2 focus:ring-primary-500 focus:border-primary-500" />
      <select v-model="filterCategory" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
        <option value="">所有分類</option>
        <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
      </select>
      <select v-model="filterStatus" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
        <option value="">所有狀態</option>
        <option value="active">上架</option>
        <option value="draft">草稿</option>
        <option value="archived">已下架</option>
      </select>
    </div>

    <!-- Table -->
    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 text-left">
          <tr>
            <th class="px-4 py-3 font-medium text-gray-600">商品</th>
            <th class="px-4 py-3 font-medium text-gray-600">分類</th>
            <th class="px-4 py-3 font-medium text-gray-600">價格</th>
            <th class="px-4 py-3 font-medium text-gray-600">庫存</th>
            <th class="px-4 py-3 font-medium text-gray-600">狀態</th>
            <th class="px-4 py-3 font-medium text-gray-600">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="p in pagedProducts" :key="p.id" class="hover:bg-gray-50">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <img :src="p.image" class="w-10 h-10 rounded-lg object-cover bg-gray-100" />
                <div>
                  <p class="font-medium text-gray-900">{{ p.name }}</p>
                  <p class="text-xs text-gray-500">SKU: {{ p.sku }}</p>
                </div>
              </div>
            </td>
            <td class="px-4 py-3 text-gray-600">{{ p.category }}</td>
            <td class="px-4 py-3">
              <span v-if="p.originalPrice" class="text-gray-400 line-through text-xs mr-1">{{ p.originalPrice }}</span>
              <span class="font-medium">NT${{ p.price.toLocaleString() }}</span>
            </td>
            <td class="px-4 py-3" :class="p.stock < 10 ? 'text-red-600 font-medium' : 'text-gray-600'">{{ p.stock }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs font-medium"
                :class="{ 'bg-green-100 text-green-700': p.status === 'active', 'bg-gray-100 text-gray-500': p.status === 'draft', 'bg-red-100 text-red-600': p.status === 'archived' }">
                {{ { active: '上架', draft: '草稿', archived: '已下架' }[p.status] }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex gap-2">
                <router-link :to="`/products/${p.id}/edit`" class="text-primary-600 hover:underline text-xs">編輯</router-link>
                <button @click="toggleStatus(p)" class="text-xs" :class="p.status === 'active' ? 'text-red-500 hover:underline' : 'text-green-600 hover:underline'">
                  {{ p.status === 'active' ? '下架' : '上架' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <BasePagination v-if="totalPages > 1" v-model="currentPage" :total-pages="totalPages" class="mt-6" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BasePagination from '@/components/ui/BasePagination.vue'
import { useAdminProductStore } from '@/stores/adminProduct'
import { useAdminBrandStore } from '@/stores/adminBrand'

const adminProductStore = useAdminProductStore()
// Initializing the brand store triggers syncDisabledBrands()
useAdminBrandStore()

const search = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const perPage = 10
const categories = ['零食點心', '茶葉飲品', '調味醬料', '穀物雜糧', '其他']

const filteredProducts = computed(() => {
  return adminProductStore.products.filter(p => {
    if (search.value && !p.name.includes(search.value) && !p.sku.includes(search.value)) return false
    if (filterCategory.value && p.category !== filterCategory.value) return false
    if (filterStatus.value && p.status !== filterStatus.value) return false
    return true
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredProducts.value.length / perPage)))

const pagedProducts = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredProducts.value.slice(start, start + perPage)
})

function toggleStatus(p) {
  adminProductStore.toggleStatus(p.id)
}
</script>
