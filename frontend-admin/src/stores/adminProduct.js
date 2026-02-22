import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { allProducts } from '@/data/products'

const SEED_VERSION = 2

/* Map front-end category slugs → admin display labels */
const categoryLabel = {
  'imported-chocolate': '零食點心',
  'fine-tea': '茶葉飲品',
  'japanese-snacks': '零食點心',
  'healthy-grains': '穀物雜糧',
  'handmade-cookies': '零食點心',
  'dried-fruits': '零食點心',
  'beverages': '茶葉飲品',
  'seasonings': '調味醬料',
  'popular-snacks': '零食點心',
  'organic-food': '穀物雜糧',
}

/* Convert slug → SKU prefix */
function slugToSku(slug, idx) {
  const prefix = slug.replace(/-/g, '').substring(0, 6).toUpperCase()
  return `${prefix}-${String(idx).padStart(3, '0')}`
}

/* Build admin seed from shared product catalog */
const SEED_PRODUCTS = allProducts.map((p, i) => ({
  id: p.id,
  name: p.name,
  slug: p.slug,
  description: p.description || '',
  price: p.salePrice || p.price,
  originalPrice: p.salePrice ? p.price : null,
  cost: Math.round((p.salePrice || p.price) * 0.5),
  stock: p.stock ?? 50,
  sku: slugToSku(p.slug, i + 1),
  status: p.inStock === false ? 'draft' : 'active',
  category: categoryLabel[p.category] || '其他',
  brand: p.brand || '',
  image: p.image,
}))

export const useAdminProductStore = defineStore('adminProduct', () => {
  // Initialize from localStorage or seed data
  const storedVer = Number(localStorage.getItem('adminProductsVer') || 0)
  const stored = storedVer >= SEED_VERSION ? localStorage.getItem('adminProducts') : null
  const products = ref(stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED_PRODUCTS)))

  // Auto-increment ID
  let nextId = Math.max(...products.value.map(p => p.id)) + 1

  function persist() {
    localStorage.setItem('adminProducts', JSON.stringify(products.value))
    localStorage.setItem('adminProductsVer', String(SEED_VERSION))
    // Sync all product statuses to share file so consumer frontend can read
    syncStatusToShared()
  }

  /** Push every product's status to the shared JSON file via Vite dev API. */
  function syncStatusToShared() {
    const payload = products.value.map(p => ({ id: p.id, status: p.status }))
    fetch('/api/product-status/bulk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ products: payload }),
    }).catch(() => { /* ignore in production – backend API handles it */ })
  }

  // Getters
  const totalProducts = computed(() => products.value.length)
  const activeProducts = computed(() => products.value.filter(p => p.status === 'active').length)

  // Actions
  function getProduct(id) {
    return products.value.find(p => p.id === Number(id))
  }

  function createProduct(data) {
    const product = {
      ...data,
      id: nextId++,
      image: data.image || `https://placehold.co/50x50/FFF3E0/EA580C?text=${encodeURIComponent(data.name?.charAt(0) || '新')}`,
    }
    products.value.push(product)
    persist()
    return product
  }

  function updateProduct(id, data) {
    const index = products.value.findIndex(p => p.id === Number(id))
    if (index === -1) return null
    products.value[index] = { ...products.value[index], ...data }
    persist()
    return products.value[index]
  }

  function deleteProduct(id) {
    const index = products.value.findIndex(p => p.id === Number(id))
    if (index === -1) return false
    products.value.splice(index, 1)
    persist()
    return true
  }

  function toggleStatus(id) {
    const product = getProduct(id)
    if (!product) return null
    product.status = product.status === 'active' ? 'archived' : 'active'
    persist()
    return product
  }

  /**
   * Bulk set status for all products belonging to a brand slug.
   * brandNames: array of brand name strings that map to the slug.
   * status: 'active' | 'archived'
   */
  function setBrandProductsStatus(brandNames, status) {
    let changed = false
    products.value.forEach(p => {
      if (brandNames.includes(p.brand)) {
        p.status = status
        changed = true
      }
    })
    if (changed) persist()
  }

  // Reset to seed data
  function resetProducts() {
    products.value = JSON.parse(JSON.stringify(SEED_PRODUCTS))
    nextId = Math.max(...products.value.map(p => p.id)) + 1
    persist()
  }

  // Initial sync on store creation — populate shared file with current statuses
  syncStatusToShared()

  return {
    products,
    totalProducts,
    activeProducts,
    getProduct,
    createProduct,
    updateProduct,
    deleteProduct,
    toggleStatus,
    setBrandProductsStatus,
    resetProducts,
  }
})
