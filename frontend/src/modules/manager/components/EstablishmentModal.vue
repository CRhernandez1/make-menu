<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
        <div class="bg-white rounded-[28px] max-w-[560px] w-full shadow-[0_40px_100px_rgba(26,92,46,0.12)] overflow-hidden max-h-[90vh] flex flex-col">
          <!-- Header -->
          <div class="flex items-start justify-between px-7 pt-7 pb-2 shrink-0">
            <div>
              <h3 class="font-display text-lg font-bold text-ink tracking-tight">{{ isEditing ? 'Editar establecimiento' : 'Nuevo establecimiento' }}</h3>
              <p class="text-[13px] text-text-muted mt-1">{{ isEditing ? 'Actualiza los datos del establecimiento.' : 'Añade un nuevo local a tu cuenta.' }}</p>
            </div>
            <button @click="$emit('close')" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- Body -->
          <form @submit.prevent="handleSubmit" class="px-7 py-5 overflow-y-auto flex-1">
            <!-- Error -->
            <Transition name="error">
              <div v-if="error" class="flex items-start gap-3 p-4 bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] rounded-2xl mb-5 text-sm text-danger leading-relaxed">
                <svg class="shrink-0 mt-0.5 w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <!-- CIF -->
            <div v-if="!isEditing" class="mb-5">
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">CIF</label>
              <input
                v-model="form.cif"
                type="text" required
                placeholder="Ej: B12345678"
                class="input-mm uppercase"
                @input="$emit('clear-error')"
              />
              <p class="text-xs text-text-muted mt-1.5">Identificación fiscal única del establecimiento.</p>
            </div>

            <!-- Name + Legal Name -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Nombre</label>
                <input v-model="form.name" type="text" required placeholder="Ej: Bar La Terraza" class="input-mm" @input="$emit('clear-error')" />
              </div>
              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Razón social</label>
                <input v-model="form.legal_name" type="text" required placeholder="Ej: La Terraza S.L." class="input-mm" @input="$emit('clear-error')" />
              </div>
            </div>

            <!-- Description -->
            <div class="mb-5">
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Descripción</label>
              <textarea
                v-model="form.description"
                rows="2"
                placeholder="Breve descripción del establecimiento..."
                class="input-mm !h-auto py-3 resize-none"
                @input="$emit('clear-error')"
              ></textarea>
            </div>

            <!-- Address -->
            <div class="mb-5">
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Dirección</label>
              <input v-model="form.address" type="text" required placeholder="Ej: Calle Mayor 12" class="input-mm" @input="$emit('clear-error')" />
            </div>

            <!-- City + Zip -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Ciudad</label>
                <input v-model="form.city" type="text" required placeholder="Ej: Santa Cruz" class="input-mm" @input="$emit('clear-error')" />
              </div>
              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Código postal</label>
                <input v-model="form.zip_code" type="text" required placeholder="Ej: 38001" class="input-mm" @input="$emit('clear-error')" />
              </div>
            </div>

            <!-- Phone -->
            <div class="mb-7">
              <label class="block text-[13px] font-semibold text-text-main mb-1.5">Teléfono <span class="text-text-muted font-normal">(opcional)</span></label>
              <input v-model="form.phone" type="tel" placeholder="Ej: +34 922 123 456" class="input-mm" @input="$emit('clear-error')" />
            </div>

            <!-- Footer -->
            <div class="flex gap-3 justify-end">
              <button type="button" @click="$emit('close')" class="btn-mm btn-ghost text-[13px] px-5 py-2.5">Cancelar</button>
              <button
                type="submit" :disabled="submitting"
                class="btn-mm btn-primary text-[13px] px-5 py-2.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                <span v-if="submitting" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
                {{ isEditing ? 'Guardar cambios' : 'Crear establecimiento' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { reactive, watch, ref } from 'vue'
import type { Establishment } from '@/types/table'

const props = defineProps<{
  visible: boolean
  establishment?: Establishment | null
  error?: string | null
  submitting?: boolean
}>()

const emit = defineEmits<{
  close: []
  submit: [form: { cif: string; name: string; legal_name: string; description: string; zip_code: string; city: string; address: string; phone: string }]
  'clear-error': []
}>()

const isEditing = ref(false)

const form = reactive({
  cif: '', name: '', legal_name: '', description: '',
  zip_code: '', city: '', address: '', phone: ''
})

function resetForm() {
  form.cif = ''; form.name = ''; form.legal_name = ''; form.description = ''
  form.zip_code = ''; form.city = ''; form.address = ''; form.phone = ''
}

watch(() => props.visible, (v) => {
  if (v) {
    if (props.establishment) {
      isEditing.value = true
      form.cif = props.establishment.cif; form.name = props.establishment.name
      form.legal_name = props.establishment.legal_name; form.description = props.establishment.description
      form.zip_code = props.establishment.zip_code; form.city = props.establishment.city
      form.address = props.establishment.address; form.phone = props.establishment.phone
    } else { isEditing.value = false; resetForm() }
  }
})

const handleSubmit = () => { emit('submit', { ...form }) }
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