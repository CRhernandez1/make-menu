<template>
  <div class="space-y-6">

    <!-- 🔔 Toast de nuevo pedido -->
    <Transition name="toast">
      <div
        v-if="newOrderToast"
        class="fixed top-6 right-6 z-[60] bg-emerald-500 text-white px-6 py-4 rounded-xl shadow-2xl shadow-emerald-500/30 flex items-center gap-3 animate-bounce-in cursor-pointer"
        @click="newOrderToast = null"
      >
        <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
        </svg>
        <div>
          <p class="font-black text-sm">¡Nuevo pedido!</p>
          <p class="text-emerald-100 text-xs font-medium">{{ newOrderToast }}</p>
        </div>
      </div>
    </Transition>

    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200 flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="flex items-center gap-3">
        <h2 class="text-xl font-bold text-gray-700">Pedidos Activos</h2>
        <span class="relative flex h-3 w-3" title="Actualizando en tiempo real">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </span>
      </div>
      
      <div class="flex flex-wrap items-center gap-4">
        
        <select 
          v-model="activeEstablishment" 
          @change="fetchOrders"
          class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block p-2 outline-none cursor-pointer"
        >
          <option value="all">Todos mis locales</option>
          <option 
            v-for="est in myEstablishments" 
            :key="est.id" 
            :value="est.id"
          >
            {{ est.name }}
          </option>
        </select>

        <div class="flex bg-gray-100 p-1 rounded-lg">
          <button 
            v-for="filter in timeFilters" 
            :key="filter.value"
            @click="activeTimeFilter = filter.value; fetchOrders()"
            class="px-4 py-1.5 text-sm font-medium rounded-md transition-colors"
            :class="activeTimeFilter === filter.value ? 'bg-white text-emerald-600 shadow-sm font-bold' : 'text-gray-500 hover:text-gray-700'"
          >
            {{ filter.label }}
          </button>
        </div>

      </div>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      
      <div v-if="isLoading" class="p-12 text-center">
        <div class="animate-spin inline-block w-8 h-8 border-4 border-emerald-400 border-t-transparent rounded-full mb-4"></div>
        <p class="text-gray-500 font-medium">Buscando pedidos...</p>
      </div>
      
      <div v-else-if="orders.length === 0" class="p-12 text-center text-gray-400">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
        <p class="text-lg">No hay pedidos para esta selección.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="bg-gray-50 border-b border-gray-200 text-gray-500 uppercase text-xs font-bold tracking-wider">
            <tr>
              <th class="px-6 py-4">ID</th>
              <th v-if="activeEstablishment === 'all'" class="px-6 py-4">Local</th>
              <th class="px-6 py-4">Fecha</th>
              <th class="px-6 py-4">Mesa</th>
              <th class="px-6 py-4">Estado</th>
              <th class="px-6 py-4 text-right">Total</th>
              <th class="px-6 py-4 text-center">Acción</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr 
              v-for="order in orders" 
              :key="order.id" 
              class="transition-colors"
              :class="newOrderIds.has(order.id) ? 'bg-emerald-50 animate-pulse-once' : 'hover:bg-gray-50'"
            >
              <td class="px-6 py-4 font-bold text-gray-900">
                <span v-if="newOrderIds.has(order.id)" class="inline-block w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse"></span>
                #{{ order.id }}
              </td>
              <td v-if="activeEstablishment === 'all'" class="px-6 py-4 text-gray-600 font-medium">
                {{ order.establishment_name || 'Desconocido' }}
              </td>
              <td class="px-6 py-4 text-gray-500">{{ formatDate(order.placed_at) }}</td>
              <td class="px-6 py-4 text-gray-700 font-semibold">{{ order.table_number || 'Barra' }}</td>
              <td class="px-6 py-4">
                <span class="px-3 py-1 rounded-full text-xs font-bold shadow-sm" :class="getStatusClass(order.status)">
                  {{ order.status_display || 'Desconocido' }}
                </span>
              </td>
              <td class="px-6 py-4 font-bold text-gray-800 text-right">{{ order.total }}€</td>
              <td class="px-6 py-4 text-center">
                <button 
                  @click="openOrderDetails(order)"
                  class="text-emerald-600 hover:text-emerald-700 font-bold bg-emerald-50 hover:bg-emerald-100 px-4 py-2 rounded-lg transition-colors border border-emerald-200"
                >
                  Ticket
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="selectedOrder" class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 transition-opacity">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] border border-gray-100">
        
        <div class="p-6 border-b border-gray-100 flex justify-between items-start bg-gray-50">
          <div>
            <h3 class="text-xl font-black text-gray-800">Pedido #{{ selectedOrder.id }}</h3>
            <p class="text-sm text-gray-500 mt-1 font-medium">Mesa {{ selectedOrder.table_number }} • {{ formatDate(selectedOrder.placed_at) }}</p>
          </div>
          <button @click="selectedOrder = null" class="text-gray-400 hover:text-red-500 transition-colors bg-white p-1 rounded-full shadow-sm">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div class="p-6 overflow-y-auto flex-1 bg-white">
          
          <div v-if="isLoadingTicket" class="py-12 text-center">
             <div class="animate-spin inline-block w-8 h-8 border-4 border-emerald-400 border-t-transparent rounded-full mb-4"></div>
             <p class="text-gray-500 font-medium">Cargando ticket...</p>
          </div>

          <ul v-else class="divide-y divide-dashed divide-gray-200">
            <li v-for="item in selectedOrder.details" :key="item.id" class="py-4 flex justify-between items-start">
              <div class="pr-4">
                <p class="font-bold text-gray-800 text-lg">
                  <span class="text-emerald-500 mr-2">{{ item.quantity }}x</span>{{ item.product_name }}
                </p>
                <p v-if="item.notes" class="text-sm text-amber-600 bg-amber-50 p-2 rounded mt-2 border border-amber-100">
                  <span class="font-bold">Nota:</span> {{ item.notes }}
                </p>
              </div>
              <p class="font-bold text-gray-600 whitespace-nowrap">{{ item.price }}€</p>
            </li>
          </ul>
        </div>

        <div class="p-6 bg-gray-50 border-t border-gray-100 shadow-[0_-10px_20px_-10px_rgba(0,0,0,0.05)]">
          <div class="flex justify-between items-center mb-6">
            <span class="text-gray-500 font-bold uppercase tracking-wider text-sm">Total</span>
            <span class="text-3xl font-black text-emerald-500">{{ selectedOrder.total }}€</span>
          </div>
          <button @click="selectedOrder = null" class="w-full bg-gray-800 text-white font-bold py-3.5 rounded-xl hover:bg-gray-900 transition-colors shadow-lg shadow-gray-200">
            Cerrar Ticket
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'

const POLLING_INTERVAL = 10_000 // 10 segundos

// --- ESTADOS ---
const orders = ref<any[]>([])
const myEstablishments = ref<any[]>([])
const isLoading = ref(true)

const selectedOrder = ref<any | null>(null)
const isLoadingTicket = ref(false)

const activeTimeFilter = ref('1')
const activeEstablishment = ref('all')

// Polling y notificaciones
let pollingTimer: ReturnType<typeof setInterval> | null = null
const knownOrderIds = ref<Set<number>>(new Set())
const newOrderIds = ref<Set<number>>(new Set())
const newOrderToast = ref<string | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null

const timeFilters = [
  { label: '24 Horas', value: '1' },
  { label: '3 Días', value: '3' },
  { label: '7 Días', value: '7' },
  { label: 'Todos', value: 'all' },
]

// --- SONIDO DE NOTIFICACIÓN ---
const playNotificationSound = () => {
  try {
    const ctx = new AudioContext()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.connect(gain)
    gain.connect(ctx.destination)

    osc.frequency.value = 880
    osc.type = 'sine'
    gain.gain.setValueAtTime(0.3, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5)

    osc.start(ctx.currentTime)
    osc.stop(ctx.currentTime + 0.5)

    // Segundo tono más agudo
    const osc2 = ctx.createOscillator()
    const gain2 = ctx.createGain()
    osc2.connect(gain2)
    gain2.connect(ctx.destination)
    osc2.frequency.value = 1100
    osc2.type = 'sine'
    gain2.gain.setValueAtTime(0.3, ctx.currentTime + 0.15)
    gain2.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.6)
    osc2.start(ctx.currentTime + 0.15)
    osc2.stop(ctx.currentTime + 0.6)
  } catch {
    // Audio no disponible, ignorar
  }
}

// --- LÓGICA DE API ---

const fetchMyEstablishments = async () => {
  try {
    const { data } = await makeMenuApi.get('establishments/')
    myEstablishments.value = data
  } catch (error) {
    console.error("Error cargando los locales:", error)
  }
}

const fetchOrders = async () => {
  isLoading.value = true
  try {
    const params: any = {}
    if (activeTimeFilter.value !== 'all') params.days = activeTimeFilter.value
    if (activeEstablishment.value !== 'all') params.establishment_id = activeEstablishment.value

    const { data } = await makeMenuApi.get('orders/waiter-orders/', { params })
    orders.value = data

    // Inicializar IDs conocidos en la primera carga
    knownOrderIds.value = new Set(data.map((o: any) => o.id))
    newOrderIds.value = new Set()
  } catch (error) {
    console.error("Error al cargar la lista de pedidos:", error)
  } finally {
    isLoading.value = false
  }
}

/** Polling silencioso: no muestra el spinner, solo compara IDs */
const pollOrders = async () => {
  try {
    const params: any = {}
    if (activeTimeFilter.value !== 'all') params.days = activeTimeFilter.value
    if (activeEstablishment.value !== 'all') params.establishment_id = activeEstablishment.value

    const { data } = await makeMenuApi.get('orders/waiter-orders/', { params })
    
    // Detectar pedidos nuevos
    const incomingIds = new Set(data.map((o: any) => o.id))
    const freshIds: number[] = []

    for (const id of incomingIds) {
      if (!knownOrderIds.value.has(id)) {
        freshIds.push(id)
      }
    }

    if (freshIds.length > 0) {
      // Actualizar la lista y marcar los nuevos
      orders.value = data
      newOrderIds.value = new Set(freshIds)
      knownOrderIds.value = incomingIds

      // Mostrar toast
      const newOrders = data.filter((o: any) => freshIds.includes(o.id))
      const toastText = newOrders
        .map((o: any) => `#${o.id} — Mesa ${o.table_number || 'Barra'}`)
        .join(', ')
      showToast(toastText)
      playNotificationSound()

      // Quitar highlight después de 8 segundos
      setTimeout(() => {
        newOrderIds.value = new Set()
      }, 8000)
    } else {
      // Actualizar datos silenciosamente (por si cambió algún estado)
      orders.value = data
      knownOrderIds.value = incomingIds
    }
  } catch (error) {
    console.error("Error en polling:", error)
  }
}

const showToast = (message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  newOrderToast.value = message
  toastTimer = setTimeout(() => {
    newOrderToast.value = null
  }, 5000)
}

const startPolling = () => {
  stopPolling()
  pollingTimer = setInterval(pollOrders, POLLING_INTERVAL)
}

const stopPolling = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
}

const openOrderDetails = async (order: any) => {
  selectedOrder.value = { ...order, details: [] }
  isLoadingTicket.value = true
  
  try {
    const { data } = await makeMenuApi.get(`orders/waiter-orders/${order.id}/details/`)
    selectedOrder.value.details = data
  } catch (error) {
    console.error("Error cargando los platos del ticket:", error)
  } finally {
    isLoadingTicket.value = false
  }
}

// --- UTILIDADES ---

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('es-ES', { 
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' 
  }).format(date)
}

const getStatusClass = (status: number) => {
  switch(status) {
    case -1: return 'bg-red-100 text-red-700 border border-red-200'
    case 1: return 'bg-amber-100 text-amber-700 border border-amber-200'
    case 2: return 'bg-blue-100 text-blue-700 border border-blue-200'
    case 3: return 'bg-emerald-100 text-emerald-700 border border-emerald-200'
    default: return 'bg-gray-100 text-gray-700 border border-gray-200'
  }
}

// --- CICLO DE VIDA ---
onMounted(async () => {
  fetchMyEstablishments()
  await fetchOrders()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
  if (toastTimer) clearTimeout(toastTimer)
})
</script>

<style scoped>
/* Animación de entrada del toast */
.toast-enter-active {
  animation: slide-in-right 0.4s ease-out;
}
.toast-leave-active {
  animation: slide-out-right 0.3s ease-in;
}

@keyframes slide-in-right {
  from { transform: translateX(120%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
@keyframes slide-out-right {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(120%); opacity: 0; }
}

/* Pulso suave para filas nuevas */
@keyframes pulse-once {
  0%, 100% { background-color: rgb(236 253 245); }
  50%      { background-color: rgb(209 250 229); }
}
.animate-pulse-once {
  animation: pulse-once 1.5s ease-in-out 3;
}
</style>
