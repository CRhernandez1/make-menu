<template>
  <div class="min-h-screen flex items-center justify-center bg-cream px-4">
    <div class="text-center" style="animation:fade-up 0.6s cubic-bezier(0.25,1,0.5,1)">
      <div class="w-24 h-24 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-6" style="animation:float 6s ease-in-out infinite">
        <svg viewBox="0 0 452 263" width="48" style="opacity:0.3" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="#1A5C2E"/></svg>
      </div>
      <h1 class="font-display text-6xl font-bold text-green-forest tracking-tighter mb-3">404</h1>
      <p class="font-display text-xl font-bold text-ink mb-2">Página no encontrada</p>
      <p class="text-sm text-text-muted mb-8 max-w-xs mx-auto">La página que buscas no existe o ha sido movida.</p>
      <RouterLink :to="{ name: 'home' }" class="btn-mm btn-primary text-[14px] px-8 py-3">
        Volver al inicio
      </RouterLink>
    </div>
  </div>
</template>