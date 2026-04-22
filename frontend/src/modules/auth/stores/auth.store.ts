import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { loginAction } from '../actions/login.action'
import { logoutAction } from '../actions/logout.action'
import { checkAuthAction } from '../actions/checkAuth.action'
import { AuthStatus } from '../interfaces'
import type { UserProfile } from '../interfaces/auth.response'

export const useAuthStore = defineStore('auth', () => {
  // STATE — el token vive en la cookie HttpOnly, no en el frontend
  const authStatus = ref<AuthStatus>(AuthStatus.Checking)
  const user = ref<UserProfile | null>(null)

  // GETTERS
  const isChecking = computed(() => authStatus.value === AuthStatus.Checking)
  const isAuthenticated = computed(() => authStatus.value === AuthStatus.Authenticated)

  // HELPERS PRIVADOS
  const setUnauthenticated = () => {
    user.value = null
    authStatus.value = AuthStatus.Unauthenticated
  }

  // ACTIONS
  const login = async (username: string, password: string, rememberMe: boolean = false) => {
    authStatus.value = AuthStatus.Checking

    try {
      // Una sola petición: autentica, obtiene el perfil y setea la cookie HttpOnly
      const result = await loginAction(username, password, rememberMe)

      if (!result.ok) {
        setUnauthenticated()
        return { ok: false as const, message: result.message }
      }

      user.value = result.user
      authStatus.value = AuthStatus.Authenticated
      return { ok: true as const, role: result.user.role }
    } catch {
      setUnauthenticated()
      return { ok: false as const, message: 'Error inesperado al iniciar sesión' }
    }
  }

  const logout = async () => {
    await logoutAction()
    setUnauthenticated()
  }

  // Valida la cookie con el backend al refrescar la página (llamado por el guard global)
  const checkAuthStatus = async (): Promise<boolean> => {
    try {
      const response = await checkAuthAction()

      if (!response.ok) {
        setUnauthenticated()
        return false
      }

      user.value = response.user
      authStatus.value = AuthStatus.Authenticated
      return true
    } catch {
      setUnauthenticated()
      return false
    }
  }

  return {
    user,
    authStatus,
    isChecking,
    isAuthenticated,
    login,
    logout,
    checkAuthStatus,
  }
})