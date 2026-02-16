<template>
  <section id="features" class="py-24 bg-gray-50">
    <div class="max-w-7xl mx-auto px-6">
      
      <div class="text-center max-w-3xl mx-auto mb-20">
        <span class="text-emerald-600 font-bold tracking-wider uppercase text-xs bg-emerald-100 px-3 py-1 rounded-full">
          Características
        </span>
        <h3 class="mt-4 text-3xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
          Todo lo que necesitas para crecer.
        </h3>
        <p class="mt-4 text-xl text-gray-500 max-w-2xl mx-auto">
          Deja atrás el papel. Pásate a un sistema más limpio, rápido e inteligente diseñado para hostelería.
        </p>
      </div>

      <div class="grid md:grid-cols-3 gap-10">
        
        <div v-for="(feature, index) in features" :key="index" 
             class="group relative bg-white p-10 rounded-3xl shadow-sm hover:shadow-2xl hover:shadow-emerald-900/10 border border-gray-100 hover:border-emerald-400 transition-all duration-300 ease-out hover:-translate-y-2">
          
          <div class="w-16 h-16 bg-emerald-50 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-emerald-500 transition-colors duration-300">
            <svg class="w-8 h-8 text-emerald-500 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" v-html="feature.svgPath">
            </svg>
          </div>
          
          <h4 class="text-2xl font-bold text-gray-900 mb-4 group-hover:text-emerald-600 transition-colors">
            {{ feature.title }}
          </h4>
          <p class="text-gray-600 leading-relaxed text-lg">
            {{ feature.desc }}
          </p>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  { 
    title: 'Carta Sin Contacto', 
    desc: 'Elimina los menús físicos sucios y costosos. Tus clientes escanean un QR y acceden a tu carta digital al instante.',
    // Icono: Mobile / Smartphone
    svgPath: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>' 
  },
  { 
    title: 'Actualización Real', 
    desc: '¿Se acabó el salmón? ¿Cambio de precios? Actualiza tu menú en segundos desde el panel de control sin reimprimir nada.',
    // Icono: Edit / Adjustments
    svgPath: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>' 
  },
  { 
    title: 'Cocina Sincronizada', 
    desc: 'Los pedidos viajan digitalmente directo a la cocina. Reduce errores de comanda y acelera la rotación de mesas.',
    // Icono: Server / Kitchen
    svgPath: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>' 
  }
];
</script>