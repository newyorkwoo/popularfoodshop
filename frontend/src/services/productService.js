import api from './api'

export default {
  getProducts(params = {}) {
    return api.get('/products', { params })
  },

  getProduct(slug) {
    return api.get(`/products/${slug}`)
  },

  getProductReviews(slug, params = {}) {
    return api.get(`/products/${slug}/reviews`, { params })
  },

  createReview(slug, data) {
    return api.post(`/products/${slug}/reviews`, data)
  },

  // Categories
  getCategories(params = {}) {
    return api.get('/categories', { params })
  },

  getCategory(slug) {
    return api.get(`/categories/${slug}`)
  },

  getCategoryProducts(slug, params = {}) {
    return api.get(`/categories/${slug}/products`, { params })
  },

  // Brands
  getBrands(params = {}) {
    return api.get('/brands', { params })
  },

  getBrand(slug) {
    return api.get(`/brands/${slug}`)
  },

  getBrandProducts(slug, params = {}) {
    return api.get(`/brands/${slug}/products`, { params })
  },

  // Search
  search(query, params = {}) {
    return api.get('/search', { params: { q: query, ...params } })
  },

  searchSuggestions(query) {
    return api.get('/search/suggestions', { params: { q: query } })
  },
}
