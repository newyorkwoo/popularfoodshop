import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

const SEED = {
  banners: [
    { id: 1, title: '新年特惠全場 85 折', image: 'https://placehold.co/800x300/FFF3E0/EA580C?text=新年特惠', link: '/products?promo=newyear' },
    { id: 2, title: '日本直送 A5 和牛', image: 'https://placehold.co/800x300/FEF2F2/DC2626?text=A5和牛', link: '/products/a5-wagyu' },
  ],
  announcement: { text: '🎉 新年快樂！全場消費滿 NT$2,000 享 85 折優惠', enabled: true },
  seo: { title: '人氣美食商店 - 全球精選頂級食材', description: '嚴選世界各地頂級食材，日本和牛、法國松露、台灣有機農產，品質保證快速到貨。', keywords: '美食,食材,和牛,有機,電商' },
}

export const useAdminContentStore = defineStore('adminContent', () => {
  const stored = localStorage.getItem('adminContent')
  const data = stored ? JSON.parse(stored) : JSON.parse(JSON.stringify(SEED))

  const banners = ref(data.banners)
  const announcement = reactive(data.announcement)
  const seo = reactive(data.seo)

  function persist() {
    localStorage.setItem('adminContent', JSON.stringify({
      banners: banners.value,
      announcement: { text: announcement.text, enabled: announcement.enabled },
      seo: { title: seo.title, description: seo.description, keywords: seo.keywords },
    }))
  }

  function addBanner() {
    banners.value.push({ id: Date.now(), title: '新輪播', image: 'https://placehold.co/800x300/E2E8F0/64748B?text=新輪播', link: '/' })
    persist()
  }

  function updateBanner(id, data) {
    const idx = banners.value.findIndex(b => b.id === id)
    if (idx >= 0) {
      Object.assign(banners.value[idx], data)
      persist()
    }
  }

  function deleteBanner(id) {
    banners.value = banners.value.filter(b => b.id !== id)
    persist()
  }

  function saveAnnouncement() { persist() }
  function saveSeo() { persist() }

  return { banners, announcement, seo, addBanner, updateBanner, deleteBanner, saveAnnouncement, saveSeo }
})
