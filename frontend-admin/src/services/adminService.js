import api from './api'

export default {
  // Dashboard
  getDashboard() {
    return api.get('/v1/admin/dashboard')
  },

  // Products
  getProducts(params = {}) {
    return api.get('/v1/admin/products', { params })
  },

  getProduct(id) {
    return api.get(`/v1/admin/products/${id}`)
  },

  createProduct(data) {
    return api.post('/v1/admin/products', data)
  },

  updateProduct(id, data) {
    return api.put(`/v1/admin/products/${id}`, data)
  },

  deleteProduct(id) {
    return api.delete(`/v1/admin/products/${id}`)
  },

  uploadProductImage(id, formData) {
    return api.post(`/v1/admin/products/${id}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  // Categories
  getCategories(params = {}) {
    return api.get('/v1/admin/categories', { params })
  },

  createCategory(data) {
    return api.post('/v1/admin/categories', data)
  },

  updateCategory(id, data) {
    return api.put(`/v1/admin/categories/${id}`, data)
  },

  deleteCategory(id) {
    return api.delete(`/v1/admin/categories/${id}`)
  },

  // Brands
  getBrands(params = {}) {
    return api.get('/v1/admin/brands', { params })
  },

  createBrand(data) {
    return api.post('/v1/admin/brands', data)
  },

  updateBrand(id, data) {
    return api.put(`/v1/admin/brands/${id}`, data)
  },

  deleteBrand(id) {
    return api.delete(`/v1/admin/brands/${id}`)
  },

  // Orders
  getOrders(params = {}) {
    return api.get('/v1/admin/orders', { params })
  },

  getOrder(id) {
    return api.get(`/v1/admin/orders/${id}`)
  },

  updateOrderStatus(id, status) {
    return api.put(`/v1/admin/orders/${id}/status`, { status })
  },

  // Users
  getUsers(params = {}) {
    return api.get('/v1/admin/users', { params })
  },

  getUser(id) {
    return api.get(`/v1/admin/users/${id}`)
  },

  updateUser(id, data) {
    return api.put(`/v1/admin/users/${id}`, data)
  },

  toggleUserStatus(id) {
    return api.put(`/v1/admin/users/${id}/toggle-status`)
  },

  // Promotions
  getPromotions(params = {}) {
    return api.get('/v1/admin/promotions', { params })
  },

  createPromotion(data) {
    return api.post('/v1/admin/promotions', data)
  },

  updatePromotion(id, data) {
    return api.put(`/v1/admin/promotions/${id}`, data)
  },

  deletePromotion(id) {
    return api.delete(`/v1/admin/promotions/${id}`)
  },

  // Reports
  getSalesReport(params = {}) {
    return api.get('/v1/admin/reports/sales', { params })
  },

  getProductsReport(params = {}) {
    return api.get('/v1/admin/reports/products', { params })
  },

  getUsersReport(params = {}) {
    return api.get('/v1/admin/reports/users', { params })
  },

  // Settings
  getShippingMethods() {
    return api.get('/v1/admin/settings/shipping-methods')
  },

  createShippingMethod(data) {
    return api.post('/v1/admin/settings/shipping-methods', data)
  },

  updateShippingMethod(id, data) {
    return api.put(`/v1/admin/settings/shipping-methods/${id}`, data)
  },

  deleteShippingMethod(id) {
    return api.delete(`/v1/admin/settings/shipping-methods/${id}`)
  },

  // Content
  getBanners() {
    return api.get('/v1/admin/content/banners')
  },

  createBanner(data) {
    return api.post('/v1/admin/content/banners', data)
  },

  updateBanner(id, data) {
    return api.put(`/v1/admin/content/banners/${id}`, data)
  },

  deleteBanner(id) {
    return api.delete(`/v1/admin/content/banners/${id}`)
  },

  getAnnouncements() {
    return api.get('/v1/admin/content/announcements')
  },

  createAnnouncement(data) {
    return api.post('/v1/admin/content/announcements', data)
  },

  updateAnnouncement(id, data) {
    return api.put(`/v1/admin/content/announcements/${id}`, data)
  },

  deleteAnnouncement(id) {
    return api.delete(`/v1/admin/content/announcements/${id}`)
  },

  getFeaturedSections() {
    return api.get('/v1/admin/content/featured-sections')
  },

  createFeaturedSection(data) {
    return api.post('/v1/admin/content/featured-sections', data)
  },

  updateFeaturedSection(id, data) {
    return api.put(`/v1/admin/content/featured-sections/${id}`, data)
  },

  deleteFeaturedSection(id) {
    return api.delete(`/v1/admin/content/featured-sections/${id}`)
  },
}
