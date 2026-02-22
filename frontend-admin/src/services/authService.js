import api from './api'

export default {
  login(credentials) {
    return api.post('/v1/admin/auth/login', credentials)
  },

  refreshToken(refreshToken) {
    return api.post('/v1/admin/auth/refresh', { refresh_token: refreshToken })
  },

  logout() {
    return api.post('/v1/admin/auth/logout')
  },

  getProfile() {
    return api.get('/v1/admin/auth/me')
  },
}
