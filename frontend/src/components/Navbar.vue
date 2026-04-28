<template>
  <header class="sticky top-0 z-50 border-b border-border-green-light" style="background:rgba(250,245,240,0.92);backdrop-filter:blur(20px)">
    <div class="max-w-7xl mx-auto px-6 py-3.5 flex items-center justify-between">
      <RouterLink :to="{ name: 'home' }" class="flex items-center gap-2.5 group">
        <div class="flex items-center justify-center w-9 h-9 bg-green-forest rounded-xl transition-transform group-hover:scale-105">
          <svg viewBox="0 0 452 263" width="18" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="white"/></svg>
        </div>
        <span class="text-sm font-extrabold text-green-forest tracking-tight">MakeMenu</span>
      </RouterLink>

      <div>
        <button
          v-if="authStore.isAuthenticated"
          @click="onLogout"
          class="btn-mm btn-ghost text-sm px-5 py-2.5"
          style="font-size:13px"
        >
          Cerrar sesión
        </button>
        <RouterLink
          v-else
          :to="{ name: 'login' }"
          class="btn-mm btn-primary text-sm px-5 py-2.5"
          style="font-size:13px"
        >
          Acceder
        </RouterLink>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const router = useRouter()
const authStore = useAuthStore()

const onLogout = async () => {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>