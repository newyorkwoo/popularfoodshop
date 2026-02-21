import { defineStore } from 'pinia'
import { ref } from 'vue'

const SEED_PROMOTIONS = [
  { id: 1, name: '新年特惠', type: '百分比折扣', code: 'NEWYEAR2025', discount: '85折', startDate: '2025-01-01', endDate: '2025-01-31', used: 45, limit: 100, active: true, minAmount: 0 },
  { id: 2, name: '免運活動', type: '免運費', code: 'FREESHIP', discount: '免運', startDate: '2025-01-15', endDate: '2025-02-15', used: 120, limit: 500, active: true, minAmount: 1500 },
  { id: 3, name: '新會員優惠', type: '固定金額折扣', code: 'WELCOME100', discount: '折 NT$100', startDate: '2025-01-01', endDate: '2025-12-31', used: 30, limit: 999, active: true, minAmount: 500 },
]

export const useAdminPromotionStore = defineStore('adminPromotion', () => {
  const stored = localStorage.getItem('adminPromotions')
  const promotions = ref(stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED_PROMOTIONS)))

  function persist() {
    localStorage.setItem('adminPromotions', JSON.stringify(promotions.value))
  }

  function createPromotion(data) {
    const id = promotions.value.length ? Math.max(...promotions.value.map(p => p.id)) + 1 : 1
    promotions.value.push({ ...data, id, used: 0, active: true })
    persist()
  }

  function updatePromotion(id, data) {
    const idx = promotions.value.findIndex(p => p.id === id)
    if (idx >= 0) {
      Object.assign(promotions.value[idx], data)
      persist()
    }
  }

  function deletePromotion(id) {
    promotions.value = promotions.value.filter(p => p.id !== id)
    persist()
  }

  return { promotions, createPromotion, updatePromotion, deletePromotion }
})
