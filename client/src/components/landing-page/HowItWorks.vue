<template>
  <section id="how-it-works" class="py-20 bg-white overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid md:grid-cols-2 gap-16 items-center">
        <div class="order-2 md:order-1 relative">
          <img src="https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&q=80&w=1000" class="rounded-2xl shadow-2xl relative z-10 w-full border-4 border-white" alt="Mobile Pay" />
          <div class="absolute -bottom-6 -right-6 w-2/3 h-2/3 bg-emerald-400/20 rounded-2xl -z-0"></div>
        </div>
        <div class="order-1 md:order-2">
          <h2 class="text-emerald-500 font-bold tracking-wide uppercase text-sm mb-2">Flujo de trabajo</h2>
          <h3 class="text-3xl font-bold text-gray-900 mb-8">De la Mesa a la Cocina.</h3>
          <div class="space-y-8">
            <div class="flex gap-4" v-for="(step, i) in steps" :key="i">
              <div class="flex-shrink-0 w-10 h-10 rounded-full border-2 border-emerald-400 font-bold flex items-center justify-center text-lg" 
                   :class="i===0 ? 'bg-emerald-400 text-white' : 'bg-white text-gray-900'">{{ i+1 }}</div>
              <div>
                <h4 class="text-xl font-bold text-gray-900 mb-2">{{ step.title }}</h4>
                <p class="text-gray-600">{{ step.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  { title: 'Escanea el QR', desc: 'El cliente escanea el código único de su mesa.' },
  { title: 'Mira y Pide', desc: 'Menú digital visual. El cliente elige y personaliza.' },
  { title: 'Paga al Instante', desc: 'La cuenta se liquida antes de servir (opcional).' }
];
</script>