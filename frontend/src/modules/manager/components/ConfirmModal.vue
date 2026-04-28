<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-[2000] p-4" @click.self="$emit('cancel')">
        <div class="bg-white rounded-[28px] p-9 max-w-[420px] w-full text-center shadow-[0_40px_100px_rgba(26,92,46,0.12)]">
          <!-- Icon -->
          <div class="w-[60px] h-[60px] rounded-full bg-danger-soft flex items-center justify-center mx-auto mb-5">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#b93c3c" stroke-width="1.8" stroke-linecap="round">
              <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </div>

          <h3 class="font-display text-xl font-bold text-ink mb-2 tracking-tight">{{ title }}</h3>
          <p class="text-sm text-text-sec leading-relaxed mb-7 max-w-xs mx-auto" v-html="message"></p>

          <!-- Error -->
          <Transition name="error">
            <div v-if="error" class="flex items-start gap-3 p-4 bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] rounded-2xl mb-6 text-sm text-danger leading-relaxed text-left">
              <svg class="shrink-0 mt-0.5 w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
              <span>{{ error }}</span>
            </div>
          </Transition>

          <div class="flex gap-3 justify-center">
            <button @click="$emit('cancel')" class="btn-mm btn-ghost text-[13px] px-6 py-2.5 flex-1">Cancelar</button>
            <button @click="$emit('confirm')" :disabled="submitting"
              class="btn-mm btn-danger text-[13px] px-6 py-2.5 flex-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
              <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
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
.error-enter-active { animation: shakeIn 0.35s ease; }
.error-leave-active { transition: opacity 0.15s ease; }
.error-leave-to { opacity: 0; }
@keyframes shakeIn { 0%{opacity:0;transform:translateX(-6px)} 25%{transform:translateX(4px)} 50%{transform:translateX(-2px)} 75%{transform:translateX(1px)} 100%{opacity:1;transform:translateX(0)} }
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: scale(0.94); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: scale(0.96); opacity: 0; }
</style>