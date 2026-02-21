import api from './api'

export default {
  createOrder(data) {
    return api.post('/orders', data)
  },

  getOrders(params = {}) {
    return api.get('/orders', { params })
  },

  getOrder(id) {
    return api.get(`/orders/${id}`)
  },

  cancelOrder(id) {
    return api.put(`/orders/${id}/cancel`)
  },

  // Returns
  createReturn(orderId, data) {
    return api.post(`/orders/${orderId}/returns`, data)
  },

  getReturns(params = {}) {
    return api.get('/returns', { params })
  },

  getReturn(id) {
    return api.get(`/returns/${id}`)
  },

  // Payment
  getPaymentMethods() {
    return api.get('/payment/methods')
  },

  processPayment(orderId, data) {
    return api.post(`/orders/${orderId}/pay`, data)
  },

  // Points
  getPoints() {
    return api.get('/points')
  },

  getPointsHistory(params = {}) {
    return api.get('/points/history', { params })
  },

  // Credits
  getCredits() {
    return api.get('/credits')
  },

  getCreditsHistory(params = {}) {
    return api.get('/credits/history', { params })
  },
}
