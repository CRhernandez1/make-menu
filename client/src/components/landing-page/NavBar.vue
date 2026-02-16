<template>
  <header 
    class="fixed top-0 z-50 w-full bg-white/90 backdrop-blur-md border-b border-gray-100 transition-transform duration-300 h-[10vh]"
    :class="{ '-translate-y-full': isHidden }"
  >
    <div class="container mx-auto px-6 h-full flex items-center justify-between">
      
      <div class="flex items-center gap-3">
        <CompanyLogo /> 
        <h1 class="font-bold text-xl tracking-tight text-gray-800">
          Make Menu
        </h1>
      </div>

      <nav class="hidden md:flex flex-row items-center gap-8">
        <a href="#" class="text-gray-600 hover:text-emerald-500 font-medium transition-colors">
          Nuestro Producto
        </a>
        <a href="#" class="text-gray-600 hover:text-emerald-500 font-medium transition-colors">
          Funcionalidades
        </a>
        <a href="#" class="text-gray-600 hover:text-emerald-500 font-medium transition-colors">
          Quiénes somos
        </a>
      </nav>

      <a 
        href="#" 
        class="px-5 py-2.5 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-400/20 flex items-center gap-2"
      >
        Empezar <span>&rarr;</span>
      </a>

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
import { ref, onMounted, onUnmounted } from 'vue';
import CompanyLogo from './CompanyLogo.vue';

const isHidden = ref(false);
const lastScrollY = ref(0);

const handleScroll = () => {
  const currentScrollY = window.scrollY;
  // Ajustamos el umbral a 100px para que no baile tanto al inicio
  if (currentScrollY > lastScrollY.value && currentScrollY > 100) {
    isHidden.value = true;
  } else {
    isHidden.value = false;
  }
  lastScrollY.value = currentScrollY;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>
