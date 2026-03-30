import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
// ❌ Borramos el import de useLocalStorage
import { loginAction } from '../actions/login.action'
import { logoutAction } from '../actions/logout.action'
import { checkAuthAction } from '../actions/checkAuth.action'
import { AuthStatus } from '../interfaces'

export const useAuthStore = defineStore('auth', () => {
  // 1. STATE (Estado)
  const authStatus = ref<AuthStatus>(AuthStatus.Checking)

  // ✅ NATIVO: Al arrancar, leemos de permanente o temporal (lo que encuentre primero)
  const token = ref<string>(localStorage.getItem('token') || sessionStorage.getItem('token') || '')

  // 2. GETTERS (Propiedades Computadas)
  const isChecking = computed(() => authStatus.value === AuthStatus.Checking)
  const isAuthenticated = computed(() => authStatus.value === AuthStatus.Authenticated)

  // 3. ACTIONS (Métodos)
  const login = async (username: string, password: string, rememberMe: boolean = false) => {
    authStatus.value = AuthStatus.Checking

    try {
      const loginResponse = await loginAction(username, password)

      if (!loginResponse.ok) {
        await logout()
        return { ok: false, message: loginResponse.message }
      }

      // 1. Guardamos en la variable reactiva
      token.value = loginResponse.token

      // 2. ✅ NATIVO: Decidimos en qué "caja fuerte" lo guardamos
      if (rememberMe) {
        localStorage.setItem('token', loginResponse.token) // Permanente
        sessionStorage.removeItem('token') // Por si había basura
      } else {
        sessionStorage.setItem('token', loginResponse.token) // Temporal
        localStorage.removeItem('token') // Por si había basura
      }

      authStatus.value = AuthStatus.Authenticated

      return { ok: true, message: '' }
    } catch (error) {
      await logout()
      return { ok: false, message: 'Error inesperado al iniciar sesión' }
    }
  }

  const logout = async () => {
    if (token.value) {
      await logoutAction()
    }

    // ✅ NATIVO: Limpiamos absolutamente todo
    token.value = ''
    localStorage.removeItem('token')
    sessionStorage.removeItem('token')

    authStatus.value = AuthStatus.Unauthenticated
  }

  const checkAuthStatus = async () => {
    // 1. Si no hay token en ninguna de las dos cajas físicas, cerramos.
    if (!token.value) {
      await logout()
      return false
    }

    try {
      const response = await checkAuthAction()

      if (!response.ok) {
        await logout()
        return false
      }

      authStatus.value = AuthStatus.Authenticated
      return true
    } catch (error) {
      await logout()
      return false
    }
  }

  return {
    token,
    authStatus,
    isChecking,
    isAuthenticated,
    login,
    logout,
    checkAuthStatus,
  }
})
