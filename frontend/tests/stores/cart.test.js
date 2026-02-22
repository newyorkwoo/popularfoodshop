/**
 * Tests for the Cart Pinia store
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCartStore } from '@/stores/cart'

describe('Cart Store', () => {
  let cart

  beforeEach(() => {
    setActivePinia(createPinia())
    cart = useCartStore()
  })

  // ── Initial State ──────────────────────────────────────────
  describe('initial state', () => {
    it('starts with empty items', () => {
      expect(cart.items).toEqual([])
    })

    it('itemCount is 0', () => {
      expect(cart.itemCount).toBe(0)
    })

    it('subtotal is 0', () => {
      expect(cart.subtotal).toBe(0)
    })

    it('shipping fee is 120 for empty cart', () => {
      expect(cart.shippingFee).toBe(120)
    })

    it('total is 120 (just shipping) for empty cart', () => {
      expect(cart.total).toBe(120)
    })
  })

  // ── addItem ────────────────────────────────────────────────
  describe('addItem', () => {
    const product = {
      id: 1,
      name: 'Test Snack',
      slug: 'test-snack',
      price: 200,
      salePrice: null,
      stock: 10,
      image: '/img/test.jpg',
    }

    it('adds a new item to the cart', () => {
      cart.addItem(product, 1)
      expect(cart.items).toHaveLength(1)
      expect(cart.items[0].productId).toBe(1)
      expect(cart.items[0].quantity).toBe(1)
    })

    it('increases quantity for same product', () => {
      cart.addItem(product, 1)
      cart.addItem(product, 2)
      expect(cart.items).toHaveLength(1)
      expect(cart.items[0].quantity).toBe(3)
    })

    it('uses salePrice for subtotal when available', () => {
      const saleProduct = { ...product, salePrice: 150 }
      cart.addItem(saleProduct, 2)
      expect(cart.subtotal).toBe(300)
    })

    it('returns false when exceeding stock', () => {
      cart.addItem(product, 10) // add all 10
      const result = cart.addItem(product, 1) // exceed stock
      expect(result).toBe(false)
    })

    it('treats different variants as separate items', () => {
      const variantA = { id: 10, name: 'Small' }
      const variantB = { id: 11, name: 'Large' }
      cart.addItem(product, 1, variantA)
      cart.addItem(product, 1, variantB)
      expect(cart.items).toHaveLength(2)
    })
  })

  // ── updateQuantity ─────────────────────────────────────────
  describe('updateQuantity', () => {
    const product = { id: 1, name: 'P1', price: 100, stock: 10 }

    beforeEach(() => {
      cart.addItem(product, 2)
    })

    it('updates quantity', () => {
      cart.updateQuantity(1, null, 5)
      expect(cart.items[0].quantity).toBe(5)
    })

    it('removes item when quantity is 0', () => {
      cart.updateQuantity(1, null, 0)
      expect(cart.items).toHaveLength(0)
    })

    it('caps at stock limit', () => {
      cart.updateQuantity(1, null, 999)
      expect(cart.items[0].quantity).toBe(10)
    })
  })

  // ── removeItem ─────────────────────────────────────────────
  describe('removeItem', () => {
    it('removes item by productId', () => {
      cart.addItem({ id: 1, name: 'P1', price: 100, stock: 5 })
      cart.addItem({ id: 2, name: 'P2', price: 200, stock: 5 })
      cart.removeItem(1)
      expect(cart.items).toHaveLength(1)
      expect(cart.items[0].productId).toBe(2)
    })

    it('does nothing for non-existent product', () => {
      cart.addItem({ id: 1, name: 'P1', price: 100, stock: 5 })
      cart.removeItem(999)
      expect(cart.items).toHaveLength(1)
    })
  })

  // ── clearCart ──────────────────────────────────────────────
  describe('clearCart', () => {
    it('removes all items and resets coupon', () => {
      cart.addItem({ id: 1, name: 'P1', price: 100, stock: 5 }, 2)
      cart.clearCart()
      expect(cart.items).toHaveLength(0)
      expect(cart.couponCode).toBe('')
      expect(cart.couponDiscount).toBe(0)
    })
  })

  // ── Computed ───────────────────────────────────────────────
  describe('computed values', () => {
    it('calculates subtotal correctly', () => {
      cart.addItem({ id: 1, name: 'P1', price: 500, stock: 10 }, 3)
      expect(cart.subtotal).toBe(1500)
    })

    it('free shipping at 1500', () => {
      cart.addItem({ id: 1, name: 'P1', price: 1500, stock: 10 }, 1)
      expect(cart.shippingFee).toBe(0)
      expect(cart.freeShippingProgress).toBe(100)
      expect(cart.freeShippingRemaining).toBe(0)
    })

    it('shipping fee 120 under 1500', () => {
      cart.addItem({ id: 1, name: 'P1', price: 1000, stock: 10 }, 1)
      expect(cart.shippingFee).toBe(120)
      expect(cart.freeShippingProgress).toBe(67) // Math.round(1000/1500*100)
      expect(cart.freeShippingRemaining).toBe(500)
    })

    it('total = subtotal - discount + shipping', () => {
      cart.addItem({ id: 1, name: 'P1', price: 500, stock: 10 }, 2)
      // subtotal = 1000, shipping = 120, no discount
      expect(cart.total).toBe(1120)
    })

    it('itemCount sums quantities', () => {
      cart.addItem({ id: 1, name: 'P1', price: 100, stock: 10 }, 3)
      cart.addItem({ id: 2, name: 'P2', price: 200, stock: 10 }, 2)
      expect(cart.itemCount).toBe(5)
    })
  })

  // ── Coupon ─────────────────────────────────────────────────
  describe('applyCoupon', () => {
    beforeEach(() => {
      cart.addItem({ id: 1, name: 'P1', price: 1000, stock: 10 }, 1)
    })

    it('applies percentage coupon', async () => {
      const result = await cart.applyCoupon('NEWYEAR2025')
      expect(result.valid).toBe(true)
      expect(cart.couponCode).toBe('NEWYEAR2025')
      expect(cart.couponDiscount).toBe(150) // 15% of 1000
    })

    it('applies fixed coupon', async () => {
      const result = await cart.applyCoupon('WELCOME100')
      expect(result.valid).toBe(true)
      expect(cart.couponDiscount).toBe(100)
    })

    it('rejects invalid coupon', async () => {
      await expect(cart.applyCoupon('FAKECODE')).rejects.toThrow('無效的優惠券')
      expect(cart.couponCode).toBe('')
      expect(cart.couponDiscount).toBe(0)
    })

    it('is case-insensitive', async () => {
      await cart.applyCoupon('newyear2025')
      expect(cart.couponCode).toBe('NEWYEAR2025')
    })
  })

  // ── removeCoupon ───────────────────────────────────────────
  describe('removeCoupon', () => {
    it('clears coupon', async () => {
      cart.addItem({ id: 1, name: 'P1', price: 1000, stock: 10 })
      await cart.applyCoupon('WELCOME100')
      cart.removeCoupon()
      expect(cart.couponCode).toBe('')
      expect(cart.couponDiscount).toBe(0)
    })
  })
})
