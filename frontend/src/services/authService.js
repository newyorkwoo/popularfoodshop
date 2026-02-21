import api from './api'

export default {
  login(credentials) {
    return api.post('/auth/login', credentials)
  },

  register(data) {
    return api.post('/auth/register', data)
  },

  logout() {
    return api.post('/auth/logout')
  },

  refreshToken(refreshToken) {
    return api.post('/auth/refresh', { refreshToken })
  },

  getProfile() {
    return api.get('/auth/me')
  },

  updateProfile(data) {
    return api.put('/auth/me', data)
  },

  changePassword(data) {
    return api.post('/auth/change-password', data)
  },

  forgotPassword(email) {
    return api.post('/auth/forgot-password', { email })
  },

  resetPassword(data) {
    return api.post('/auth/reset-password', data)
  },

  // Addresses
  getAddresses() {
    return api.get('/auth/addresses')
  },

  addAddress(data) {
    return api.post('/auth/addresses', data)
  },

  updateAddress(id, data) {
    return api.put(`/auth/addresses/${id}`, data)
  },

  deleteAddress(id) {
    return api.delete(`/auth/addresses/${id}`)
  },

  setDefaultAddress(id) {
    return api.put(`/auth/addresses/${id}/default`)
  },
}
