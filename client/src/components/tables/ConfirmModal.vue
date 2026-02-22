<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[2000] p-4"
        @click.self="$emit('cancel')">
        <div class="bg-white rounded-2xl p-8 max-w-[400px] w-full text-center shadow-[0_20px_60px_rgba(0,0,0,0.15)]">
          <!-- Icon -->
          <div class="w-14 h-14 rounded-2xl bg-red-50 flex items-center justify-center mx-auto mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"
              stroke-linecap="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
          </div>

          <h3 class="text-lg font-bold text-[#1a1a2e] mb-2">{{ title }}</h3>
          <p class="text-sm text-gray-400 leading-relaxed mb-6">{{ message }}</p>

          <!-- Error -->
          <Transition name="error">
            <div v-if="error"
              class="flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-100 rounded-xl mb-6 text-sm text-red-600 leading-relaxed text-left">
              <svg class="shrink-0 mt-0.5" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
              <span>{{ error }}</span>
            </div>
          </Transition>

          <div class="flex gap-3 justify-center">
            <button @click="$emit('cancel')"
              class="py-2.5 px-6 rounded-xl text-sm font-semibold cursor-pointer border-none bg-gray-100 text-gray-500 hover:bg-gray-200 transition-colors">Cancel</button>
            <button @click="$emit('confirm')" :disabled="submitting"
              class="inline-flex items-center gap-2 py-2.5 px-6 rounded-xl text-sm font-semibold cursor-pointer border-none bg-red-500 text-white hover:bg-red-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed">
              <span v-if="submitting"
                class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean
  title?: string
  message?: string
  confirmText?: string
  error?: string | null
  submitting?: boolean
}>()

defineEmits<{ confirm: []; cancel: [] }>()
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
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-enter-from {
  opacity: 0;
}

.modal-enter-from>div {
  transform: scale(0.95);
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-leave-to>div {
  transform: scale(0.95);
  opacity: 0;
}
</style>