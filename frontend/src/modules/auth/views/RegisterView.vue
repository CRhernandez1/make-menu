<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { registerUser } from '../actions/register.action'
import { makeMenuApi } from '@/api/makeMenu'

const route = useRoute()
const router = useRouter()

const isLoading = ref(false)
const isValidating = ref(true)
const invitationError = ref('')
const errorMessage = ref('')
const establishmentInfo = ref({ name: '', role: '' })

const form = reactive({
  username: '',
  password: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  invitation_id: '',
})

onMounted(async () => {
  const invitationCode = route.query.code as string

  if (!invitationCode) {
    router.push({ name: 'login' })
    return
  }

  form.invitation_id = invitationCode

  try {
    const { data } = await makeMenuApi.get(`/establishments/invite/validate/${invitationCode}/`)
    establishmentInfo.value = {
      name: data.establishment_name,
      role: data.role,
    }
  } catch (error: any) {
    invitationError.value = error.response?.data?.error || 'Invitación no válida.'
  } finally {
    isValidating.value = false
  }
})

const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''

  const result = await registerUser(form)

  if (result.ok) {
    router.push({ name: 'login' })
  } else {
    errorMessage.value = result.error
  }

  isLoading.value = false
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 px-4">
    <div class="max-w-md w-full bg-gray-800 rounded-xl shadow-lg p-8 border border-gray-700">
      <h2 class="text-3xl font-bold text-center text-green-400 mb-2">Registro de Equipo</h2>
      <p v-if="establishmentInfo.name" class="text-center text-gray-400 mb-8 italic">
        Uniéndote a: <span class="text-white font-semibold">{{ establishmentInfo.name }}</span>
      </p>

      <div v-if="isValidating" class="py-10 text-center">
        <div
          class="animate-spin inline-block w-8 h-8 border-4 border-green-400 border-t-transparent rounded-full mb-4"
        ></div>
        <p class="text-gray-400">Comprobando invitación...</p>
      </div>

      <div v-else-if="invitationError" class="py-6 text-center">
        <div class="bg-red-900/30 border border-red-500 p-4 rounded-lg mb-6">
          <p class="text-red-200">{{ invitationError }}</p>
        </div>
        <button @click="router.push({ name: 'login' })" class="text-green-400 hover:underline">
          Volver al inicio
        </button>
      </div>

      <div v-else>
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
            {{ isLoading ? 'Creando cuenta...' : 'Registrarse como ' + establishmentInfo.role }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
