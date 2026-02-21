import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const SEED_USERS = [
  { id: 1, name: '王小明', email: 'wang@example.com', joinDate: '2025-01-01', orderCount: 5, totalSpent: 12800, active: true },
  { id: 2, name: '李美麗', email: 'li@example.com', joinDate: '2025-01-05', orderCount: 3, totalSpent: 5670, active: true },
  { id: 3, name: '張大華', email: 'zhang@example.com', joinDate: '2025-01-10', orderCount: 8, totalSpent: 24500, active: true },
  { id: 4, name: '陳小芳', email: 'chen@example.com', joinDate: '2025-01-12', orderCount: 1, totalSpent: 680, active: true },
  { id: 5, name: '林志偉', email: 'lin@example.com', joinDate: '2025-01-15', orderCount: 0, totalSpent: 0, active: false },
]

export const useAdminUserStore = defineStore('adminUser', () => {
  const stored = localStorage.getItem('adminUsers')
  const users = ref(stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED_USERS)))

  function persist() {
    localStorage.setItem('adminUsers', JSON.stringify(users.value))
  }

  const totalUsers = computed(() => users.value.length)
  const activeUsers = computed(() => users.value.filter(u => u.active).length)

  function toggleActive(id) {
    const user = users.value.find(u => u.id === Number(id))
    if (!user) return null
    user.active = !user.active
    persist()
    return user
  }

  function resetUsers() {
    users.value = JSON.parse(JSON.stringify(SEED_USERS))
    persist()
  }

  return { users, totalUsers, activeUsers, toggleActive, resetUsers }
})
