<template>
  <div class="px-6 py-6 lg:px-10 lg:py-8">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Mesas</h1>
        <p class="text-sm text-gray-400 mt-0.5">{{ store.establishmentName }}</p>
      </div>
      <button
        @click="store.fetchTables()"
        class="p-2.5 rounded-xl bg-white border border-gray-200 text-gray-400 hover:text-emerald-500 hover:border-emerald-300 transition-all"
        title="Actualizar"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
        </svg>
      </button>
    </div>

    <!-- Leyenda -->
    <div class="flex flex-wrap gap-4 mb-5 text-xs text-gray-400">
      <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-gray-200"></span> Libre</span>
      <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-400"></span> Pendiente</span>
      <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-400"></span> En progreso</span>
      <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-emerald-400"></span> Listo</span>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 bg-red-50 text-red-600 border border-red-100">
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError()" class="text-red-300 hover:text-red-500">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <div v-for="n in 8" :key="n" class="h-36 rounded-2xl bg-gray-100 animate-pulse"></div>
    </div>

    <!-- Grid mesas -->
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <div
        v-for="table in store.tables"
        :key="table.number"
        @click="openTable(table)"
        class="relative rounded-2xl border-2 p-5 cursor-pointer transition-all hover:shadow-md"
        :class="tableCardClass(table.status)"
      >
        <div class="absolute top-3 right-3">
          <span class="w-3 h-3 rounded-full block" :class="dotClass(table.status)"></span>
        </div>

        <div class="text-center">
          <span class="text-3xl font-bold" :class="numberClass(table.status)">
            {{ String(table.number).padStart(2, '0') }}
          </span>
          <p class="text-xs text-gray-400 mt-1">{{ table.max_guests }} personas</p>
        </div>

        <div v-if="table.order" class="mt-3 pt-3 border-t text-center" :class="borderClass(table.status)">
          <p class="text-xs font-medium" :class="statusTextClass(table.status)">{{ table.order.status_display }}</p>
          <p class="text-sm font-bold mt-0.5" :class="numberClass(table.status)">{{ table.order.total }}€</p>
          <p class="text-[10px] text-gray-400 mt-0.5">{{ table.order.items_count }} productos</p>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div
        v-if="toast"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-3 px-5 py-3 rounded-xl text-sm shadow-lg border z-50"
        :class="toast.type === 'success' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200'"
      >
        <span>{{ toast.message }}</span>
        <button @click="toast = null" class="text-current opacity-50 hover:opacity-100">&times;</button>
      </div>
    </Transition>

    <!-- Modal detalle mesa -->
    <Teleport to="body">
      <div v-if="selectedTable" class="fixed inset-0 bg-black/40 flex items-end sm:items-center justify-center z-50 p-4" @click.self="selectedTable = null">
        <div class="bg-white rounded-2xl w-full max-w-md max-h-[85vh] overflow-y-auto">

          <div class="flex items-center justify-between p-5 border-b border-gray-100">
            <div>
              <h3 class="text-lg font-bold text-gray-800">Mesa {{ String(selectedTable.number).padStart(2, '0') }}</h3>
              <p class="text-sm text-gray-400">{{ selectedTable.max_guests }} personas</p>
            </div>
            <button @click="selectedTable = null" class="text-gray-300 hover:text-gray-500 p-1">
              <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- Sin pedido -->
          <div v-if="!orderDetail" class="p-8 text-center text-gray-400">
            <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            </div>
            <p class="font-medium">Mesa libre</p>
            <p class="text-sm mt-1">Esperando pedido del cliente</p>
          </div>

          <!-- Con pedido -->
          <div v-else class="p-5 space-y-4">

            <div class="flex items-center justify-between">
              <span
                class="text-xs font-semibold px-3 py-1.5 rounded-full"
                :class="orderStatusClass(orderDetail.status)"
              >
                {{ orderDetail.status_display }}
              </span>
              <span class="text-xs text-gray-400">{{ formatTime(orderDetail.placed_at) }}</span>
            </div>

            <div class="space-y-2">
              <div
                v-for="item in orderDetail.items"
                :key="item.id"
                class="flex items-start justify-between gap-3 p-3 bg-gray-50 rounded-xl"
              >
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-semibold text-gray-800">{{ item.quantity }}x {{ item.product_name }}</p>
                  <p v-if="item.notes" class="text-xs text-amber-600 mt-0.5">{{ item.notes }}</p>
                </div>
                <span class="text-sm font-medium text-gray-600 shrink-0">
                  {{ (parseFloat(item.price) * item.quantity).toFixed(2) }}€
                </span>
              </div>
            </div>

            <div class="flex justify-between items-center pt-3 border-t border-gray-200">
              <span class="text-gray-500 font-medium">Total</span>
              <span class="text-xl font-bold text-gray-800">{{ orderDetail.total }}€</span>
            </div>

            <div class="flex gap-3 pt-2">
              <button
                v-if="orderDetail.status === 1 || orderDetail.status === 2"
                @click="handleCancel(orderDetail.id)"
                class="flex-1 py-3 rounded-xl border border-red-200 text-red-500 text-sm font-semibold hover:bg-red-50 transition-colors"
              >
                Cancelar
              </button>

              <button
                v-if="orderDetail.status === 1"
                @click="handleAdvance(orderDetail.id)"
                class="flex-1 py-3 rounded-xl bg-amber-500 text-white text-sm font-semibold hover:bg-amber-600 transition-colors"
              >
                En preparación
              </button>

              <button
                v-if="orderDetail.status === 2"
                @click="handleAdvance(orderDetail.id)"
                class="flex-1 py-3 rounded-xl bg-emerald-500 text-white text-sm font-semibold hover:bg-emerald-600 transition-colors"
              >
                Marcar listo
              </button>

              <button
                v-if="orderDetail.status === 3"
                @click="handleClose(selectedTable!.number)"
                class="flex-1 py-3 rounded-xl bg-blue-500 text-white text-sm font-semibold hover:bg-blue-600 transition-colors"
              >
                Cobrar {{ orderDetail.total }}€
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useWaiterStore } from '../stores/waiter.store'
import type { TableInfo, OrderDetail } from '../stores/waiter.store'

const store = useWaiterStore()

// Toast
interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 4000)
}

// Mesa seleccionada
const selectedTable = ref<TableInfo | null>(null)
const orderDetail = ref<OrderDetail | null>(null)

const openTable = async (table: TableInfo) => {
  selectedTable.value = table
  orderDetail.value = null
  if (table.order) {
    orderDetail.value = await store.fetchOrderDetail(table.number)
  }
}

const handleAdvance = async (orderId: number) => {
  const result = await store.advanceOrder(orderId)
  showToast(result.ok ? 'success' : 'error', result.ok ? result.message! : result.error!)
  if (result.ok && selectedTable.value) {
    orderDetail.value = await store.fetchOrderDetail(selectedTable.value.number)
  }
}

const handleCancel = async (orderId: number) => {
  const result = await store.cancelOrder(orderId)
  showToast(result.ok ? 'success' : 'error', result.ok ? result.message! : result.error!)
  if (result.ok) {
    selectedTable.value = null
    orderDetail.value = null
  }
}

const handleClose = async (tableNum: number) => {
  const result = await store.closeTable(tableNum)
  showToast(result.ok ? 'success' : 'error', result.ok ? result.message! : result.error!)
  if (result.ok) {
    selectedTable.value = null
    orderDetail.value = null
  }
}

// Helpers
const formatTime = (iso: string) => {
  return new Date(iso).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const tableCardClass = (status: string) => {
  switch (status) {
    case 'pending': return 'border-amber-300 bg-amber-50/50'
    case 'in_progress': return 'border-blue-300 bg-blue-50/50'
    case 'done': return 'border-emerald-300 bg-emerald-50/50'
    default: return 'border-gray-200 bg-white'
  }
}

const dotClass = (status: string) => {
  switch (status) {
    case 'pending': return 'bg-amber-400 animate-pulse'
    case 'in_progress': return 'bg-blue-400'
    case 'done': return 'bg-emerald-400'
    default: return 'bg-gray-200'
  }
}

const numberClass = (status: string) => {
  switch (status) {
    case 'pending': return 'text-amber-600'
    case 'in_progress': return 'text-blue-600'
    case 'done': return 'text-emerald-600'
    default: return 'text-gray-300'
  }
}

const statusTextClass = (status: string) => {
  switch (status) {
    case 'pending': return 'text-amber-500'
    case 'in_progress': return 'text-blue-500'
    case 'done': return 'text-emerald-500'
    default: return 'text-gray-400'
  }
}

const borderClass = (status: string) => {
  switch (status) {
    case 'pending': return 'border-amber-200'
    case 'in_progress': return 'border-blue-200'
    case 'done': return 'border-emerald-200'
    default: return 'border-gray-100'
  }
}

const orderStatusClass = (status: number) => {
  switch (status) {
    case 1: return 'bg-amber-50 text-amber-600'
    case 2: return 'bg-blue-50 text-blue-600'
    case 3: return 'bg-emerald-50 text-emerald-600'
    default: return 'bg-gray-50 text-gray-400'
  }
}

// Auto-refresh cada 30 segundos
let refreshInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  store.fetchTables()
  refreshInterval = setInterval(() => store.fetchTables(), 30000)
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