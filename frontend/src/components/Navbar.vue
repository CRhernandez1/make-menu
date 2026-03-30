<template>
  <header class="flex place-content-between items-center p-4 bg-green-400 text-gray-900">
    <h2 class="text-xl font-bold">Mi Restaurante</h2>

    <button
      v-if="authStore.isAuthenticated"
      @click="onLogout"
      class="font-semibold hover:text-white transition-colors"
    >
      Cerrar Sesión
    </button>

    <RouterLink
      v-else
      :to="{ name: 'login' }"
      class="font-semibold hover:text-white transition-colors"
    >
      Login
    </RouterLink>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
// Asegúrate de que la ruta de importación coincida con la estructura de tus carpetas
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const router = useRouter()
const authStore = useAuthStore()

// Esta función se dispara al hacer clic en "Cerrar Sesión"
const onLogout = async () => {
  // 1. Ejecutamos tu acción perfecta de logout (borra token y avisa a Django)
  await authStore.logout()

  // 2. Lo mandamos de vuelta a la pantalla de login para que no se quede mirando la nada
  router.push({ name: 'login' })
}
</script>
