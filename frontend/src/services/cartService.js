import api from './api'

export default {
  getCart() {
    return api.get('/cart')
  },

  addToCart(productId, quantity = 1, variantId = null) {
    return api.post('/cart/items', { productId, quantity, variantId })
  },

  updateCartItem(itemId, quantity) {
    return api.put(`/cart/items/${itemId}`, { quantity })
  },

  removeCartItem(itemId) {
    return api.delete(`/cart/items/${itemId}`)
  },

  clearCart() {
    return api.delete('/cart')
  },

  applyCoupon(code) {
    return api.post('/cart/coupon', { code })
  },

  removeCoupon() {
    return api.delete('/cart/coupon')
  },

  getShippingOptions() {
    return api.get('/cart/shipping-options')
  },
}
