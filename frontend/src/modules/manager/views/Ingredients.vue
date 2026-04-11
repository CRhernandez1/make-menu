<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-700">Ingredientes</h2>
      <button
        @click="openModal()"
        class="flex items-center gap-2 px-4 py-2 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-all shadow-md shadow-emerald-400/20"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Añadir ingrediente
      </button>
    </div>

    <!-- Loading -->
    <div v-if="productsStore.isLoading" class="text-center py-12 text-gray-400">
      Cargando ingredientes...
    </div>

    <!-- Lista -->
    <div v-else-if="productsStore.ingredients.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="ingredient in productsStore.ingredients"
        :key="ingredient.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 space-y-3"
      >
        <div class="flex items-start justify-between gap-2">
          <div class="space-y-1">
            <h3 class="font-semibold text-gray-800">{{ ingredient.name }}</h3>
            <span class="text-xs font-medium bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full capitalize">
              {{ ingredient.ingredient_type }}
            </span>
          </div>
          <span
            class="text-xs font-semibold px-2 py-1 rounded-full whitespace-nowrap"
            :class="ingredient.available ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
          >
            {{ ingredient.available ? 'Disponible' : 'No disponible' }}
          </span>
        </div>

        <p v-if="ingredient.description" class="text-sm text-gray-500 line-clamp-2">
          {{ ingredient.description }}
        </p>
        <p v-else class="text-sm text-gray-300 italic">Sin descripción</p>

        <div class="flex justify-end gap-2 pt-1">
          <button
            @click="openModal(ingredient)"
            class="p-2 text-gray-400 hover:text-emerald-500 hover:bg-emerald-50 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button
            @click="handleDelete(ingredient.id)"
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

    <!-- Vacío -->
    <div v-else class="text-center py-16 text-gray-400">
      <p class="text-lg font-medium">No hay ingredientes aún</p>
      <p class="text-sm">Añade tu primer ingrediente con el botón de arriba</p>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-lg font-bold text-gray-700">
          {{ editingIngredient ? 'Editar ingrediente' : 'Nuevo ingrediente' }}
        </h3>

        <div class="space-y-3">
          <input
            v-model="form.name"
            placeholder="Nombre"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
          />

          <textarea
            v-model="form.description"
            placeholder="Descripción (opcional)"
            rows="3"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300 resize-none"
          />

          <select
            v-model="form.ingredient_type"
            class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
          >
            <option disabled value="">Selecciona un tipo</option>
            <option v-for="type in ingredientTypes" :key="type.value" :value="type.value">
              {{ type.label }}
            </option>
          </select>

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
            {{ editingIngredient ? 'Guardar cambios' : 'Añadir' }}
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
import type { Ingredient } from '../interfaces/product.interface'

const productsStore = useProductsStore()
const authStore = useAuthStore()
const cif = authStore.user?.establishment_cif as string

const ingredientTypes = [
  { value: 'meat', label: 'Carne' },
  { value: 'fish', label: 'Pescado' },
  { value: 'vegetables', label: 'Verduras' },
  { value: 'dairy', label: 'Lácteos' },
  { value: 'bakery', label: 'Panadería' },
  { value: 'sauces', label: 'Salsas' },
  { value: 'drinks', label: 'Bebidas' },
  { value: 'other', label: 'Otros' },
]

onMounted(() => productsStore.fetchIngredients(cif))

const showModal = ref(false)
const editingIngredient = ref<Ingredient | null>(null)

const form = ref({
  name: '',
  description: '',
  ingredient_type: '',
  available: true,
})

const openModal = (ingredient?: Ingredient) => {
  editingIngredient.value = ingredient || null
  form.value = ingredient
    ? {
        name: ingredient.name,
        description: ingredient.description,
        ingredient_type: ingredient.ingredient_type,
        available: ingredient.available,
      }
    : { name: '', description: '', ingredient_type: '', available: true }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingIngredient.value = null
}

const handleSave = async () => {
  if (editingIngredient.value) {
    await productsStore.editIngredient(cif, editingIngredient.value.id, form.value)
  } else {
    await productsStore.addIngredient(cif, form.value)
  }
  closeModal()
}

const handleDelete = async (ingredientId: number) => {
  if (confirm('¿Seguro que quieres eliminar este ingrediente?')) {
    await productsStore.deleteIngredient(cif, ingredientId)
  }
}
</script>