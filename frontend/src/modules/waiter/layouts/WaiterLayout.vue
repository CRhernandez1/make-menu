<template>
  <div class="flex h-screen bg-cream">

    <aside
      class="flex flex-col bg-white border-r border-border-green-light transition-all duration-300 relative"
      :class="isCollapsed ? 'w-16' : 'w-56'"
    >
      <div class="flex items-center gap-2.5 px-4 py-5 border-b border-border-green-light overflow-hidden">
        <div class="flex items-center justify-center w-9 h-9 min-w-[36px] bg-green-medium rounded-xl">
          <svg viewBox="0 0 452 263" width="18" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="white"/></svg>
        </div>
        <span v-if="!isCollapsed" class="text-sm font-extrabold text-green-forest tracking-tight whitespace-nowrap">Camarero</span>
      </div>

      <button
        @click="isCollapsed = !isCollapsed"
        class="absolute -right-3 top-6 w-6 h-6 bg-green-forest rounded-full flex items-center justify-center shadow-md z-10 hover:bg-green-medium transition-colors"
      >
        <svg class="w-3 h-3 text-cream transition-transform duration-300" :class="isCollapsed ? 'rotate-180' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
      </button>

      <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto scrollbar-hide">
        <RouterLink
          v-for="item in navItems" :key="item.id"
          :to="{ name: item.routeName }"
          :title="isCollapsed ? item.label : ''"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-[14px] text-left transition-all duration-200"
          :class="route.name === item.routeName
            ? 'bg-green-forest text-cream shadow-[0_2px_12px_rgba(26,92,46,0.2)]'
            : 'text-text-sec hover:bg-green-soft hover:text-green-forest'"
        >
          <span class="flex-shrink-0 w-5 h-5" v-html="item.icon"></span>
          <span v-if="!isCollapsed" class="text-[13px] font-medium whitespace-nowrap flex-1">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="border-t border-border-green-light p-2">
        <button
          @click="handleLogout"
          :title="isCollapsed ? 'Cerrar sesión' : ''"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-[14px] text-text-muted hover:bg-danger-soft hover:text-danger transition-all duration-200"
        >
          <svg class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          <span v-if="!isCollapsed" class="text-[13px] font-medium whitespace-nowrap">Cerrar sesión</span>
        </button>
      </div>
    </aside>

    <div class="flex flex-col flex-1 overflow-hidden">
      <header class="bg-white border-b border-border-green-light px-8 py-4 flex items-center justify-between">
        <div>
          <h1 class="font-display text-lg font-bold text-ink tracking-tight">{{ currentPageTitle }}</h1>
          <p v-if="authStore.user?.username" class="text-xs text-text-muted mt-0.5">{{ authStore.user.username }}</p>
        </div>
      </header>
      <main class="flex-1 overflow-y-auto p-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute, RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const isCollapsed = ref(false)

const navItems = [
  { id: 'mesas', routeName: 'waiter', label: 'Mesas', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>` },
  { id: 'pedidos', routeName: 'waiter-orders', label: 'Pedidos', icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>` },
]

const currentPageTitle = computed(() => {
  const item = navItems.find(i => i.routeName === route.name)
  return item ? item.label : 'Panel Camarero'
})

const handleLogout = async () => { await authStore.logout(); router.push({ name: 'home' }) }
</script>