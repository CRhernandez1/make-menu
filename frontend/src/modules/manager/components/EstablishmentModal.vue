<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
        <div class="bg-white rounded-2xl max-w-[560px] w-full shadow-[0_20px_60px_rgba(0,0,0,0.15)] overflow-hidden max-h-[90vh] flex flex-col">
          <!-- Header -->
          <div class="flex items-start justify-between px-6 pt-6 pb-1 shrink-0">
            <div>
              <h3 class="text-lg font-bold text-[#1a1a2e]">{{ isEditing ? 'Edit Establishment' : 'New Establishment' }}</h3>
              <p class="text-sm text-gray-400 mt-0.5">{{ isEditing ? 'Update the establishment details.' : 'Add a new establishment to your account.' }}</p>
            </div>
            <button @click="$emit('close')" class="bg-transparent border-none text-gray-300 cursor-pointer p-2 -mr-2 rounded-lg flex hover:bg-gray-100 hover:text-gray-500 transition-all">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <!-- Body -->
          <form @submit.prevent="handleSubmit" class="px-6 py-5 overflow-y-auto flex-1">
            <!-- Error -->
            <Transition name="error">
              <div v-if="error" class="flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-100 rounded-xl mb-5 text-sm text-red-600 leading-relaxed">
                <svg class="shrink-0 mt-0.5" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <!-- CIF (solo crear) -->
            <div v-if="!isEditing" class="mb-4">
              <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">CIF</label>
              <input
                v-model="form.cif"
                type="text" required
                placeholder="e.g. B12345678"
                class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300 uppercase"
                @input="$emit('clear-error')"
              />
              <p class="text-xs text-gray-400 mt-1.5">Unique tax identification number.</p>
            </div>

            <!-- Name + Legal Name (2 cols) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div>
                <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Name</label>
                <input
                  v-model="form.name"
                  type="text" required
                  placeholder="e.g. La Taberna"
                  class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300"
                  @input="$emit('clear-error')"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Legal Name</label>
                <input
                  v-model="form.legal_name"
                  type="text" required
                  placeholder="e.g. La Taberna S.L."
                  class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300"
                  @input="$emit('clear-error')"
                />
              </div>
            </div>

            <!-- Description -->
            <div class="mb-4">
              <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Description</label>
              <textarea
                v-model="form.description"
                rows="2"
                placeholder="Brief description of the establishment..."
                class="w-full border-[1.5px] border-gray-200 rounded-xl px-4 py-3 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300 resize-none"
                @input="$emit('clear-error')"
              ></textarea>
            </div>

            <!-- Address + City (2 cols) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div class="sm:col-span-2">
                <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Address</label>
                <input
                  v-model="form.address"
                  type="text" required
                  placeholder="e.g. Calle Mayor 12"
                  class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300"
                  @input="$emit('clear-error')"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">City</label>
                <input
                  v-model="form.city"
                  type="text" required
                  placeholder="e.g. Madrid"
                  class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300"
                  @input="$emit('clear-error')"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Zip Code</label>
                <input
                  v-model="form.zip_code"
                  type="text" required
                  placeholder="e.g. 28001"
                  class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300"
                  @input="$emit('clear-error')"
                />
              </div>
            </div>

            <!-- Phone -->
            <div class="mb-6">
              <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Phone</label>
              <input
                v-model="form.phone"
                type="tel"
                placeholder="e.g. +34 922 123 456"
                class="w-full h-11 border-[1.5px] border-gray-200 rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10 placeholder:text-gray-300"
                @input="$emit('clear-error')"
              />
            </div>

            <!-- Footer -->
            <div class="flex gap-3 justify-end">
              <button type="button" @click="$emit('close')" class="py-2.5 px-5 rounded-xl text-sm font-semibold cursor-pointer border-none bg-gray-100 text-gray-500 hover:bg-gray-200 transition-colors">Cancel</button>
              <button
                type="submit" :disabled="submitting"
                class="inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold cursor-pointer border-none bg-emerald-500 text-white hover:bg-emerald-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
              >
                <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                {{ isEditing ? 'Save Changes' : 'Create Establishment' }}
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
  cif: '',
  name: '',
  legal_name: '',
  description: '',
  zip_code: '',
  city: '',
  address: '',
  phone: ''
})

function resetForm() {
  form.cif = ''
  form.name = ''
  form.legal_name = ''
  form.description = ''
  form.zip_code = ''
  form.city = ''
  form.address = ''
  form.phone = ''
}

watch(() => props.visible, (v) => {
  if (v) {
    if (props.establishment) {
      isEditing.value = true
      form.cif = props.establishment.cif
      form.name = props.establishment.name
      form.legal_name = props.establishment.legal_name
      form.description = props.establishment.description
      form.zip_code = props.establishment.zip_code
      form.city = props.establishment.city
      form.address = props.establishment.address
      form.phone = props.establishment.phone
    } else {
      isEditing.value = false
      resetForm()
    }
  }
})

const handleSubmit = () => {
  emit('submit', { ...form })
}
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