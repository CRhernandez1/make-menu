<template>
  <div class="space-y-6">

    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-700">Productos</h2>
      <button
        @click="openModal()"
        class="flex items-center gap-2 px-4 py-2 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-all shadow-md shadow-emerald-400/20"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Añadir producto
      </button>
    </div>

    <div v-if="productsStore.isLoading" class="text-center py-12 text-gray-400">
      Cargando productos...
    </div>

    <div v-else-if="productsStore.products.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="product in productsStore.products"
        :key="product.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden"
      >
        <img
          v-if="product.product_image"
          :src="product.product_image"
          :alt="product.name"
          class="w-full h-40 object-cover"
        />
        <div v-else class="w-full h-40 bg-gray-100 flex items-center justify-center text-gray-300">
          <svg class="w-12 h-12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d='M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2'/>
            <path d='M7 2v20'/>
            <path d='M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1'/>
            <path d='M21 22v-7'/>
          </svg>
        </div>

        <div class="p-4 space-y-2">
          <div class="flex items-start justify-between gap-2">
            <div>
              <h3 class="font-semibold text-gray-800">{{ product.name }}</h3>
              <span class="text-xs text-emerald-600 font-medium bg-emerald-50 px-2 py-0.5 rounded-full">
                {{ product.category.name }}
              </span>
            </div>
            <span class="text-emerald-600 font-bold text-lg whitespace-nowrap">{{ product.price }}€</span>
          </div>

          <p class="text-sm text-gray-500 line-clamp-2">{{ product.description }}</p>

          <div class="flex items-center justify-between pt-1">
            <span
              class="text-xs font-semibold px-2 py-1 rounded-full"
              :class="product.available ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
            >
              {{ product.available ? 'Disponible' : 'No disponible' }}
            </span>

            <div class="flex gap-2">
              <button
                @click="openModal(product)"
                class="p-2 text-gray-400 hover:text-emerald-500 hover:bg-emerald-50 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
              <button
                @click="handleDelete(product.id)"
                class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
              >
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                  <path d="M10 11v6M14 11v6"/>
                  <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-16 text-gray-400">
      <p class="text-lg font-medium">No hay productos aún</p>
      <p class="text-sm">Añade tu primer producto con el botón de arriba</p>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-lg font-bold text-gray-700">
          {{ editingProduct ? 'Editar producto' : 'Nuevo producto' }}
        </h3>

        <div class="space-y-3">
          <input
            v-model="form.name"
            placeholder="Nombre"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
          />

          <textarea
            v-model="form.description"
            placeholder="Descripción"
            rows="3"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300 resize-none"
          />

          <input
            v-model="form.price"
            type="number"
            step="0.01"
            placeholder="Precio"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
          />

          <select
            v-model="form.category_id"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
          >
            <option disabled :value="null">Selecciona una categoría</option>
            <option
              v-for="cat in productsStore.categories"
              :key="cat.id"
              :value="cat.id"
            >
              {{ cat.name }}
            </option>
          </select>

          <!-- Imagen -->
          <div class="space-y-2">
            <label class="text-sm text-gray-500">Imagen del producto</label>
            <input
              type="file"
              accept="image/*"
              @change="onImageChange"
              class="w-full text-sm text-gray-500 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-emerald-50 file:text-emerald-700 file:font-semibold hover:file:bg-emerald-100"
            />
            <img
              v-if="imagePreview"
              :src="imagePreview"
              class="w-full h-32 object-cover rounded-xl border border-gray-100"
            />
          </div>

          <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input v-model="form.available" type="checkbox" class="accent-emerald-500" />
            Disponible
          </label>
        </div>

        <div class="flex gap-3 pt-2">
          <button
            @click="closeModal"
            class="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            @click="handleSave"
            class="flex-1 px-4 py-2.5 rounded-xl bg-emerald-400 text-white text-sm font-semibold hover:bg-emerald-500"
          >
            {{ editingProduct ? 'Guardar cambios' : 'Añadir' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useProductsStore } from '../stores/products.store'
import { useAuthStore } from '@/modules/auth/stores/auth.store'
import type { Product } from '../interfaces/product.interface'

const productsStore = useProductsStore()
const authStore = useAuthStore()
const cif = authStore.user?.establishment_cif as string

onMounted(() => {
  productsStore.fetchProducts(cif)
  productsStore.fetchCategories(cif)
})

// Modal
const showModal = ref(false)
const editingProduct = ref<Product | null>(null)
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)

const form = ref({
  name: '',
  description: '',
  price: 0,
  available: true,
  category_id: null as number | null,
})

const onImageChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  imageFile.value = file
  imagePreview.value = URL.createObjectURL(file)
}

const openModal = (product?: Product) => {
  editingProduct.value = product || null
  imageFile.value = null
  imagePreview.value = product?.product_image || null
  form.value = product
    ? {
        name: product.name,
        description: product.description,
        price: product.price,
        available: product.available,
        category_id: product.category.id,
      }
    : { name: '', description: '', price: 0, available: true, category_id: null }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingProduct.value = null
  imageFile.value = null
  imagePreview.value = null
}

const handleSave = async () => {
  const payload = {
    name: form.value.name,
    description: form.value.description,
    price: form.value.price,
    available: form.value.available,
    category: form.value.category_id,
  }

  if (editingProduct.value) {
    await productsStore.editProduct(cif, editingProduct.value.id, payload)
  } else {
    await productsStore.addProduct(cif, payload)
  }
  closeModal()
}

const handleDelete = async (productId: number) => {
  if (confirm('¿Seguro que quieres eliminar este producto?')) {
    await productsStore.deleteProduct(cif, productId)
  }
}
</script>