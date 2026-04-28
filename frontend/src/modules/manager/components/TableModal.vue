<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
        <div class="bg-white rounded-[28px] max-w-[440px] w-full shadow-[0_40px_100px_rgba(26,92,46,0.12)] overflow-hidden">
          <!-- Header -->
          <div class="flex items-start justify-between px-7 pt-7 pb-2">
            <div>
              <h3 class="font-display text-lg font-bold text-ink tracking-tight">{{ isEditing ? 'Editar mesa' : 'Nueva mesa' }}</h3>
              <p class="text-[13px] text-text-muted mt-1">{{ isEditing ? 'Actualiza la configuración de la mesa.' : 'Añade una nueva mesa al establecimiento.' }}</p>
            </div>
            <button @click="$emit('close')" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- Body -->
          <form @submit.prevent="handleSubmit" class="px-7 py-5">
            <!-- Error -->
            <Transition name="error">
              <div v-if="error" class="flex items-start gap-3 p-4 bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] rounded-2xl mb-5 text-sm text-danger leading-relaxed">
                <svg class="shrink-0 mt-0.5 w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <!-- Number -->
            <div v-if="!isEditing" class="mb-5">
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Número de mesa</label>
              <input
                v-model.number="localNumber" type="number" min="1" required
                placeholder="Ej: 1, 2, 3..."
                class="input-mm [-moz-appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none"
                :class="error && !isEditing ? '!border-danger focus:!shadow-[0_0_0_4px_rgba(185,60,60,0.06)]' : ''"
                @input="$emit('clear-error')"
              />
              <p class="text-xs text-text-muted mt-1.5">Número visible para el staff y los clientes.</p>
            </div>

            <!-- Guests -->
            <div class="mb-7">
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Capacidad máxima</label>
              <div
                class="flex items-center border-[1.5px] rounded-[var(--radius-input)] overflow-hidden transition-all"
                :class="error && isEditing
                  ? 'border-danger focus-within:shadow-[0_0_0_4px_rgba(185,60,60,0.06)]'
                  : 'border-border-green focus-within:border-green-medium focus-within:shadow-[0_0_0_4px_rgba(26,92,46,0.06)]'"
              >
                <button type="button" @click="dec" :disabled="localMaxGuests <= 1"
                  class="w-12 h-[48px] border-none bg-cream text-text-sec cursor-pointer flex items-center justify-center transition-colors hover:bg-green-soft hover:text-green-forest disabled:opacity-25 disabled:cursor-not-allowed">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>
                </button>
                <input v-model.number="localMaxGuests" type="number" min="1" max="50" required
                  class="flex-1 h-[48px] border-none text-center text-xl font-bold text-ink bg-transparent outline-none font-display [-moz-appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none"
                  @input="$emit('clear-error')"
                />
                <button type="button" @click="inc" :disabled="localMaxGuests >= 50"
                  class="w-12 h-[48px] border-none bg-cream text-text-sec cursor-pointer flex items-center justify-center transition-colors hover:bg-green-soft hover:text-green-forest disabled:opacity-25 disabled:cursor-not-allowed">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                </button>
              </div>
              <p class="text-xs text-text-muted mt-1.5">Número de comensales que caben en esta mesa.</p>
            </div>

            <!-- Footer -->
            <div class="flex gap-3 justify-end">
              <button type="button" @click="$emit('close')" class="btn-mm btn-ghost text-[13px] px-5 py-2.5">Cancelar</button>
              <button type="submit" :disabled="submitting"
                class="btn-mm btn-primary text-[13px] px-5 py-2.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                <span v-if="submitting" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
                {{ isEditing ? 'Guardar cambios' : 'Añadir mesa' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Table } from '@/types/table'

const props = defineProps<{
  visible: boolean
  table?: Table | null
  error?: string | null
  submitting?: boolean
}>()

const emit = defineEmits<{
  close: []
  submit: [number: number, maxGuests: number]
  'clear-error': []
}>()

const localNumber = ref(1)
const localMaxGuests = ref(4)
const isEditing = ref(false)

watch(() => props.visible, (v) => {
  if (v) {
    if (props.table) {
      localNumber.value = props.table.number
      localMaxGuests.value = props.table.max_guests
      isEditing.value = true
    } else {
      localNumber.value = 1; localMaxGuests.value = 4; isEditing.value = false
    }
  }
})

const inc = () => { if (localMaxGuests.value < 50) localMaxGuests.value++ }
const dec = () => { if (localMaxGuests.value > 1) localMaxGuests.value-- }
const handleSubmit = () => { emit('submit', localNumber.value, localMaxGuests.value) }
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