<template>
  <header class="sticky top-0 z-50 w-full bg-white/90 backdrop-blur-md border-b border-gray-100">
    <div class="container mx-auto px-6 h-20 flex items-center justify-between">
      
      <div class="flex items-center gap-3">
        <CompanyLogo class="h-10 w-10 text-emerald-500" /> 
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
  </header>
</template>

<script setup lang="ts">
import CompanyLogo from './CompanyLogo.vue';
</script>