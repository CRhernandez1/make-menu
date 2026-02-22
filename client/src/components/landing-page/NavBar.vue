<script setup lang="ts">
  import { ref, onMounted, onUnmounted } from 'vue';
  import { RouterLink } from 'vue-router'; 
  import CompanyLogo from './CompanyLogo.vue';
  import { useAuthStore } from '@/stores/auth';

  const auth = useAuthStore();
  const isHidden = ref(false);
  const lastScrollY = ref(0);

  const handleScroll = () => {
    const currentScrollY = window.scrollY;
    // Lógica para ocultar el navbar al bajar y mostrar al subir
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

      <div class="flex items-center gap-4">
        
        <button
          v-if="auth.isLoggedIn"
          @click="auth.logout()"
          class="px-5 py-2.5 bg-red-400 text-white font-semibold rounded-xl hover:bg-red-500 transition-all shadow-lg shadow-red-400/20"
        >
          Cerrar sesión
        </button>

        <RouterLink
          v-else
          to="/login"
          class="px-5 py-2.5 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-400/20 flex items-center gap-2"
        >
          Empezar <span>&rarr;</span>
        </RouterLink>

      </div>

    </div>
  </header>
</template>

<style scoped>
.nav-bar {
  background-color: #fff;
}
</style>