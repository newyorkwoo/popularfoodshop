<template>
  <div>
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/products" class="text-gray-400 hover:text-gray-600"><ArrowLeftIcon class="w-5 h-5" /></router-link>
      <h2 class="text-2xl font-bold text-gray-900">新增商品</h2>
    </div>

    <form @submit.prevent="handleSave" class="space-y-8">
      <div class="grid lg:grid-cols-3 gap-6">
        <!-- Main Info -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">基本資訊</h3>
            <BaseInput v-model="form.name" label="商品名稱" required />
            <BaseInput v-model="form.slug" label="網址代稱 (slug)" />
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">商品描述</label>
              <textarea v-model="form.description" rows="5" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">營養標示</label>
              <textarea v-model="form.nutrition" rows="3" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"></textarea>
            </div>
          </div>

          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">商品圖片</h3>
            <div class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-primary-400 transition cursor-pointer">
              <PhotoIcon class="w-12 h-12 text-gray-300 mx-auto mb-2" />
              <p class="text-sm text-gray-500">拖放圖片或<span class="text-primary-600 font-medium">點擊上傳</span></p>
              <p class="text-xs text-gray-400 mt-1">支援 JPG、PNG、WebP，最大 5MB</p>
            </div>
          </div>

          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">價格與庫存</h3>
            <div class="grid grid-cols-2 gap-4">
              <BaseInput v-model.number="form.price" label="售價 (NT$)" type="number" required />
              <BaseInput v-model.number="form.originalPrice" label="原價 (NT$)" type="number" />
              <BaseInput v-model.number="form.cost" label="成本 (NT$)" type="number" />
              <BaseInput v-model.number="form.stock" label="庫存數量" type="number" required />
            </div>
            <BaseInput v-model="form.sku" label="SKU" />
            <BaseInput v-model="form.barcode" label="條碼" />
          </div>

          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">產品規格</h3>
            <div class="grid grid-cols-2 gap-4">
              <BaseInput v-model="form.weight" label="重量" />
              <BaseInput v-model="form.unit" label="單位" placeholder="例如：500g、1kg" />
              <BaseInput v-model="form.origin" label="產地" />
              <BaseInput v-model="form.shelfLife" label="保存期限" />
              <BaseInput v-model="form.storage" label="保存方式" placeholder="常溫/冷藏/冷凍" />
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">發布狀態</h3>
            <select v-model="form.status" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option value="draft">草稿</option>
              <option value="active">上架</option>
              <option value="archived">已下架</option>
            </select>
            <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" v-model="form.isNew" class="accent-primary-600" /> 標記為新品
            </label>
            <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" v-model="form.isFeatured" class="accent-primary-600" /> 精選商品
            </label>
          </div>

          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">分類</h3>
            <select v-model="form.category" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option value="">選擇分類</option>
              <option v-for="c in categories" :key="c">{{ c }}</option>
            </select>
          </div>

          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">品牌</h3>
            <select v-model="form.brand" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option value="">選擇品牌</option>
              <option v-for="b in brands" :key="b">{{ b }}</option>
            </select>
          </div>

          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">標籤</h3>
            <BaseInput v-model="form.tags" label="" placeholder="以逗號分隔" />
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-3">
        <router-link to="/products" class="px-6 py-2.5 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50">取消</router-link>
        <BaseButton type="submit" :loading="saving">儲存商品</BaseButton>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon, PhotoIcon } from '@heroicons/vue/24/outline'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAdminProductStore } from '@/stores/adminProduct'

const router = useRouter()
const saving = ref(false)
const adminProductStore = useAdminProductStore()
const categories = ['肉品海鮮', '調味醬料', '茶葉飲品', '乳製品', '零食點心', '有機食品', '日本食品', '歐洲食品']
const brands = ['和牛專門店', '地中海莊園', '台灣茶莊', '法國甜品屋', '北海道牧場', '義式美食']

const form = reactive({
  name: '', slug: '', description: '', nutrition: '',
  price: null, originalPrice: null, cost: null, stock: null,
  sku: '', barcode: '', weight: '', unit: '', origin: '', shelfLife: '', storage: '',
  status: 'draft', isNew: false, isFeatured: false, category: '', brand: '', tags: '',
})

async function handleSave() {
  saving.value = true
  await new Promise(r => setTimeout(r, 500))
  adminProductStore.createProduct({ ...form })
  saving.value = false
  router.push('/products')
}
</script>
