<template>
    <div class="max-w-3xl mx-auto px-4 py-12">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">常見問題</h1>

      <div class="space-y-4">
        <div v-for="(item, i) in faqItems" :key="i" class="border border-gray-200 rounded-xl overflow-hidden">
          <button
            @click="toggle(i)"
            class="w-full flex items-center justify-between px-6 py-4 text-left hover:bg-gray-50 transition"
          >
            <span class="font-medium text-gray-900">{{ item.q }}</span>
            <ChevronDownIcon class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openIndex === i }" />
          </button>
          <div v-show="openIndex === i" class="px-6 pb-4 text-gray-600 text-sm leading-relaxed">
            {{ item.a }}
          </div>
        </div>
      </div>

      <div class="mt-12 bg-primary-50 rounded-xl p-8 text-center">
        <h3 class="text-lg font-bold text-gray-900 mb-2">找不到答案？</h3>
        <p class="text-gray-600 mb-4">歡迎聯繫我們的客服團隊</p>
        <router-link to="/contact" class="inline-block bg-primary-600 text-white px-6 py-2.5 rounded-lg hover:bg-primary-700 transition font-medium">聯絡客服</router-link>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

const openIndex = ref(0)
const toggle = (i) => { openIndex.value = openIndex.value === i ? -1 : i }

const faqItems = [
  { q: '如何下單購買？', a: '您可以在網站上瀏覽商品，加入購物車後前往結帳頁面完成付款即可。我們接受信用卡、LINE Pay 及貨到付款等多種付款方式。' },
  { q: '運費如何計算？', a: '台灣本島消費滿 NT$1,500 免運費。未滿免運門檻，一般宅配運費為 NT$120，冷凍/冷藏商品運費為 NT$200。離島地區另計。' },
  { q: '多久可以收到商品？', a: '一般商品於訂單成立後 1-3 個工作天內出貨，台灣本島約 1-2 天送達。預購商品及特殊商品出貨時間請參考商品頁面說明。' },
  { q: '可以退換貨嗎？', a: '依照消費者保護法，您享有 7 天猶豫期。食品類商品基於衛生安全考量，拆封後恕不接受退換貨。詳情請參考退換貨政策。' },
  { q: '商品保存方式為何？', a: '每項商品頁面都有標示建議保存方式及有效期限。冷凍商品請保存在 -18°C 以下，冷藏商品請保存在 0-7°C。' },
  { q: '有提供發票嗎？', a: '是的，所有訂單均提供電子發票。發票會於出貨後以 Email 寄送，您也可以在會員中心查詢。如需統一編號，請於結帳時填寫。' },
  { q: '如何使用優惠碼？', a: '在購物車頁面或結帳頁面輸入優惠碼即可享受折扣。每筆訂單限使用一組優惠碼，且不可與其他優惠併用（除非特別說明）。' },
  { q: '可以指定配送時間嗎？', a: '目前暫不提供指定配送時間服務，但您可以在訂單備註中填寫希望配送的時段，我們會盡量配合。' },
]
</script>
