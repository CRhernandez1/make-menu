<template>
  <header class="bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-6 py-3.5 flex items-center justify-between">

      <div class="flex items-center gap-2.5">
        <div class="flex items-center justify-center w-8 h-8 bg-emerald-400 rounded-lg">
          <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        </div>
        <h2 class="text-sm font-bold text-gray-700 tracking-tight">MakeMenu</h2>
      </div>

      <div>
        <button
          v-if="authStore.isAuthenticated"
          @click="onLogout"
          class="px-4 py-2 bg-red-400 text-white text-sm font-semibold rounded-xl hover:bg-red-500 transition-colors shadow-sm shadow-red-400/20"
        >
          Cerrar Sesión
        </button>
        <RouterLink
          v-else
          :to="{ name: 'login' }"
          class="px-4 py-2 bg-emerald-400 text-white text-sm font-semibold rounded-xl hover:bg-emerald-500 transition-colors shadow-sm shadow-emerald-400/20"
        >
          Login
        </RouterLink>
      </div>

    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
// Asegúrarse de que la ruta de importación coincida con la estructura de tus carpetas
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const router = useRouter()
const authStore = useAuthStore()

const onLogout = async () => {
  // 1. Ejecutamos tu acción perfecta de logout (borra token y avisa a Django)
  await authStore.logout()
  // 2. Lo mandamos de vuelta a la pantalla de login para que no se quede mirando la nada
  router.push({ name: 'login' })
}
</script>
