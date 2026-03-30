<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { registerUser } from '../actions/register.action'

const route = useRoute()
const router = useRouter()

// Estados para mostrar mensajes al usuario en pantalla
const isLoading = ref(false)
const errorMessage = ref('')

// 1. LA LIBRETA: Aquí se guardan los datos mientras el usuario teclea
const form = reactive({
  username: '',
  password: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  invite_token: '', // Guardaremos el código del QR aquí de forma invisible
})

// 2. LA CAPTURA DEL QR: Cuando la página carga, miramos la URL
onMounted(() => {
  const tokenFromUrl = route.query.invite as string
  if (tokenFromUrl) {
    // Si hay token en la URL (?invite=123), lo guardamos en la libreta
    form.invite_token = tokenFromUrl
  } else {
    // Seguridad: Si alguien entra a /register sin QR, lo echamos al login
    router.push({ name: 'login' })
  }
})

// 3. EL ENVÍO: Se ejecuta cuando el usuario pulsa el botón verde
const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''

  // Llamamos a la función del Paso 2 y le pasamos la libreta entera
  const result = await registerUser(form)

  if (result.ok) {
    // ¡Éxito! Django lo ha guardado. Lo mandamos a que inicie sesión.
    router.push({ name: 'login' })
  } else {
    // Fallo (ej: el username ya existe). Mostramos el error en pantalla.
    errorMessage.value = result.error
  }

  isLoading.value = false
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="max-w-md w-full bg-gray-800 rounded-xl shadow-lg p-8 border border-gray-700">
      <h2 class="text-3xl font-bold text-center text-green-400 mb-8">Registro de Equipo</h2>

      <div
        v-if="errorMessage"
        class="mb-4 p-3 bg-red-900/50 border border-red-500 rounded text-red-200 text-sm text-center"
      >
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1">Usuario *</label>
          <input
            v-model="form.username"
            type="text"
            required
            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none"
          />
        </div>

        <div class="flex gap-4">
          <div class="w-1/2">
            <label class="block text-sm font-medium text-gray-300 mb-1">Nombre *</label>
            <input
              v-model="form.first_name"
              type="text"
              required
              class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none"
            />
          </div>
          <div class="w-1/2">
            <label class="block text-sm font-medium text-gray-300 mb-1">Apellidos *</label>
            <input
              v-model="form.last_name"
              type="text"
              required
              class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1">Email *</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1">Contraseña *</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1">Teléfono (Opcional)</label>
          <input
            v-model="form.phone"
            type="tel"
            class="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white focus:border-green-400 focus:ring-1 focus:ring-green-400 outline-none"
          />
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full mt-6 bg-green-500 hover:bg-green-400 text-gray-900 font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50"
        >
          {{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}
        </button>
      </form>
    </div>
  </div>
</template>
