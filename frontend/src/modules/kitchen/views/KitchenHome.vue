<template>
  <div class="min-h-screen bg-ink p-6 lg:p-8">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 rounded-xl bg-warning flex items-center justify-center">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
        </div>
        <div>
          <h1 class="font-display text-2xl font-bold text-cream tracking-tight">Cocina</h1>
          <p class="text-sm text-[#7a7a6e]">{{ store.establishmentName }}</p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-[#7a7a6e] font-display">{{ store.orders.length }} activos</span>
        <button @click="store.fetchOrders()"
          class="w-10 h-10 rounded-[14px] bg-[#2c2c2a] border border-[#3d3d38] text-[#7a7a6e] flex items-center justify-center cursor-pointer hover:text-warning hover:border-[rgba(196,138,26,0.3)] transition-all">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
        </button>
        <button @click="handleLogout"
          class="w-10 h-10 rounded-[14px] bg-[#2c2c2a] border border-[#3d3d38] text-[#7a7a6e] flex items-center justify-center cursor-pointer hover:text-danger hover:border-[rgba(185,60,60,0.3)] transition-all" title="Cerrar sesión">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </button>
      </div>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="flex items-center gap-3 p-4 rounded-2xl text-sm mb-5 bg-[rgba(185,60,60,0.08)] text-danger border border-[rgba(185,60,60,0.15)]">
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError()" class="text-danger/40 hover:text-danger/80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading && store.orders.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="n in 4" :key="n" class="h-48 rounded-[var(--radius-card)] bg-[#2c2c2a]" style="background:linear-gradient(90deg,#2c2c2a 25%,#3d3d38 37%,#2c2c2a 63%);background-size:800px 100%;animation:shimmer 1.8s infinite linear"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="store.orders.length === 0" class="text-center py-24">
      <div class="w-20 h-20 rounded-full bg-[rgba(255,255,255,0.04)] flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7a7a6e" stroke-width="1.5" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-cream mb-2">Cocina despejada</h3>
      <p class="text-sm text-[#7a7a6e]">Los pedidos aparecerán aquí cuando los clientes pidan desde el QR.</p>
    </div>

    <!-- Grid pedidos -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="order in store.orders" :key="order.id"
        class="bg-[#2c2c2a] border-2 rounded-[var(--radius-card)] p-5 space-y-3 transition-all"
        :class="cardBorderClass(order)">

        <!-- Header pedido -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <span class="font-display text-[28px] font-bold text-cream tracking-tight">{{ String(order.table_number).padStart(2, '0') }}</span>
            <span class="text-[11px] text-[#7a7a6e]">Mesa</span>
            <span v-if="isUrgent(order)" class="badge-mm bg-danger-soft text-danger text-[10px] px-2.5 py-0.5" style="animation:ring-pulse 2s infinite">Urgente</span>
          </div>
          <div class="text-right">
            <span class="text-xs text-[#7a7a6e]">{{ formatTime(order.placed_at) }}</span>
            <p class="text-xs font-semibold mt-0.5" :class="isUrgent(order) ? 'text-danger' : order.status === 1 ? 'text-warning' : 'text-info'">
              {{ elapsedTime(order.placed_at) }}
            </p>
          </div>
        </div>

        <!-- Progreso -->
        <div class="flex items-center gap-2.5">
          <div class="flex-1 h-[5px] bg-[#3d3d38] rounded-full overflow-hidden">
            <div class="h-full rounded-full transition-all duration-500"
              :class="order.ready_count === order.total_count ? 'bg-green-bright' : isUrgent(order) ? 'bg-danger' : 'bg-info'"
              :style="{ width: `${(order.ready_count / order.total_count) * 100}%` }"></div>
          </div>
          <span class="text-xs font-display font-semibold min-w-[28px] text-right"
            :class="isUrgent(order) ? 'text-danger' : 'text-[#7a7a6e]'">{{ order.ready_count }}/{{ order.total_count }}</span>
        </div>

        <!-- Items -->
        <div class="space-y-1.5">
          <div v-for="item in order.items" :key="item.id" @click="handleToggleItem(item.id)"
            class="flex items-start gap-3 p-3 rounded-[14px] cursor-pointer transition-all border-[1.5px]"
            :class="item.ready
              ? 'bg-[rgba(26,92,46,0.1)] border-[rgba(26,92,46,0.15)]'
              : 'bg-[rgba(255,255,255,0.04)] border-transparent hover:border-[rgba(255,255,255,0.06)]'">
            <div class="w-[22px] h-[22px] rounded-[7px] flex items-center justify-center shrink-0 mt-0.5 transition-all"
              :class="item.ready ? 'bg-green-forest' : 'border-2 border-[rgba(255,255,255,0.2)]'"
              :style="item.ready ? 'transform:scale(1.1)' : ''">
              <svg v-if="item.ready" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-baseline gap-2">
                <span class="font-bold text-sm" :class="item.ready ? 'text-green-bright' : 'text-cream'">{{ item.quantity }}x</span>
                <span class="text-sm font-medium" :class="item.ready ? 'text-[rgba(60,176,106,0.6)] line-through' : 'text-[rgba(255,255,255,0.9)]'">{{ item.product_name }}</span>
              </div>
              <p v-if="item.notes" class="text-xs text-danger font-semibold mt-1 flex items-center gap-1">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
                {{ item.notes }}
              </p>
            </div>
          </div>
        </div>

        <!-- Botón completar -->
        <button v-if="order.ready_count < order.total_count" @click="handleCompleteAll(order)"
          class="w-full py-2.5 rounded-full border-[1.5px] border-[rgba(26,92,46,0.15)] text-green-bright text-xs font-semibold bg-[rgba(26,92,46,0.08)] hover:bg-[rgba(26,92,46,0.15)] transition-colors cursor-pointer">
          Marcar todo como listo
        </button>
      </div>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-3 px-5 py-3 rounded-full text-sm shadow-lg z-50"
        :class="toast.type === 'success' ? 'bg-green-forest text-cream' : 'bg-danger text-white'">
        <svg v-if="toast.type === 'success'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        <span class="font-semibold">{{ toast.message }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useKitchenStore } from '../stores/kitchen.store'
import { useAuthStore } from '@/modules/auth/stores/auth.store'
import type { KitchenOrder } from '../stores/kitchen.store'

const store = useKitchenStore()
const authStore = useAuthStore()
const router = useRouter()

interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 3000)
}

const handleToggleItem = async (itemId: number) => {
  const result = await store.toggleItem(itemId)
  if (result.ok) { if (result.order_done) showToast('success', 'Pedido completo — listo para servir') }
  else { showToast('error', result.error!) }
}

const handleCompleteAll = async (order: KitchenOrder) => {
  const pendingItems = order.items.filter(i => !i.ready)
  for (const item of pendingItems) { await store.toggleItem(item.id) }
  showToast('success', `Mesa ${order.table_number} — pedido completo`)
}

const handleLogout = async () => { await authStore.logout(); router.push({ name: 'home' }) }

const formatTime = (iso: string) => new Date(iso).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
const elapsedTime = (iso: string) => {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 60000)
  if (diff < 1) return 'ahora'
  if (diff < 60) return `${diff} min`
  return `${Math.floor(diff / 60)}h ${diff % 60}m`
}
const isUrgent = (order: KitchenOrder) => Math.floor((Date.now() - new Date(order.placed_at).getTime()) / 60000) >= 15

const cardBorderClass = (order: KitchenOrder) => {
  if (isUrgent(order)) return 'border-[rgba(185,60,60,0.5)]'
  return order.status === 1 ? 'border-[rgba(196,138,26,0.3)]' : 'border-[rgba(37,99,235,0.3)]'
}

let refreshInterval: ReturnType<typeof setInterval> | null = null
onMounted(() => { store.fetchOrders(); refreshInterval = setInterval(() => store.fetchOrders(), 15000) })
onUnmounted(() => { if (refreshInterval) clearInterval(refreshInterval) })
</script>

<style scoped>
.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(20px) translateX(-50%); }
</style>