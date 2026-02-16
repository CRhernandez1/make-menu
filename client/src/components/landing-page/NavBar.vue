<template>
  <header class="nav-bar flex flex-row justify-between h-[10vh] items-center px-4">
    <div class="flex flex-row">
      <div class="flex flex-row">
        <CompanyLogo class="position: absolute top-5 left-2" />
        <h1 class="position: relative mr-16 font-bold ml-10">Make Menu</h1>
      </div>
      <nav class="flex flex-row gap-4">
        <a href="#">Nuestro Producto</a>
        <a href="#">Funcionalidades</a>
        <a href="#">Quiénes somos</a>
      </nav>
    </div>

    <button
      v-if="auth.isLoggedIn"
      @click="auth.logout()"
      class="block p-2.5 bg-red-400 text-white rounded-xl"
    >
      Cerrar sesión
    </button>
    <RouterLink
      v-else
      to="/login"
      class="block p-2.5 bg-emerald-400 rounded-xl"
    >
      Empezar &rarr;
    </RouterLink>
  </header>
</template>

<script setup lang="ts">
import CompanyLogo from './CompanyLogo.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.nav-bar {
  background-color: #fff;
}
</style>
