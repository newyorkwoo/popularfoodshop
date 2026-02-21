import api from './api'

export default {
  // Dashboard
  getDashboard() {
    return api.get('/admin/dashboard')
  },

  // Products
  getProducts(params = {}) {
    return api.get('/admin/products', { params })
  },

  getProduct(id) {
    return api.get(`/admin/products/${id}`)
  },

  createProduct(data) {
    return api.post('/admin/products', data)
  },

  updateProduct(id, data) {
    return api.put(`/admin/products/${id}`, data)
  },

  deleteProduct(id) {
    return api.delete(`/admin/products/${id}`)
  },

  uploadProductImage(id, formData) {
    return api.post(`/admin/products/${id}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  // Categories
  getCategories(params = {}) {
    return api.get('/admin/categories', { params })
  },

  createCategory(data) {
    return api.post('/admin/categories', data)
  },

  updateCategory(id, data) {
    return api.put(`/admin/categories/${id}`, data)
  },

  deleteCategory(id) {
    return api.delete(`/admin/categories/${id}`)
  },

  // Brands
  getBrands(params = {}) {
    return api.get('/admin/brands', { params })
  },

  createBrand(data) {
    return api.post('/admin/brands', data)
  },

  updateBrand(id, data) {
    return api.put(`/admin/brands/${id}`, data)
  },

  deleteBrand(id) {
    return api.delete(`/admin/brands/${id}`)
  },

  // Orders
  getOrders(params = {}) {
    return api.get('/admin/orders', { params })
  },

  getOrder(id) {
    return api.get(`/admin/orders/${id}`)
  },

  updateOrderStatus(id, status) {
    return api.put(`/admin/orders/${id}/status`, { status })
  },

  // Users
  getUsers(params = {}) {
    return api.get('/admin/users', { params })
  },

  getUser(id) {
    return api.get(`/admin/users/${id}`)
  },

  updateUser(id, data) {
    return api.put(`/admin/users/${id}`, data)
  },

  toggleUserStatus(id) {
    return api.put(`/admin/users/${id}/toggle-status`)
  },

  // Promotions
  getPromotions(params = {}) {
    return api.get('/admin/promotions', { params })
  },

  createPromotion(data) {
    return api.post('/admin/promotions', data)
  },

  updatePromotion(id, data) {
    return api.put(`/admin/promotions/${id}`, data)
  },

  deletePromotion(id) {
    return api.delete(`/admin/promotions/${id}`)
  },

  // Reports
  getSalesReport(params = {}) {
    return api.get('/admin/reports/sales', { params })
  },

  getProductsReport(params = {}) {
    return api.get('/admin/reports/products', { params })
  },

  getUsersReport(params = {}) {
    return api.get('/admin/reports/users', { params })
  },

  // Settings
  getSettings() {
    return api.get('/admin/settings')
  },

  updateSettings(data) {
    return api.put('/admin/settings', data)
  },

  // Content (banners, pages)
  getBanners() {
    return api.get('/admin/content/banners')
  },

  createBanner(data) {
    return api.post('/admin/content/banners', data)
  },

  updateBanner(id, data) {
    return api.put(`/admin/content/banners/${id}`, data)
  },

  deleteBanner(id) {
    return api.delete(`/admin/content/banners/${id}`)
  },
}
