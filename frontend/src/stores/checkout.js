import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useCartStore } from './cart'

export const useCheckoutStore = defineStore('checkout', () => {
  const cartStore = useCartStore()

  // State
  const step = ref(1) // 1: shipping, 2: payment, 3: review
  const shippingInfo = ref({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    district: '',
    postalCode: '',
    notes: '',
  })
  const deliveryMethod = ref('home') // home, convenience
  const convenienceStore = ref(null)
  const paymentMethod = ref('credit_card') // credit_card, line_pay, cod
  const loading = ref(false)
  const error = ref(null)
  const orderId = ref(null)

  // Getters
  const isShippingValid = computed(() => {
    const s = shippingInfo.value
    if (deliveryMethod.value === 'home') {
      return !!(s.firstName && s.lastName && s.email && s.phone && s.address && s.city && s.district && s.postalCode)
    }
    return !!(s.firstName && s.lastName && s.email && s.phone && convenienceStore.value)
  })

  const orderSummary = computed(() => ({
    items: cartStore.items,
    subtotal: cartStore.subtotal,
    shipping: cartStore.shippingFee,
    discount: cartStore.discount,
    total: cartStore.total,
    couponCode: cartStore.couponCode,
  }))

  // Actions
  function setStep(s) {
    step.value = s
  }

  function nextStep() {
    if (step.value < 3) step.value++
  }

  function prevStep() {
    if (step.value > 1) step.value--
  }

  function setShippingInfo(info) {
    shippingInfo.value = { ...shippingInfo.value, ...info }
  }

  function setDeliveryMethod(method) {
    deliveryMethod.value = method
    if (method !== 'convenience') {
      convenienceStore.value = null
    }
  }

  function setPaymentMethod(method) {
    paymentMethod.value = method
  }

  async function placeOrder() {
    loading.value = true
    error.value = null
    try {
      // TODO: Call order API
      const orderData = {
        items: cartStore.items.map((item) => ({
          productId: item.productId,
          variantId: item.variantId,
          quantity: item.quantity,
        })),
        shipping: shippingInfo.value,
        deliveryMethod: deliveryMethod.value,
        convenienceStore: convenienceStore.value,
        paymentMethod: paymentMethod.value,
        couponCode: cartStore.couponCode,
      }
      console.log('Place order:', orderData)
      // const response = await orderService.createOrder(orderData)
      // orderId.value = response.data.id
      orderId.value = 'MOCK-' + Date.now()
      cartStore.clearCart()
      return orderId.value
    } catch (err) {
      error.value = err.response?.data?.message || '下單失敗，請稍後再試'
      throw err
    } finally {
      loading.value = false
    }
  }

  function reset() {
    step.value = 1
    shippingInfo.value = {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      address: '',
      city: '',
      district: '',
      postalCode: '',
      notes: '',
    }
    deliveryMethod.value = 'home'
    convenienceStore.value = null
    paymentMethod.value = 'credit_card'
    loading.value = false
    error.value = null
    orderId.value = null
  }

  return {
    step,
    shippingInfo,
    deliveryMethod,
    convenienceStore,
    paymentMethod,
    loading,
    error,
    orderId,
    isShippingValid,
    orderSummary,
    setStep,
    nextStep,
    prevStep,
    setShippingInfo,
    setDeliveryMethod,
    setPaymentMethod,
    placeOrder,
    reset,
  }
})
