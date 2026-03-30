import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useLocalStorage } from '@vueuse/core'
import { loginAction } from '../actions/login.action'
import { logoutAction } from '../actions/logout.action'
import { AuthStatus } from '../interfaces'

export const useAuthStore = defineStore('auth', () => {
  // 1. STATE (Estado)
  const authStatus = ref<AuthStatus>(AuthStatus.Unauthenticated)

  // VueUse enlaza esta variable automáticamente con el localStorage del navegador
  const token = ref(useLocalStorage('token', ''))

  // 2. GETTERS (Propiedades Computadas)
  const isChecking = computed(() => authStatus.value === AuthStatus.Checking)
  const isAuthenticated = computed(() => authStatus.value === AuthStatus.Authenticated)

  // 3. ACTIONS (Métodos)

  const login = async (username: string, password: string) => {
    // Ponemos la app en estado de carga
    authStatus.value = AuthStatus.Checking

    try {
      const loginResponse = await loginAction(username, password)

      if (!loginResponse.ok) {
        // Si fallan las credenciales, aseguramos que todo quede limpio
        await logout()
        return { ok: false, message: loginResponse.message }
      }

      // Si Django da el OK, guardamos la llave y abrimos la puerta
      token.value = loginResponse.token // VueUse lo guarda en el disco duro automáticamente
      authStatus.value = AuthStatus.Authenticated

      return { ok: true, message: '' }
    } catch (error) {
      await logout()
      return { ok: false, message: 'Error inesperado al iniciar sesión' }
    }
  }

  const logout = async () => {
    // 1. Si tenemos token, le decimos a Django que lo destruya en su base de datos.
    // (No hace falta pasarle el token a la acción porque el Interceptor de Axios ya se lo inyecta).
    if (token.value) {
      await logoutAction()
    }

    // 2. Borramos la memoria local (VueUse lo elimina de localStorage al asignarle '')
    token.value = ''
    authStatus.value = AuthStatus.Unauthenticated
  }

  // 4. RETORNO (Lo que exponemos a los componentes)
  return {
    // State
    token,
    authStatus,

    // Getters
    isChecking,
    isAuthenticated,

    // Actions
    login,
    logout,
  }
})
