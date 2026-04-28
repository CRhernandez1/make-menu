<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[9999] flex flex-col gap-2.5 max-w-sm">
      <TransitionGroup name="toast">
        <div
          v-for="t in toasts"
          :key="t.id"
          class="flex items-center gap-3 px-5 py-3.5 rounded-2xl text-sm font-medium shadow-lg border-[1.5px] backdrop-blur-sm"
          :class="toastClass(t.type)"
        >
          <svg v-if="t.type === 'success'" class="shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          <svg v-else-if="t.type === 'error'" class="shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          <svg v-else class="shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          <span class="flex-1">{{ t.message }}</span>
          <button @click="dismiss(t.id)" class="text-current opacity-40 hover:opacity-80 text-lg leading-none bg-transparent border-none cursor-pointer">&times;</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const { toasts, dismiss } = useToast()

const toastClass = (type: string) => {
  switch (type) {
    case 'success': return 'bg-green-soft text-green-forest border-border-green'
    case 'error': return 'bg-danger-soft text-danger border-[rgba(185,60,60,0.15)]'
    case 'warning': return 'bg-warning-soft text-warning border-[rgba(196,138,26,0.15)]'
    default: return 'bg-cream text-text-sec border-border-green'
  }
}
</script>

<style scoped>
.toast-enter-active { transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1); }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from { opacity: 0; transform: translateX(40px); }
.toast-leave-to { opacity: 0; transform: translateX(40px) scale(0.95); }
.toast-move { transition: transform 0.3s ease; }
</style>