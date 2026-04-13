<template>
  <div class="space-y-6">

    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-700">Ingredientes</h2>
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
        <button
          @click="openModal()"
          :disabled="!activeCif"
          class="flex items-center gap-2 px-4 py-2 bg-emerald-400 text-white font-semibold rounded-xl hover:bg-emerald-500 transition-all shadow-md shadow-emerald-400/20 disabled:opacity-50"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Añadir ingrediente
        </button>
      </div>
    </div>

    <div v-if="productsStore.isLoading" class="text-center py-12 text-gray-400">
      Cargando ingredientes...
    </div>

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
              {{ ingredientTypes.find(t => t.value === ingredient.ingredient_type)?.label ?? ingredient.ingredient_type }}
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

        <div v-if="ingredient.allergens?.length" class="flex flex-wrap gap-1">
          <span
            v-for="allergen in ingredient.allergens"
            :key="allergen.id"
            class="text-xs bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-full font-medium"
          >
            {{ allergen.name }}
          </span>
        </div>
        <p v-else class="text-xs text-gray-300 italic">Sin alérgenos</p>

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
            @click="openDeleteModal(ingredient)"
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

    <div v-else class="text-center py-16 text-gray-400">
      <p class="text-lg font-medium">No hay ingredientes aún</p>
      <p class="text-sm">Añade tu primer ingrediente con el botón de arriba</p>
    </div>

    <!-- Modal crear/editar -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4 max-h-[90vh] overflow-y-auto">
          <h3 class="text-lg font-bold text-gray-700">
            {{ editingIngredient ? 'Editar ingrediente' : 'Nuevo ingrediente' }}
          </h3>

          <div class="space-y-3">
            <FormField :error="formErrors.errors.name">
              <input
                v-model="form.name"
                placeholder="Nombre"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              />
            </FormField>

            <textarea
              v-model="form.description"
              placeholder="Descripción (opcional)"
              rows="3"
              class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300 resize-none"
            />

            <FormField :error="formErrors.errors.ingredient_type">
              <select
                v-model="form.ingredient_type"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              >
                <option disabled value="">Selecciona un tipo</option>
                <option v-for="type in ingredientTypes" :key="type.value" :value="type.value">
                  {{ type.label }}
                </option>
              </select>
            </FormField>

            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-600">Alérgenos</label>
              <div class="flex flex-wrap gap-2 p-3 border border-gray-200 rounded-xl min-h-[48px]">
                <button
                  v-for="allergen in productsStore.allergens"
                  :key="allergen.id"
                  type="button"
                  @click="toggleAllergen(allergen.id)"
                  class="text-xs px-3 py-1 rounded-full border font-medium transition-colors"
                  :class="form.allergens.includes(allergen.id)
                    ? 'bg-amber-400 text-white border-amber-400'
                    : 'bg-white text-gray-500 border-gray-200 hover:border-amber-300 hover:text-amber-600'"
                >
                  {{ allergen.name }}
                </button>
                <span v-if="!productsStore.allergens.length" class="text-xs text-gray-300">
                  Cargando alérgenos...
                </span>
              </div>
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
              :disabled="formSubmitting"
              class="flex-1 px-4 py-2.5 rounded-xl bg-emerald-400 text-white text-sm font-semibold hover:bg-emerald-500 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {{ editingIngredient ? 'Guardar cambios' : 'Añadir' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modal eliminar -->
    <ConfirmModal
      :visible="showDeleteModal"
      title="Eliminar ingrediente"
      :message="`¿Eliminar &quot;${ingredientToDelete?.name}&quot;? Esta acción no se puede deshacer.`"
      confirm-text="Eliminar"
      :submitting="deleteSubmitting"
      @confirm="handleDelete"
      @cancel="closeDeleteModal"
    />

  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { makeMenuApi } from '@/api/makeMenu'
import { useProductsStore } from '../stores/products.store'
import { useToast } from '@/composables/useToast'
import { useFormErrors } from '@/composables/useFormErrors'
import FormField from '@/components/FormField.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import type { Ingredient } from '../interfaces/product.interface'

const productsStore = useProductsStore()
const toast = useToast()
const formErrors = useFormErrors()

const myEstablishments = ref<any[]>([])
const activeCif = ref('')

const fetchMyEstablishments = async () => {
  try {
    const { data } = await makeMenuApi.get('/establishments/')
    myEstablishments.value = data
    if (data.length > 0) {
      activeCif.value = data[0].cif
      await productsStore.fetchIngredients(activeCif.value)
    }
  } catch {
    toast.error('Error cargando establecimientos.')
  }
}

const onEstablishmentChange = async () => {
  await productsStore.fetchIngredients(activeCif.value)
}

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

onMounted(async () => {
  await fetchMyEstablishments()
  await productsStore.fetchAllergens()
})

// Modal crear/editar
const showModal = ref(false)
const editingIngredient = ref<Ingredient | null>(null)
const formSubmitting = ref(false)

const form = ref({
  name: '',
  description: '',
  ingredient_type: '',
  available: true,
  allergens: [] as number[],
})

const toggleAllergen = (id: number) => {
  const idx = form.value.allergens.indexOf(id)
  if (idx === -1) form.value.allergens.push(id)
  else form.value.allergens.splice(idx, 1)
}

const openModal = (ingredient?: Ingredient) => {
  editingIngredient.value = ingredient || null
  formErrors.clear()
  form.value = ingredient
    ? {
        name: ingredient.name,
        description: ingredient.description,
        ingredient_type: ingredient.ingredient_type,
        available: ingredient.available,
        allergens: ingredient.allergens?.map(a => a.id) ?? [],
      }
    : { name: '', description: '', ingredient_type: '', available: true, allergens: [] }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingIngredient.value = null
  formErrors.clear()
}

const handleSave = async () => {
  const valid = formErrors.validate({
    name: [{ value: form.value.name.trim(), message: 'El nombre es obligatorio.' }],
    ingredient_type: [{ value: form.value.ingredient_type, message: 'Selecciona un tipo.' }],
  })
  if (!valid) return

  formSubmitting.value = true

  const payload = {
    name: form.value.name,
    description: form.value.description,
    ingredient_type: form.value.ingredient_type,
    available: form.value.available,
    allergens: form.value.allergens,
  }

  try {
    if (editingIngredient.value) {
      await productsStore.editIngredient(activeCif.value, editingIngredient.value.id, payload)
      toast.success('Ingrediente actualizado.')
    } else {
      await productsStore.addIngredient(activeCif.value, payload)
      toast.success('Ingrediente creado.')
    }
    closeModal()
  } catch (err: any) {
    if (err.response?.data?.errors) {
      formErrors.setFromBackend(err.response.data.errors)
    } else {
      toast.error(err.response?.data?.error || 'Error al guardar el ingrediente.')
    }
  } finally {
    formSubmitting.value = false
  }
}

// Modal eliminar
const showDeleteModal = ref(false)
const ingredientToDelete = ref<Ingredient | null>(null)
const deleteSubmitting = ref(false)

const openDeleteModal = (ingredient: Ingredient) => {
  ingredientToDelete.value = ingredient
  showDeleteModal.value = true
}
const closeDeleteModal = () => {
  showDeleteModal.value = false
  ingredientToDelete.value = null
}
const handleDelete = async () => {
  if (!ingredientToDelete.value) return
  deleteSubmitting.value = true
  try {
    await productsStore.deleteIngredient(activeCif.value, ingredientToDelete.value.id)
    toast.success('Ingrediente eliminado.')
    closeDeleteModal()
  } catch {
    toast.error('Error al eliminar. Puede estar asignado a un producto.')
  } finally {
    deleteSubmitting.value = false
  }
}
</script>