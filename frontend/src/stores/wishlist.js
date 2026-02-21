import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useWishlistStore = defineStore('wishlist', () => {
  const items = ref(JSON.parse(localStorage.getItem('wishlist') || '[]'))
  const loading = ref(false)

  const itemCount = computed(() => items.value.length)

  function isInWishlist(productId) {
    return items.value.some((item) => item.productId === productId)
  }

  function toggleWishlist(product) {
    const index = items.value.findIndex((item) => item.productId === product.id)
    if (index > -1) {
      items.value.splice(index, 1)
    } else {
      items.value.push({
        productId: product.id,
        name: product.name,
        slug: product.slug,
        image: product.image || product.images?.[0],
        price: product.price,
        salePrice: product.salePrice,
        addedAt: new Date().toISOString(),
      })
    }
    localStorage.setItem('wishlist', JSON.stringify(items.value))
  }

  function removeFromWishlist(productId) {
    items.value = items.value.filter((item) => item.productId !== productId)
    localStorage.setItem('wishlist', JSON.stringify(items.value))
  }

  function clearWishlist() {
    items.value = []
    localStorage.removeItem('wishlist')
  }

  return {
    items,
    loading,
    itemCount,
    isInWishlist,
    toggleWishlist,
    removeFromWishlist,
    clearWishlist,
  }
})
