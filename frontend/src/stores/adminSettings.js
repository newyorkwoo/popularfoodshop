import { defineStore } from 'pinia'
import { reactive } from 'vue'

const SEED_SETTINGS = {
  storeName: '人氣美食商店', email: 'support@popularfoodshop.com',
  phone: '(02) 2345-6789', address: '台北市大安區美食路 123 號',
  freeShippingThreshold: 1500, normalShipping: 120, coldShipping: 200, convenienceShipping: 60,
  creditCard: true, linePay: true, cod: true, bankTransfer: false,
  pointRate: 1, pointValue: 0.1, pointExpiry: 365,
  orderNotify: true, lowStockNotify: true, lowStockThreshold: 10,
}

export const useAdminSettingsStore = defineStore('adminSettings', () => {
  const stored = localStorage.getItem('adminSettings')
  const settings = reactive(stored ? JSON.parse(stored) : { ...SEED_SETTINGS })

  function save() {
    localStorage.setItem('adminSettings', JSON.stringify(settings))
  }

  return { settings, save }
})
