import { defineStore } from 'pinia'
import { ref } from 'vue'

const SEED_CATEGORIES = [
  { id: 1, name: '肉品海鮮', slug: 'meat-seafood', icon: '🥩', productCount: 45, sort: 1, description: '' },
  { id: 2, name: '蔬果生鮮', slug: 'vegetables', icon: '🥬', productCount: 38, sort: 2, description: '' },
  { id: 3, name: '調味醬料', slug: 'sauces', icon: '🫙', productCount: 28, sort: 3, description: '' },
  { id: 4, name: '茶葉飲品', slug: 'tea-drinks', icon: '🍵', productCount: 22, sort: 4, description: '' },
  { id: 5, name: '乳製品', slug: 'dairy', icon: '🧀', productCount: 18, sort: 5, description: '' },
  { id: 6, name: '零食點心', slug: 'snacks', icon: '🍪', productCount: 35, sort: 6, description: '' },
]

export const useAdminCategoryStore = defineStore('adminCategory', () => {
  const stored = localStorage.getItem('adminCategories')
  const categories = ref(stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED_CATEGORIES)))

  function persist() {
    localStorage.setItem('adminCategories', JSON.stringify(categories.value))
  }

  function createCategory(data) {
    const id = categories.value.length ? Math.max(...categories.value.map(c => c.id)) + 1 : 1
    categories.value.push({ ...data, id, productCount: 0 })
    persist()
  }

  function updateCategory(id, data) {
    const idx = categories.value.findIndex(c => c.id === id)
    if (idx >= 0) {
      Object.assign(categories.value[idx], data)
      persist()
    }
  }

  function deleteCategory(id) {
    categories.value = categories.value.filter(c => c.id !== id)
    persist()
  }

  return { categories, createCategory, updateCategory, deleteCategory }
})
