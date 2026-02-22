<template>
  <div>
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/products" class="text-gray-400 hover:text-gray-600"><ArrowLeftIcon class="w-5 h-5" /></router-link>
      <h2 class="text-2xl font-bold text-gray-900">編輯商品</h2>
    </div>
    <!-- Reusing same form structure as ProductCreate -->
    <form @submit.prevent="handleSave" class="space-y-8">
      <div class="grid lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">基本資訊</h3>
            <BaseInput v-model="form.name" label="商品名稱" required />
            <BaseInput v-model="form.slug" label="網址代稱 (slug)" />
            <div><label class="block text-sm font-medium text-gray-700 mb-1">商品描述</label>
              <textarea v-model="form.description" rows="5" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"></textarea></div>
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
          </div>
        </div>
        <div class="space-y-6">
          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">發布狀態</h3>
            <select v-model="form.status" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option value="draft">草稿</option><option value="active">上架</option><option value="archived">已下架</option>
            </select>
          </div>
          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">分類</h3>
            <select v-model="form.category" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option value="">選擇分類</option>
              <option v-for="c in ['肉品海鮮','調味醬料','茶葉飲品','乳製品','零食點心']" :key="c">{{ c }}</option>
            </select>
          </div>
          <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-4">
            <h3 class="font-bold text-gray-900">品牌</h3>
            <select v-model="form.brand" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm">
              <option value="">選擇品牌</option>
              <option v-for="b in ['和牛專門店','地中海莊園','台灣茶莊','北海道牧場']" :key="b">{{ b }}</option>
            </select>
          </div>
        </div>
      </div>
      <div class="flex justify-end gap-3">
        <router-link to="/products" class="px-6 py-2.5 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50">取消</router-link>
        <BaseButton type="submit" :loading="saving">更新商品</BaseButton>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAdminProductStore } from '@/stores/adminProduct'

const route = useRoute()
const router = useRouter()
const saving = ref(false)
const adminProductStore = useAdminProductStore()

const form = reactive({
  name: '', slug: '', description: '',
  price: null, originalPrice: null, cost: null, stock: null, sku: '',
  status: 'draft', category: '', brand: '',
})

onMounted(() => {
  const product = adminProductStore.getProduct(route.params.id)
  if (product) {
    Object.assign(form, {
      name: product.name,
      slug: product.slug || '',
      description: product.description || '',
      price: product.price,
      originalPrice: product.originalPrice || null,
      cost: product.cost || null,
      stock: product.stock,
      sku: product.sku || '',
      status: product.status || 'draft',
      category: product.category || '',
      brand: product.brand || '',
    })
  }
})

async function handleSave() {
  saving.value = true
  await new Promise(r => setTimeout(r, 500))
  adminProductStore.updateProduct(route.params.id, { ...form })
  saving.value = false
  router.push('/products')
}
</script>
