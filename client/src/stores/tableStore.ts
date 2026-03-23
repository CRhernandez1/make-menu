import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Table, TableCreate, TableUpdate } from '@/types/table'
import { useAuthFetch } from '@/composables/useAuthFetch'
 
const API_URL = 'http://localhost:8000/api'
 
export interface ActionResult {
  ok: boolean
  error?: string
  message?: string
}
 
async function parseError(response: Response, fallback: string): Promise<string> {
  try {
    const data = await response.json()
    if (data.message) return data.message
    const fieldErrors = Object.values(data).flat()
    if (fieldErrors.length > 0) return fieldErrors.join('. ')
  } catch { /* ignore */ }
 
  switch (response.status) {
    case 400: return 'The data you entered is invalid. Please check the fields and try again.'
    case 403: return 'You don\'t have permission to perform this action.'
    case 404: return 'This resource was not found. It may have been deleted.'
    case 409: return 'A table with this number already exists in this establishment.'
    case 500: return 'Something went wrong on the server. Please try again later.'
    default: return fallback
  }
}
 
export const useTableStore = defineStore('tables', () => {
  const tables = ref<Table[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const { authFetch } = useAuthFetch()
 
  const clearError = () => { error.value = null }
 
  const fetchTables = async (cif: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await authFetch(`${API_URL}/establishments/${cif}/tables/`)
      if (!response.ok) {
        error.value = await parseError(response, 'Could not load the tables. Please refresh the page.')
        return
      }
      tables.value = await response.json()
    } catch {
      error.value = 'Unable to connect to the server. Check that the API is running.'
    } finally {
      loading.value = false
    }
  }
 
  const createTable = async (cif: string, data: TableCreate): Promise<ActionResult> => {
    try {
      const response = await authFetch(`${API_URL}/establishments/${cif}/tables/add/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ number: data.number, max_guests: data.max_guests })
      })
      if (!response.ok) {
        const msg = await parseError(response, 'Could not create the table. Please check the data and try again.')
        return { ok: false, error: msg }
      }
      await fetchTables(cif)
      return { ok: true, message: `Table ${String(data.number).padStart(2, '0')} created successfully.` }
    } catch {
      return { ok: false, error: 'Unable to connect to the server. Check that the API is running.' }
    }
  }
 
  const updateTable = async (cif: string, tableNum: number, data: TableUpdate): Promise<ActionResult> => {
    try {
      const response = await authFetch(`${API_URL}/establishments/${cif}/tables/${tableNum}/edit/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        const msg = await parseError(response, 'Could not update the table. Please check the data and try again.')
        return { ok: false, error: msg }
      }
      await fetchTables(cif)
      return { ok: true, message: `Table ${String(tableNum).padStart(2, '0')} updated to ${data.max_guests} guests.` }
    } catch {
      return { ok: false, error: 'Unable to connect to the server. Check that the API is running.' }
    }
  }
 
  const toggleTable = async (cif: string, tableNum: number): Promise<ActionResult> => {
    try {
      const response = await authFetch(`${API_URL}/establishments/${cif}/tables/${tableNum}/change/`)
      if (!response.ok) {
        const msg = await parseError(response, 'Could not change the table status. Please try again.')
        return { ok: false, error: msg }
      }
      await fetchTables(cif)
      const table = tables.value.find(t => t.number === tableNum)
      const status = table?.active ? 'activated' : 'deactivated'
      return { ok: true, message: `Table ${String(tableNum).padStart(2, '0')} ${status}.` }
    } catch {
      return { ok: false, error: 'Unable to connect to the server. Check that the API is running.' }
    }
  }
 
  const deleteTable = async (cif: string, tableNum: number): Promise<ActionResult> => {
    try {
      const response = await authFetch(`${API_URL}/establishments/${cif}/tables/${tableNum}/delete/`)
      if (!response.ok) {
        const msg = await parseError(response, 'Could not delete the table. It may have active orders.')
        return { ok: false, error: msg }
      }
      await fetchTables(cif)
      return { ok: true, message: `Table ${String(tableNum).padStart(2, '0')} deleted successfully.` }
    } catch {
      return { ok: false, error: 'Unable to connect to the server. Check that the API is running.' }
    }
  }
 
  return {
    tables, loading, error,
    clearError, fetchTables, createTable, updateTable, toggleTable, deleteTable
  }
})