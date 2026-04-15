<template>
  <div class="space-y-6">

    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-700">Carta pública</h2>
      <div class="flex items-center gap-3">
        <select
          v-model="activeCif"
          @change="onEstablishmentChange"
          class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-lg p-2 outline-none cursor-pointer focus:ring-2 focus:ring-emerald-300"
        >
          <option v-for="est in myEstablishments" :key="est.cif" :value="est.cif">
            {{ est.name }}
          </option>
        </select>
        <a
          v-if="activeCif"
          :href="`/menu/${activeCif}`"
          target="_blank"
          class="flex items-center gap-2 px-4 py-2 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-all shadow-md shadow-emerald-400/20"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15 3 21 3 21 9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
          Ver carta
        </a>
      </div>
    </div>

    <div v-if="!myEstablishments.length && !isLoadingEstablishments" class="text-center py-16 text-gray-400">
      <p class="text-lg font-medium">No gestionas ningún establecimiento</p>
    </div>

    <template v-else-if="activeCif">

      <div v-if="isLoading" class="text-center py-12 text-gray-400">
        Cargando productos...
      </div>

      <div v-else-if="products.length" class="space-y-3">

        <div v-for="(group, category) in groupedProducts" :key="category">
          <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-2 px-1">
            {{ category }}
          </h3>
          <div class="bg-white border border-gray-200 rounded-2xl overflow-hidden divide-y divide-gray-100">
            <div
              v-for="product in group"
              :key="product.id"
              class="flex items-center gap-4 px-4 py-3"
            >
              <img
                v-if="product.product_image"
                :src="product.product_image"
                :alt="product.name"
                class="w-12 h-12 rounded-xl object-cover flex-shrink-0"
              />
              <div v-else class="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d='M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2'/>
                  <path d='M7 2v20'/>
                  <path d='M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1'/>
                  <path d='M21 22v-7'/>
                </svg>
              </div>

              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-800 truncate">{{ product.name }}</p>
                <p class="text-xs text-gray-400 truncate">{{ product.description || '—' }}</p>
              </div>

              <span class="text-emerald-600 font-bold text-sm whitespace-nowrap">{{ product.price }}€</span>

              <button
                @click="handleToggle(product)"
                :class="product.available
                  ? 'bg-emerald-400 hover:bg-emerald-500'
                  : 'bg-gray-200 hover:bg-gray-300'"
                class="relative inline-flex h-6 w-11 flex-shrink-0 rounded-full transition-colors duration-200"
                :title="product.available ? 'Visible en carta' : 'Oculto en carta'"
              >
                <span
                  :class="product.available ? 'translate-x-5' : 'translate-x-1'"
                  class="inline-block h-4 w-4 mt-1 rounded-full bg-white shadow transition-transform duration-200"
                ></span>
              </button>
            </div>
          </div>
        </div>

      </div>

      <div v-else class="text-center py-16 text-gray-400">
        <p class="text-lg font-medium">No hay productos aún</p>
        <p class="text-sm">Añade productos desde la sección Productos</p>
      </div>

    </template>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { getProductsAction, toggleProductAvailableAction } from '../actions/getProducts.action'
import { useToast } from '@/composables/useToast'
import type { Product } from '../interfaces/product.interface'

const toast = useToast()

const myEstablishments = ref<any[]>([])
const activeCif = ref('')
const isLoadingEstablishments = ref(true)
const products = ref<Product[]>([])
const isLoading = ref(false)

const fetchMyEstablishments = async () => {
  isLoadingEstablishments.value = true
  try {
    const { data } = await makeMenuApi.get('/establishments/')
    myEstablishments.value = data
    if (data.length > 0) {
      activeCif.value = data[0].cif
      await fetchProducts()
    }
  } catch {
    toast.error('Error cargando establecimientos.')
  } finally {
    isLoadingEstablishments.value = false
  }
}

const fetchProducts = async () => {
  isLoading.value = true
  try {
    products.value = await getProductsAction(activeCif.value)
  } catch {
    toast.error('Error cargando productos.')
  } finally {
    isLoading.value = false
  }
}

const onEstablishmentChange = async () => {
  await fetchProducts()
}

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
  } catch {
    toast.error('Error al actualizar el producto.')
  }
}

onMounted(() => { fetchMyEstablishments() })
</script>