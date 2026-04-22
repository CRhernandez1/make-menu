import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'

export interface TableInfo {
  number: number
  max_guests: number
  status: 'free' | 'pending' | 'in_progress' | 'done'
  order: {
    id: number
    status: number
    status_display: string
    total: string
    items_count: number
    placed_at: string
  } | null
}

export interface OrderItem {
  id: number
  product_name: string
  price: string
  quantity: number
  notes: string
}

export interface OrderDetail {
  id: number
  status: number
  status_display: string
  table_number: number
  placed_at: string
  total: string
  paid: boolean
  items: OrderItem[]
}

export interface ActionResult {
  ok: boolean
  error?: string
  message?: string
}

function extractError(err: unknown, fallback: string): string {
  if (isAxiosError(err) && err.response?.data) {
    return err.response.data.error || err.response.data.message || fallback
  }
  return fallback
}

export const useWaiterStore = defineStore('waiter', () => {
  const establishmentName = ref('')
  const tables = ref<TableInfo[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const clearError = () => { error.value = null }

  const fetchTables = async () => {
    loading.value = true
    error.value = null
    try {
      const { data } = await makeMenuApi.get('/orders/waiter/tables/')
      establishmentName.value = data.establishment
      tables.value = data.tables
    } catch (err) {
      error.value = extractError(err, 'Error cargando mesas.')
    } finally {
      loading.value = false
    }
  }

  const fetchOrderDetail = async (tableNum: number): Promise<OrderDetail | null> => {
    try {
      const { data } = await makeMenuApi.get(`/orders/waiter/tables/${tableNum}/order/`)
      return data.order
    } catch (err) {
      error.value = extractError(err, 'Error cargando pedido.')
      return null
    }
  }

  const advanceOrder = async (orderId: number): Promise<ActionResult> => {
    try {
      const { data } = await makeMenuApi.post(`/orders/waiter/orders/${orderId}/advance/`)
      await fetchTables()
      return { ok: true, message: data.message }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Error actualizando pedido.') }
    }
  }

  const cancelOrder = async (orderId: number): Promise<ActionResult> => {
    try {
      const { data } = await makeMenuApi.post(`/orders/waiter/orders/${orderId}/cancel/`)
      await fetchTables()
      return { ok: true, message: data.message }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Error cancelando pedido.') }
    }
  }

  const closeTable = async (tableNum: number): Promise<ActionResult> => {
    try {
      const { data } = await makeMenuApi.post(`/orders/waiter/tables/${tableNum}/close/`)
      await fetchTables()
      return { ok: true, message: data.message }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Error cerrando mesa.') }
    }
  }

  

  return {
    establishmentName, tables, loading, error,
    clearError, fetchTables, fetchOrderDetail,
    advanceOrder, cancelOrder, closeTable
  }
})