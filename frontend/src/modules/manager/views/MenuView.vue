<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
      <h2 class="font-display text-2xl font-bold text-green-forest tracking-tight">Carta pública</h2>
      <div class="flex items-center gap-3">
        <select v-model="activeCif" @change="onEstablishmentChange" class="input-mm !w-auto !h-11 pr-10 cursor-pointer text-[13px]">
          <option v-for="est in myEstablishments" :key="est.cif" :value="est.cif">{{ est.name }}</option>
        </select>
        <a v-if="activeCif" :href="`/menu/${activeCif}`" target="_blank" class="btn-mm btn-primary text-[13px] px-5 py-2.5">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          Ver carta
        </a>
      </div>
    </div>

    <!-- No establishments -->
    <div v-if="!myEstablishments.length && !isLoadingEstablishments" class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
      <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-ink mb-2">No gestionas ningún establecimiento</h3>
    </div>

    <template v-else-if="activeCif">

      <!-- Loading -->
      <div v-if="isLoading" class="p-16 text-center">
        <div class="w-10 h-10 border-[3px] border-green-soft border-t-green-forest rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-sm text-text-muted">Cargando productos...</p>
      </div>

      <!-- Products grouped -->
      <div v-else-if="products.length" class="space-y-5">
        <div v-for="(group, category) in groupedProducts" :key="category">
          <h3 class="text-[11px] font-bold text-text-muted uppercase tracking-[0.12em] mb-2.5 px-1 font-display">{{ category }}</h3>
          <div class="bg-white border border-border-green-light rounded-[var(--radius-card)] overflow-hidden divide-y divide-border-green-light">
            <div v-for="product in group" :key="product.id" class="flex items-center gap-4 px-5 py-3.5 hover:bg-green-soft-2 transition-colors">
              <img v-if="product.product_image" :src="product.product_image" :alt="product.name" class="w-12 h-12 rounded-2xl object-cover flex-shrink-0 border border-border-green-light" />
              <div v-else class="w-12 h-12 rounded-2xl bg-cream flex items-center justify-center flex-shrink-0">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" class="text-text-ghost"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
              </div>

              <div class="flex-1 min-w-0">
                <p class="text-sm font-bold text-ink truncate">{{ product.name }}</p>
                <p class="text-xs text-text-muted truncate">{{ product.description || '—' }}</p>
              </div>

              <span class="font-display text-green-forest font-bold text-sm whitespace-nowrap">{{ product.price }}€</span>

              <!-- Toggle -->
              <button
                @click="handleToggle(product)"
                :class="product.available ? 'bg-green-forest' : 'bg-cream-dark'"
                class="relative inline-flex h-6 w-11 flex-shrink-0 rounded-full transition-colors duration-300 cursor-pointer border-none"
                :title="product.available ? 'Visible en carta' : 'Oculto en carta'"
              >
                <span
                  :class="product.available ? 'translate-x-5' : 'translate-x-1'"
                  class="inline-block h-4 w-4 mt-1 rounded-full bg-white shadow-sm transition-transform duration-300"
                ></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty -->
      <div v-else class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
        <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
        </div>
        <h3 class="font-display text-lg font-bold text-ink mb-2">No hay productos aún</h3>
        <p class="text-sm text-text-muted">Añade productos desde la sección Productos.</p>
      </div>

      <!-- QR -->
      <div class="card-mm p-7 !cursor-default !transform-none flex flex-col items-center gap-5">
        <h3 class="font-display text-[15px] font-bold text-ink self-start tracking-tight">Acceso para clientes</h3>
        <canvas ref="qrCanvas" class="rounded-2xl"></canvas>
        <div class="w-full flex items-center bg-cream border border-border-green rounded-[var(--radius-input)] overflow-hidden max-w-md">
          <span class="text-[12px] text-text-sec flex-1 truncate px-4 py-3 font-mono">{{ menuUrl }}</span>
          <button @click="copyLink" class="px-4 py-3 bg-green-soft text-green-forest text-[12px] font-semibold hover:bg-[rgba(26,92,46,0.12)] transition-colors whitespace-nowrap border-l border-border-green">
            {{ copied ? '¡Copiado!' : 'Copiar' }}
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { getProductsAction, toggleProductAvailableAction } from '../actions/getProducts.action'
import { useToast } from '@/composables/useToast'
import type { Product } from '../interfaces/product.interface'
import QRCode from 'qrcode'
import { nextTick } from 'vue'

const toast = useToast()

const myEstablishments = ref<any[]>([])
const activeCif = ref('')
const isLoadingEstablishments = ref(true)
const products = ref<Product[]>([])
const isLoading = ref(false)

const qrCanvas = ref<HTMLCanvasElement | null>(null)
const copied = ref(false)

const menuUrl = computed(() => `${window.location.origin}/menu/${activeCif.value}`)

const generateQR = async () => {
  if (!qrCanvas.value || !activeCif.value) return
  await QRCode.toCanvas(qrCanvas.value, menuUrl.value, {
    width: 200, margin: 2,
    color: { dark: '#1a5c2e', light: '#ffffff' },
  })
}

const copyLink = async () => {
  await navigator.clipboard.writeText(menuUrl.value)
  copied.value = true
  setTimeout(() => copied.value = false, 2000)
}

watch(activeCif, () => generateQR(), { immediate: false })

const fetchMyEstablishments = async () => {
  isLoadingEstablishments.value = true
  try {
    const { data } = await makeMenuApi.get('/establishments/')
    myEstablishments.value = data
    if (data.length > 0) {
      activeCif.value = data[0].cif
      await nextTick(); generateQR()
      await fetchProducts()
    }
  } catch { toast.error('Error cargando establecimientos.') }
  finally { isLoadingEstablishments.value = false }
}

const fetchProducts = async () => {
  isLoading.value = true
  try { products.value = await getProductsAction(activeCif.value) }
  catch { toast.error('Error cargando productos.') }
  finally { isLoading.value = false }
}

const onEstablishmentChange = async () => { await fetchProducts() }

const groupedProducts = computed(() => {
  return products.value.reduce((groups: Record<string, Product[]>, product) => {
    const cat = product.category.name
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(product)
    return groups
  }, {})
})

const handleToggle = async (product: Product) => {
  try {
    const updated = await toggleProductAvailableAction(activeCif.value, product.id)
    const index = products.value.findIndex(p => p.id === product.id)
    if (index !== -1) products.value[index] = updated
    toast.success(updated.available ? 'Visible en carta.' : 'Oculto de la carta.')
  } catch { toast.error('Error al actualizar el producto.') }
}

onMounted(() => { fetchMyEstablishments() })
</script>