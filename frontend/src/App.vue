<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/auth.store'
import ToastContainer from '@/components/ToastContainer.vue'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.checkAuthStatus()
})
</script>

<template>
  <RouterView />
  <ToastContainer />
</template>
