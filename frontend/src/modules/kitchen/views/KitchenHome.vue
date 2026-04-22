<template>
  <div class="p-6 lg:p-8">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-white">Pedidos</h1>
        <p class="text-sm text-gray-500 mt-0.5">{{ store.establishmentName }}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-500">{{ store.orders.length }} activos</span>
        <button
          @click="store.fetchOrders()"
          class="p-2.5 rounded-xl bg-gray-800 border border-gray-700 text-gray-400 hover:text-orange-400 hover:border-orange-500/50 transition-all"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 bg-red-500/10 text-red-400 border border-red-500/20">
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError()" class="text-red-300 hover:text-red-200">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading && store.orders.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="n in 4" :key="n" class="h-48 rounded-2xl bg-gray-800 animate-pulse"></div>
    </div>

    <!-- Sin pedidos -->
    <div v-else-if="store.orders.length === 0" class="text-center py-24">
      <div class="w-20 h-20 rounded-full bg-gray-800 flex items-center justify-center mx-auto mb-5">
        <svg class="w-10 h-10 text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/>
          <path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/>
        </svg>
      </div>
      <p class="text-gray-500 font-medium text-lg">No hay pedidos</p>
      <p class="text-gray-600 text-sm mt-1">Los pedidos aparecerán aquí cuando los clientes pidan</p>
    </div>

    <!-- Grid de pedidos -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="order in store.orders"
        :key="order.id"
        class="bg-gray-800 border-2 rounded-2xl p-4 space-y-3 transition-all"
        :class="order.status === 1 ? 'border-amber-500/30' : 'border-blue-500/30'"
      >
        <!-- Header del pedido -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-2xl font-bold text-white">
              {{ String(order.table_number).padStart(2, '0') }}
            </span>
            <span class="text-xs text-gray-500">Mesa</span>
          </div>
          <div class="text-right">
            <span class="text-xs text-gray-500">{{ formatTime(order.placed_at) }}</span>
            <p class="text-xs font-medium" :class="order.status === 1 ? 'text-amber-400' : 'text-blue-400'">
              {{ elapsedTime(order.placed_at) }}
            </p>
          </div>
        </div>

        <!-- Progreso -->
        <div class="flex items-center gap-2">
          <div class="flex-1 h-1.5 bg-gray-700 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full transition-all duration-500"
              :class="order.ready_count === order.total_count ? 'bg-emerald-400' : 'bg-blue-400'"
              :style="{ width: `${(order.ready_count / order.total_count) * 100}%` }"
            ></div>
          </div>
          <span class="text-xs text-gray-500 min-w-[40px] text-right">
            {{ order.ready_count }}/{{ order.total_count }}
          </span>
        </div>

        <!-- Items -->
        <div class="space-y-1">
          <div
            v-for="item in order.items"
            :key="item.id"
            @click="handleToggleItem(item.id)"
            class="flex items-start gap-3 p-2.5 rounded-xl cursor-pointer transition-all"
            :class="item.ready
              ? 'bg-emerald-500/10 border border-emerald-500/20'
              : 'bg-gray-700/50 border border-transparent hover:border-gray-600'"
          >
            <!-- Checkbox visual -->
            <div
              class="w-5 h-5 rounded-md border-2 flex items-center justify-center shrink-0 mt-0.5 transition-all"
              :class="item.ready
                ? 'bg-emerald-500 border-emerald-500'
                : 'border-gray-500'"
            >
              <svg v-if="item.ready" class="w-3 h-3 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex items-baseline gap-2">
                <span class="font-bold text-sm" :class="item.ready ? 'text-emerald-400' : 'text-white'">
                  {{ item.quantity }}x
                </span>
                <span
                  class="text-sm font-medium transition-all"
                  :class="item.ready ? 'text-emerald-400/70 line-through' : 'text-white'"
                >
                  {{ item.product_name }}
                </span>
              </div>
              <p v-if="item.notes" class="text-xs text-red-400 font-medium mt-0.5">
                {{ item.notes }}
              </p>
            </div>
          </div>
        </div>

        <!-- Botón completar todo (si quedan pendientes) -->
        <button
          v-if="order.ready_count < order.total_count"
          @click="handleCompleteAll(order)"
          class="w-full py-2 rounded-xl border border-gray-600 text-gray-400 text-xs font-medium hover:border-emerald-500/50 hover:text-emerald-400 transition-colors"
        >
          Marcar todo como listo
        </button>
      </div>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div
        v-if="toast"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-3 px-5 py-3 rounded-xl text-sm shadow-lg border z-50"
        :class="toast.type === 'success'
          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
          : 'bg-red-500/10 text-red-400 border-red-500/20'"
      >
        <span>{{ toast.message }}</span>
        <button @click="toast = null" class="text-current opacity-50 hover:opacity-100">&times;</button>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useKitchenStore } from '../stores/kitchen.store'
import type { KitchenOrder } from '../stores/kitchen.store'

const store = useKitchenStore()

// Toast
interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 3000)
}

// Toggle plato individual
const handleToggleItem = async (itemId: number) => {
  const result = await store.toggleItem(itemId)
  if (result.ok) {
    if (result.order_done) {
      showToast('success', 'Pedido completo — listo para servir')
    }
  } else {
    showToast('error', result.error!)
  }
}

// Completar todos los platos de un pedido
const handleCompleteAll = async (order: KitchenOrder) => {
  const pendingItems = order.items.filter(i => !i.ready)
  for (const item of pendingItems) {
    await store.toggleItem(item.id)
  }
  showToast('success', `Mesa ${order.table_number} — pedido completo`)
}

// Helpers
const formatTime = (iso: string) => {
  return new Date(iso).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const elapsedTime = (iso: string) => {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 60000)
  if (diff < 1) return 'ahora'
  if (diff < 60) return `${diff} min`
  return `${Math.floor(diff / 60)}h ${diff % 60}m`
}

// Auto-refresh cada 15 segundos
let refreshInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  store.fetchOrders()
  refreshInterval = setInterval(() => store.fetchOrders(), 15000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style scoped>
.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(20px) translateX(-50%); }
</style>