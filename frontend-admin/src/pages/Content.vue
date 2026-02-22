<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 mb-6">內容管理</h2>

    <!-- Banners -->
    <div class="mb-10">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold text-gray-900">首頁輪播</h3>
        <BaseButton size="sm" @click="store.addBanner()"><PlusIcon class="w-4 h-4 mr-1" /> 新增</BaseButton>
      </div>
      <div class="grid md:grid-cols-2 gap-4">
        <div v-for="b in banners" :key="b.id" class="border border-gray-200 rounded-xl overflow-hidden">
          <img :src="b.image" class="w-full h-40 object-cover bg-gray-100" />
          <div class="p-4">
            <p class="font-medium text-gray-900 text-sm">{{ b.title }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ b.link }}</p>
            <div class="flex gap-3 mt-3">
              <button @click="store.updateBanner(b.id, { title: prompt('輪播標題', b.title) || b.title })" class="text-primary-600 hover:underline text-xs">編輯</button>
              <button @click="store.deleteBanner(b.id)" class="text-red-500 hover:underline text-xs">刪除</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Announcement -->
    <div class="mb-10">
      <h3 class="text-lg font-bold text-gray-900 mb-4">公告欄</h3>
      <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
        <BaseInput v-model="announcement.text" label="公告文字" />
        <label class="flex items-center gap-2 text-sm">
          <input type="checkbox" v-model="announcement.enabled" class="accent-primary-600" /> 啟用公告欄
        </label>
        <BaseButton size="sm" @click="store.saveAnnouncement()">儲存</BaseButton>
      </div>
    </div>

    <!-- SEO -->
    <div>
      <h3 class="text-lg font-bold text-gray-900 mb-4">首頁 SEO 設定</h3>
      <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-4">
        <BaseInput v-model="seo.title" label="頁面標題" />
        <div><label class="block text-sm font-medium text-gray-700 mb-1">Meta Description</label>
          <textarea v-model="seo.description" rows="3" class="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm"></textarea></div>
        <BaseInput v-model="seo.keywords" label="關鍵字 (逗號分隔)" />
        <BaseButton size="sm" @click="store.saveSeo()">儲存</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { PlusIcon } from '@heroicons/vue/24/outline'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useAdminContentStore } from '@/stores/adminContent'

const store = useAdminContentStore()
const { banners, announcement, seo } = storeToRefs(store)
</script>
