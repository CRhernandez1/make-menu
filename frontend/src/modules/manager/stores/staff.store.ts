import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'
import type { Staff, ActionResult } from '../../auth/interfaces'

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

export const useStaffStore = defineStore('staff', () => {
  const staff = ref<Staff[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const clearError = () => { error.value = null }

  const fetchStaff = async (cif: string) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await makeMenuApi.get(`/establishments/${cif}/staff/`)
      staff.value = data
    } catch (err) {
      error.value = extractError(err, 'Could not load staff. Please refresh the page.')
    } finally {
      loading.value = false
    }
  }

  const updateRole = async (cif: string, memberId: number, role: string): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/staff/${memberId}/edit/`, { role })
      await fetchStaff(cif)
      return { ok: true, message: 'Role updated successfully.' }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Could not update the role.') }
    }
  }

  const removeMember = async (cif: string, memberId: number): Promise<ActionResult> => {
    try {
      await makeMenuApi.post(`/establishments/${cif}/staff/${memberId}/remove/`)
      await fetchStaff(cif)
      return { ok: true, message: 'Member removed successfully.' }
    } catch (err) {
      return { ok: false, error: extractError(err, 'Could not remove the member.') }
    }
  }

  return {
    staff, loading, error,
    clearError, fetchStaff, updateRole, removeMember
  }
})