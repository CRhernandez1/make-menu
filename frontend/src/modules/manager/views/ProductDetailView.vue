<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center gap-4">
      <button @click="$router.back()" class="w-10 h-10 rounded-[14px] bg-white border border-border-green text-text-muted flex items-center justify-center cursor-pointer hover:bg-green-soft hover:text-green-forest hover:border-[rgba(26,92,46,0.2)] transition-all">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
      </button>
      <div>
        <h2 class="font-display text-xl font-bold text-green-forest tracking-tight">{{ product?.name ?? 'Cargando...' }}</h2>
        <p class="text-sm text-text-muted">Gestión de ingredientes y componentes</p>
      </div>
    </div>

    <!-- Info del producto -->
    <div v-if="product" class="card-mm p-6 flex gap-5 items-center !cursor-default !transform-none">
      <img v-if="product.product_image" :src="product.product_image" :alt="product.name" class="w-20 h-20 object-cover rounded-2xl border border-border-green-light" />
      <div v-else class="w-20 h-20 bg-cream rounded-2xl flex items-center justify-center text-text-ghost">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
      </div>
      <div class="flex-1 space-y-1.5">
        <h3 class="font-bold text-ink text-[16px]">{{ product.name }}</h3>
        <span class="badge-mm bg-green-soft text-green-forest">{{ product.category.name }}</span>
        <p class="text-sm text-text-sec">{{ product.description }}</p>
      </div>
      <span class="font-display text-green-forest font-bold text-2xl tracking-tight">{{ product.price }}€</span>
    </div>

    <!-- Componentes -->
    <div class="bg-white border border-border-green-light rounded-[var(--radius-card)] overflow-hidden">
      <div class="flex items-center justify-between px-6 py-5 border-b border-border-green-light">
        <h3 class="font-display text-[15px] font-bold text-ink tracking-tight">Ingredientes del producto</h3>
        <button @click="openModal()" class="btn-mm btn-primary text-[12px] px-4 py-2">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Añadir
        </button>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="p-8 space-y-4">
        <div v-for="n in 3" :key="n" class="flex items-center gap-6">
          <div class="h-4 w-32 rounded-xl skeleton-mm"></div>
          <div class="h-4 w-16 rounded-xl skeleton-mm"></div>
          <div class="h-4 w-16 rounded-xl skeleton-mm"></div>
          <div class="h-6 w-12 rounded-full skeleton-mm"></div>
        </div>
      </div>

      <!-- Tabla -->
      <div v-else-if="components.length">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-border-green-light bg-cream">
                <th class="text-left px-6 py-3 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Ingrediente</th>
                <th class="text-left px-6 py-3 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Cantidad</th>
                <th class="text-left px-6 py-3 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Unidad</th>
                <th class="text-left px-6 py-3 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em]">Removible</th>
                <th class="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="component in components" :key="component.id" class="border-b border-border-green-light last:border-b-0 hover:bg-green-soft-2 transition-colors">
                <td class="px-6 py-4 font-semibold text-ink">{{ component.ingredient_name }}</td>
                <td class="px-6 py-4 text-text-sec font-display font-medium">{{ component.quantity }}</td>
                <td class="px-6 py-4 text-text-sec">{{ unityLabel(component.unity) }}</td>
                <td class="px-6 py-4">
                  <span class="badge-mm" :class="component.removable ? 'bg-info-soft text-info' : 'bg-cream-dark text-text-muted'">
                    {{ component.removable ? 'Sí' : 'No' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <button @click="openDeleteModal(component)" title="Eliminar"
                    class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-danger-soft hover:text-danger hover:border-[rgba(185,60,60,0.15)]">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty -->
      <div v-else class="p-16 text-center">
        <div class="w-16 h-16 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-4" style="animation:float 6s ease-in-out infinite">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
        </div>
        <h3 class="font-display text-base font-bold text-ink mb-1">Sin ingredientes asignados</h3>
        <p class="text-sm text-text-muted">Añade los ingredientes que componen este producto.</p>
      </div>
    </div>

    <!-- Modal añadir componente -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-50 p-4" @click.self="closeModal">
          <div class="bg-white rounded-[28px] shadow-[0_40px_100px_rgba(26,92,46,0.12)] w-full max-w-md">
            <div class="px-7 pt-7 pb-2 flex items-start justify-between">
              <div>
                <h3 class="font-display text-lg font-bold text-ink tracking-tight">Añadir ingrediente</h3>
                <p class="text-[13px] text-text-muted mt-1">Vincula un ingrediente a este producto.</p>
              </div>
              <button @click="closeModal" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <div class="px-7 py-5 space-y-5">
              <FormField :error="formErrors.errors.ingredient">
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Ingrediente</label>
                <select v-model="form.ingredient" class="input-mm cursor-pointer">
                  <option disabled :value="null">Selecciona un ingrediente</option>
                  <option v-for="ing in availableIngredients" :key="ing.id" :value="ing.id">{{ ing.name }}</option>
                </select>
              </FormField>

              <div class="grid grid-cols-2 gap-3">
                <FormField :error="formErrors.errors.quantity">
                  <label class="block text-[13px] font-semibold text-text-main mb-1.5">Cantidad</label>
                  <input v-model="form.quantity" type="number" step="0.01" placeholder="0.00" class="input-mm font-display" />
                </FormField>
                <FormField :error="formErrors.errors.unity">
                  <label class="block text-[13px] font-semibold text-text-main mb-1.5">Unidad</label>
                  <select v-model="form.unity" class="input-mm cursor-pointer">
                    <option disabled value="">Selecciona</option>
                    <option v-for="u in unities" :key="u.value" :value="u.value">{{ u.label }}</option>
                  </select>
                </FormField>
              </div>

              <label class="flex items-center gap-2.5 cursor-pointer group">
                <div class="w-[22px] h-[22px] rounded-[7px] border-2 flex items-center justify-center transition-all"
                  :class="form.removable ? 'bg-green-forest border-green-forest scale-105' : 'border-[rgba(26,92,46,0.2)] group-hover:border-[rgba(26,92,46,0.3)]'">
                  <svg v-if="form.removable" class="w-3 h-3 text-cream" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <input v-model="form.removable" type="checkbox" class="sr-only" />
                <span class="text-sm text-text-sec">El cliente puede pedir que se quite</span>
              </label>

              <div class="flex gap-3 pt-2">
                <button @click="closeModal" class="btn-mm btn-ghost text-[13px] px-5 py-2.5 flex-1">Cancelar</button>
                <button @click="handleAddComponent" :disabled="formSubmitting"
                  class="btn-mm btn-primary text-[13px] px-5 py-2.5 flex-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                  <span v-if="formSubmitting" class="w-4 h-4 border-2 border-cream/30 border-t-cream rounded-full animate-spin"></span>
                  Añadir
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <ConfirmModal :visible="showDeleteModal" title="¿Eliminar ingrediente?"
      :message="`Se eliminará &quot;${componentToDelete?.ingredient_name}&quot; de este producto.`"
      confirm-text="Eliminar" :submitting="deleteSubmitting" @confirm="handleDeleteComponent" @cancel="closeDeleteModal" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { makeMenuApi } from '@/api/makeMenu'
import { useProductsStore } from '../stores/products.store'
import { useToast } from '@/composables/useToast'
import { useFormErrors } from '@/composables/useFormErrors'
import FormField from '@/components/FormField.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import type { Product } from '../interfaces/product.interface'

const route = useRoute()
const productsStore = useProductsStore()
const toast = useToast()
const formErrors = useFormErrors()

const productId = Number(route.params.productId)
const activeCif = ref(route.query.cif as string)
const product = ref<Product | null>(null)
const components = ref<any[]>([])
const isLoading = ref(true)

const unities = [
  { value: 'ea', label: 'Unidad' }, { value: 'gr', label: 'Gramos' },
  { value: 'kg', label: 'Kilogramos' }, { value: 'l', label: 'Litros' }, { value: 'ml', label: 'Mililitros' },
]
const unityLabel = (value: string) => unities.find(u => u.value === value)?.label ?? value

const availableIngredients = computed(() =>
  productsStore.ingredients.filter(ing => !components.value.some(c => c.ingredient === ing.id))
)

const fetchData = async () => {
  isLoading.value = true
  try {
    if (!activeCif.value) return
    const { data: prod } = await makeMenuApi.get(`/establishments/${activeCif.value}/products/${productId}/`)
    product.value = prod
    const { data: comps } = await makeMenuApi.get(`/establishments/${activeCif.value}/products/${productId}/components/`)
    components.value = comps
    await productsStore.fetchIngredients(activeCif.value)
  } catch { toast.error('Error cargando datos del producto.') }
  finally { isLoading.value = false }
}

onMounted(fetchData)

const showModal = ref(false)
const formSubmitting = ref(false)
const form = ref({ ingredient: null as number | null, quantity: 1, unity: '', removable: false })

const openModal = () => { form.value = { ingredient: null, quantity: 1, unity: '', removable: false }; formErrors.clear(); showModal.value = true }
const closeModal = () => { showModal.value = false; formErrors.clear() }

const handleAddComponent = async () => {
  const valid = formErrors.validate({
    ingredient: [{ value: form.value.ingredient, message: 'Selecciona un ingrediente.' }],
    quantity: [{ value: form.value.quantity, message: 'La cantidad debe ser mayor a 0.' }],
    unity: [{ value: form.value.unity, message: 'Selecciona una unidad.' }],
  })
  if (!valid) return
  formSubmitting.value = true
  try {
    await makeMenuApi.post(`/establishments/${activeCif.value}/products/${productId}/components/add/`, {
      ingredient: form.value.ingredient, quantity: form.value.quantity, unity: form.value.unity, removable: form.value.removable,
    })
    const { data } = await makeMenuApi.get(`/establishments/${activeCif.value}/products/${productId}/components/`)
    components.value = data
    toast.success('Ingrediente añadido al producto.')
    closeModal()
  } catch (err: any) {
    if (err.response?.data?.errors) { formErrors.setFromBackend(err.response.data.errors) }
    else { toast.error(err.response?.data?.error || 'Error al añadir el ingrediente.') }
  } finally { formSubmitting.value = false }
}

const showDeleteModal = ref(false)
const componentToDelete = ref<any>(null)
const deleteSubmitting = ref(false)
const openDeleteModal = (component: any) => { componentToDelete.value = component; showDeleteModal.value = true }
const closeDeleteModal = () => { showDeleteModal.value = false; componentToDelete.value = null }
const handleDeleteComponent = async () => {
  if (!componentToDelete.value) return
  deleteSubmitting.value = true
  try {
    await makeMenuApi.post(`/establishments/${activeCif.value}/products/${productId}/components/${componentToDelete.value.id}/delete/`)
    components.value = components.value.filter(c => c.id !== componentToDelete.value.id)
    toast.success('Ingrediente eliminado del producto.')
    closeDeleteModal()
  } catch { toast.error('Error al eliminar el ingrediente.') }
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