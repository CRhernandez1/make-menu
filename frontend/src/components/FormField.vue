<template>
  <div class="space-y-1">
    <label v-if="label" class="block text-sm font-semibold text-gray-700">{{ label }}</label>
    <slot />
    <Transition name="error">
      <p v-if="error" class="text-xs text-red-500 flex items-center gap-1">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        {{ error }}
      </p>
    </Transition>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label?: string
  error?: string
}>()
</script>

<style scoped>
.error-enter-active { transition: all 0.2s ease; }
.error-leave-active { transition: all 0.15s ease; }
.error-enter-from, .error-leave-to { opacity: 0; transform: translateY(-4px); }
</style>