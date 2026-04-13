<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
        <div class="bg-white rounded-2xl max-w-[420px] w-full shadow-[0_20px_60px_rgba(0,0,0,0.15)] overflow-hidden">
          <div class="flex items-start justify-between px-6 pt-6 pb-1">
            <div>
              <h3 class="text-lg font-bold text-[#1a1a2e]">Change Role</h3>
              <p class="text-sm text-gray-400 mt-0.5">Update role for {{ memberName }}.</p>
            </div>
            <button @click="$emit('close')" class="bg-transparent border-none text-gray-300 cursor-pointer p-2 -mr-2 rounded-lg flex hover:bg-gray-100 hover:text-gray-500 transition-all">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <div class="px-6 py-5">
            <Transition name="error">
              <div v-if="error" class="flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-100 rounded-xl mb-5 text-sm text-red-600">
                <svg class="shrink-0 mt-0.5" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Role</label>
            <div class="flex flex-col gap-2 mb-6">
              <button
                v-for="r in roles" :key="r.value"
                @click="selectedRole = r.value"
                class="flex items-center gap-3 p-3.5 rounded-xl border-[1.5px] cursor-pointer transition-all text-left"
                :class="selectedRole === r.value
                  ? 'border-emerald-400 bg-emerald-50/50'
                  : 'border-gray-200 bg-white hover:border-gray-300'"
              >
                <span class="w-8 h-8 rounded-lg flex items-center justify-center text-sm"
                  :class="selectedRole === r.value ? 'bg-emerald-500 text-white' : 'bg-gray-100 text-gray-400'">
                  {{ r.icon }}
                </span>
                <div>
                  <span class="block text-sm font-semibold text-[#1a1a2e]">{{ r.label }}</span>
                  <span class="block text-xs text-gray-400 mt-0.5">{{ r.description }}</span>
                </div>
              </button>
            </div>

            <div class="flex gap-3 justify-end">
              <button @click="$emit('close')" class="py-2.5 px-5 rounded-xl text-sm font-semibold cursor-pointer border-none bg-gray-100 text-gray-500 hover:bg-gray-200 transition-colors">Cancel</button>
              <button
                @click="$emit('submit', selectedRole)"
                :disabled="submitting || selectedRole === currentRole"
                class="inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold cursor-pointer border-none bg-emerald-500 text-white hover:bg-emerald-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
              >
                <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Save
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
  { value: 'manager', label: 'Manager', icon: '👔', description: 'Full access to all settings and staff.' },
  { value: 'waiter', label: 'Waiter', icon: '🍽️', description: 'Can manage tables and take orders.' },
  { value: 'kitchen', label: 'Kitchen', icon: '👨‍🍳', description: 'Can view and manage orders.' }
]

watch(() => props.visible, (v) => {
  if (v) selectedRole.value = props.currentRole
})
</script>

<style scoped>
.error-enter-active { animation: shakeIn 0.35s ease; }
.error-leave-active { transition: opacity 0.15s ease; }
.error-leave-to { opacity: 0; }
@keyframes shakeIn {
  0% { opacity: 0; transform: translateX(-6px); }
  25% { transform: translateX(4px); }
  50% { transform: translateX(-2px); }
  75% { transform: translateX(1px); }
  100% { opacity: 1; transform: translateX(0); }
}
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-active > div, .modal-leave-active > div { transition: transform 0.2s ease, opacity 0.2s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: translateY(12px) scale(0.97); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: translateY(-8px) scale(0.97); opacity: 0; }
</style>