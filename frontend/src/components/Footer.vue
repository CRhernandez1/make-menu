<template>
  <footer class="border-t border-border-green-light py-10 px-6">
    <div class="max-w-7xl mx-auto flex items-center justify-between">

      <div class="flex items-center gap-2.5">
        <svg viewBox="0 0 452 263" width="20" style="opacity:0.15" xmlns="http://www.w3.org/2000/svg">
          <path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="#1A5C2E"/>
        </svg>
        <span class="text-xs text-text-ghost">MakeMenu · {{ new Date().getFullYear() }}</span>
      </div>

      <div class="flex items-center gap-4">
        <RouterLink :to="{ name: 'privacy' }" class="text-xs text-text-ghost hover:text-gray-600 transition-colors">
          Política de privacidad
        </RouterLink>
        <RouterLink :to="{ name: 'legal' }" class="text-xs text-text-ghost hover:text-gray-600 transition-colors">
          Aviso legal
        </RouterLink>
      </div>

      <span class="text-xs text-text-ghost font-display">Hecho en Tenerife</span>

    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>