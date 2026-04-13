<template>
  <section class="py-20 px-6 text-center">
    <span class="inline-flex items-center gap-1.5 bg-emerald-100 text-emerald-700 text-xs font-semibold px-3 py-1 rounded-full mb-6">
      <span class="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
      Software para hostelería
    </span>
    <h1 class="text-4xl sm:text-5xl font-bold text-gray-800 leading-tight tracking-tight mb-5">
      Del cliente a la cocina,<br>
      <span class="text-emerald-500">sin intermediarios</span>
    </h1>
    <p class="text-gray-500 max-w-lg mx-auto mb-10 leading-relaxed">
      Automatiza los pedidos de tu restaurante en tiempo real. Sin papel, sin malentendidos, sin esperas innecesarias.
    </p>
    <div class="flex gap-3 justify-center flex-wrap">
      <RouterLink :to="{ name: 'login' }" class="px-6 py-3 bg-emerald-400 text-white text-sm font-semibold rounded-xl hover:bg-emerald-500 transition-colors shadow-sm shadow-emerald-400/20">
        Empezar ahora
      </RouterLink>
      <button class="px-6 py-3 bg-white text-gray-700 text-sm font-medium rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors">
        Ver demo
      </button>
    </div>
  </section>

  <hr class="border-gray-200 mx-6">

  <section class="py-16 px-6 max-w-5xl mx-auto">
    <p class="text-xs font-semibold text-emerald-500 tracking-widest uppercase text-center mb-2">Por qué elegirnos</p>
    <h2 class="text-2xl font-bold text-gray-800 text-center tracking-tight mb-2">Todo lo que tu local necesita</h2>
    <p class="text-sm text-gray-400 text-center mb-12">Diseñado para que tu equipo trabaje más rápido y tus clientes estén más satisfechos.</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="feature in features" :key="feature.title" class="bg-white border border-gray-200 rounded-2xl p-6">
        <div class="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center mb-4">
          <span class="text-emerald-600" v-html="feature.icon"></span>
        </div>
        <p class="text-sm font-semibold text-gray-800 mb-1">{{ feature.title }}</p>
        <p class="text-xs text-gray-400 leading-relaxed">{{ feature.desc }}</p>
      </div>
    </div>
  </section>

  <hr class="border-gray-200 mx-6">

  <section class="py-14 px-6 max-w-2xl mx-auto">
    <p class="text-xs font-semibold text-emerald-500 tracking-widest uppercase text-center mb-2">Cómo funciona</p>
    <h2 class="text-2xl font-bold text-gray-800 text-center tracking-tight mb-10">Tres pasos, cero caos</h2>
    <div class="flex flex-col divide-y divide-gray-100">
      <div v-for="step in steps" :key="step.num" class="flex gap-5 py-5">
        <div class="w-8 h-8 min-w-[32px] rounded-full bg-emerald-400 text-white text-sm font-bold flex items-center justify-center mt-0.5">
          {{ step.num }}
        </div>
        <div>
          <p class="text-sm font-semibold text-gray-800 mb-1">{{ step.title }}</p>
          <p class="text-xs text-gray-400 leading-relaxed">{{ step.desc }}</p>
        </div>
      </div>
    </div>
  </section>

  <hr class="border-gray-200 mx-6">

</template>

<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth.store'
import { onMounted } from 'vue'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  const result = await authStore.checkAuthStatus()
  console.log('checkAuthStatus result:', result)
  console.log('isAuthenticated:', authStore.isAuthenticated)
  console.log('user:', authStore.user)
  console.log('role:', authStore.user?.role)

  if (authStore.isAuthenticated) {
    const role = authStore.user?.role
    if (role === 'manager') router.push({ name: 'manager' })
    else if (role === 'kitchen') router.push({ name: 'kitchen' })
    else if (role === 'waiter') router.push({ name: 'waiter' })
  }
})

const features = [
  { title: 'Pedidos en tiempo real', desc: 'El cliente hace el pedido desde la mesa y llega directamente a cocina al instante.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>` },
  { title: 'Gestión de carta digital', desc: 'Actualiza precios, disponibilidad e ingredientes sin imprimir nada nuevo.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 9h6M9 12h6M9 15h4"/></svg>` },
  { title: 'Sin tiempos muertos', desc: 'Menos idas y venidas del camarero. El equipo se centra en dar un mejor servicio.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>` },
  { title: 'Gestión de equipo', desc: 'Invita a tu equipo con un QR y asigna roles fácilmente desde el panel.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>` },
  { title: 'Control de ingredientes', desc: 'Gestiona el stock de ingredientes y vincula cada producto con sus componentes.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-8 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>` },
  { title: 'Panel de estadísticas', desc: 'Visualiza pedidos, productos más vendidos y el rendimiento del local.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>` },
]

const steps = [
  { num: 1, title: 'El cliente escanea el QR de su mesa', desc: 'Accede a la carta digital desde su móvil, sin descargar ninguna app. Navega, elige y confirma su pedido.' },
  { num: 2, title: 'El pedido llega directamente a cocina', desc: 'Sin pasar por el camarero. La cocina ve el pedido en tiempo real con todos los detalles.' },
  { num: 3, title: 'El equipo gestiona y sirve', desc: 'El panel del manager muestra el estado de cada pedido. El camarero solo tiene que llevar y cobrar.' },
]
</script>