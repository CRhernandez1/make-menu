import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { loginAction } from '../actions/login.action'
import { logoutAction } from '../actions/logout.action'
import { checkAuthAction } from '../actions/checkAuth.action'
import { AuthStatus } from '../interfaces'

export const useAuthStore = defineStore('auth', () => {
  // 1. STATE
  const authStatus = ref<AuthStatus>(AuthStatus.Checking)
  const token = ref<string>(localStorage.getItem('token') || sessionStorage.getItem('token') || '')
  
  // Guardamos el usuario (y su rol)
  const user = ref<any>(null) 

  // 2. GETTERS
  const isChecking = computed(() => authStatus.value === AuthStatus.Checking)
  const isAuthenticated = computed(() => authStatus.value === AuthStatus.Authenticated)

  // 3. ACTIONS
  const login = async (username: string, password: string, rememberMe: boolean = false) => {
    authStatus.value = AuthStatus.Checking

    try {
      // 1. Hacemos login normal
      const loginResponse = await loginAction(username, password)

      if (!loginResponse.ok) {
        await logout()
        return { ok: false, message: loginResponse.message }
      }

      // 2. Guardamos el token
      token.value = loginResponse.token

      if (rememberMe) {
        localStorage.setItem('token', loginResponse.token)
        sessionStorage.removeItem('token')
      } else {
        sessionStorage.setItem('token', loginResponse.token)
        localStorage.removeItem('token')
      }

      // 3. Pedimos el perfil del usuario para saber su ROL
      const isAuthValid = await checkAuthStatus()
      
      if (isAuthValid && user.value) {
        // Todo perfecto: devolvemos ok y el rol
        return { ok: true, message: '', role: user.value.role } 
      } else {
        await logout()
        return { ok: false, message: 'No se pudo obtener el perfil del usuario' }
      }

    } catch (error) {
      await logout()
      return { ok: false, message: 'Error inesperado al iniciar sesión' }
    }
  }

  const logout = async () => {
    if (token.value) {
      await logoutAction()
    }

    token.value = ''
    user.value = null // Limpiamos la libreta
    localStorage.removeItem('token')
    sessionStorage.removeItem('token')

    authStatus.value = AuthStatus.Unauthenticated
  }

  const checkAuthStatus = async () => {
    if (!token.value) {
      await logout()
      return false
    }

    try {
      // Usamos la acción del paso 1
      const response = await checkAuthAction()

      if (!response.ok) {
        await logout()
        return false
      }

      // Guardamos al usuario en memoria
      user.value = response.user 
      authStatus.value = AuthStatus.Authenticated
      return true
    } catch (error) {
      await logout()
      return false
    }
  }

  return {
    token,
    user,
    authStatus,
    isChecking,
    isAuthenticated,
    login,
    logout,
    checkAuthStatus,
  }
})