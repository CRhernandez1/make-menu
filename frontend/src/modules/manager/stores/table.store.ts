import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'
import type { Table, TableCreate, TableUpdate, ActionResult } from '../../auth/interfaces'

function extractError(error: unknown, fallback: string): string {
  if (isAxiosError(error) && error.response?.data) {
    const data = error.response.data
    if (data.message) return data.message
    if (data.error) return data.error
    if (data.errors) {
      return Object.entries(data.errors)
        .map(([field, msgs]) => `${field}: ${(msgs as string[]).join(', ')}`)
        .join('. ')
    }
  }
  return fallback
}

export const useTableStore = defineStore('tables', () => {
  const tables = ref<Table[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const clearError = () => { error.value = null }

  const fetchTables = async (cif: string) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await makeMenuApi.get(`/establishments/${cif}/tables/`)
      tables.value = data
    } catch (err) {
      error.value = extractError(err, 'Could not load tables. Please refresh the page.')
    } finally {
      loading.value = false
    }
  }

  const createTable = async (cif: string, payload: TableCreate): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/tables/add/`, payload)
      await fetchTables(cif)
      return { ok: true, message: `Table ${String(payload.number).padStart(2, '0')} created successfully.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Could not create the table.') }
    }
  }

  const updateTable = async (cif: string, tableNum: number, payload: TableUpdate): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/tables/${tableNum}/edit/`, payload)
      await fetchTables(cif)
      return { ok: true, message: `Table ${String(tableNum).padStart(2, '0')} updated.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Could not update the table.') }
    }
  }

  const toggleTable = async (cif: string, tableNum: number): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/tables/${tableNum}/change/`)
      await fetchTables(cif)
      const table = tables.value.find(t => t.number === tableNum)
      const status = table?.active ? 'activated' : 'deactivated'
      return { ok: true, message: `Table ${String(tableNum).padStart(2, '0')} ${status}.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Could not change the table status.') }
    }
  }

  const deleteTable = async (cif: string, tableNum: number): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/tables/${tableNum}/delete/`)
      await fetchTables(cif)
      return { ok: true, message: `Table ${String(tableNum).padStart(2, '0')} deleted successfully.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Could not delete the table.') }
    }
  }

  return {
    tables, loading, error,
    clearError, fetchTables, createTable, updateTable, toggleTable, deleteTable
  }
})