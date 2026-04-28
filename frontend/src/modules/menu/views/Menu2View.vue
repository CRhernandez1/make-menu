<template>
  <div class="min-h-screen bg-cream">

    <!-- ═══ PANTALLA 1: Selector de mesa (solo si no viene en la URL) ═══ -->
    <div v-if="step === 'table'" class="max-w-lg mx-auto px-6 py-12" style="animation:fade-up 0.6s cubic-bezier(0.25,1,0.5,1)">
      <div class="text-center mb-10">
        <div class="w-14 h-14 bg-green-forest rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-[0_4px_20px_rgba(26,92,46,0.2)]">
          <svg viewBox="0 0 452 263" width="28" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="white"/></svg>
        </div>
        <h1 class="font-display text-2xl font-bold text-green-forest tracking-tight">{{ establishmentName }}</h1>
        <p class="text-sm text-text-muted mt-1">Selecciona tu mesa para continuar</p>
      </div>

      <div v-if="isLoadingTables" class="grid grid-cols-4 gap-3">
        <div v-for="n in 8" :key="n" class="aspect-square rounded-[var(--radius-card)] skeleton-mm"></div>
      </div>

      <div v-else-if="tables.length" class="grid grid-cols-4 gap-3">
        <button
          v-for="table in tables" :key="table.id"
          @click="selectTable(table.number)"
          class="aspect-square flex flex-col items-center justify-center bg-white border-2 border-border-green rounded-[var(--radius-card)] cursor-pointer transition-all duration-300 hover:border-green-forest hover:bg-green-soft hover:-translate-y-1 hover:shadow-md group"
        >
          <span class="font-display text-xl font-bold text-text-muted group-hover:text-green-forest transition-colors">{{ table.number }}</span>
          <span class="text-[10px] text-text-ghost group-hover:text-green-medium transition-colors mt-0.5">Mesa</span>
        </button>
      </div>

      <div v-else class="text-center py-16">
        <div class="w-16 h-16 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-4" style="animation:float 6s ease-in-out infinite">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
        </div>
        <h3 class="font-display text-base font-bold text-ink mb-1">No hay mesas disponibles</h3>
        <p class="text-sm text-text-muted">Consulta al personal del establecimiento.</p>
      </div>
    </div>

    <!-- ═══ PANTALLA 2: Carta + Carrito ═══ -->
    <div v-else-if="step === 'menu'" class="flex flex-col md:flex-row h-screen overflow-hidden">

      <!-- Productos -->
      <div class="flex-1 overflow-y-auto">

        <!-- Header -->
        <div class="bg-white border-b border-border-green-light px-5 py-3.5 flex items-center justify-between sticky top-0 z-10">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 bg-green-forest rounded-xl flex items-center justify-center">
              <svg viewBox="0 0 452 263" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M 444,244 L 430,216 L 380,128 L 374,127 L 369,130 L 335,161 L 333,160 L 281,15 L 277,8 L 272,10 L 188,159 L 170,188 L 151,194 L 139,193 L 207,92 L 215,74 L 214,69 L 208,69 L 194,79 L 11,229 L 8,235 L 12,240 L 138,240 L 139,242 L 134,250 L 136,255 L 197,255 L 209,253 L 220,249 L 228,242 L 245,211 L 268,153 L 297,241 L 309,242 L 318,238 L 339,218 L 361,193 L 365,199 L 378,231 L 386,243 L 405,248 L 440,248 Z" fill="white"/></svg>
            </div>
            <div>
              <h1 class="text-sm font-bold text-ink">{{ establishmentName }}</h1>
              <p class="text-xs text-text-muted">Mesa {{ currentTable }}</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge-mm bg-green-soft text-green-forest">
              <span class="w-1.5 h-1.5 bg-green-bright rounded-full" style="animation:pulse-dot 2s infinite"></span>
              En línea
            </span>
            <button v-if="!tableFromUrl" @click="step = 'table'; currentTable = null"
              class="text-xs text-text-muted hover:text-green-forest flex items-center gap-1 bg-transparent border-none cursor-pointer transition-colors">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
              Cambiar
            </button>
          </div>
        </div>

        <!-- Filtro categorías -->
        <div class="bg-white border-b border-border-green-light px-5 py-3 flex gap-2 overflow-x-auto sticky top-[57px] z-10 scrollbar-hide">
          <button @click="activeCategory = null"
            :class="activeCategory === null
              ? 'bg-green-forest text-cream shadow-[0_2px_10px_rgba(26,92,46,0.15)]'
              : 'bg-cream text-text-sec hover:bg-green-soft hover:text-green-forest'"
            class="px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all border-none cursor-pointer">
            Todos
          </button>
          <button v-for="cat in categories" :key="cat.id" @click="activeCategory = cat.id"
            :class="activeCategory === cat.id
              ? 'bg-green-forest text-cream shadow-[0_2px_10px_rgba(26,92,46,0.15)]'
              : 'bg-cream text-text-sec hover:bg-green-soft hover:text-green-forest'"
            class="px-4 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all border-none cursor-pointer">
            {{ cat.name }}
          </button>
        </div>

        <!-- Productos -->
        <div class="px-5 py-5 space-y-7 pb-32">
          <div v-if="isLoadingProducts" class="space-y-3">
            <div v-for="n in 4" :key="n" class="h-24 rounded-[var(--radius-card)] skeleton-mm"></div>
          </div>

          <template v-else>
            <div v-for="(group, category) in filteredGrouped" :key="category">
              <h2 class="text-[11px] font-bold text-text-muted uppercase tracking-[0.12em] mb-3 font-display">{{ category }}</h2>
              <div class="space-y-2.5">
                <div v-for="product in group" :key="product.id"
                  class="bg-white border border-border-green-light rounded-2xl p-3.5 flex gap-3.5 transition-all hover:shadow-sm">
                  <img v-if="product.product_image" :src="product.product_image" :alt="product.name"
                    class="w-[72px] h-[72px] rounded-xl object-cover flex-shrink-0 border border-border-green-light" />
                  <div v-else class="w-[72px] h-[72px] rounded-xl bg-cream flex-shrink-0 flex items-center justify-center">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" class="text-text-ghost"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="font-bold text-ink text-[14px]">{{ product.name }}</p>
                    <p class="text-xs text-text-muted mt-0.5 line-clamp-2">{{ product.description }}</p>
                    <p class="font-display text-green-forest font-bold text-[14px] mt-1">{{ product.price }}€</p>
                  </div>
                  <div class="flex flex-col items-center justify-center gap-1.5 flex-shrink-0">
                    <template v-if="cartQuantity(product.id) > 0">
                      <button @click="removeFromCart(product.id)"
                        class="w-8 h-8 rounded-full bg-danger-soft text-danger hover:bg-[rgba(185,60,60,0.15)] flex items-center justify-center font-bold text-lg leading-none transition-colors cursor-pointer border-none">−</button>
                      <span class="text-sm font-bold text-ink font-display">{{ cartQuantity(product.id) }}</span>
                    </template>
                    <button @click="addToCart(product)"
                      class="w-8 h-8 rounded-full bg-green-forest text-cream hover:bg-green-medium flex items-center justify-center font-bold text-lg leading-none transition-colors cursor-pointer border-none shadow-[0_2px_10px_rgba(26,92,46,0.2)]">+</button>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Botón flotante carrito (móvil) -->
        <button v-if="cart.length && !showMobileCart" @click="showMobileCart = true"
          class="md:hidden fixed bottom-6 left-1/2 -translate-x-1/2 btn-mm btn-primary px-6 py-3.5 text-[14px] z-20 shadow-[0_8px_30px_rgba(26,92,46,0.3)]">
          Ver pedido ({{ cartItemsCount }}) · {{ cartTotal }}€
        </button>
      </div>

      <!-- Carrito lateral (desktop) -->
      <div class="hidden md:flex w-80 bg-white border-l border-border-green-light flex-col">
        <div class="px-6 py-5 border-b border-border-green-light">
          <h2 class="font-display font-bold text-ink tracking-tight">Tu pedido</h2>
          <p class="text-xs text-text-muted mt-0.5">Mesa {{ currentTable }}</p>
        </div>
        <div class="flex-1 overflow-y-auto px-6 py-5 space-y-3">
          <div v-if="!cart.length" class="text-center py-12">
            <div class="w-14 h-14 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-3" style="animation:float 6s ease-in-out infinite">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>
            </div>
            <p class="text-sm text-text-muted">Tu carrito está vacío</p>
            <p class="text-xs text-text-ghost mt-0.5">Añade productos desde la carta</p>
          </div>
          <div v-for="item in cart" :key="item.product.id" class="flex items-center gap-3 p-3 bg-cream rounded-2xl">
            <div class="flex-1 min-w-0">
              <p class="text-sm font-bold text-ink truncate">{{ item.product.name }}</p>
              <p class="text-xs text-text-muted font-display">{{ item.product.price }}€ × {{ item.quantity }}</p>
            </div>
            <div class="flex items-center gap-2">
              <button @click="removeFromCart(item.product.id)" class="w-7 h-7 rounded-full bg-danger-soft text-danger flex items-center justify-center font-bold text-sm leading-none border-none cursor-pointer">−</button>
              <span class="text-sm font-bold text-ink w-4 text-center font-display">{{ item.quantity }}</span>
              <button @click="addToCart(item.product)" class="w-7 h-7 rounded-full bg-green-soft text-green-forest flex items-center justify-center font-bold text-sm leading-none border-none cursor-pointer">+</button>
            </div>
          </div>
        </div>
        <div class="px-6 py-5 border-t border-border-green-light space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-semibold text-text-sec">Total</span>
            <span class="font-display text-xl font-bold text-green-forest">{{ cartTotal }}€</span>
          </div>
          <button @click="sendOrder" :disabled="!cart.length || isSending"
            class="btn-mm btn-primary w-full h-[50px] text-[15px] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
            <span v-if="isSending" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
            {{ isSending ? 'Enviando...' : 'Enviar pedido →' }}
          </button>
        </div>
      </div>

      <!-- Carrito móvil (bottom sheet) -->
      <Teleport to="body">
        <Transition name="sheet">
          <div v-if="showMobileCart" class="md:hidden fixed inset-0 bg-ink/50 backdrop-blur-[4px] z-50 flex items-end" @click.self="showMobileCart = false">
            <div class="bg-white rounded-t-[28px] w-full max-h-[80vh] flex flex-col shadow-[0_-20px_60px_rgba(26,92,46,0.1)]">
              <div class="flex items-center justify-between px-6 py-5 border-b border-border-green-light">
                <div>
                  <h2 class="font-display font-bold text-ink tracking-tight">Tu pedido</h2>
                  <p class="text-xs text-text-muted">Mesa {{ currentTable }}</p>
                </div>
                <button @click="showMobileCart = false" class="bg-transparent border-none text-text-ghost p-2 rounded-[10px] hover:bg-green-soft cursor-pointer">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
              <div class="flex-1 overflow-y-auto px-6 py-4 space-y-3">
                <div v-for="item in cart" :key="item.product.id" class="flex items-center gap-3 p-3 bg-cream rounded-2xl">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-ink truncate">{{ item.product.name }}</p>
                    <p class="text-xs text-text-muted font-display">{{ item.product.price }}€ × {{ item.quantity }}</p>
                  </div>
                  <div class="flex items-center gap-2">
                    <button @click="removeFromCart(item.product.id)" class="w-7 h-7 rounded-full bg-danger-soft text-danger flex items-center justify-center font-bold text-sm leading-none border-none cursor-pointer">−</button>
                    <span class="text-sm font-bold text-ink w-4 text-center font-display">{{ item.quantity }}</span>
                    <button @click="addToCart(item.product)" class="w-7 h-7 rounded-full bg-green-soft text-green-forest flex items-center justify-center font-bold text-sm leading-none border-none cursor-pointer">+</button>
                  </div>
                </div>
              </div>
              <div class="px-6 py-5 border-t border-border-green-light space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-semibold text-text-sec">Total</span>
                  <span class="font-display text-xl font-bold text-green-forest">{{ cartTotal }}€</span>
                </div>
                <button @click="sendOrder" :disabled="!cart.length || isSending"
                  class="btn-mm btn-primary w-full h-[50px] text-[15px] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                  {{ isSending ? 'Enviando...' : 'Enviar pedido →' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>

    <!-- ═══ PANTALLA 3: Confirmación ═══ -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="step === 'confirm'" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-50 p-4">
          <div class="bg-white rounded-[28px] p-10 max-w-sm w-full text-center shadow-[0_40px_100px_rgba(26,92,46,0.12)]">
            <div class="w-16 h-16 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
            <h2 class="font-display text-2xl font-bold text-green-forest tracking-tight mb-2">
              {{ wasMerged ? '¡Añadido al pedido!' : '¡Pedido enviado!' }}
            </h2>
            <p class="text-sm text-text-sec mb-3 leading-relaxed">
              {{ wasMerged
                ? 'Los nuevos productos se han añadido a tu pedido activo.'
                : 'Tu pedido está siendo preparado.' }}
            </p>
            <p class="text-text-muted text-xs mb-8">Mesa {{ currentTable }}</p>
            <button @click="resetOrder" class="btn-mm btn-primary px-8 py-3.5 text-[15px]">Pedir más →</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { makeMenuApi } from '@/api/makeMenu'

const route = useRoute()
const cif = route.params.cif as string
const tableFromUrl = route.params.tableNum ? Number(route.params.tableNum) : null

const step = ref<'table' | 'menu' | 'confirm'>(tableFromUrl ? 'menu' : 'table')
const currentTable = ref<number | null>(tableFromUrl)
const establishmentName = ref('')
const tables = ref<any[]>([])
const products = ref<any[]>([])
const categories = ref<any[]>([])
const activeCategory = ref<number | null>(null)
const cart = ref<{ product: any; quantity: number }[]>([])
const isLoadingTables = ref(false)
const isLoadingProducts = ref(false)
const isSending = ref(false)
const showMobileCart = ref(false)
const wasMerged = ref(false)

// ── Fetch ──
const fetchEstablishment = async () => {
  try {
    const { data } = await makeMenuApi.get(`/establishments/${cif}/`)
    establishmentName.value = data.name
  } catch { establishmentName.value = 'Restaurante' }
}

const fetchTables = async () => {
  isLoadingTables.value = true
  try {
    const { data } = await makeMenuApi.get(`/menu/${cif}/tables/`)
    tables.value = data
  } catch { console.error('Error cargando mesas') }
  finally { isLoadingTables.value = false }
}

const fetchProducts = async () => {
  isLoadingProducts.value = true
  try {
    const { data } = await makeMenuApi.get(`/menu/${cif}/products/`)
    products.value = data
    const seen = new Set()
    categories.value = data
      .map((p: any) => p.category)
      .filter((cat: any) => { if (seen.has(cat.id)) return false; seen.add(cat.id); return true })
  } catch { console.error('Error cargando productos') }
  finally { isLoadingProducts.value = false }
}

// ── Mesa ──
const selectTable = (num: number) => {
  currentTable.value = num
  step.value = 'menu'
  if (!products.value.length) fetchProducts()
}

// ── Categorías ──
const filteredGrouped = computed(() => {
  const filtered = activeCategory.value ? products.value.filter(p => p.category.id === activeCategory.value) : products.value
  return filtered.reduce((groups: Record<string, any[]>, product) => {
    const cat = product.category.name
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(product)
    return groups
  }, {})
})

// ── Carrito ──
const cartQuantity = (productId: number) => cart.value.find(i => i.product.id === productId)?.quantity ?? 0
const cartItemsCount = computed(() => cart.value.reduce((sum, i) => sum + i.quantity, 0))
const cartTotal = computed(() => cart.value.reduce((sum, item) => sum + item.product.price * item.quantity, 0).toFixed(2))

const addToCart = (product: any) => {
  const existing = cart.value.find(i => i.product.id === product.id)
  if (existing) existing.quantity++
  else cart.value.push({ product, quantity: 1 })
}

const removeFromCart = (productId: number) => {
  const index = cart.value.findIndex(i => i.product.id === productId)
  if (index === -1) return
  if (cart.value[index].quantity > 1) cart.value[index].quantity--
  else cart.value.splice(index, 1)
}

// ── Enviar pedido ──
const sendOrder = async () => {
  if (!cart.value.length || !currentTable.value) return
  isSending.value = true
  try {
    const { data } = await makeMenuApi.post(`/orders/public/${cif}/`, {
      table: currentTable.value,
      items: cart.value.map(i => ({ product_id: i.product.id, quantity: i.quantity })),
    })
    wasMerged.value = data.merged ?? false
    showMobileCart.value = false
    step.value = 'confirm'
  } catch { console.error('Error enviando pedido') }
  finally { isSending.value = false }
}

const resetOrder = () => { cart.value = []; step.value = 'menu' }

// ── Init ──
onMounted(async () => {
  await fetchEstablishment()
  if (tableFromUrl) {
    await fetchProducts()
  } else {
    await fetchTables()
  }
})
</script>

<style scoped>
.sheet-enter-active { transition: all 0.35s cubic-bezier(0.25,1,0.5,1); }
.sheet-leave-active { transition: all 0.25s ease; }
.sheet-enter-from > div { transform: translateY(100%); }
.sheet-leave-to > div { transform: translateY(100%); }
.sheet-enter-from { opacity: 0; }
.sheet-leave-to { opacity: 0; }
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: scale(0.94); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: scale(0.96); opacity: 0; }
</style>