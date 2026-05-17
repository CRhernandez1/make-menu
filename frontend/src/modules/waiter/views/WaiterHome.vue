<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="font-display text-2xl font-bold text-green-forest tracking-tight">Mesas</h1>
        <p class="text-sm text-text-muted mt-0.5">{{ store.establishmentName }}</p>
      </div>
      <button @click="store.fetchTables()" class="w-10 h-10 rounded-[14px] bg-white border border-border-green text-text-muted flex items-center justify-center cursor-pointer hover:bg-green-soft hover:text-green-forest hover:border-[rgba(26,92,46,0.2)] transition-all" title="Actualizar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
      </button>
    </div>

    <!-- Leyenda -->
    <div class="flex flex-wrap gap-5 mb-6 text-xs text-text-muted">
      <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-text-ghost"></span> Libre</span>
      <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-warning" style="animation:pulse-dot 2s infinite"></span> Pendiente</span>
      <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-green-medium"></span> En progreso</span>
      <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-green-forest"></span> Listo</span>
      <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-danger" style="animation:ring-pulse 1.5s infinite"></span> +15 min</span>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="alert-mm bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] text-danger mb-5">
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError()" class="text-danger/40 hover:text-danger/80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <div v-for="n in 10" :key="n" class="h-36 rounded-[var(--radius-card)] skeleton-mm"></div>
    </div>

    <!-- Grid mesas -->
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <div
        v-for="table in store.tables" :key="table.number"
        @click="openTable(table)"
        class="relative rounded-[var(--radius-card)] border-2 p-5 cursor-pointer transition-all duration-300 hover:shadow-md hover:-translate-y-1"
        :class="tableCardClass(table)"
      >
        <div class="absolute top-3.5 right-3.5">
          <span class="w-2.5 h-2.5 rounded-full block" :class="dotClass(table)"></span>
        </div>
        <div class="text-center">
          <span class="font-display text-[32px] font-bold tracking-tight" :class="numberClass(table.status)">
            {{ String(table.number).padStart(2, '0') }}
          </span>
          <p class="text-[11px] text-text-muted mt-1">{{ table.max_guests }} pers.</p>
        </div>
        <div v-if="table.order" class="mt-3 pt-3 border-t text-center" :class="borderClass(table.status)">
          <p class="text-[11px] font-semibold" :class="statusTextClass(table.status)">{{ table.order.status_display }}</p>
          <p class="font-display text-[17px] font-bold mt-0.5" :class="numberClass(table.status)">{{ table.order.total }}€</p>
          <p class="text-[10px] text-text-muted mt-0.5">{{ table.order.items_count }} productos</p>
          <p v-if="isUrgent(table.order.placed_at)" class="text-[10px] font-semibold text-danger mt-1">{{ elapsedTime(table.order.placed_at) }}</p>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="localToast.toast.value" class="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-3 px-5 py-3 rounded-full text-sm shadow-lg z-50"
        :class="localToast.toast.value.type === 'success' ? 'bg-green-forest text-cream' : 'bg-danger text-white'">
        <svg v-if="localToast.toast.value.type === 'success'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        <span class="font-semibold">{{ localToast.toast.value.message }}</span>
      </div>
    </Transition>

    <!-- Modal detalle mesa -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedTable" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-end sm:items-center justify-center z-50 p-4" @click.self="selectedTable = null">
          <div class="bg-white rounded-[28px] w-full max-w-md max-h-[85vh] overflow-y-auto shadow-[0_40px_100px_rgba(26,92,46,0.12)]">

            <div class="flex items-center justify-between px-7 pt-7 pb-4 border-b border-border-green-light">
              <div>
                <h3 class="font-display text-lg font-bold text-ink tracking-tight">Mesa {{ String(selectedTable.number).padStart(2, '0') }}</h3>
                <p class="text-[13px] text-text-muted">{{ selectedTable.max_guests }} personas</p>
              </div>
              <button @click="selectedTable = null" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <!-- Sin pedido -->
            <div v-if="!orderDetail" class="p-10 text-center">
              <div class="w-16 h-16 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-4" style="animation:float 6s ease-in-out infinite">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
              </div>
              <h3 class="font-display text-base font-bold text-ink mb-1">Mesa libre</h3>
              <p class="text-sm text-text-muted">Esperando pedido del cliente</p>
            </div>

            <!-- Con pedido -->
            <div v-else class="px-7 py-5 space-y-4">
              <div class="flex items-center justify-between">
                <span class="badge-mm" :class="orderBadgeClass(orderDetail.status)">
                  <span class="w-1.5 h-1.5 rounded-full" :class="orderDotClass(orderDetail.status)"></span>
                  {{ orderDetail.status_display }}
                </span>
                <span class="text-xs text-text-muted">{{ formatTime(orderDetail.placed_at) }}</span>
              </div>

              <div class="space-y-2">
                <div v-for="item in orderDetail.items" :key="item.id" class="flex items-start justify-between gap-3 p-3.5 bg-cream rounded-2xl">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-ink"><span class="text-green-forest font-display mr-1">{{ item.quantity }}x</span> {{ item.product_name }}</p>
                    <p v-if="item.notes" class="text-xs text-warning font-semibold mt-1">{{ item.notes }}</p>
                  </div>
                  <span class="text-sm font-semibold text-text-sec font-display shrink-0">{{ (parseFloat(item.price) * item.quantity).toFixed(2) }}€</span>
                </div>
              </div>

              <div class="flex justify-between items-center pt-4 border-t border-border-green-light">
                <span class="text-text-sec font-medium">Total</span>
                <span class="font-display text-xl font-bold text-ink">{{ orderDetail.total }}€</span>
              </div>

              <div class="flex gap-3 pt-2">
                <button v-if="orderDetail.status === 1 || orderDetail.status === 2" @click="handleCancel(orderDetail.id)"
                  class="btn-mm btn-ghost flex-1 text-[13px] py-3 !text-danger hover:!bg-danger-soft">Cancelar</button>
                <button v-if="orderDetail.status === 1" @click="handleAdvance(orderDetail.id)"
                  class="btn-mm flex-1 text-[13px] py-3 bg-warning text-white" style="box-shadow:0 4px 16px rgba(196,138,26,0.25)">En preparación</button>
                <button v-if="orderDetail.status === 2" @click="handleAdvance(orderDetail.id)"
                  class="btn-mm btn-primary flex-1 text-[13px] py-3">Marcar listo</button>
                <button v-if="orderDetail.status === 3" @click="handleClose(selectedTable!.number)"
                  class="btn-mm flex-1 text-[13px] py-3 bg-ink text-cream" style="box-shadow:0 4px 20px rgba(26,26,24,0.2)">Cobrar {{ orderDetail.total }}€</button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useWaiterStore } from '../stores/waiter.store'
import { useFormatters } from '@/composables/useFormatters'
import { useLocalToast } from '@/composables/useLocalToast'
import type { TableInfo, OrderDetail } from '../stores/waiter.store'

const store = useWaiterStore()
const { formatTime, elapsedTime, isUrgent } = useFormatters()
const localToast = useLocalToast()

const selectedTable = ref<TableInfo | null>(null)
const orderDetail = ref<OrderDetail | null>(null)

const openTable = async (table: TableInfo) => {
  selectedTable.value = table; orderDetail.value = null
  if (table.order) { orderDetail.value = await store.fetchOrderDetail(table.number) }
}

const handleAdvance = async (orderId: number) => {
  const result = await store.advanceOrder(orderId)
  localToast.show(result.ok ? 'success' : 'error', result.ok ? result.message! : result.error!)
  if (result.ok && selectedTable.value) { orderDetail.value = await store.fetchOrderDetail(selectedTable.value.number) }
}
const handleCancel = async (orderId: number) => {
  const result = await store.cancelOrder(orderId)
  localToast.show(result.ok ? 'success' : 'error', result.ok ? result.message! : result.error!)
  if (result.ok) { selectedTable.value = null; orderDetail.value = null }
}
const handleClose = async (tableNum: number) => {
  const result = await store.closeTable(tableNum)
  localToast.show(result.ok ? 'success' : 'error', result.ok ? result.message! : result.error!)
  if (result.ok) { selectedTable.value = null; orderDetail.value = null }
}

const tableCardClass = (table: TableInfo) => {
  if (table.order && isUrgent(table.order.placed_at)) return 'border-[rgba(185,60,60,0.3)] bg-[rgba(185,60,60,0.04)]'
  switch (table.status) {
    case 'pending': return 'border-[rgba(196,138,26,0.3)] bg-warning-soft'
    case 'in_progress': return 'border-[rgba(26,92,46,0.2)] bg-green-soft'
    case 'done': return 'border-[rgba(26,92,46,0.3)] bg-[rgba(26,92,46,0.06)]'
    default: return 'border-border-green bg-white'
  }
}
const dotClass = (table: TableInfo) => {
  if (table.order && isUrgent(table.order.placed_at)) return 'bg-danger'
  switch (table.status) {
    case 'pending': return 'bg-warning'
    case 'in_progress': return 'bg-green-medium'
    case 'done': return 'bg-green-forest'
    default: return 'bg-text-ghost'
  }
}
const numberClass = (status: string) => {
  switch (status) { case 'pending': return 'text-warning'; case 'in_progress': return 'text-green-medium'; case 'done': return 'text-green-forest'; default: return 'text-text-ghost' }
}
const statusTextClass = (status: string) => {
  switch (status) { case 'pending': return 'text-warning'; case 'in_progress': return 'text-green-medium'; case 'done': return 'text-green-forest'; default: return 'text-text-muted' }
}
const borderClass = (status: string) => {
  switch (status) { case 'pending': return 'border-[rgba(196,138,26,0.15)]'; case 'in_progress': return 'border-[rgba(26,92,46,0.1)]'; case 'done': return 'border-[rgba(26,92,46,0.15)]'; default: return 'border-border-green-light' }
}
const orderBadgeClass = (status: number) => {
  switch (status) { case 1: return 'bg-warning-soft text-warning'; case 2: return 'bg-info-soft text-info'; case 3: return 'bg-green-soft text-green-forest'; default: return 'bg-cream-dark text-text-muted' }
}
const orderDotClass = (status: number) => {
  switch (status) { case 1: return 'bg-warning'; case 2: return 'bg-info'; case 3: return 'bg-green-bright'; default: return 'bg-text-ghost' }
}

let refreshInterval: ReturnType<typeof setInterval> | null = null
onMounted(() => { store.fetchTables(); refreshInterval = setInterval(() => store.fetchTables(), 10000) })
onUnmounted(() => { if (refreshInterval) clearInterval(refreshInterval) })
</script>

<style scoped>
.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(20px) translateX(-50%); }
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: translateY(16px) scale(0.96); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: translateY(-8px) scale(0.97); opacity: 0; }
</style>