<template>
  <div class="space-y-6">

    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
      <h2 class="font-display text-2xl font-bold text-green-forest tracking-tight">Ingredientes</h2>
      <div class="flex items-center gap-3">
        <select v-model="activeCif" @change="onEstablishmentChange" class="input-mm !w-auto !h-11 pr-10 cursor-pointer text-[13px]">
          <option v-for="est in myEstablishments" :key="est.cif" :value="est.cif">{{ est.name }}</option>
        </select>
        <button @click="openModal()" :disabled="!activeCif" class="btn-mm btn-primary text-[13px] px-5 py-2.5 disabled:opacity-50 disabled:transform-none disabled:cursor-not-allowed">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Añadir ingrediente
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="productsStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="n in 6" :key="n" class="bg-white rounded-[var(--radius-card)] border border-border-green-light p-5 space-y-3">
        <div class="flex justify-between"><div class="h-4 w-1/2 rounded-xl skeleton-mm"></div><div class="h-6 w-20 rounded-full skeleton-mm"></div></div>
        <div class="h-3 w-3/4 rounded-lg skeleton-mm"></div>
        <div class="flex gap-2"><div class="h-5 w-16 rounded-full skeleton-mm"></div><div class="h-5 w-14 rounded-full skeleton-mm"></div></div>
      </div>
    </div>

    <!-- Grid -->
    <div v-else-if="productsStore.ingredients.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="ingredient in productsStore.ingredients" :key="ingredient.id" class="card-mm p-6 space-y-3">
        <div class="flex items-start justify-between gap-3">
          <div class="space-y-1.5">
            <h3 class="font-bold text-ink text-[15px]">{{ ingredient.name }}</h3>
            <span class="badge-mm bg-info-soft text-info capitalize">
              {{ ingredientTypes.find(t => t.value === ingredient.ingredient_type)?.label ?? ingredient.ingredient_type }}
            </span>
          </div>
          <span class="badge-mm" :class="ingredient.available ? 'bg-green-soft text-green-forest' : 'bg-danger-soft text-danger'">
            <span class="w-1.5 h-1.5 rounded-full" :class="ingredient.available ? 'bg-green-bright' : 'bg-danger'"></span>
            {{ ingredient.available ? 'Disponible' : 'No disponible' }}
          </span>
        </div>

        <p v-if="ingredient.description" class="text-sm text-text-sec line-clamp-2">{{ ingredient.description }}</p>
        <p v-else class="text-sm text-text-ghost italic">Sin descripción</p>

        <div v-if="ingredient.allergens?.length" class="flex flex-wrap gap-1.5">
          <span v-for="allergen in ingredient.allergens" :key="allergen.id"
            class="text-[10px] font-semibold bg-warning-soft text-warning border border-[rgba(196,138,26,0.15)] px-2.5 py-0.5 rounded-full">
            {{ allergen.name }}
          </span>
        </div>
        <p v-else class="text-xs text-text-ghost italic">Sin alérgenos</p>

        <div class="flex justify-end gap-1.5 pt-2 border-t border-border-green-light">
          <button @click="openModal(ingredient)" title="Editar"
            class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-warning-soft hover:text-warning hover:border-[rgba(196,138,26,0.15)]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          </button>
          <button @click="openDeleteModal(ingredient)" title="Eliminar"
            class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-danger-soft hover:text-danger hover:border-[rgba(185,60,60,0.15)]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
      <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-ink mb-2">No hay ingredientes aún</h3>
      <p class="text-sm text-text-muted mb-6">Añade tu primer ingrediente con el botón de arriba.</p>
    </div>

    <!-- Modal crear/editar -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-50 p-4" @click.self="closeModal">
          <div class="bg-white rounded-[28px] shadow-[0_40px_100px_rgba(26,92,46,0.12)] w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div class="px-7 pt-7 pb-2 flex items-start justify-between">
              <div>
                <h3 class="font-display text-lg font-bold text-ink tracking-tight">{{ editingIngredient ? 'Editar ingrediente' : 'Nuevo ingrediente' }}</h3>
                <p class="text-[13px] text-text-muted mt-1">{{ editingIngredient ? 'Actualiza los datos.' : 'Añade un nuevo ingrediente.' }}</p>
              </div>
              <button @click="closeModal" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <div class="px-7 py-5 space-y-5">
              <FormField :error="formErrors.errors.name">
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Nombre</label>
                <input v-model="form.name" placeholder="Ej: Tomate cherry" class="input-mm" />
              </FormField>

              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Descripción <span class="text-text-muted font-normal">(opcional)</span></label>
                <textarea v-model="form.description" placeholder="Descripción del ingrediente..." rows="3" class="input-mm !h-auto py-3 resize-none"></textarea>
              </div>

              <FormField :error="formErrors.errors.ingredient_type">
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Tipo</label>
                <select v-model="form.ingredient_type" class="input-mm cursor-pointer">
                  <option disabled value="">Selecciona un tipo</option>
                  <option v-for="type in ingredientTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
                </select>
              </FormField>

              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-2">Alérgenos</label>
                <div class="flex flex-wrap gap-2 p-4 border-[1.5px] border-border-green rounded-2xl min-h-[52px] bg-cream">
                  <button v-for="allergen in productsStore.allergens" :key="allergen.id" type="button" @click="toggleAllergen(allergen.id)"
                    class="text-xs px-3.5 py-1.5 rounded-full border-[1.5px] font-semibold transition-all cursor-pointer"
                    :class="form.allergens.includes(allergen.id)
                      ? 'bg-warning text-white border-warning'
                      : 'bg-white text-text-sec border-border-green hover:border-warning hover:text-warning'">
                    {{ allergen.name }}
                  </button>
                  <span v-if="!productsStore.allergens.length" class="text-xs text-text-ghost">Cargando alérgenos...</span>
                </div>
              </div>

              <label class="flex items-center gap-2.5 cursor-pointer group">
                <div class="w-[22px] h-[22px] rounded-[7px] border-2 flex items-center justify-center transition-all"
                  :class="form.available ? 'bg-green-forest border-green-forest scale-105' : 'border-[rgba(26,92,46,0.2)] group-hover:border-[rgba(26,92,46,0.3)]'">
                  <svg v-if="form.available" class="w-3 h-3 text-cream" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <input v-model="form.available" type="checkbox" class="sr-only" />
                <span class="text-sm text-text-sec">Disponible</span>
              </label>

              <div class="flex gap-3 pt-2">
                <button @click="closeModal" class="btn-mm btn-ghost text-[13px] px-5 py-2.5 flex-1">Cancelar</button>
                <button @click="handleSave" :disabled="formSubmitting"
                  class="btn-mm btn-primary text-[13px] px-5 py-2.5 flex-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                  <span v-if="formSubmitting" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
                  {{ editingIngredient ? 'Guardar cambios' : 'Añadir' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <ConfirmModal :visible="showDeleteModal" title="¿Eliminar ingrediente?"
      :message="`Se eliminará &quot;${ingredientToDelete?.name}&quot;. No se puede deshacer.`"
      confirm-text="Eliminar" :submitting="deleteSubmitting" @confirm="handleDelete" @cancel="closeDeleteModal" />
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
  } catch { toast.error('Error cargando establecimientos.') }
}

const onEstablishmentChange = async () => { await productsStore.fetchIngredients(activeCif.value) }

const ingredientTypes = [
  { value: 'meat', label: 'Carne' }, { value: 'fish', label: 'Pescado' },
  { value: 'vegetables', label: 'Verduras' }, { value: 'dairy', label: 'Lácteos' },
  { value: 'bakery', label: 'Panadería' }, { value: 'sauces', label: 'Salsas' },
  { value: 'drinks', label: 'Bebidas' }, { value: 'other', label: 'Otros' },
]

onMounted(async () => { await fetchMyEstablishments(); await productsStore.fetchAllergens() })

const showModal = ref(false)
const editingIngredient = ref<Ingredient | null>(null)
const formSubmitting = ref(false)
const form = ref({ name: '', description: '', ingredient_type: '', available: true, allergens: [] as number[] })

const toggleAllergen = (id: number) => {
  const idx = form.value.allergens.indexOf(id)
  if (idx === -1) form.value.allergens.push(id)
  else form.value.allergens.splice(idx, 1)
}

const openModal = (ingredient?: Ingredient) => {
  editingIngredient.value = ingredient || null; formErrors.clear()
  form.value = ingredient
    ? { name: ingredient.name, description: ingredient.description, ingredient_type: ingredient.ingredient_type, available: ingredient.available, allergens: ingredient.allergens?.map(a => a.id) ?? [] }
    : { name: '', description: '', ingredient_type: '', available: true, allergens: [] }
  showModal.value = true
}
const closeModal = () => { showModal.value = false; editingIngredient.value = null; formErrors.clear() }

const handleSave = async () => {
  const valid = formErrors.validate({
    name: [{ value: form.value.name.trim(), message: 'El nombre es obligatorio.' }],
    ingredient_type: [{ value: form.value.ingredient_type, message: 'Selecciona un tipo.' }],
  })
  if (!valid) return
  formSubmitting.value = true
  const payload = { name: form.value.name, description: form.value.description, ingredient_type: form.value.ingredient_type, available: form.value.available, allergens: form.value.allergens }
  try {
    if (editingIngredient.value) { await productsStore.editIngredient(activeCif.value, editingIngredient.value.id, payload); toast.success('Ingrediente actualizado.') }
    else { await productsStore.addIngredient(activeCif.value, payload); toast.success('Ingrediente creado.') }
    closeModal()
  } catch (err: any) {
    if (err.response?.data?.errors) { formErrors.setFromBackend(err.response.data.errors) }
    else { toast.error(err.response?.data?.error || 'Error al guardar el ingrediente.') }
  } finally { formSubmitting.value = false }
}

const showDeleteModal = ref(false)
const ingredientToDelete = ref<Ingredient | null>(null)
const deleteSubmitting = ref(false)
const openDeleteModal = (ingredient: Ingredient) => { ingredientToDelete.value = ingredient; showDeleteModal.value = true }
const closeDeleteModal = () => { showDeleteModal.value = false; ingredientToDelete.value = null }
const handleDelete = async () => {
  if (!ingredientToDelete.value) return
  deleteSubmitting.value = true
  try { await productsStore.deleteIngredient(activeCif.value, ingredientToDelete.value.id); toast.success('Ingrediente eliminado.'); closeDeleteModal() }
  catch { toast.error('Error al eliminar. Puede estar asignado a un producto.') }
  finally { deleteSubmitting.value = false }
}
</script>

<style scoped>
.modal-enter-active,.modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-active > div,.modal-leave-active > div { transition: transform 0.3s cubic-bezier(0.25,1,0.5,1), opacity 0.25s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div { transform: translateY(16px) scale(0.96); opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div { transform: translateY(-8px) scale(0.97); opacity: 0; }
</style>