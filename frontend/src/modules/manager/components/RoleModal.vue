<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
        <div class="bg-white rounded-[28px] max-w-[420px] w-full shadow-[0_40px_100px_rgba(26,92,46,0.12)] overflow-hidden">
          <div class="flex items-start justify-between px-7 pt-7 pb-2">
            <div>
              <h3 class="font-display text-lg font-bold text-ink tracking-tight">Cambiar rol</h3>
              <p class="text-[13px] text-text-muted mt-1">Actualizar rol de {{ memberName }}.</p>
            </div>
            <button @click="$emit('close')" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <div class="px-7 py-5">
            <Transition name="error">
              <div v-if="error" class="flex items-start gap-3 p-4 bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] rounded-2xl mb-5 text-sm text-danger">
                <svg class="shrink-0 mt-0.5 w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <label class="block text-[13px] font-semibold text-text-main mb-3">Rol</label>
            <div class="flex flex-col gap-2.5 mb-7">
              <button
                v-for="r in roles" :key="r.value"
                @click="selectedRole = r.value"
                class="flex items-center gap-3.5 p-4 rounded-2xl border-[1.5px] cursor-pointer transition-all text-left"
                :class="selectedRole === r.value
                  ? 'border-green-medium bg-green-soft'
                  : 'border-border-green bg-white hover:border-[rgba(26,92,46,0.2)] hover:bg-green-soft-2'"
              >
                <span
                  class="w-9 h-9 rounded-xl flex items-center justify-center transition-all"
                  :class="selectedRole === r.value ? r.activeClass : 'bg-cream text-text-muted'"
                >
                  <span v-html="r.icon"></span>
                </span>
                <div>
                  <span class="block text-sm font-bold text-ink">{{ r.label }}</span>
                  <span class="block text-xs text-text-muted mt-0.5">{{ r.description }}</span>
                </div>
                <div class="ml-auto">
                  <div
                    class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all"
                    :class="selectedRole === r.value ? 'border-green-forest bg-green-forest' : 'border-text-ghost'"
                  >
                    <svg v-if="selectedRole === r.value" class="w-3 h-3 text-cream" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                  </div>
                </div>
              </button>
            </div>

            <div class="flex gap-3 justify-end">
              <button @click="$emit('close')" class="btn-mm btn-ghost text-[13px] px-5 py-2.5">Cancelar</button>
              <button
                @click="$emit('submit', selectedRole)"
                :disabled="submitting || selectedRole === currentRole"
                class="btn-mm btn-primary text-[13px] px-5 py-2.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <span v-if="submitting" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
                Guardar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  visible: boolean
  memberName: string
  currentRole: string
  error?: string | null
  submitting?: boolean
}>()

defineEmits<{
  close: []
  submit: [role: string]
}>()

const selectedRole = ref(props.currentRole)

const roles = [
  {
    value: 'manager', label: 'Manager',
    icon: `<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><path d="M20 8v6M23 11h-6"/></svg>`,
    description: 'Acceso total a configuración y equipo.',
    activeClass: 'bg-green-forest text-cream'
  },
  {
    value: 'waiter', label: 'Camarero',
    icon: `<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>`,
    description: 'Gestiona mesas y pedidos activos.',
    activeClass: 'bg-green-medium text-cream'
  },
  {
    value: 'kitchen', label: 'Cocina',
    icon: `<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>`,
    description: 'Ve y gestiona los pedidos en cocina.',
    activeClass: 'bg-warning text-white'
  }
]

watch(() => props.visible, (v) => {
  if (v) selectedRole.value = props.currentRole
})
</script>

<style scoped>
.error-enter-active { animation: shakeIn 0.35s ease; }
.error-leave-active { transition: opacity 0.15s ease; }
.error-leave-to { opacity: 0; }
@keyframes shakeIn { 0%{opacity:0;transform:translateX(-6px)} 25%{transform:translateX(4px)} 50%{transform:translateX(-2px)} 75%{transform:translateX(1px)} 100%{opacity:1;transform:translateX(0)} }
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: translateY(16px) scale(0.96); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: translateY(-8px) scale(0.97); opacity: 0; }
</style>