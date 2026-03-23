import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Establishment } from '@/types/table'
import { useAuthFetch } from '@/composables/useAuthFetch'

const API_URL = 'http://localhost:8000/api'

export const useEstablishmentStore = defineStore('establishments', () => {
  const establishments = ref<Establishment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const { authFetch } = useAuthFetch()
  
  const clearError = () => {
    error.value = null
  }

  const fetchEstablishments = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await authFetch(`${API_URL}/establishments/`)
      if (!response.ok) throw new Error('Error al cargar los establecimientos')
      establishments.value = await response.json()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  return {
    establishments,
    loading,
    error,
    clearError,
    fetchEstablishments
  }
})