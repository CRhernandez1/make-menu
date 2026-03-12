<template>
  <div class="min-h-screen flex items-center justify-center bg-stone-50">
    <div class="w-full max-w-sm bg-white border border-stone-200 rounded-2xl shadow-sm p-8">

      <!-- Brand -->
      <div class="flex items-center gap-2 mb-8">
        <div class="w-2.5 h-2.5 rounded-full bg-emerald-400" />
        <span class="font-serif text-xl tracking-tight text-stone-800">acceso</span>
      </div>

      <!-- Tabs -->
      <div class="relative flex bg-stone-100 rounded-xl p-1 mb-7">
        <button
          @click="switchTab('login')"
          :class="['flex-1 py-2 text-sm font-medium rounded-lg z-10 transition-colors duration-200', tab === 'login' ? 'text-stone-800' : 'text-stone-400']"
        >Entrar</button>
        <button
          @click="switchTab('register')"
          :class="['flex-1 py-2 text-sm font-medium rounded-lg z-10 transition-colors duration-200', tab === 'register' ? 'text-stone-800' : 'text-stone-400']"
        >Registro</button>
        <div
          class="absolute top-1 bottom-1 w-[calc(50%-4px)] bg-white rounded-lg shadow-sm transition-all duration-300"
          :class="tab === 'login' ? 'left-1' : 'left-[calc(50%+4px)]'"
        />
      </div>

      <form @submit.prevent="handleSubmit" novalidate>
        <div class="flex flex-col gap-4 mb-5">

          <!-- Usuario -->
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-stone-500 tracking-wide">Usuario</label>
            <input
              v-model="username"
              type="text"
              autocomplete="username"
              @blur="validateField('username')"
              :class="inputClass(errors.username)"
            />
            <span class="text-xs text-red-400 min-h-[16px]">{{ errors.username }}</span>
          </div>

          <!-- Contraseña -->
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-stone-500 tracking-wide">Contraseña</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                @blur="validateField('password')"
                :class="inputClass(errors.password) + ' pr-10'"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-600 text-sm"
              >{{ showPassword ? '🙈' : '👁' }}</button>
            </div>
            <span class="text-xs text-red-400 min-h-[16px]">{{ errors.password }}</span>
          </div>

          <template v-if="tab === 'register'">
            <!-- Nombre + Apellido -->
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium text-stone-500 tracking-wide">Nombre</label>
                <input v-model="firstName" type="text" @blur="validateField('firstName')" :class="inputClass(errors.firstName)" />
                <span class="text-xs text-red-400 min-h-[16px]">{{ errors.firstName }}</span>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium text-stone-500 tracking-wide">Apellido</label>
                <input v-model="lastName" type="text" @blur="validateField('lastName')" :class="inputClass(errors.lastName)" />
                <span class="text-xs text-red-400 min-h-[16px]">{{ errors.lastName }}</span>
              </div>
            </div>

            <!-- Email -->
            <div class="flex flex-col gap-1">
              <label class="text-xs font-medium text-stone-500 tracking-wide">Correo</label>
              <input v-model="email" type="email" autocomplete="email" @blur="validateField('email')" :class="inputClass(errors.email)" />
              <span class="text-xs text-red-400 min-h-[16px]">{{ errors.email }}</span>
            </div>

            <!-- Teléfono -->
            <div class="flex flex-col gap-1">
              <label class="text-xs font-medium text-stone-500 tracking-wide">Teléfono</label>
              <input v-model="phone" type="tel" placeholder="+34 600 000 000" @blur="validateField('phone')" :class="inputClass(errors.phone)" />
              <span class="text-xs text-red-400 min-h-[16px]">{{ errors.phone }}</span>
            </div>
          </template>
        </div>

        <!-- Error servidor -->
        <p v-if="serverError" class="text-xs text-red-400 text-center mb-4">{{ serverError }}</p>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 bg-emerald-400 hover:bg-emerald-500 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-medium rounded-xl transition-colors duration-150 flex items-center justify-center min-h-[44px]"
        >
          <svg v-if="loading" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          <span v-else>{{ tab === 'login' ? 'Entrar' : 'Crear cuenta' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const tab = ref<'login' | 'register'>('login')
const username = ref('')
const password = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const showPassword = ref(false)
const loading = ref(false)
const serverError = ref('')

const errors = reactive<Record<string, string>>({
  username: '', password: '', firstName: '', lastName: '', email: '', phone: '',
})

const inputClass = (error: string) =>
  `w-full px-3 py-2.5 text-sm rounded-lg border outline-none transition-colors duration-150 ${
    error
      ? 'border-red-300 focus:border-red-400'
      : 'border-stone-200 focus:border-emerald-400'
  } text-stone-800 placeholder:text-stone-300`

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const PHONE_RE = /^\+?[\d\s\-().]{7,15}$/

const validators: Record<string, () => string> = {
  username: () => !username.value.trim() ? 'El usuario es obligatorio' : '',
  password: () => {
    if (!password.value) return 'La contraseña es obligatoria'
    return ''
  },
  firstName: () => !firstName.value.trim() ? 'El nombre es obligatorio' : '',
  lastName: () => !lastName.value.trim() ? 'El apellido es obligatorio' : '',
  email: () => {
    if (!email.value.trim()) return 'El correo es obligatorio'
    if (!EMAIL_RE.test(email.value)) return 'Correo no válido'
    return ''
  },
  phone: () => {
    if (!phone.value.trim()) return 'El teléfono es obligatorio'
    const digits = phone.value.replace(/\D/g, '')
    if (!PHONE_RE.test(phone.value)) return 'Formato no válido'
    if (digits.length < 7) return 'Teléfono demasiado corto'
    if (digits.length > 15) return 'Teléfono demasiado largo'
    return ''
  },
}

function validateField(field: string) {
  errors[field] = validators[field]?.() ?? ''
}

function validateAll(): boolean {
  const fields = tab.value === 'login'
    ? ['username', 'password']
    : ['username', 'password', 'firstName', 'lastName', 'email', 'phone']
  fields.forEach(validateField)
  return fields.every(f => !errors[f])
}

function switchTab(newTab: 'login' | 'register') {
  tab.value = newTab
  serverError.value = ''
  Object.keys(errors).forEach(k => (errors[k] = ''))
}

async function handleSubmit() {
  serverError.value = ''
  if (!validateAll()) return
  loading.value = true
  try {
    if (tab.value === 'login') {
      await auth.login(username.value, password.value)
    } else {
      await auth.register(username.value, password.value, firstName.value, lastName.value, email.value, phone.value)
    }
  } catch {
    serverError.value = tab.value === 'login'
      ? 'Usuario o contraseña incorrectos'
      : 'Error al registrar. Inténtalo de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>