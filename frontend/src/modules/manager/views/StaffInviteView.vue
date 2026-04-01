<template>
  <div class="p-8 max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold text-white mb-6">Gestionar Equipo</h1>

    <div class="bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-700">
      <h2 class="text-xl text-green-400 mb-4">Invitar nuevo personal</h2>
      <p class="text-gray-400 mb-6">
        Genera un código QR temporal para que un nuevo camarero se registre y se una automáticamente
        a este restaurante.
      </p>

      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-300 mb-2">Rol del invitado</label>
        <select
          v-model="selectedRole"
          class="bg-gray-900 border border-gray-600 text-white rounded-lg p-2.5 w-full md:w-1/2"
        >
          <option value="waiter">Camarero (Sala)</option>
          <option value="kitchen">Cocinero (Cocina)</option>
        </select>
      </div>

      <button
        @click="generateQR"
        :disabled="isLoading"
        class="bg-green-500 hover:bg-green-400 text-gray-900 font-bold py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
      >
        {{ isLoading ? 'Generando...' : 'Generar Pase VIP' }}
      </button>

      <div v-if="inviteUrl" class="mt-8 pt-8 border-t border-gray-700 flex flex-col items-center">
        <h3 class="text-lg font-semibold text-white mb-4">¡Escanea este código!</h3>

        <div class="bg-white p-4 rounded-xl shadow-inner mb-4">
          <qrcode-vue :value="inviteUrl" :size="250" level="H" />
        </div>

        <p class="text-sm text-gray-400 text-center max-w-md">
          Pide al nuevo integrante que escanee este código con su móvil. También puedes enviarle
          este enlace:
        </p>

        <div
          class="mt-4 flex items-center bg-gray-900 rounded-lg border border-gray-700 w-full max-w-md"
        >
          <input
            type="text"
            readonly
            :value="inviteUrl"
            class="bg-transparent text-gray-300 px-4 py-2 w-full outline-none text-sm"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import QrcodeVue from 'qrcode.vue' // Importamos la librería
import { makeMenuApi } from '@/api/makeMenu'

const selectedRole = ref('waiter')
const isLoading = ref(false)
const inviteUrl = ref<string | null>(null)

const generateQR = async () => {
  isLoading.value = true

  try {
    // 1. Llamamos al endpoint de Django que hicimos antes
    const response = await makeMenuApi.post('/establishments/invite/', {
      role: selectedRole.value,
    })

    // 2. Django nos devuelve el UUID secreto
    const invitationId = response.data.invitation_id

    // 3. Construimos la URL completa de tu frontend (ej. http://localhost:5173/register?code=uuid)
    // window.location.origin pilla tu dominio actual automáticamente
    const frontendDomain = window.location.origin
    inviteUrl.value = `${frontendDomain}/register?code=${invitationId}`
  } catch (error) {
    console.error('Error al generar la invitación', error)
    // Aquí pondrías un toast de error si falla
  } finally {
    isLoading.value = false
  }
}
</script>
