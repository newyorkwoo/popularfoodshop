<template>
  <footer class="bg-linear-to-b from-gray-900 to-gray-950 text-gray-300 relative overflow-hidden">
    <!-- Decorative top border -->
    <div class="h-1 bg-linear-to-r from-primary-500 via-amber-400 to-primary-500"></div>

    <!-- Main footer -->
    <div class="container mx-auto px-4 py-14">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
        <!-- Brand -->
        <div>
          <div class="flex items-center gap-2.5 mb-5">
            <span class="text-3xl">🍜</span>
            <span class="text-xl font-bold text-white">人氣美食商店</span>
          </div>
          <p class="text-sm text-gray-400 leading-relaxed mb-6">
            精選全球美味零食、茶品、巧克力與健康食品，讓您在家就能品嚐世界美味。
          </p>
          <div class="flex gap-3">
            <a href="#" class="w-9 h-9 flex items-center justify-center bg-gray-800 hover:bg-primary-600 rounded-lg transition-all duration-300 text-gray-400 hover:text-white hover:scale-110" aria-label="Facebook">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
            <a href="#" class="w-9 h-9 flex items-center justify-center bg-gray-800 hover:bg-pink-600 rounded-lg transition-all duration-300 text-gray-400 hover:text-white hover:scale-110" aria-label="Instagram">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z"/></svg>
            </a>
            <a href="#" class="w-9 h-9 flex items-center justify-center bg-gray-800 hover:bg-green-600 rounded-lg transition-all duration-300 text-gray-400 hover:text-white hover:scale-110" aria-label="LINE">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/></svg>
            </a>
          </div>
        </div>

        <!-- Customer Service -->
        <div>
          <h3 class="text-white font-semibold mb-5 text-base">客戶服務</h3>
          <ul class="space-y-3 text-sm">
            <li><router-link to="/faq" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.faq') }}</router-link></li>
            <li><router-link to="/shipping" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.shipping') }}</router-link></li>
            <li><router-link to="/returns" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.returns') }}</router-link></li>
            <li><router-link to="/contact" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.contact') }}</router-link></li>
          </ul>
        </div>

        <!-- About -->
        <div>
          <h3 class="text-white font-semibold mb-5 text-base">關於我們</h3>
          <ul class="space-y-3 text-sm">
            <li><router-link to="/about" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.about') }}</router-link></li>
            <li><router-link to="/terms" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.terms') }}</router-link></li>
            <li><router-link to="/privacy" class="hover:text-white hover:pl-1 transition-all duration-200">{{ $t('footer.privacy') }}</router-link></li>
          </ul>
        </div>

        <!-- Newsletter -->
        <div>
          <h3 class="text-white font-semibold mb-5 text-base">訂閱電子報</h3>
          <p class="text-sm text-gray-400 mb-4">訂閱即可獲得最新優惠與新品資訊</p>
          <form @submit.prevent="subscribeNewsletter" class="flex gap-2">
            <input
              v-model="email"
              type="email"
              placeholder="your@email.com"
              class="flex-1 px-4 py-2.5 rounded-xl bg-gray-800/80 border border-gray-700 text-white placeholder-gray-500 text-sm focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all"
            />
            <button
              type="submit"
              class="px-5 py-2.5 bg-primary-600 text-white text-sm font-semibold rounded-xl hover:bg-primary-500 hover:shadow-lg hover:shadow-primary-600/30 transition-all duration-300"
            >
              訂閱
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-gray-800/80">
      <div class="container mx-auto px-4 py-5 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p class="text-xs text-gray-500">
          {{ $t('footer.copyright', { year: new Date().getFullYear() }) }}
        </p>
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 bg-gray-800 rounded text-[10px] font-semibold tracking-wider text-gray-400 hover:text-white transition-colors">VISA</span>
          <span class="px-3 py-1 bg-gray-800 rounded text-[10px] font-semibold tracking-wider text-gray-400 hover:text-white transition-colors">MC</span>
          <span class="px-3 py-1 bg-gray-800 rounded text-[10px] font-semibold tracking-wider text-gray-400 hover:text-white transition-colors">JCB</span>
          <span class="px-3 py-1 bg-gray-800 rounded text-[10px] font-semibold tracking-wider text-gray-400 hover:text-white transition-colors">LINE Pay</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import { useUIStore } from '@/stores/ui'

const email = ref('')
const uiStore = useUIStore()

function subscribeNewsletter() {
  if (email.value) {
    // TODO: Call newsletter API
    uiStore.showToast('感謝您的訂閱！我們將定期發送最新優惠資訊給您。', 'success')
    email.value = ''
  }
}
</script>
