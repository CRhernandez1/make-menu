<template>
  <!-- HERO -->
  <section class="relative py-24 px-6 text-center overflow-hidden">
    <div class="absolute w-[500px] h-[500px] top-[-200px] left-1/2 -translate-x-1/2 pointer-events-none opacity-60" style="background:rgba(26,92,46,0.03);animation:blob-morph 10s ease-in-out infinite"></div>

    <div class="relative z-10">
      <span class="inline-flex items-center gap-2 bg-green-soft text-green-forest text-xs font-semibold px-4 py-1.5 rounded-full mb-8">
        <span class="w-1.5 h-1.5 bg-green-bright rounded-full" style="animation:pulse-dot 2s infinite"></span>
        Software para hostelería
      </span>

      <h1 class="font-display text-5xl sm:text-6xl font-bold text-green-forest leading-[1.05] tracking-tighter mb-6">
        Adiós al caos en sala.<br>
        <span class="text-green-medium">Hola, control.</span>
      </h1>

      <p class="text-text-sec max-w-lg mx-auto mb-10 leading-relaxed text-base">
        Tu cliente escanea, pide y cocina recibe. Sin papel, sin malentendidos, sin esperas. Tú te sirves un café mientras tanto.
      </p>

      <div class="flex gap-3 justify-center flex-wrap">
        <RouterLink
          :to="{ name: 'login' }"
          class="btn-mm btn-primary px-8 py-3.5 text-[15px]"
        >
          Empezar gratis →
        </RouterLink>
        <button class="btn-mm btn-secondary px-8 py-3.5 text-[15px]">
          Ver cómo funciona
        </button>
      </div>
    </div>
  </section>

  <div class="mx-6 h-px bg-border-green-light"></div>

  <!-- FEATURES -->
  <section class="py-20 px-6 max-w-5xl mx-auto">
    <p class="text-xs font-bold text-green-bright tracking-[0.14em] uppercase text-center mb-2 font-display">Por qué elegirnos</p>
    <h2 class="font-display text-3xl font-bold text-green-forest text-center tracking-tight mb-3">Todo lo que tu local necesita</h2>
    <p class="text-sm text-text-muted text-center mb-14 max-w-md mx-auto">Diseñado para que tu equipo trabaje más rápido y tus clientes estén más satisfechos.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="feature in features"
        :key="feature.title"
        class="card-mm p-7 cursor-default"
      >
        <div class="w-11 h-11 bg-green-soft rounded-2xl flex items-center justify-center mb-5">
          <span class="text-green-forest" v-html="feature.icon"></span>
        </div>
        <p class="text-[15px] font-bold text-ink mb-1.5">{{ feature.title }}</p>
        <p class="text-xs text-text-muted leading-relaxed">{{ feature.desc }}</p>
      </div>
    </div>
  </section>

  <div class="mx-6 h-px bg-border-green-light"></div>

  <!-- HOW IT WORKS -->
  <section class="py-20 px-6 max-w-2xl mx-auto">
    <p class="text-xs font-bold text-green-bright tracking-[0.14em] uppercase text-center mb-2 font-display">Cómo funciona</p>
    <h2 class="font-display text-3xl font-bold text-green-forest text-center tracking-tight mb-12">Tres pasos, cero caos</h2>

    <div class="flex flex-col">
      <div
        v-for="step in steps"
        :key="step.num"
        class="flex gap-5 py-6 border-b border-border-green-light last:border-b-0"
      >
        <div class="w-9 h-9 min-w-[36px] rounded-full bg-green-forest text-cream text-sm font-bold flex items-center justify-center mt-0.5 font-display">
          {{ step.num }}
        </div>
        <div>
          <p class="text-[15px] font-bold text-ink mb-1">{{ step.title }}</p>
          <p class="text-sm text-text-sec leading-relaxed">{{ step.desc }}</p>
        </div>
      </div>
    </div>
  </section>

  <div class="mx-6 h-px bg-border-green-light"></div>

  <!-- CTA FINAL -->
  <section class="py-20 px-6 text-center">
    <h2 class="font-display text-3xl font-bold text-green-forest tracking-tight mb-4">¿Listo para el control?</h2>
    <p class="text-text-sec mb-8 max-w-md mx-auto">Crea tu cuenta gratis. Sin tarjeta de crédito. Cancela cuando quieras.</p>
    <RouterLink
      :to="{ name: 'login' }"
      class="btn-mm btn-primary px-10 py-4 text-[15px]"
    >
      Empezar ahora →
    </RouterLink>
  </section>
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
  { title: 'Pedidos en tiempo real', desc: 'El cliente hace el pedido desde la mesa y llega directamente a cocina al instante.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>` },
  { title: 'Carta digital con QR', desc: 'Actualiza precios, disponibilidad e ingredientes sin imprimir nada nuevo.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 9h6M9 12h6M9 15h4"/></svg>` },
  { title: 'Sin tiempos muertos', desc: 'Menos idas y venidas del camarero. El equipo se centra en dar un mejor servicio.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>` },
  { title: 'Gestión de equipo', desc: 'Invita a tu equipo con un QR y asigna roles fácilmente desde el panel.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>` },
  { title: 'Control de ingredientes', desc: 'Gestiona el stock y vincula cada producto con sus componentes y alérgenos.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-8 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>` },
  { title: 'Panel de estadísticas', desc: 'Visualiza pedidos, productos más vendidos y el rendimiento del local.', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>` },
]

const steps = [
  { num: 1, title: 'El cliente escanea el QR de su mesa', desc: 'Accede a la carta digital desde su móvil, sin descargar ninguna app. Navega, elige y confirma su pedido.' },
  { num: 2, title: 'El pedido llega directamente a cocina', desc: 'Sin pasar por el camarero. La cocina ve el pedido en tiempo real con todos los detalles y notas.' },
  { num: 3, title: 'El equipo gestiona y sirve', desc: 'El camarero ve el estado de cada mesa. Cocina marca los platos listos. Solo queda servir y cobrar.' },
]
</script>