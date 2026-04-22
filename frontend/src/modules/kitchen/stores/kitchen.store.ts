import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'

export interface OrderItem {
  id: number
  product_name: string
  quantity: number
  notes: string
  ready: boolean
}

export interface KitchenOrder {
  id: number
  status: number
  status_display: string
  table_number: number
  placed_at: string
  total: string
  ready_count: number
  total_count: number
  items: OrderItem[]
}

export interface ActionResult {
  ok: boolean
  error?: string
  message?: string
  order_done?: boolean
}

function extractError(err: unknown, fallback: string): string {
  if (isAxiosError(err) && err.response?.data) {
    return err.response.data.error || err.response.data.message || fallback
  }
  return fallback
}

export const useKitchenStore = defineStore('kitchen', () => {
  const establishmentName = ref('')
  const orders = ref<KitchenOrder[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const clearError = () => { error.value = null }

  const fetchOrders = async () => {
    loading.value = true
    error.value = null
    try {
      const { data } = await makeMenuApi.get('/orders/kitchen/orders/')
      establishmentName.value = data.establishment
      orders.value = data.orders
    } catch (err) {
      error.value = extractError(err, 'Error cargando pedidos.')
    } finally {
      loading.value = false
    }
  }

  const advanceOrder = async (orderId: number): Promise<ActionResult> => {
    try {
      const { data } = await makeMenuApi.post(`/orders/kitchen/orders/${orderId}/advance/`)
      await fetchOrders()
      return { ok: true, message: data.message }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Error actualizando pedido.') }
    }
  }

  const toggleItem = async (itemId: number): Promise<ActionResult> => {
    try {
      const { data } = await makeMenuApi.post(`/orders/kitchen/items/${itemId}/toggle/`)
      await fetchOrders()
      return { ok: true, message: data.message, order_done: data.order_done }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Error actualizando plato.') }
    }
  }

  return {
    establishmentName, orders, loading, error,
    clearError, fetchOrders, advanceOrder, toggleItem
  }
})