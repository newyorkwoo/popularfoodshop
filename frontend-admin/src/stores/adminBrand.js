import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProductsByBrand, brandNameToSlug } from '@/data/products'
import { useAdminProductStore } from './adminProduct'

const SEED_VERSION = 2

const SEED_BRANDS = [
  { id: 1,  name: '和牛專門店', slug: 'wagyu-shop',    logo: 'https://placehold.co/40x40/FFF3E0/EA580C?text=W', active: true,  description: '' },
  { id: 2,  name: '地中海莊園', slug: 'mediterranean', logo: 'https://placehold.co/40x40/F0FDF4/16A34A?text=M', active: true,  description: '' },
  { id: 3,  name: '台灣茶莊',   slug: 'taiwan-tea',    logo: 'https://placehold.co/40x40/ECFDF5/059669?text=T', active: true,  description: '' },
  { id: 4,  name: '北海道牧場', slug: 'hokkaido-farm', logo: 'https://placehold.co/40x40/EFF6FF/2563EB?text=H', active: true,  description: '' },
  { id: 5,  name: '法國甜品屋', slug: 'french-sweets', logo: 'https://placehold.co/40x40/FEF2F2/DC2626?text=F', active: true,  description: '' },
  { id: 6,  name: '義式美食',   slug: 'italian-food',  logo: 'https://placehold.co/40x40/F5F3FF/7C3AED?text=I', active: true,  description: '' },
  { id: 7,  name: '有機農場',   slug: 'organic-farm',  logo: 'https://placehold.co/40x40/F0FDF4/15803D?text=O', active: true,  description: '' },
  { id: 8,  name: '韓國美味',   slug: 'korean-taste',  logo: 'https://placehold.co/40x40/FEF9C3/CA8A04?text=K', active: true,  description: '' },
  { id: 9,  name: '泰式料理',   slug: 'thai-cuisine',  logo: 'https://placehold.co/40x40/FFF7ED/EA580C?text=Th', active: true,  description: '' },
  { id: 10, name: '德國工藝',   slug: 'german-craft',  logo: 'https://placehold.co/40x40/F1F5F9/475569?text=G', active: true,  description: '' },
].map(b => ({ ...b, productCount: getProductsByBrand(b.slug).length }))

export const useAdminBrandStore = defineStore('adminBrand', () => {
  const storedVer = Number(localStorage.getItem('adminBrandsVer') || 0)
  const stored = storedVer >= SEED_VERSION ? localStorage.getItem('adminBrands') : null
  const brands = ref(stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED_BRANDS)))

  function persist() {
    localStorage.setItem('adminBrands', JSON.stringify(brands.value))
    localStorage.setItem('adminBrandsVer', String(SEED_VERSION))
  }

  function createBrand(data) {
    const id = brands.value.length ? Math.max(...brands.value.map(b => b.id)) + 1 : 1
    brands.value.push({
      ...data, id,
      logo: `https://placehold.co/40x40/E2E8F0/64748B?text=${encodeURIComponent(data.name?.charAt(0) || 'N')}`,
      productCount: 0, active: true,
    })
    persist()
  }

  function updateBrand(id, data) {
    const idx = brands.value.findIndex(b => b.id === id)
    if (idx >= 0) {
      Object.assign(brands.value[idx], data)
      persist()
    }
  }

  function toggleActive(id) {
    const brand = brands.value.find(b => b.id === id)
    if (brand) {
      brand.active = !brand.active
      persist()

      // Sync: set matching products' status in adminProduct store
      const matchingNames = Object.entries(brandNameToSlug)
        .filter(([, slug]) => slug === brand.slug)
        .map(([name]) => name)
      if (matchingNames.length) {
        const productStore = useAdminProductStore()
        productStore.setBrandProductsStatus(matchingNames, brand.active ? 'active' : 'archived')
      }
    }
  }

  /**
   * On init, sync products for any already-disabled brands.
   * Called lazily so the product store is ready.
   */
  function syncDisabledBrands() {
    const disabled = brands.value.filter(b => !b.active)
    if (!disabled.length) return
    const productStore = useAdminProductStore()
    for (const brand of disabled) {
      const matchingNames = Object.entries(brandNameToSlug)
        .filter(([, slug]) => slug === brand.slug)
        .map(([name]) => name)
      if (matchingNames.length) {
        productStore.setBrandProductsStatus(matchingNames, 'archived')
      }
    }
  }

  // Run sync on first access
  syncDisabledBrands()

  return { brands, createBrand, updateBrand, toggleActive }
})
