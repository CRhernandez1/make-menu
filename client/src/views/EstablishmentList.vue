<template>
  <div class="px-8 py-8 lg:px-12 lg:py-10">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-extrabold text-[#1a1a2e] tracking-tight">Establishments</h1>
      <p class="text-[15px] text-gray-400 mt-1">Select a location to manage its floor plan and tables.</p>
    </div>

    <!-- Error -->
    <div v-if="store.error"
      class="flex items-center gap-3 p-4 rounded-xl text-sm mb-6 bg-red-50 text-red-600 border border-red-100">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="15" y1="9" x2="9" y2="15" />
        <line x1="9" y1="9" x2="15" y2="15" />
      </svg>
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError"
        class="text-red-300 hover:text-red-500 cursor-pointer text-xl leading-none bg-transparent border-none">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div v-for="n in 6" :key="n" class="bg-white rounded-2xl border border-gray-100 p-6 animate-pulse">
        <div class="flex items-center gap-4 mb-5">
          <div class="w-12 h-12 rounded-xl bg-gray-100"></div>
          <div class="flex-1 space-y-2">
            <div class="h-4 w-2/3 rounded bg-gray-100"></div>
            <div class="h-3 w-1/2 rounded bg-gray-100"></div>
          </div>
        </div>
        <div class="space-y-2">
          <div class="h-3 w-full rounded bg-gray-100"></div>
          <div class="h-3 w-3/4 rounded bg-gray-100"></div>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div v-else-if="store.establishments.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <router-link v-for="est in store.establishments" :key="est.id" :to="{ name: 'tables', params: { cif: est.cif } }"
        class="group bg-white rounded-2xl border border-gray-100 p-6 no-underline text-inherit transition-all duration-200 hover:border-emerald-200 hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)] hover:-translate-y-0.5">
        <!-- Top row -->
        <div class="flex items-start justify-between mb-5">
          <div class="w-12 h-12 rounded-xl bg-[#1a1a2e] text-white text-lg font-bold flex items-center justify-center">
            {{ est.name.charAt(0) }}
          </div>
          <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full" :class="est.opened
            ? 'bg-emerald-50 text-emerald-600'
            : 'bg-gray-50 text-gray-400'">
            <span class="w-1.5 h-1.5 rounded-full" :class="est.opened ? 'bg-emerald-500' : 'bg-gray-300'"></span>
            {{ est.opened ? 'Open' : 'Closed' }}
          </span>
        </div>

        <!-- Name -->
        <h3 class="text-[16px] font-bold text-[#1a1a2e] mb-0.5 truncate">{{ est.name }}</h3>
        <p class="text-[13px] text-gray-400 mb-4 truncate">{{ est.legal_name }}</p>

        <!-- Details -->
        <div class="space-y-2.5 mb-5">
          <div class="flex items-start gap-2.5 text-[13px] text-gray-500 leading-snug">
            <svg class="text-gray-300 shrink-0 mt-0.5" width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            <span>{{ est.address }}, {{ est.city }}</span>
          </div>
          <div class="flex items-center gap-2.5 text-[13px] text-gray-500">
            <svg class="text-gray-300 shrink-0" width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path
                d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.6.7 2.33a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.52.57 2.33.7A2 2 0 0 1 22 16.92z" />
            </svg>
            <span>{{ est.phone || '—' }}</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <span class="text-[11px] font-semibold text-gray-300 tracking-wider font-mono">{{ est.cif }}</span>
          <div
            class="flex items-center gap-1.5 text-xs font-medium text-gray-300 transition-colors group-hover:text-emerald-500">
            <span class="hidden group-hover:inline">Manage</span>
            <svg class="w-4 h-4 transition-transform group-hover:translate-x-0.5" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border border-dashed border-gray-200 rounded-2xl">
      <div class="w-16 h-16 rounded-2xl bg-gray-50 flex items-center justify-center mx-auto mb-5">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#c4c9d4" stroke-width="1.5"
          stroke-linecap="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
          <polyline points="9 22 9 12 15 12 15 22" />
        </svg>
      </div>
      <h3 class="text-base font-bold text-[#1a1a2e] mb-1">No establishments yet</h3>
      <p class="text-sm text-gray-400">Create your first establishment to get started.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useEstablishmentStore } from '@/stores/establishmentStore'

const store = useEstablishmentStore()
onMounted(() => { store.fetchEstablishments() })
</script>