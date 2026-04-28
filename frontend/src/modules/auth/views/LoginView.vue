<template>
  <div class="min-h-screen flex items-center justify-center bg-cream px-4 py-12 relative overflow-hidden">
    <!-- Blobs decorativos -->
    <div class="absolute w-[350px] h-[350px] top-[-120px] right-[-100px] pointer-events-none bg-green-soft-2" style="animation:blob-morph 8s ease-in-out infinite"></div>
    <div class="absolute w-[280px] h-[280px] bottom-[-100px] left-[-80px] pointer-events-none bg-green-soft-2" style="animation:blob-morph 8s ease-in-out infinite;animation-delay:-4s"></div>

    <div class="max-w-[400px] w-full relative z-10" style="animation:fade-up 0.6s cubic-bezier(0.25,1,0.5,1)">
      <!-- Logo -->
      <div class="text-center mb-9">
        <svg viewBox="0 0 452 263" class="w-14 mx-auto mb-4" style="animation:float 5s ease-in-out infinite" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="#1A5C2E"/></svg>
        <h1 class="font-display text-[26px] font-bold text-green-forest tracking-tight">Iniciar sesión</h1>
        <p class="text-sm text-text-sec mt-1">Accede a tu cuenta de MakeMenu</p>
      </div>

      <!-- Card -->
      <div class="bg-white border border-border-green rounded-[24px] p-8 shadow-md">
        <!-- Error -->
        <div
          v-if="errorMessage"
          class="mb-5 p-4 bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] rounded-2xl text-danger text-sm flex items-center gap-3"
          style="animation:fade-up 0.3s ease"
        >
          <svg class="w-5 h-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          {{ errorMessage }}
        </div>

        <form @submit.prevent="onLogin">
          <!-- Usuario -->
          <div class="mb-5">
            <label for="username" class="block text-[13px] font-semibold text-text-main mb-1.5">Usuario</label>
            <input
              v-model="form.username"
              ref="usernameInputRef"
              type="text"
              id="username"
              name="username"
              placeholder="tu.usuario"
              class="input-mm"
              autocomplete="off"
            />
          </div>

          <!-- Contraseña -->
          <div class="mb-5">
            <label for="password" class="block text-[13px] font-semibold text-text-main mb-1.5">Contraseña</label>
            <input
              v-model="form.password"
              ref="passwordInputRef"
              type="password"
              id="password"
              name="password"
              placeholder="••••••••"
              class="input-mm"
              autocomplete="off"
            />
          </div>

          <!-- Recordar + olvidaste -->
          <div class="flex items-center justify-between mb-6">
            <label for="remember" class="flex items-center gap-2.5 cursor-pointer group">
              <div
                class="w-[22px] h-[22px] rounded-[7px] border-2 flex items-center justify-center transition-all"
                :class="form.rememberMe
                  ? 'bg-green-forest border-green-forest scale-105'
                  : 'border-[rgba(26,92,46,0.2)] group-hover:border-[rgba(26,92,46,0.3)]'"
              >
                <svg v-if="form.rememberMe" class="w-3 h-3 text-cream" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
              <input v-model="form.rememberMe" type="checkbox" id="remember" class="sr-only" />
              <span class="text-[13px] text-text-sec">Recordar</span>
            </label>
            <a href="#" class="text-[13px] text-green-medium font-medium hover:text-green-forest transition-colors">¿Olvidaste?</a>
          </div>

          <!-- Botón -->
          <button
            type="submit"
            class="btn-mm btn-primary w-full h-[50px] text-[15px]"
          >
            Ingresar →
          </button>
        </form>
      </div>

      <!-- Footer -->
      <p class="text-center mt-6 text-sm text-text-sec">
        ¿No tienes cuenta?
        <RouterLink :to="{ name: 'register' }" class="text-green-medium font-semibold hover:text-green-forest transition-colors">
          Crear cuenta
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.store'

const authStore = useAuthStore()
const router = useRouter()

const usernameInputRef = ref<HTMLInputElement | null>(null)
const passwordInputRef = ref<HTMLInputElement | null>(null)
const errorMessage = ref('')

const form = reactive({
  username: '',
  password: '',
  rememberMe: false,
})

onMounted(() => {
  const savedUsername = localStorage.getItem('saved_username')
  if (savedUsername) {
    form.username = savedUsername
    form.rememberMe = true
  }
})

const onLogin = async () => {
  errorMessage.value = ''

  if (!form.username) return usernameInputRef.value?.focus()
  if (form.password.length < 3) return passwordInputRef.value?.focus()

  localStorage[form.rememberMe ? 'setItem' : 'removeItem']('saved_username', form.username)

  const result = await authStore.login(form.username, form.password, form.rememberMe)

  if (result.ok) {
    const roleRoutes: Record<string, string> = {
      manager: 'manager',
      waiter: 'waiter',
      kitchen: 'kitchen',
    }
    router.push({ name: roleRoutes[result.role ?? ''] ?? 'home' })
    return
  }

  errorMessage.value = result.message || 'Usuario/Contraseña no son correctos'
}
</script>