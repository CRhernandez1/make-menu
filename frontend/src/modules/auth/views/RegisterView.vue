<template>
  <div class="min-h-screen flex items-center justify-center bg-cream px-4 py-12 relative overflow-hidden">
    <div class="absolute w-[350px] h-[350px] top-[-120px] right-[-100px] pointer-events-none bg-green-soft-2" style="animation:blob-morph 8s ease-in-out infinite"></div>
    <div class="absolute w-[280px] h-[280px] bottom-[-100px] left-[-80px] pointer-events-none bg-green-soft-2" style="animation:blob-morph 8s ease-in-out infinite;animation-delay:-4s"></div>

    <div class="max-w-[420px] w-full relative z-10" style="animation:fade-up 0.6s cubic-bezier(0.25,1,0.5,1)">
      <!-- Logo -->
      <div class="text-center mb-9">
        <svg viewBox="0 0 452 263" class="w-14 mx-auto mb-4" style="animation:float 5s ease-in-out infinite" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="#1A5C2E"/></svg>
        <h2 class="font-display text-[26px] font-bold text-green-forest tracking-tight">Registro de equipo</h2>
        <p v-if="establishmentInfo.name" class="text-sm text-text-sec mt-1">
          Uniéndote a: <span class="text-ink font-semibold">{{ establishmentInfo.name }}</span>
        </p>
      </div>

      <!-- Validando -->
      <div v-if="isValidating" class="bg-white border border-border-green rounded-[24px] p-12 shadow-md text-center">
        <div class="w-10 h-10 border-[3px] border-green-soft border-t-green-forest rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-text-sec text-sm">Comprobando invitación...</p>
      </div>

      <!-- Error de invitación -->
      <div v-else-if="invitationError" class="bg-white border border-border-green rounded-[24px] p-10 shadow-md text-center">
        <div class="w-14 h-14 rounded-full bg-danger-soft flex items-center justify-center mx-auto mb-5">
          <svg class="w-7 h-7 text-danger" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        </div>
        <p class="font-display text-lg font-bold text-ink mb-2">Invitación no válida</p>
        <p class="text-sm text-text-sec mb-6">{{ invitationError }}</p>
        <button @click="router.push({ name: 'login' })" class="btn-mm btn-secondary text-sm">
          Volver al inicio
        </button>
      </div>

      <!-- Formulario -->
      <div v-else class="bg-white border border-border-green rounded-[24px] p-8 shadow-md">
        <!-- Error -->
        <div
          v-if="errorMessage"
          class="mb-5 p-4 bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] rounded-2xl text-danger text-sm flex items-center gap-3"
          style="animation:fade-up 0.3s ease"
        >
          <svg class="w-5 h-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label class="block text-[13px] font-semibold text-text-main mb-1.5">Usuario *</label>
            <input v-model="form.username" type="text" required class="input-mm" placeholder="tu.usuario" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Nombre *</label>
              <input v-model="form.first_name" type="text" required class="input-mm" placeholder="Daniele" />
            </div>
            <div>
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Apellidos *</label>
              <input v-model="form.last_name" type="text" required class="input-mm" placeholder="Dettori" />
            </div>
          </div>

          <div>
            <label class="block text-[13px] font-semibold text-text-main mb-1.5">Email *</label>
            <input v-model="form.email" type="email" required class="input-mm" placeholder="tu@email.com" />
          </div>

          <div>
            <label class="block text-[13px] font-semibold text-text-main mb-1.5">Contraseña *</label>
            <input v-model="form.password" type="password" required class="input-mm" placeholder="Mínimo 8 caracteres" />
          </div>

          <div>
            <label class="block text-[13px] font-semibold text-text-main mb-1.5">Teléfono
              <span class="text-text-muted font-normal">(opcional)</span>
            </label>
            <input v-model="form.phone" type="tel" class="input-mm" placeholder="+34 600 000 000" />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="btn-mm btn-primary w-full h-[50px] text-[15px] mt-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {{ isLoading ? 'Creando cuenta...' : 'Registrarse como ' + establishmentInfo.role + ' →' }}
          </button>
        </form>
      </div>

      <!-- Footer -->
      <p class="text-center mt-6 text-sm text-text-sec">
        ¿Ya tienes cuenta?
        <RouterLink :to="{ name: 'login' }" class="text-green-medium font-semibold hover:text-green-forest transition-colors">
          Iniciar sesión
        </RouterLink>
      </p>
    </div>
  </div>
</template>

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