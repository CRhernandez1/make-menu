<template>
  <div class="flex h-screen bg-gray-50">

    <aside
      class="flex flex-col bg-white border-r border-gray-200 transition-all duration-300 relative"
      :class="isCollapsed ? 'w-16' : 'w-56'"
    >

      <div class="flex items-center gap-3 px-4 py-5 border-b border-gray-200 overflow-hidden">
        <div class="flex items-center justify-center w-9 h-9 min-w-[36px] bg-emerald-500 rounded-xl">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="8.5" cy="7" r="4"/>
            <path d="M20 8v6M23 11h-6"/>
          </svg>
        </div>
        <span v-if="!isCollapsed" class="font-bold text-gray-700 text-sm tracking-tight whitespace-nowrap">
          Panel Camarero
        </span>
      </div>

      <button
        @click="isCollapsed = !isCollapsed"
        class="absolute -right-3 top-6 w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center shadow-md z-10 hover:bg-emerald-600 transition-colors"
      >
        <svg
          class="w-3 h-3 text-white transition-transform duration-300"
          :class="isCollapsed ? 'rotate-180' : ''"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
        >
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>

      <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
        <RouterLink
          v-for="item in navItems"
          :key="item.id"
          :to="{ name: item.routeName }"
          :title="isCollapsed ? item.label : ''"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors duration-150"
          :class="route.name === item.routeName
            ? 'bg-emerald-500 text-white'
            : 'text-gray-700 hover:bg-emerald-50 hover:text-emerald-700'"
        >
          <span class="flex-shrink-0 w-5 h-5" v-html="item.icon"></span>

          <span v-if="!isCollapsed" class="text-sm font-medium whitespace-nowrap flex-1">
            {{ item.label }}
          </span>

          <span
            v-if="!isCollapsed && item.badge"
            class="text-xs font-semibold px-2 py-0.5 rounded-full"
            :class="route.name === item.routeName ? 'bg-white text-emerald-600' : 'bg-emerald-100 text-emerald-700'"
          >
            {{ item.badge }}
          </span>
        </RouterLink>
      </nav>

      <div class="border-t border-gray-200 p-3"></div>
    </aside>

    <div class="flex flex-col flex-1 overflow-hidden">

      <header class="bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between">
        <h1 class="text-lg font-bold text-gray-700 tracking-tight">{{ currentPageTitle }}</h1>
        <div>
          <button
            @click="handleLogout"
            class="px-5 py-2.5 bg-red-400 text-white font-semibold rounded-xl hover:bg-red-500 transition-all shadow-lg shadow-red-400/20"
          >
            Cerrar sesión
          </button>
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
  {
    id: 'pedidos',
    routeName: 'waiter-orders',
    label: 'Pedidos',
    badge: null,
    icon: `<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>`,
  },
]

const currentPageTitle = computed(() => {
  const currentItem = navItems.find(item => item.routeName === route.name)
  return currentItem ? currentItem.label : 'Panel Camarero'
})

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'home' })
}
</script>