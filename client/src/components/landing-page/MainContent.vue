<template>
  <section class="relative pt-12 pb-20 lg:pt-20 overflow-hidden">
    <div class="container mx-auto px-6 flex flex-col-reverse lg:flex-row items-center gap-12">
      
      <div class="w-full lg:w-1/2 text-center lg:text-left">
        <div class="inline-block mb-4 px-3 py-1 rounded-full bg-emerald-50 text-emerald-600 text-sm font-semibold border border-emerald-100">
          🚀 La evolución de tu restaurante
        </div>
        
        <h2 class="text-5xl lg:text-6xl font-bold tracking-tight text-gray-900 leading-tight mb-6">
          Pide y paga, <br />
          <span class="text-emerald-400">así de fácil.</span>
        </h2>
        
        <p class="text-lg text-gray-600 mb-8 leading-relaxed max-w-lg mx-auto lg:mx-0">
          Digitaliza tu carta y optimiza el servicio. Tus clientes escanean, piden y pagan desde su móvil sin esperas. Más rotación de mesas, menos errores y clientes más felices.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
          <button class="px-8 py-4 bg-emerald-400 text-white font-bold rounded-xl hover:bg-emerald-500 transition-transform hover:-translate-y-1 shadow-lg shadow-emerald-400/30">
            Crear mi Menú Gratis
          </button>
          <button class="px-8 py-4 bg-white text-gray-700 font-bold border border-gray-200 rounded-xl hover:border-emerald-400 hover:text-emerald-500 transition-colors">
            Ver Demo
          </button>
        </div>

        <p class="mt-6 text-sm text-gray-400">
          * No requiere tarjeta de crédito para empezar.
        </p>
      </div>

      <div class="w-full lg:w-1/2 relative">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-emerald-400/10 rounded-full blur-3xl -z-10"></div>
        
        <img 
          src="https://images.unsplash.com/photo-1556742049-0cfed4f7a07d?q=80&w=1000&auto=format&fit=crop" 
          alt="Cliente pagando con el móvil" 
          class="rounded-3xl shadow-2xl transform rotate-1 hover:rotate-0 transition-all duration-500 border-4 border-white"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
</script>