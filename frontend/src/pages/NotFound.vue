<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="text-center">
      <h1 class="text-9xl font-black text-primary-600">404</h1>
      <p class="text-2xl font-bold text-gray-900 mt-4 mb-2">找不到頁面</p>
      <p class="text-gray-500 mb-8">您要尋找的頁面不存在或已被移除。</p>
      <div class="flex gap-4 justify-center">
        <router-link to="/" class="bg-primary-600 text-white px-6 py-2.5 rounded-lg hover:bg-primary-700 transition font-medium">回到首頁</router-link>
        <router-link to="/products" class="border border-gray-300 text-gray-700 px-6 py-2.5 rounded-lg hover:bg-gray-100 transition font-medium">瀏覽商品</router-link>
      </div>
    </div>
  </div>
</template>
