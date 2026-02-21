import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // Mobile menu
  const mobileMenuOpen = ref(false)
  // Search overlay
  const searchOpen = ref(false)
  // Cart drawer
  const cartDrawerOpen = ref(false)
  // Toast notifications
  const toasts = ref([])
  // Global loading overlay
  const globalLoading = ref(false)
  // Modal
  const modalComponent = ref(null)
  const modalProps = ref({})

  let toastId = 0

  function toggleMobileMenu(value) {
    mobileMenuOpen.value = value ?? !mobileMenuOpen.value
    if (mobileMenuOpen.value) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
  }

  function toggleSearch(value) {
    searchOpen.value = value ?? !searchOpen.value
  }

  function toggleCartDrawer(value) {
    cartDrawerOpen.value = value ?? !cartDrawerOpen.value
    if (cartDrawerOpen.value) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
  }

  function showToast(message, type = 'info', duration = 3000) {
    const id = ++toastId
    toasts.value.push({ id, message, type, duration })
    if (duration > 0) {
      setTimeout(() => removeToast(id), duration)
    }
    return id
  }

  function removeToast(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  function showModal(component, props = {}) {
    modalComponent.value = component
    modalProps.value = props
    document.body.style.overflow = 'hidden'
  }

  function closeModal() {
    modalComponent.value = null
    modalProps.value = {}
    document.body.style.overflow = ''
  }

  function setGlobalLoading(value) {
    globalLoading.value = value
  }

  return {
    mobileMenuOpen,
    searchOpen,
    cartDrawerOpen,
    toasts,
    globalLoading,
    modalComponent,
    modalProps,
    toggleMobileMenu,
    toggleSearch,
    toggleCartDrawer,
    showToast,
    removeToast,
    showModal,
    closeModal,
    setGlobalLoading,
  }
})
