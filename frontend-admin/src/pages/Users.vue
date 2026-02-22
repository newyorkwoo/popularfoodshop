<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">會員管理</h2>
    <div class="flex flex-wrap items-center gap-3 mb-6">
      <input v-model="search" placeholder="搜尋會員..." class="border border-gray-300 rounded-lg px-3 py-2 text-sm w-60 focus:ring-2 focus:ring-primary-500" />
      <select v-model="filterStatus" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
        <option value="">所有狀態</option><option value="active">啟用</option><option value="inactive">停用</option>
      </select>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50"><tr>
          <th class="px-4 py-3 text-left font-medium text-gray-600">會員</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">電子郵件</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">註冊日期</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">訂單數</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">總消費</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">狀態</th>
          <th class="px-4 py-3 text-left font-medium text-gray-600">操作</th>
        </tr></thead>
        <tbody class="divide-y">
          <tr v-for="u in filteredUsers" :key="u.id" class="hover:bg-gray-50">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-sm font-bold text-primary-600">{{ u.name.charAt(0) }}</div>
                <span class="font-medium text-gray-900">{{ u.name }}</span>
              </div>
            </td>
            <td class="px-4 py-3 text-gray-500">{{ u.email }}</td>
            <td class="px-4 py-3 text-gray-500">{{ u.joinDate }}</td>
            <td class="px-4 py-3 text-gray-600">{{ u.orderCount }}</td>
            <td class="px-4 py-3 font-medium">NT${{ u.totalSpent.toLocaleString() }}</td>
            <td class="px-4 py-3"><span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="u.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">{{ u.active ? '啟用' : '停用' }}</span></td>
            <td class="px-4 py-3">
              <button @click="adminUserStore.toggleActive(u.id)" class="text-xs mr-3" :class="u.active ? 'text-red-500 hover:underline' : 'text-green-600 hover:underline'">{{ u.active ? '停用' : '啟用' }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <BasePagination :current-page="1" :total-pages="3" class="mt-6" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BasePagination from '@/components/ui/BasePagination.vue'
import { useAdminUserStore } from '@/stores/adminUser'

const adminUserStore = useAdminUserStore()

const search = ref('')
const filterStatus = ref('')

const filteredUsers = computed(() =>
  adminUserStore.users.filter(u => {
    if (search.value && !u.name.includes(search.value) && !u.email.includes(search.value)) return false
    if (filterStatus.value === 'active' && !u.active) return false
    if (filterStatus.value === 'inactive' && u.active) return false
    return true
  })
)
</script>
