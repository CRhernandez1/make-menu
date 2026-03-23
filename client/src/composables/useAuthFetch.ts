import { useAuthStore } from '@/stores/auth'

export const useAuthFetch = () => {
  const authStore = useAuthStore()

  const authFetch = (url: string, options: RequestInit = {}) => {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(authStore.token && { Authorization: `Token ${authStore.token}` }),
      ...options.headers
    }
    return fetch(url, { ...options, headers })
  }

  return { authFetch }
}