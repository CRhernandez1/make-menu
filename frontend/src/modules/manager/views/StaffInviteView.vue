<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="font-display text-2xl font-bold text-green-forest tracking-tight mb-6">Invitar equipo</h1>

    <div class="card-mm p-7 !cursor-default !transform-none space-y-6">
      <div>
        <h2 class="font-display text-lg font-bold text-ink tracking-tight mb-2">Invitar nuevo personal</h2>
        <p class="text-sm text-text-sec leading-relaxed">
          Genera un código QR temporal para que un nuevo miembro se registre y se una automáticamente a tu establecimiento.
        </p>
      </div>

      <!-- Rol -->
      <div>
        <label class="block text-[13px] font-semibold text-text-main mb-1.5">Rol del invitado</label>
        <select v-model="selectedRole" class="input-mm !w-full sm:!w-1/2 cursor-pointer">
          <option value="waiter">Camarero (Sala)</option>
          <option value="kitchen">Cocinero (Cocina)</option>
        </select>
      </div>

      <!-- Establecimiento -->
      <div v-if="establishments.length > 1">
        <label class="block text-[13px] font-semibold text-text-main mb-1.5">Establecimiento</label>
        <select v-model="selectedEstablishment" class="input-mm !w-full sm:!w-1/2 cursor-pointer">
          <option v-for="est in establishments" :key="est.id" :value="est.id">
            {{ est.name }}
          </option>
        </select>
      </div>

      <!-- Botón -->
      <button
        @click="generateQR"
        :disabled="isLoading"
        class="btn-mm btn-primary text-[14px] px-6 py-3 disabled:opacity-50 disabled:transform-none disabled:cursor-not-allowed"
      >
        <svg v-if="!isLoading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
          <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3"/><path d="M21 14v3h-3"/><path d="M14 21h7"/>
        </svg>
        <span v-if="isLoading" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
        {{ isLoading ? 'Generando...' : 'Generar código QR' }}
      </button>

      <!-- QR Result -->
      <div v-if="inviteUrl" class="pt-6 border-t border-border-green-light flex flex-col items-center" style="animation:fade-up 0.4s cubic-bezier(0.25,1,0.5,1)">
        <div class="w-14 h-14 rounded-full bg-green-soft flex items-center justify-center mb-4">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.8" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <h3 class="font-display text-lg font-bold text-ink mb-1">¡Código listo!</h3>
        <p class="text-sm text-text-muted mb-6 text-center max-w-sm">Pide al nuevo integrante que escanee este código con su móvil.</p>

        <div class="bg-white p-5 rounded-2xl border border-border-green shadow-md mb-6">
          <qrcode-vue :value="inviteUrl" :size="220" level="H" />
        </div>

        <p class="text-xs text-text-muted mb-3">También puedes enviarle este enlace:</p>
        <div class="flex items-center bg-cream border border-border-green rounded-[var(--radius-input)] w-full max-w-md overflow-hidden">
          <input
            type="text"
            readonly
            :value="inviteUrl"
            class="bg-transparent text-text-sec px-4 py-3 w-full outline-none text-[13px] font-mono"
          />
          <button
            @click="copyLink"
            class="px-4 py-3 bg-green-soft text-green-forest text-[12px] font-semibold hover:bg-[rgba(26,92,46,0.12)] transition-colors whitespace-nowrap border-l border-border-green"
          >
            {{ copied ? '¡Copiado!' : 'Copiar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import QrcodeVue from 'qrcode.vue'
import { makeMenuApi } from '@/api/makeMenu'

const selectedRole = ref('waiter')
const selectedEstablishment = ref<number | null>(null)
const establishments = ref<any[]>([])
const isLoading = ref(false)
const inviteUrl = ref<string | null>(null)
const copied = ref(false)

onMounted(async () => {
  try {
    const res = await makeMenuApi.get('/establishments/')
    establishments.value = res.data
    if (establishments.value.length > 0) {
      selectedEstablishment.value = establishments.value[0].id
    }
  } catch (error) {
    console.error('Error fetching establishments', error)
  }
})

const generateQR = async () => {
  isLoading.value = true
  try {
    const payload: any = { role: selectedRole.value }
    if (selectedEstablishment.value) {
      payload.establishment_id = selectedEstablishment.value
    }
    const response = await makeMenuApi.post('/establishments/invite/', payload)
    const invitationId = response.data.invitation_id
    const frontendDomain = window.location.origin
    inviteUrl.value = `${frontendDomain}/register?code=${invitationId}`
  } catch (error) {
    console.error('Error al generar la invitación', error)
  } finally {
    isLoading.value = false
  }
}

const copyLink = async () => {
  if (!inviteUrl.value) return
  try {
    await navigator.clipboard.writeText(inviteUrl.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // fallback
  }
}
</script>