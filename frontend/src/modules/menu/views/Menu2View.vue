<template>
  <div class="min-h-screen bg-gray-50">

    <!-- PANTALLA 1: Selector de mesa -->
    <div v-if="step === 'table'" class="max-w-lg mx-auto px-6 py-12">
      <div class="text-center mb-10">
        <div class="w-14 h-14 bg-emerald-400 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 tracking-tight">{{ establishmentName }}</h1>
        <p class="text-gray-400 text-sm mt-1">Selecciona tu mesa para continuar</p>
      </div>

      <div v-if="isLoadingTables" class="text-center py-12 text-gray-400">Cargando mesas...</div>

      <div v-else-if="tables.length" class="grid grid-cols-4 gap-3">
        <button
          v-for="table in tables"
          :key="table.id"
          @click="selectTable(table)"
          class="aspect-square flex flex-col items-center justify-center bg-white border border-gray-200 rounded-2xl hover:border-emerald-400 hover:bg-emerald-50 transition-all group"
        >
          <span class="text-xl font-bold text-gray-700 group-hover:text-emerald-600">{{ table.number }}</span>
          <span class="text-xs text-gray-400 group-hover:text-emerald-500">Mesa</span>
        </button>
      </div>

      <div v-else class="text-center py-12 text-gray-400">
        <p class="font-medium">No hay mesas disponibles</p>
      </div>
    </div>

    <!-- PANTALLA 2: Carta + Carrito -->
    <div v-else-if="step === 'menu'" class="flex h-screen overflow-hidden">

      <!-- Carta -->
      <div class="flex-1 overflow-y-auto">

        <!-- Header -->
        <div class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between sticky top-0 z-10">
          <div>
            <h1 class="text-base font-bold text-gray-800">{{ establishmentName }}</h1>
            <p class="text-xs text-gray-400">Mesa {{ selectedTable?.number }}</p>
          </div>
          <button
            @click="step = 'table'"
            class="text-xs text-gray-400 hover:text-gray-600 flex items-center gap-1"
          >
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
            Cambiar mesa
          </button>
        </div>

        <!-- Filtro categorías -->
        <div class="bg-white border-b border-gray-200 px-6 py-3 flex gap-2 overflow-x-auto sticky top-[65px] z-10">
          <button
            @click="activeCategory = null"
            :class="activeCategory === null
              ? 'bg-emerald-400 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
            class="px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors"
          >
            Todos
          </button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="activeCategory = cat.id"
            :class="activeCategory === cat.id
              ? 'bg-emerald-400 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
            class="px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors"
          >
            {{ cat.name }}
          </button>
        </div>

        <!-- Productos -->
        <div class="px-6 py-6 space-y-8 pb-32">
          <div v-if="isLoadingProducts" class="text-center py-12 text-gray-400">Cargando carta...</div>

          <template v-else>
            <div v-for="(group, category) in filteredGrouped" :key="category">
              <h2 class="text-sm font-bold text-gray-500 uppercase tracking-widest mb-3">{{ category }}</h2>
              <div class="space-y-3">
                <div
                  v-for="product in group"
                  :key="product.id"
                  class="bg-white border border-gray-200 rounded-2xl p-4 flex gap-4"
                >
                  <img
                    v-if="product.product_image"
                    :src="product.product_image"
                    :alt="product.name"
                    class="w-20 h-20 rounded-xl object-cover flex-shrink-0"
                  />
                  <div v-else class="w-20 h-20 rounded-xl bg-gray-100 flex-shrink-0 flex items-center justify-center">
                    <svg class="w-6 h-6 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/>
                      <path d="M7 2v20"/>
                      <path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/>
                      <path d="M21 22v-7"/>
                    </svg>
                  </div>

                  <div class="flex-1 min-w-0">
                    <p class="font-semibold text-gray-800 text-sm">{{ product.name }}</p>
                    <p class="text-xs text-gray-400 mt-0.5 line-clamp-2">{{ product.description }}</p>
                    <p class="text-emerald-600 font-bold text-sm mt-1">{{ product.price }}€</p>
                  </div>

                  <!-- Controles carrito -->
                  <div class="flex flex-col items-center justify-center gap-2 flex-shrink-0">
                    <template v-if="cartQuantity(product.id) > 0">
                      <button
                        @click="removeFromCart(product.id)"
                        class="w-7 h-7 rounded-full bg-red-100 text-red-500 hover:bg-red-200 flex items-center justify-center font-bold text-lg leading-none transition-colors"
                      >−</button>
                      <span class="text-sm font-bold text-gray-700">{{ cartQuantity(product.id) }}</span>
                    </template>
                    <button
                      @click="addToCart(product)"
                      class="w-7 h-7 rounded-full bg-emerald-400 text-white hover:bg-emerald-500 flex items-center justify-center font-bold text-lg leading-none transition-colors"
                    >+</button>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Carrito lateral -->
      <div class="w-80 bg-white border-l border-gray-200 flex flex-col">
        <div class="px-5 py-4 border-b border-gray-200">
          <h2 class="font-bold text-gray-800">Tu pedido</h2>
          <p class="text-xs text-gray-400">Mesa {{ selectedTable?.number }}</p>
        </div>

        <div class="flex-1 overflow-y-auto px-5 py-4 space-y-3">
          <div v-if="!cart.length" class="text-center py-12 text-gray-400">
            <p class="text-sm">Tu carrito está vacío</p>
            <p class="text-xs mt-1">Añade productos desde la carta</p>
          </div>

          <div
            v-for="item in cart"
            :key="item.product.id"
            class="flex items-center gap-3"
          >
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-800 truncate">{{ item.product.name }}</p>
              <p class="text-xs text-gray-400">{{ item.product.price }}€ x {{ item.quantity }}</p>
            </div>
            <div class="flex items-center gap-2">
              <button
                @click="removeFromCart(item.product.id)"
                class="w-6 h-6 rounded-full bg-red-100 text-red-500 hover:bg-red-200 flex items-center justify-center font-bold text-sm leading-none"
              >−</button>
              <span class="text-sm font-bold text-gray-700 w-4 text-center">{{ item.quantity }}</span>
              <button
                @click="addToCart(item.product)"
                class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-600 hover:bg-emerald-200 flex items-center justify-center font-bold text-sm leading-none"
              >+</button>
            </div>
          </div>
        </div>

        <!-- Total y enviar -->
        <div class="px-5 py-4 border-t border-gray-200 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-semibold text-gray-600">Total</span>
            <span class="text-lg font-bold text-emerald-600">{{ cartTotal }}€</span>
          </div>
          <button
            @click="sendOrder"
            :disabled="!cart.length || isSending"
            class="w-full py-3 bg-emerald-400 text-white font-bold rounded-xl hover:bg-emerald-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSending ? 'Enviando...' : 'Enviar pedido' }}
          </button>
        </div>
      </div>

    </div>

    <!-- PANTALLA 3: Confirmación -->
    <div v-else-if="step === 'confirm'" class="max-w-lg mx-auto px-6 py-20 text-center">
      <div class="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-8 h-8 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
      </div>
      <h2 class="text-2xl font-bold text-gray-800 mb-2">¡Pedido enviado!</h2>
      <p class="text-gray-400 text-sm mb-8">Tu pedido está siendo preparado. En breve lo recibirás en la mesa {{ selectedTable?.number }}.</p>
      <button
        @click="resetOrder"
        class="px-6 py-3 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-colors"
      >
        Hacer otro pedido
      </button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { makeMenuApi } from '@/api/makeMenu'

const route = useRoute()
const cif = route.params.cif as string

const step = ref<'table' | 'menu' | 'confirm'>('table')
const establishmentName = ref('')
const tables = ref<any[]>([])
const products = ref<any[]>([])
const categories = ref<any[]>([])
const selectedTable = ref<any>(null)
const activeCategory = ref<number | null>(null)
const cart = ref<{ product: any; quantity: number }[]>([])
const isLoadingTables = ref(false)
const isLoadingProducts = ref(false)
const isSending = ref(false)

const fetchTables = async () => {
  isLoadingTables.value = true
  try {
    const { data } = await makeMenuApi.get(`/menu/${cif}/tables/`)
    tables.value = data
  } catch {
    console.error('Error cargando mesas')
  } finally {
    isLoadingTables.value = false
  }
}

const fetchProducts = async () => {
  isLoadingProducts.value = true
  try {
    const { data } = await makeMenuApi.get(`/menu/${cif}/products/`)
    products.value = data

    const seen = new Set()
    categories.value = data
      .map((p: any) => p.category)
      .filter((cat: any) => {
        if (seen.has(cat.id)) return false
        seen.add(cat.id)
        return true
      })
  } catch {
    console.error('Error cargando productos')
  } finally {
    isLoadingProducts.value = false
  }
}

const fetchEstablishment = async () => {
  try {
    const { data } = await makeMenuApi.get(`/establishments/${cif}/`)
    establishmentName.value = data.name
  } catch {
    establishmentName.value = 'Restaurante'
  }
}

const selectTable = async (table: any) => {
  selectedTable.value = table
  step.value = 'menu'
  if (!products.value.length) await fetchProducts()
}

const filteredGrouped = computed(() => {
  const filtered = activeCategory.value
    ? products.value.filter(p => p.category.id === activeCategory.value)
    : products.value

  return filtered.reduce((groups: Record<string, any[]>, product) => {
    const cat = product.category.name
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(product)
    return groups
  }, {})
})

const cartQuantity = (productId: number) => {
  return cart.value.find(i => i.product.id === productId)?.quantity ?? 0
}

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

const cartTotal = computed(() => {
  return cart.value
    .reduce((sum, item) => sum + item.product.price * item.quantity, 0)
    .toFixed(2)
})

const sendOrder = async () => {
  if (!cart.value.length || !selectedTable.value) return
  isSending.value = true
  try {
    await makeMenuApi.post(`/orders/public/${cif}/`, {
      table: selectedTable.value.number,
      items: cart.value.map(i => ({
        product_id: i.product.id,
        quantity: i.quantity,
      })),
    })
    step.value = 'confirm'
  } catch {
    console.error('Error enviando pedido')
  } finally {
    isSending.value = false
  }
}

const resetOrder = () => {
  cart.value = []
  selectedTable.value = null
  step.value = 'table'
}

onMounted(async () => {
  await fetchEstablishment()
  await fetchTables()
})
</script>