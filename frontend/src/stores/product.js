import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import productService from '@/services/productService'

export const useProductStore = defineStore('product', () => {
  // State
  const products = ref([])
  const currentProduct = ref(null)
  const categories = ref([])
  const brands = ref([])
  const filters = ref({
    category: null,
    brand: null,
    priceMin: null,
    priceMax: null,
    origin: null,
    sort: 'newest',
    search: '',
  })
  const pagination = ref({
    page: 1,
    perPage: 24,
    total: 0,
    totalPages: 0,
  })
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const hasMore = computed(() => pagination.value.page < pagination.value.totalPages)

  const activeFiltersCount = computed(() => {
    let count = 0
    if (filters.value.category) count++
    if (filters.value.brand) count++
    if (filters.value.priceMin || filters.value.priceMax) count++
    if (filters.value.origin) count++
    return count
  })

  // Actions
  async function fetchProducts(params = {}) {
    loading.value = true
    error.value = null
    try {
      const queryParams = {
        page: pagination.value.page,
        per_page: pagination.value.perPage,
        sort: filters.value.sort,
        ...params,
      }

      if (filters.value.category) queryParams.category = filters.value.category
      if (filters.value.brand) queryParams.brand = filters.value.brand
      if (filters.value.priceMin) queryParams.price_min = filters.value.priceMin
      if (filters.value.priceMax) queryParams.price_max = filters.value.priceMax
      if (filters.value.origin) queryParams.origin = filters.value.origin
      if (filters.value.search) queryParams.search = filters.value.search

      const response = await productService.getProducts(queryParams)
      products.value = response.data.items
      pagination.value = {
        page: response.data.page,
        perPage: response.data.perPage,
        total: response.data.total,
        totalPages: response.data.totalPages,
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '載入商品失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchProductBySlug(slug) {
    loading.value = true
    error.value = null
    try {
      const response = await productService.getProduct(slug)
      currentProduct.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '載入商品詳情失敗'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await productService.getCategories()
      categories.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch categories:', err)
    }
  }

  async function fetchBrands() {
    try {
      const response = await productService.getBrands()
      brands.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch brands:', err)
    }
  }

  async function searchProducts(query) {
    filters.value.search = query
    pagination.value.page = 1
    return fetchProducts()
  }

  function setFilter(key, value) {
    filters.value[key] = value
    pagination.value.page = 1
  }

  function clearFilters() {
    filters.value = {
      category: null,
      brand: null,
      priceMin: null,
      priceMax: null,
      origin: null,
      sort: 'newest',
      search: '',
    }
    pagination.value.page = 1
  }

  function setPage(page) {
    pagination.value.page = page
  }

  function clearCurrentProduct() {
    currentProduct.value = null
  }

  return {
    products,
    currentProduct,
    categories,
    brands,
    filters,
    pagination,
    loading,
    error,
    hasMore,
    activeFiltersCount,
    fetchProducts,
    fetchProductBySlug,
    fetchCategories,
    fetchBrands,
    searchProducts,
    setFilter,
    clearFilters,
    setPage,
    clearCurrentProduct,
  }
})
