import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'
import sharedProductStatus from '../shared/vite-plugin-product-status.js'

export default defineConfig({
  plugins: [vue(), tailwindcss(), sharedProductStatus()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 3001,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    cssCodeSplit: true,
    chunkSizeWarningLimit: 600,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia', 'axios'],
          ui: ['@heroicons/vue'],
        },
      },
    },
    target: 'es2020',
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'axios', 'nprogress'],
  },
})
