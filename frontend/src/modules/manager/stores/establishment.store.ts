import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'
import type { Establishment, EstablishmentCreate, EstablishmentUpdate, ActionResult } from '../../auth/interfaces'

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

export const useEstablishmentStore = defineStore('establishments', () => {
  const establishments = ref<Establishment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const clearError = () => { error.value = null }

  const fetchEstablishments = async () => {
    loading.value = true
    error.value = null
    try {
      const { data } = await makeMenuApi.get('/establishments/')
      establishments.value = data
    } catch (err) {
      error.value = extractError(err, 'No se han podido cargar los establecimientos. Recarga la página.')
    } finally {
      loading.value = false
    }
  }

  const createEstablishment = async (payload: EstablishmentCreate): Promise<ActionResult> => {
    try {
      await makeMenuApi.post('/establishments/add/', payload)
      await fetchEstablishments()
      return { ok: true, message: `Establecimiento "${payload.name}" creado correctamente.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'No se ha podido crear el establecimiento.') }
    }
  }

  const updateEstablishment = async (cif: string, payload: EstablishmentUpdate): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/edit/`, payload)
      await fetchEstablishments()
      return { ok: true, message: `Establecimiento "${payload.name}" actualizado correctamente.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'No se ha podido actualizar el establecimiento.') }
    }
  }

  const toggleEstablishment = async (cif: string): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/toggle/`)
      await fetchEstablishments()
      const est = establishments.value.find(e => e.cif === cif)
      const status = est?.opened ? 'abierto' : 'cerrado'
      return { ok: true, message: `Establecimiento ${status}.` }
    } catch (err) {
      return { ok: false, error: extractError(err, 'No se ha podido cambiar el estado del establecimiento.') }
    }
  }

  const deleteEstablishment = async (cif: string): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/delete/`)
      await fetchEstablishments()
      return { ok: true, message: 'Establecimiento eliminado correctamente.' }
    } catch (err) {
      return { ok: false, error: extractError(err, 'No se ha podido eliminar el establecimiento.') }
    }
  }

  return {
    establishments, loading, error,
    clearError, fetchEstablishments, createEstablishment, updateEstablishment, toggleEstablishment, deleteEstablishment
  }
})
