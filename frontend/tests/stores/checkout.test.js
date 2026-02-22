/**
 * Tests for the Checkout Pinia store
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCheckoutStore } from '@/stores/checkout'
import { useCartStore } from '@/stores/cart'

describe('Checkout Store', () => {
  let checkout
  let cart

  beforeEach(() => {
    setActivePinia(createPinia())
    checkout = useCheckoutStore()
    cart = useCartStore()
  })

  // ── Initial State ──────────────────────────────────────────
  describe('initial state', () => {
    it('starts at step 1', () => {
      expect(checkout.step).toBe(1)
    })

    it('starts with empty shipping info', () => {
      expect(checkout.shippingInfo.firstName).toBe('')
      expect(checkout.shippingInfo.email).toBe('')
    })

    it('default delivery method is home', () => {
      expect(checkout.deliveryMethod).toBe('home')
    })

    it('default payment method is credit_card', () => {
      expect(checkout.paymentMethod).toBe('credit_card')
    })

    it('is not loading', () => {
      expect(checkout.loading).toBe(false)
    })

    it('has no order id', () => {
      expect(checkout.orderId).toBeNull()
    })
  })

  // ── Step Navigation ────────────────────────────────────────
  describe('step navigation', () => {
    it('nextStep goes from 1 to 2', () => {
      checkout.nextStep()
      expect(checkout.step).toBe(2)
    })

    it('nextStep goes from 2 to 3', () => {
      checkout.setStep(2)
      checkout.nextStep()
      expect(checkout.step).toBe(3)
    })

    it('nextStep does not go beyond 3', () => {
      checkout.setStep(3)
      checkout.nextStep()
      expect(checkout.step).toBe(3)
    })

    it('prevStep goes from 2 to 1', () => {
      checkout.setStep(2)
      checkout.prevStep()
      expect(checkout.step).toBe(1)
    })

    it('prevStep does not go below 1', () => {
      checkout.prevStep()
      expect(checkout.step).toBe(1)
    })

    it('setStep goes to arbitrary step', () => {
      checkout.setStep(3)
      expect(checkout.step).toBe(3)
    })
  })

  // ── Shipping Info ──────────────────────────────────────────
  describe('setShippingInfo', () => {
    it('merges partial shipping info', () => {
      checkout.setShippingInfo({ firstName: 'John', lastName: 'Doe' })
      expect(checkout.shippingInfo.firstName).toBe('John')
      expect(checkout.shippingInfo.lastName).toBe('Doe')
      expect(checkout.shippingInfo.email).toBe('')
    })

    it('validates home delivery requires all fields', () => {
      expect(checkout.isShippingValid).toBe(false)
      checkout.setShippingInfo({
        firstName: 'Test',
        lastName: 'User',
        email: 'test@test.com',
        phone: '0912345678',
        address: '信義路1號',
        city: '台北市',
        district: '信義區',
        postalCode: '110',
      })
      expect(checkout.isShippingValid).toBe(true)
    })
  })

  // ── Delivery Method ────────────────────────────────────────
  describe('setDeliveryMethod', () => {
    it('sets delivery method', () => {
      checkout.setDeliveryMethod('convenience')
      expect(checkout.deliveryMethod).toBe('convenience')
    })

    it('clears convenience store when switching to home', () => {
      checkout.setDeliveryMethod('convenience')
      checkout.convenienceStore = { id: 1, name: '7-11 信義店' }
      checkout.setDeliveryMethod('home')
      expect(checkout.convenienceStore).toBeNull()
    })
  })

  // ── Payment Method ─────────────────────────────────────────
  describe('setPaymentMethod', () => {
    it('sets payment method', () => {
      checkout.setPaymentMethod('line_pay')
      expect(checkout.paymentMethod).toBe('line_pay')
    })
  })

  // ── Order Summary ──────────────────────────────────────────
  describe('orderSummary', () => {
    it('reflects cart data', () => {
      cart.addItem({ id: 1, name: 'P1', price: 500, stock: 10 }, 2)
      const summary = checkout.orderSummary
      expect(summary.items).toHaveLength(1)
      expect(summary.subtotal).toBe(1000)
    })
  })

  // ── Place Order ────────────────────────────────────────────
  describe('placeOrder', () => {
    beforeEach(() => {
      cart.addItem({ id: 1, name: 'P1', price: 500, stock: 10 }, 2)
      checkout.setShippingInfo({
        firstName: 'Test',
        lastName: 'User',
        email: 'test@test.com',
        phone: '0912345678',
        address: '信義路1號',
        city: '台北市',
        district: '信義區',
        postalCode: '110',
      })
    })

    it('returns an order id', async () => {
      const id = await checkout.placeOrder()
      expect(id).toContain('MOCK-')
    })

    it('clears cart after placing order', async () => {
      await checkout.placeOrder()
      expect(cart.items).toHaveLength(0)
    })

    it('stores orderId', async () => {
      await checkout.placeOrder()
      expect(checkout.orderId).not.toBeNull()
    })
  })

  // ── Reset ──────────────────────────────────────────────────
  describe('reset', () => {
    it('resets all state', async () => {
      checkout.setStep(3)
      checkout.setShippingInfo({ firstName: 'John' })
      checkout.setPaymentMethod('line_pay')
      checkout.reset()

      expect(checkout.step).toBe(1)
      expect(checkout.shippingInfo.firstName).toBe('')
      expect(checkout.paymentMethod).toBe('credit_card')
      expect(checkout.orderId).toBeNull()
    })
  })
})
