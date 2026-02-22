<template>
  <div class="flex min-h-screen bg-[#f5f6f8]">
    <!-- Sidebar -->
    <aside class="w-[250px] shrink-0 bg-[#0c0c12] flex flex-col sticky top-0 h-screen max-md:hidden">
      <!-- Brand -->
      <div class="flex items-center gap-3 px-5 h-16 border-b border-white/[0.06]">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <rect x="2" y="2" width="9" height="9" rx="2" fill="#34d399" />
          <rect x="13" y="2" width="9" height="9" rx="2" fill="#34d399" opacity="0.5" />
          <rect x="2" y="13" width="9" height="9" rx="2" fill="#34d399" opacity="0.5" />
          <rect x="13" y="13" width="9" height="9" rx="2" fill="#34d399" opacity="0.25" />
        </svg>
        <span class="text-[17px] font-bold text-white tracking-tight">MakeMenu</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 flex flex-col px-3 pt-5 gap-1">
        <span class="text-[10px] font-bold uppercase tracking-[0.12em] text-white/20 px-3 mb-1">Menu</span>
        <router-link to="/"
          class="flex items-center gap-3 py-2.5 px-3 rounded-lg text-white/40 no-underline text-sm font-medium transition-all duration-150 hover:text-white/70 hover:bg-white/5"
          exact-active-class="!text-white !bg-white/[0.08] [&_svg]:!text-emerald-400">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span>Establishments</span>
        </router-link>
      </nav>

      <!-- User -->
      <div class="px-3 pb-4 pt-3 border-t border-white/[0.06]">
        <div class="flex items-center gap-3 py-2.5 px-3 rounded-lg hover:bg-white/5 transition-colors cursor-pointer">
          <div
            class="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-500 to-emerald-300 text-white text-sm font-bold flex items-center justify-center">
            D</div>
          <div class="flex flex-col">
            <span class="text-sm font-semibold text-white/90">Daniele</span>
            <span class="text-[11px] text-white/30">Manager</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 min-w-0">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1a1a2e;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.15s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  aside {
    display: none !important;
  }
}
</style>
