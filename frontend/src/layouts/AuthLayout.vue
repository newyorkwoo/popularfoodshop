<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50">
    <div class="w-full max-w-md mx-4">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-block">
          <h1 class="text-3xl font-bold text-primary-600">🍜 人氣美食商店</h1>
        </router-link>
      </div>
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
      <p class="text-center text-sm text-gray-500 mt-6">
        © {{ new Date().getFullYear() }} Popular Food Shop
      </p>
    </div>
  </div>
</template>
