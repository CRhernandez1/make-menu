<template>
  <div class="space-y-6">

    <!-- Toast nuevo pedido -->
    <Transition name="toast-right">
      <div v-if="newOrderToast"
        class="fixed top-6 right-6 z-[60] bg-green-forest text-cream px-6 py-4 rounded-2xl shadow-[0_20px_50px_rgba(26,92,46,0.3)] flex items-center gap-3 cursor-pointer"
        style="animation:fade-up 0.4s cubic-bezier(0.25,1,0.5,1)"
        @click="newOrderToast = null">
        <div class="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
        </div>
        <div>
          <p class="font-bold text-sm">¡Nuevo pedido!</p>
          <p class="text-cream/70 text-xs font-medium">{{ newOrderToast }}</p>
        </div>
      </div>
    </Transition>

    <!-- Header -->
    <div class="card-mm p-5 !cursor-default !transform-none flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="flex items-center gap-3">
        <h2 class="font-display text-xl font-bold text-green-forest tracking-tight">Pedidos activos</h2>
        <span class="relative flex h-2.5 w-2.5" title="Actualizando en tiempo real">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-bright opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-forest"></span>
        </span>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <select v-model="activeEstablishment" @change="fetchOrders" class="input-mm !w-auto !h-10 pr-10 cursor-pointer text-[13px]">
          <option value="all">Todos mis locales</option>
          <option v-for="est in myEstablishments" :key="est.id" :value="est.id">{{ est.name }}</option>
        </select>

        <div class="inline-flex bg-cream border border-border-green rounded-[12px] p-1 gap-0.5">
          <button v-for="filter in timeFilters" :key="filter.value"
            @click="activeTimeFilter = filter.value; fetchOrders()"
            class="px-3.5 py-1.5 text-[12px] font-semibold rounded-[8px] transition-all duration-200 cursor-pointer border-none"
            :class="activeTimeFilter === filter.value
              ? 'bg-green-forest text-cream shadow-[0_2px_8px_rgba(26,92,46,0.15)]'
              : 'text-text-muted hover:text-green-forest hover:bg-green-soft'">
            {{ filter.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-[var(--radius-card)] border border-border-green-light shadow-sm overflow-hidden">

      <div v-if="isLoading" class="p-16 text-center">
        <div class="w-10 h-10 border-[3px] border-green-soft border-t-green-forest rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-sm text-text-muted font-medium">Buscando pedidos...</p>
      </div>

      <div v-else-if="orders.length === 0" class="p-16 text-center">
        <div class="w-16 h-16 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-4" style="animation:float 6s ease-in-out infinite">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/></svg>
        </div>
        <h3 class="font-display text-base font-bold text-ink mb-1">Sin pedidos</h3>
        <p class="text-sm text-text-muted">No hay pedidos para esta selección.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border-green-light bg-cream">
              <th class="text-left px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">ID</th>
              <th v-if="activeEstablishment === 'all'" class="text-left px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Local</th>
              <th class="text-left px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Fecha</th>
              <th class="text-left px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Mesa</th>
              <th class="text-left px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Estado</th>
              <th class="text-right px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Total</th>
              <th class="text-center px-6 py-3.5 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id"
              class="border-b border-border-green-light last:border-b-0 transition-colors"
              :class="newOrderIds.has(order.id) ? 'bg-green-soft animate-pulse-once' : 'hover:bg-green-soft-2'">
              <td class="px-6 py-4 font-bold text-ink font-display">
                <span v-if="newOrderIds.has(order.id)" class="inline-block w-2 h-2 bg-green-forest rounded-full mr-2" style="animation:pulse-dot 2s infinite"></span>
                #{{ order.id }}
              </td>
              <td v-if="activeEstablishment === 'all'" class="px-6 py-4 text-text-sec font-medium">{{ order.establishment_name || 'Desconocido' }}</td>
              <td class="px-6 py-4 text-text-sec">{{ formatDate(order.placed_at) }}</td>
              <td class="px-6 py-4 text-ink font-semibold font-display">{{ order.table_number || 'Barra' }}</td>
              <td class="px-6 py-4">
                <span class="badge-mm" :class="getStatusClass(order.status)">
                  <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDot(order.status)"></span>
                  {{ order.status_display || 'Desconocido' }}
                </span>
              </td>
              <td class="px-6 py-4 font-bold text-ink text-right font-display">{{ order.total }}€</td>
              <td class="px-6 py-4 text-center">
                <button @click="openOrderDetails(order)" class="btn-mm btn-ghost text-[12px] px-4 py-1.5 !text-green-forest">Ticket</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Ticket Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedOrder" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-50 p-4" @click.self="selectedOrder = null">
          <div class="bg-white rounded-[28px] shadow-[0_40px_100px_rgba(26,92,46,0.12)] w-full max-w-md overflow-hidden flex flex-col max-h-[90vh]">
            <div class="px-7 pt-7 pb-4 border-b border-border-green-light flex justify-between items-start">
              <div>
                <h3 class="font-display text-xl font-bold text-ink tracking-tight">Pedido #{{ selectedOrder.id }}</h3>
                <p class="text-[13px] text-text-muted mt-1">Mesa {{ selectedOrder.table_number }} · {{ formatDate(selectedOrder.placed_at) }}</p>
              </div>
              <button @click="selectedOrder = null" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
            <div class="px-7 py-5 overflow-y-auto flex-1">
              <div v-if="isLoadingTicket" class="py-12 text-center">
                <div class="w-8 h-8 border-[3px] border-green-soft border-t-green-forest rounded-full animate-spin mx-auto mb-3"></div>
                <p class="text-sm text-text-muted">Cargando ticket...</p>
              </div>
              <div v-else class="space-y-1">
                <div v-for="item in ticketDetails" :key="item.id" class="flex justify-between items-start py-3.5 border-b border-dashed border-border-green-light last:border-b-0">
                  <div class="pr-4">
                    <p class="font-bold text-ink"><span class="text-green-forest font-display mr-1.5">{{ item.quantity }}x</span>{{ item.product_name }}</p>
                    <p v-if="item.notes" class="text-[12px] text-warning font-semibold bg-warning-soft px-3 py-1.5 rounded-xl mt-2 border border-[rgba(196,138,26,0.15)]">{{ item.notes }}</p>
                  </div>
                  <p class="font-bold text-text-sec font-display whitespace-nowrap">{{ item.price }}€</p>
                </div>
              </div>
            </div>
            <div class="px-7 py-6 bg-cream border-t border-border-green-light">
              <div class="flex justify-between items-center mb-5">
                <span class="text-[11px] text-text-muted font-bold uppercase tracking-[0.1em]">Total</span>
                <span class="font-display text-3xl font-bold text-green-forest tracking-tight">{{ selectedOrder.total }}€</span>
              </div>
              <button @click="selectedOrder = null" class="btn-mm bg-ink text-cream w-full h-[48px] text-[14px] hover:bg-[#2a2a28]" style="box-shadow:0 4px 20px rgba(26,26,24,0.2)">Cerrar ticket</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { useFormatters } from '@/composables/useFormatters'
import { useOrderStatus } from '@/composables/useOrderStatus'
import type { OrderSummary, OrderDetailItem, EstablishmentOption, TimeFilter } from '@/interfaces/orders'

const POLLING_INTERVAL = 10_000

const { formatDate } = useFormatters()
const { getStatusClass, getStatusDot } = useOrderStatus()

const orders = ref<OrderSummary[]>([])
const myEstablishments = ref<EstablishmentOption[]>([])
const isLoading = ref(true)
const selectedOrder = ref<OrderSummary | null>(null)
const ticketDetails = ref<OrderDetailItem[]>([])
const isLoadingTicket = ref(false)
const activeTimeFilter = ref('1')
const activeEstablishment = ref<string>('all')

let pollingTimer: ReturnType<typeof setInterval> | null = null
const knownOrderIds = ref<Set<number>>(new Set())
const newOrderIds = ref<Set<number>>(new Set())
const newOrderToast = ref<string | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
let isPolling = false

const timeFilters: TimeFilter[] = [
  { label: '24h', value: '1' }, { label: '3 días', value: '3' },
  { label: '7 días', value: '7' }, { label: 'Todos', value: 'all' },
]

let audioCtx: AudioContext | null = null

const playNotificationSound = () => {
  try {
    if (!audioCtx) audioCtx = new AudioContext()
    const ctx = audioCtx

    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.connect(gain); gain.connect(ctx.destination)
    osc.frequency.value = 880; osc.type = 'sine'
    gain.gain.setValueAtTime(0.3, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5)
    osc.start(ctx.currentTime); osc.stop(ctx.currentTime + 0.5)

    const osc2 = ctx.createOscillator()
    const gain2 = ctx.createGain()
    osc2.connect(gain2); gain2.connect(ctx.destination)
    osc2.frequency.value = 1100; osc2.type = 'sine'
    gain2.gain.setValueAtTime(0.3, ctx.currentTime + 0.15)
    gain2.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.6)
    osc2.start(ctx.currentTime + 0.15); osc2.stop(ctx.currentTime + 0.6)
  } catch {}
}

const fetchMyEstablishments = async () => {
  try {
    const { data } = await makeMenuApi.get<EstablishmentOption[]>('establishments/')
    myEstablishments.value = data
  } catch {}
}

const fetchOrders = async () => {
  isLoading.value = true
  try {
    const params: Record<string, string> = {}
    if (activeTimeFilter.value !== 'all') params.days = activeTimeFilter.value
    if (activeEstablishment.value !== 'all') params.establishment_id = activeEstablishment.value
    const { data } = await makeMenuApi.get<OrderSummary[]>('orders/waiter-orders/', { params })
    orders.value = data
    knownOrderIds.value = new Set(data.map(o => o.id))
    newOrderIds.value = new Set()
  } catch {}
  finally { isLoading.value = false }
}

const pollOrders = async () => {
  if (isPolling) return
  isPolling = true
  try {
    const params: Record<string, string> = {}
    if (activeTimeFilter.value !== 'all') params.days = activeTimeFilter.value
    if (activeEstablishment.value !== 'all') params.establishment_id = activeEstablishment.value
    const { data } = await makeMenuApi.get<OrderSummary[]>('orders/waiter-orders/', { params })

    const incomingIds = new Set(data.map(o => o.id))
    const freshIds: number[] = []
    for (const id of incomingIds) {
      if (!knownOrderIds.value.has(id)) freshIds.push(id)
    }

    if (freshIds.length > 0) {
      orders.value = data
      newOrderIds.value = new Set(freshIds)
      knownOrderIds.value = incomingIds
      const newOrders = data.filter(o => freshIds.includes(o.id))
      showToast(newOrders.map(o => `#${o.id} — Mesa ${o.table_number || 'Barra'}`).join(', '))
      playNotificationSound()
      setTimeout(() => { newOrderIds.value = new Set() }, 8000)
    } else {
      orders.value = data
      knownOrderIds.value = incomingIds
    }
  } catch {}
  finally { isPolling = false }
}

const showToast = (message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  newOrderToast.value = message
  toastTimer = setTimeout(() => { newOrderToast.value = null }, 5000)
}

const openOrderDetails = async (order: OrderSummary) => {
  selectedOrder.value = order
  ticketDetails.value = []
  isLoadingTicket.value = true
  try {
    const { data } = await makeMenuApi.get<OrderDetailItem[]>(`orders/waiter-orders/${order.id}/details/`)
    ticketDetails.value = data
  } catch {}
  finally { isLoadingTicket.value = false }
}

onMounted(async () => {
  fetchMyEstablishments()
  await fetchOrders()
  pollingTimer = setInterval(pollOrders, POLLING_INTERVAL)
})

onUnmounted(() => {
  if (pollingTimer) clearInterval(pollingTimer)
  if (toastTimer) clearTimeout(toastTimer)
  if (audioCtx) { audioCtx.close(); audioCtx = null }
})
</script>

<style scoped>
.toast-right-enter-active { animation: slide-in-right 0.4s cubic-bezier(0.25,1,0.5,1); }
.toast-right-leave-active { animation: slide-out-right 0.3s ease-in; }
@keyframes slide-in-right { from { transform: translateX(120%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@keyframes slide-out-right { from { transform: translateX(0); opacity: 1; } to { transform: translateX(120%); opacity: 0; } }
@keyframes pulse-once { 0%, 100% { background-color: rgba(26,92,46,0.08); } 50% { background-color: rgba(26,92,46,0.14); } }
.animate-pulse-once { animation: pulse-once 1.5s ease-in-out 3; }
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: translateY(16px) scale(0.96); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: translateY(-8px) scale(0.97); opacity: 0; }
</style>