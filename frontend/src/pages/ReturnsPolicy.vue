<template>
    <div class="max-w-3xl mx-auto px-4 py-12">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">退換貨政策</h1>
      <div class="space-y-8">
        <div class="bg-yellow-50 rounded-xl p-6 border border-yellow-200">
          <p class="text-yellow-800 font-medium">⚠️ 食品類商品基於食品安全衛生考量，拆封後恕不接受退換貨。</p>
        </div>

        <div>
          <h2 class="text-lg font-bold text-gray-900 mb-3">退換貨條件</h2>
          <ul class="text-sm text-gray-600 space-y-2 list-disc pl-5">
            <li>收到商品後 7 天內（含例假日）可申請退換貨。</li>
            <li>商品須為全新未拆封狀態，且包裝完整。</li>
            <li>商品有瑕疵、損壞或與訂單不符，可免費換貨或全額退款。</li>
            <li>非商品瑕疵之退貨，退貨運費由消費者自行負擔。</li>
          </ul>
        </div>

        <div>
          <h2 class="text-lg font-bold text-gray-900 mb-3">退換貨流程</h2>
          <div class="flex flex-col md:flex-row gap-4">
            <div v-for="(step, i) in steps" :key="i" class="flex-1 bg-gray-50 rounded-xl p-4 text-center">
              <div class="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-2 text-sm font-bold">{{ i + 1 }}</div>
              <h3 class="font-medium text-gray-900 text-sm mb-1">{{ step.title }}</h3>
              <p class="text-xs text-gray-500">{{ step.desc }}</p>
            </div>
          </div>
        </div>

        <div>
          <h2 class="text-lg font-bold text-gray-900 mb-3">退款方式</h2>
          <p class="text-sm text-gray-600 leading-relaxed">退款將於收到退回商品並確認後 5-7 個工作天內退回原付款方式。信用卡退款時間依各發卡銀行規定而有所不同。</p>
        </div>

        <div class="bg-gray-50 rounded-xl p-6">
          <p class="text-sm text-gray-600">如有退換貨需求，請聯繫客服：<a href="mailto:support@popularfoodshop.com" class="text-primary-600 hover:underline">support@popularfoodshop.com</a> 或撥打 (02) 2345-6789。</p>
        </div>
      </div>
    </div>
</template>

<script setup>
const steps = [
  { title: '申請退換貨', desc: '登入會員中心提交退換貨申請' },
  { title: '等待審核', desc: '客服將於 1-2 天內審核' },
  { title: '寄回商品', desc: '依指示將商品寄回指定地址' },
  { title: '完成退款', desc: '確認商品後 5-7 天退款' },
]
</script>
