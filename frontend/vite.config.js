import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    // Performance: enable CSS code splitting
    cssCodeSplit: true,
    // Increase chunk size warning limit
    chunkSizeWarningLimit: 600,
    // Minify with esbuild (fastest)
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia', 'axios'],
          ui: ['swiper', '@heroicons/vue'],
          i18n: ['vue-i18n'],
          forms: ['vee-validate', 'yup'],
        },
      },
    },
    // Target modern browsers for smaller bundles
    target: 'es2020',
  },
  // Dependency pre-bundling optimization
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'axios',
      'vue-i18n',
      'nprogress',
      '@heroicons/vue/24/outline',
      '@heroicons/vue/24/solid',
    ],
  },
})
