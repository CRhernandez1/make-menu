<template>
  <div class="space-y-6">

    <!-- Header + Filters -->
    <div class="card-mm p-5 !cursor-default !transform-none flex flex-col md:flex-row gap-4 items-center justify-between">
      <h2 class="font-display text-xl font-bold text-green-forest tracking-tight">Historial de pedidos</h2>

      <div class="flex flex-wrap items-center gap-3">
        <select
          v-model="activeEstablishment"
          @change="fetchOrders"
          class="input-mm !w-auto !h-10 pr-10 cursor-pointer text-[13px]"
        >
          <option value="all">Todos mis locales</option>
          <option v-for="est in myEstablishments" :key="est.id" :value="est.id">{{ est.name }}</option>
        </select>

        <div class="inline-flex bg-cream border border-border-green rounded-[12px] p-1 gap-0.5">
          <button
            v-for="filter in timeFilters" :key="filter.value"
            @click="activeTimeFilter = filter.value; fetchOrders()"
            class="px-3.5 py-1.5 text-[12px] font-semibold rounded-[8px] transition-all duration-200 cursor-pointer border-none"
            :class="activeTimeFilter === filter.value
              ? 'bg-green-forest text-cream shadow-[0_2px_8px_rgba(26,92,46,0.15)]'
              : 'text-text-muted hover:text-green-forest hover:bg-green-soft'"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-[var(--radius-card)] border border-border-green-light shadow-sm overflow-hidden">

      <!-- Loading -->
      <div v-if="isLoading" class="p-16 text-center">
        <div class="w-10 h-10 border-[3px] border-green-soft border-t-green-forest rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-sm text-text-muted font-medium">Buscando pedidos...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="orders.length === 0" class="p-16 text-center">
        <div class="w-16 h-16 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-4" style="animation:float 6s ease-in-out infinite">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/></svg>
        </div>
        <h3 class="font-display text-base font-bold text-ink mb-1">Sin pedidos</h3>
        <p class="text-sm text-text-muted">No hay pedidos para esta selección.</p>
      </div>

      <!-- Data -->
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
            <tr v-for="order in orders" :key="order.id" class="border-b border-border-green-light last:border-b-0 hover:bg-green-soft-2 transition-colors">
              <td class="px-6 py-4 font-bold text-ink font-display">#{{ order.id }}</td>
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
                <button @click="openOrderDetails(order)" class="btn-mm btn-ghost text-[12px] px-4 py-1.5 !text-green-forest">
                  Ticket
                </button>
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

            <!-- Header -->
            <div class="px-7 pt-7 pb-4 border-b border-border-green-light flex justify-between items-start">
              <div>
                <h3 class="font-display text-xl font-bold text-ink tracking-tight">Pedido #{{ selectedOrder.id }}</h3>
                <p class="text-[13px] text-text-muted mt-1">Mesa {{ selectedOrder.table_number }} · {{ formatDate(selectedOrder.placed_at) }}</p>
              </div>
              <button @click="selectedOrder = null" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <!-- Items -->
            <div class="px-7 py-5 overflow-y-auto flex-1">
              <div v-if="isLoadingTicket" class="py-12 text-center">
                <div class="w-8 h-8 border-[3px] border-green-soft border-t-green-forest rounded-full animate-spin mx-auto mb-3"></div>
                <p class="text-sm text-text-muted">Cargando ticket...</p>
              </div>

              <div v-else class="space-y-1">
                <div v-for="item in ticketDetails" :key="item.id" class="flex justify-between items-start py-3.5 border-b border-dashed border-border-green-light last:border-b-0">
                  <div class="pr-4">
                    <p class="font-bold text-ink">
                      <span class="text-green-forest font-display mr-1.5">{{ item.quantity }}x</span>{{ item.product_name }}
                    </p>
                    <p v-if="item.notes" class="text-[12px] text-warning font-semibold bg-warning-soft px-3 py-1.5 rounded-xl mt-2 border border-[rgba(196,138,26,0.15)]">
                      {{ item.notes }}
                    </p>
                  </div>
                  <p class="font-bold text-text-sec font-display whitespace-nowrap">{{ item.price }}€</p>
                </div>
              </div>
            </div>

            <!-- Footer -->
            <div class="px-7 py-6 bg-cream border-t border-border-green-light">
              <div class="flex justify-between items-center mb-5">
                <span class="text-[11px] text-text-muted font-bold uppercase tracking-[0.1em]">Total cobrado</span>
                <span class="font-display text-3xl font-bold text-green-forest tracking-tight">{{ selectedOrder.total }}€</span>
              </div>
              <button @click="selectedOrder = null" class="btn-mm bg-ink text-cream w-full h-[48px] text-[14px] hover:bg-[#2a2a28]" style="box-shadow:0 4px 20px rgba(26,26,24,0.2)">
                Cerrar ticket
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { useFormatters } from '@/composables/useFormatters'
import { useOrderStatus } from '@/composables/useOrderStatus'
import type { OrderSummary, OrderDetailItem, EstablishmentOption, TimeFilter } from '@/interfaces/orders'

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

const timeFilters: TimeFilter[] = [
  { label: '24h', value: '1' },
  { label: '3 días', value: '3' },
  { label: '7 días', value: '7' },
  { label: 'Todos', value: 'all' },
]

const fetchMyEstablishments = async () => {
  try {
    const { data } = await makeMenuApi.get<EstablishmentOption[]>('establishments/')
    myEstablishments.value = data
  } catch {
    // El interceptor global maneja 401; otros errores no bloquean la UI
  }
}

const fetchOrders = async () => {
  isLoading.value = true
  try {
    const params: Record<string, string> = {}
    if (activeTimeFilter.value !== 'all') params.days = activeTimeFilter.value
    if (activeEstablishment.value !== 'all') params.establishment_id = activeEstablishment.value
    const { data } = await makeMenuApi.get<OrderSummary[]>('orders/manager-orders/', { params })
    orders.value = data
  } catch {
    // El interceptor global maneja 401
  } finally {
    isLoading.value = false
  }
}

const openOrderDetails = async (order: OrderSummary) => {
  selectedOrder.value = order
  ticketDetails.value = []
  isLoadingTicket.value = true
  try {
    const { data } = await makeMenuApi.get<OrderDetailItem[]>(`orders/manager-orders/${order.id}/details/`)
    ticketDetails.value = data
  } catch {
    // El interceptor global maneja 401
  } finally {
    isLoadingTicket.value = false
  }
}

onMounted(() => { fetchMyEstablishments(); fetchOrders() })
</script>

<style scoped>
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: translateY(16px) scale(0.96); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: translateY(-8px) scale(0.97); opacity: 0; }
</style>