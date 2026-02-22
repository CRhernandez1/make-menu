<template>
  <div class="flex items-center justify-center mt-20">
    <div class="w-full max-w-xs">
      <div class="flex mb-4">
        <button
          @click="tab = 'login'"
          :class="tab === 'login' ? 'border-b-2 border-emerald-400 font-bold' : 'text-gray-400'"
          class="flex-1 pb-2"
        >
          Login
        </button>
        <button
          @click="tab = 'register'"
          :class="tab === 'register' ? 'border-b-2 border-emerald-400 font-bold' : 'text-gray-400'"
          class="flex-1 pb-2"
        >
          Registro
        </button>
      </div>

      <input
        v-model="username"
        type="text"
        placeholder="Usuario"
        class="w-full mb-3 p-2 border rounded"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Contraseña"
        class="w-full mb-3 p-2 border rounded"
      />

      <template v-if="tab === 'register'">
        <input
          v-model="firstName"
          type="text"
          placeholder="Nombre"
          class="w-full mb-3 p-2 border rounded"
        />
        <input
          v-model="lastName"
          type="text"
          placeholder="Apellido"
          class="w-full mb-3 p-2 border rounded"
        />
        <input
          v-model="email"
          type="email"
          placeholder="Correo"
          class="w-full mb-3 p-2 border rounded"
        />
        <input
          v-model="phone"
          type="tel"
          placeholder="Teléfono"
          class="w-full mb-3 p-2 border rounded"
        />
      </template>

      <button
        @click="handleSubmit"
        class="w-full bg-emerald-400 text-white p-2 rounded"
      >
        {{ tab === 'login' ? 'Entrar' : 'Registrarse' }}
      </button>
      <p v-if="message" class="mt-2 text-sm text-red-500">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const tab = ref('login')
const username = ref('')
const password = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const message = ref('')

const handleSubmit = async () => {
  message.value = ''
  try {
    if (tab.value === 'login') {
      await auth.login(username.value, password.value)
    } else {
      await auth.register(
        username.value,
        password.value,
        firstName.value,
        lastName.value,
        email.value,
        phone.value
      )
    }
  } catch {
    message.value = tab.value === 'login'
      ? 'Usuario o contraseña incorrectos'
      : 'Error al registrar'
  }
}
</script>
