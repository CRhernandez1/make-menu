<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="max-w-md w-full bg-gray-800 rounded-xl shadow-lg p-8 border border-gray-700">
      <h1 class="text-3xl font-bold text-center text-green-400 mb-8">Iniciar Sesión</h1>

      <form @submit.prevent="onLogin">
        <div class="mb-5">
          <label for="username" class="block text-sm font-medium text-gray-300 mb-1">Usuario</label>
          <input
            v-model="myForm.username"
            ref="usernameInputRef"
            type="text"
            id="username"
            name="username"
            class="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400 transition-colors"
            autocomplete="off"
          />
        </div>

        <div class="mb-5">
          <label for="password" class="block text-sm font-medium text-gray-300 mb-1"
            >Contraseña</label
          >
          <input
            v-model="myForm.password"
            ref="passwordInputRef"
            type="password"
            id="password"
            name="password"
            class="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400 transition-colors"
            autocomplete="off"
          />
        </div>

        <div class="mb-6 flex items-center">
          <input
            v-model="myForm.rememberMe"
            type="checkbox"
            id="remember"
            name="remember"
            class="w-4 h-4 text-green-500 bg-gray-900 border-gray-700 rounded focus:ring-green-400 focus:ring-offset-gray-800"
          />
          <label for="remember" class="text-sm text-gray-400 ml-2 cursor-pointer"
            >Recordar usuario</label
          >
        </div>

        <div class="mb-6 text-sm text-right">
          <a href="#" class="text-green-400 hover:text-green-300 transition-colors"
            >¿Olvidaste la contraseña?</a
          >
        </div>

        <button
          type="submit"
          class="w-full bg-green-500 hover:bg-green-400 text-gray-900 font-bold py-3 px-4 rounded-lg transition-colors"
        >
          Ingresar
        </button>
      </form>

      <div class="mt-6 text-sm text-center text-gray-400">
        ¿No tienes cuenta?
        <RouterLink
          :to="{ name: 'register' }"
          class="text-green-400 hover:text-green-300 transition-colors"
        >
          Crear cuenta aquí
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.store'

const authStore = useAuthStore()
const router = useRouter()

// Referencias directas a los elementos HTML del DOM
const usernameInputRef = ref<HTMLInputElement | null>(null)
const passwordInputRef = ref<HTMLInputElement | null>(null)

// Estado reactivo del formulario
const myForm = reactive({
  username: '',
  password: '',
  rememberMe: false,
})

// Función que se ejecuta al enviar el formulario
const onLogin = async () => {
  // 1. Validación de campos vacíos
  if (myForm.username === '') {
    return usernameInputRef.value?.focus() // Pone el cursor en el input del usuario
  }

  if (myForm.password.length < 6) {
    return passwordInputRef.value?.focus() // Pone el cursor en el input de la contraseña
  }

  // 2. Lógica de "Recordar usuario"
  if (myForm.rememberMe) {
    localStorage.setItem('saved_username', myForm.username)
  } else {
    localStorage.removeItem('saved_username')
  }

  // 3. Llamada al Store de Pinia
  const result = await authStore.login(myForm.username, myForm.password)

  // 4. Manejo del resultado
  if (result.ok) {
    router.push({ name: 'home' }) // Si todo va bien, vamos a la página principal
    return
  }

  // 5. Si falla, mostramos el error usando Toastification
  console.error(result.message || 'Usuario/Contraseña no son correctos')
}

// Se ejecuta automáticamente al cargar el componente
watchEffect(() => {
  const savedUsername = localStorage.getItem('saved_username')
  if (savedUsername) {
    myForm.username = savedUsername
    myForm.rememberMe = true
  }
})
</script>
