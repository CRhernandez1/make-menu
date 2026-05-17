import axios from 'axios'

const makeMenuApi = axios.create({
  baseURL: import.meta.env.VITE_MAKE_MENU_API_URL,
  withCredentials: true,
})

// Interceptor global: si cualquier respuesta es 401 (cookie expirada/inválida),
// limpiamos el estado de auth y redirigimos al login automáticamente.
makeMenuApi.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Importación dinámica para evitar dependencia circular
      const { default: router } = await import('@/router')
      
      const currentRoute = router.currentRoute.value.name as string
      
      // Rutas donde un 401 es normal o esperado (ej: visitantes en la landing)
      const PUBLIC_ROUTES = ['home', 'login', 'register', 'NotFound', 'landing', 'public-menu']

      if (currentRoute && !PUBLIC_ROUTES.includes(currentRoute)) {
        const { useAuthStore } = await import('@/modules/auth/stores/auth.store')
        const authStore = useAuthStore()

        // Limpiar estado sin llamar al backend (la cookie ya es inválida)
        authStore.user = null
        authStore.authStatus = 'Unauthenticated' as any // AuthStatus.Unauthenticated
        router.push({ name: 'login' })
      }
    }
    return Promise.reject(error)
  },
)

export { makeMenuApi }