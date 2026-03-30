<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const authStore = useAuthStore()

// onMounted se dispara una única vez en cuanto la página web se carga en el navegador
onMounted(async () => {
  // Aquí es donde apretamos el gatillo
  await authStore.checkAuthStatus()
})
</script>

<template>
  <RouterView />
</template>
