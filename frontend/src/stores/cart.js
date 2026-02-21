import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref(JSON.parse(localStorage.getItem('cart') || '[]'))
  const couponCode = ref('')
  const couponDiscount = ref(0)
  const loading = ref(false)

  // Persist cart to localStorage
  watch(items, (val) => {
    localStorage.setItem('cart', JSON.stringify(val))
  }, { deep: true })

  // Getters
  const itemCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const subtotal = computed(() =>
    items.value.reduce((sum, item) => {
      const price = item.salePrice || item.price
      return sum + price * item.quantity
    }, 0)
  )

  const discount = computed(() => couponDiscount.value)

  const shippingFee = computed(() => {
    if (subtotal.value >= 1500) return 0
    return 120
  })

  const total = computed(() =>
    Math.max(0, subtotal.value - discount.value + shippingFee.value)
  )

  const freeShippingProgress = computed(() => {
    if (subtotal.value >= 1500) return 100
    return Math.round((subtotal.value / 1500) * 100)
  })

  const freeShippingRemaining = computed(() =>
    Math.max(0, 1500 - subtotal.value)
  )

  // Actions
  function addItem(product, quantity = 1, variant = null) {
    const existingIndex = items.value.findIndex(
      (item) =>
        item.productId === product.id &&
        item.variantId === (variant?.id || null)
    )

    if (existingIndex > -1) {
      const existing = items.value[existingIndex]
      const newQty = existing.quantity + quantity
      if (newQty > (product.stock || 99)) {
        return false
      }
      items.value[existingIndex] = { ...existing, quantity: newQty }
    } else {
      items.value.push({
        productId: product.id,
        variantId: variant?.id || null,
        name: product.name,
        slug: product.slug,
        image: product.image || product.images?.[0],
        price: product.price,
        salePrice: product.salePrice,
        variant: variant
          ? { id: variant.id, name: variant.name, value: variant.value }
          : null,
        quantity,
        stock: product.stock || 99,
      })
    }
    return true
  }

  function updateQuantity(productId, variantId, quantity) {
    const index = items.value.findIndex(
      (item) => item.productId === productId && item.variantId === (variantId || null)
    )
    if (index > -1) {
      if (quantity <= 0) {
        items.value.splice(index, 1)
      } else {
        items.value[index] = {
          ...items.value[index],
          quantity: Math.min(quantity, items.value[index].stock),
        }
      }
    }
  }

  function removeItem(productId, variantId = null) {
    items.value = items.value.filter(
      (item) =>
        !(item.productId === productId && item.variantId === (variantId || null))
    )
  }

  function clearCart() {
    items.value = []
    couponCode.value = ''
    couponDiscount.value = 0
  }

  async function applyCoupon(code) {
    loading.value = true
    try {
      // Mock coupon validation
      const upperCode = code.toUpperCase().trim()
      const coupons = {
        NEWYEAR2025: { type: 'percent', value: 15, label: '新年85折' },
        WELCOME100: { type: 'fixed', value: 100, label: '新會員折扣 NT$100' },
        SAVE200: { type: 'fixed', value: 200, label: '滿額折扣 NT$200' },
        VIP20: { type: 'percent', value: 20, label: 'VIP 8折優惠' },
        FREESHIP: { type: 'fixed', value: 120, label: '免運費' },
      }

      const matched = coupons[upperCode]
      if (!matched) {
        couponCode.value = ''
        couponDiscount.value = 0
        throw new Error('無效的優惠券')
      }

      couponCode.value = upperCode
      if (matched.type === 'percent') {
        couponDiscount.value = Math.round(subtotal.value * (matched.value / 100))
      } else {
        couponDiscount.value = matched.value
      }
      return { valid: true, discount: couponDiscount.value, label: matched.label }
    } catch (err) {
      couponCode.value = ''
      couponDiscount.value = 0
      throw err
    } finally {
      loading.value = false
    }
  }

  function removeCoupon() {
    couponCode.value = ''
    couponDiscount.value = 0
  }

  return {
    items,
    couponCode,
    couponDiscount,
    loading,
    itemCount,
    subtotal,
    discount,
    shippingFee,
    total,
    freeShippingProgress,
    freeShippingRemaining,
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
    applyCoupon,
    removeCoupon,
  }
})
