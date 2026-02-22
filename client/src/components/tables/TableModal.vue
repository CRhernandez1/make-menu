<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[2000] p-4"
        @click.self="$emit('close')">
        <div class="bg-white rounded-2xl max-w-[440px] w-full shadow-[0_20px_60px_rgba(0,0,0,0.15)] overflow-hidden">
          <!-- Header -->
          <div class="flex items-start justify-between px-6 pt-6 pb-1">
            <div>
              <h3 class="text-lg font-bold text-[#1a1a2e]">
                {{ isEditing ? 'Edit Table' : 'New Table' }}
              </h3>
              <p class="text-sm text-gray-400 mt-0.5">
                {{
                  isEditing
                    ? 'Update the table configuration.'
                    : 'Add a new table to this establishment.'
                }}
              </p>
            </div>
            <button @click="$emit('close')"
              class="bg-transparent border-none text-gray-300 cursor-pointer p-2 -mr-2 rounded-lg flex hover:bg-gray-100 hover:text-gray-500 transition-all">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                stroke-linecap="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <form @submit.prevent="handleSubmit" class="px-6 py-5">
            <!-- Error -->
            <Transition name="error">
              <div v-if="error"
                class="flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-100 rounded-xl mb-5 text-sm text-red-600 leading-relaxed">
                <svg class="shrink-0 mt-0.5" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                <span>{{ error }}</span>
              </div>
            </Transition>

            <!-- Number -->
            <div v-if="!isEditing" class="mb-5">
              <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Table Number</label>
              <input v-model.number="localNumber" type="number" min="1" required placeholder="e.g. 1, 2, 3..."
                class="w-full h-11 border-[1.5px] rounded-xl px-4 text-sm text-[#1a1a2e] outline-none transition-all [-moz-appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none"
                :class="error && !isEditing
                  ? 'border-red-200 focus:border-red-400 focus:ring-2 focus:ring-red-500/10'
                  : 'border-gray-200 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/10'
                  " @input="$emit('clear-error')" />
              <p class="text-xs text-gray-400 mt-1.5">
                Unique number visible to staff and customers.
              </p>
            </div>

            <!-- Guests -->
            <div class="mb-6">
              <label class="block text-sm font-semibold text-[#1a1a2e] mb-2">Maximum Guests</label>
              <div class="flex items-center border-[1.5px] rounded-xl overflow-hidden transition-all" :class="error && isEditing
                ? 'border-red-200 focus-within:border-red-400 focus-within:ring-2 focus-within:ring-red-500/10'
                : 'border-gray-200 focus-within:border-emerald-400 focus-within:ring-2 focus-within:ring-emerald-500/10'
                ">
                <button type="button" @click="dec" :disabled="localMaxGuests <= 1"
                  class="w-12 h-11 border-none bg-gray-50 text-gray-500 cursor-pointer flex items-center justify-center transition-colors hover:bg-emerald-50 hover:text-emerald-600 disabled:opacity-25 disabled:cursor-not-allowed">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
                    stroke-linecap="round">
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                </button>
                <input v-model.number="localMaxGuests" type="number" min="1" max="50" required
                  class="flex-1 h-11 border-none text-center text-xl font-bold text-[#1a1a2e] bg-transparent outline-none [-moz-appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none"
                  @input="$emit('clear-error')" />
                <button type="button" @click="inc" :disabled="localMaxGuests >= 50"
                  class="w-12 h-11 border-none bg-gray-50 text-gray-500 cursor-pointer flex items-center justify-center transition-colors hover:bg-emerald-50 hover:text-emerald-600 disabled:opacity-25 disabled:cursor-not-allowed">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
                    stroke-linecap="round">
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                </button>
              </div>
              <p class="text-xs text-gray-400 mt-1.5">Seating capacity for this table.</p>
            </div>

            <!-- Footer -->
            <div class="flex gap-3 justify-end">
              <button type="button" @click="$emit('close')"
                class="py-2.5 px-5 rounded-xl text-sm font-semibold cursor-pointer border-none bg-gray-100 text-gray-500 hover:bg-gray-200 transition-colors">
                Cancel
              </button>
              <button type="submit" :disabled="submitting"
                class="inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold cursor-pointer border-none bg-emerald-500 text-white hover:bg-emerald-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed">
                <span v-if="submitting"
                  class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                {{ isEditing ? 'Save Changes' : 'Add Table' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Table } from '@/types/table';

const props = defineProps<{
  visible: boolean;
  table?: Table | null;
  error?: string | null;
  submitting?: boolean;
}>();

const emit = defineEmits<{
  close: [];
  submit: [number: number, maxGuests: number];
  'clear-error': [];
}>();

const localNumber = ref(1);
const localMaxGuests = ref(4);
const isEditing = ref(false);

watch(
  () => props.visible,
  (v) => {
    if (v) {
      if (props.table) {
        localNumber.value = props.table.number;
        localMaxGuests.value = props.table.max_guests;
        isEditing.value = true;
      } else {
        localNumber.value = 1;
        localMaxGuests.value = 4;
        isEditing.value = false;
      }
    }
  },
);

const inc = () => {
  if (localMaxGuests.value < 50) localMaxGuests.value++;
};
const dec = () => {
  if (localMaxGuests.value > 1) localMaxGuests.value--;
};
const handleSubmit = () => {
  emit('submit', localNumber.value, localMaxGuests.value);
};
</script>

<style scoped>
.error-enter-active {
  animation: shakeIn 0.35s ease;
}

.error-leave-active {
  transition: opacity 0.15s ease;
}

.error-leave-to {
  opacity: 0;
}

@keyframes shakeIn {
  0% {
    opacity: 0;
    transform: translateX(-6px);
  }

  25% {
    transform: translateX(4px);
  }

  50% {
    transform: translateX(-2px);
  }

  75% {
    transform: translateX(1px);
  }

  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active>div,
.modal-leave-active>div {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.modal-enter-from {
  opacity: 0;
}

.modal-enter-from>div {
  transform: translateY(12px) scale(0.97);
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-leave-to>div {
  transform: translateY(-8px) scale(0.97);
  opacity: 0;
}
</style>
