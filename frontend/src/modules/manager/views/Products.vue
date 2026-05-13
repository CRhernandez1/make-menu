<template>
  <div class="space-y-6">

    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
      <h2 class="font-display text-2xl font-bold text-green-forest tracking-tight">Productos</h2>
      <div class="flex items-center gap-3">
        <select
          v-model="activeCif"
          @change="onEstablishmentChange"
          class="input-mm !w-auto !h-11 pr-10 cursor-pointer text-[13px]"
        >
          <option v-for="est in myEstablishments" :key="est.cif" :value="est.cif">{{ est.name }}</option>
        </select>
        <button @click="openModal()" :disabled="!activeCif" class="btn-mm btn-primary text-[13px] px-5 py-2.5 disabled:opacity-50 disabled:transform-none disabled:cursor-not-allowed">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Añadir producto
        </button>
      </div>
    </div>

    <div v-if="!myEstablishments.length && !isLoadingEstablishments" class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
      <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-ink mb-2">No gestionas ningún establecimiento</h3>
    </div>

    <template v-else-if="activeCif">

      <!-- Categorías -->
      <div class="bg-white border border-border-green-light rounded-[var(--radius-card)] p-5">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-[13px] font-bold text-ink">Categorías</h3>
          <div class="flex items-center gap-2">
            <input v-model="newCategory" placeholder="Nueva categoría..." class="input-mm !h-9 !text-[13px] !w-48" @keyup.enter="handleAddCategory" />
            <button @click="handleAddCategory" class="btn-mm btn-primary text-[12px] px-4 py-2">Añadir</button>
          </div>
        </div>
        <div class="flex flex-wrap gap-2">
          <span v-for="cat in productsStore.categories" :key="cat.id" 
                @click="toggleCategoryFilter(cat.id)"
                class="badge-mm cursor-pointer transition-colors"
                :class="selectedCategoryId === cat.id ? 'bg-green-forest text-white' : 'bg-green-soft text-green-forest hover:bg-[rgba(26,92,46,0.12)]'">
            {{ cat.name }}
            <button @click.stop="openDeleteCategoryModal(cat.id)" class="hover:text-danger transition-colors font-bold leading-none ml-1 opacity-70 hover:opacity-100">×</button>
          </span>
          <span v-if="!productsStore.categories.length" class="text-xs text-text-muted">No hay categorías aún</span>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="productsStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <div v-for="n in 6" :key="n" class="bg-white rounded-[var(--radius-card)] border border-border-green-light overflow-hidden">
          <div class="h-40 skeleton-mm"></div>
          <div class="p-5 space-y-3"><div class="h-4 w-2/3 rounded-xl skeleton-mm"></div><div class="h-3 w-1/2 rounded-lg skeleton-mm"></div></div>
        </div>
      </div>

      <!-- Grid productos -->
      <div v-else-if="filteredProducts.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <div v-for="product in filteredProducts" :key="product.id" class="card-mm overflow-hidden !p-0">
          <img v-if="product.product_image" :src="product.product_image" :alt="product.name" class="w-full h-40 object-cover" />
          <div v-else class="w-full h-40 bg-cream flex items-center justify-center text-text-ghost">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1"/><path d="M21 22v-7"/></svg>
          </div>

          <div class="p-5 space-y-3">
            <div class="flex items-start justify-between gap-2">
              <div>
                <h3 class="font-bold text-ink text-[15px]">{{ product.name }}</h3>
                <span class="badge-mm bg-green-soft text-green-forest mt-1">{{ product.category.name }}</span>
              </div>
              <span class="font-display text-green-forest font-bold text-lg whitespace-nowrap">{{ product.price }}€</span>
            </div>

            <p class="text-sm text-text-sec line-clamp-2">{{ product.description }}</p>

            <div class="flex items-center justify-between pt-2 border-t border-border-green-light">
              <span class="badge-mm" :class="product.available ? 'bg-green-soft text-green-forest' : 'bg-danger-soft text-danger'">
                <span class="w-1.5 h-1.5 rounded-full" :class="product.available ? 'bg-green-bright' : 'bg-danger'"></span>
                {{ product.available ? 'Disponible' : 'No disponible' }}
              </span>
              <div class="flex gap-1">
                <button @click="$router.push(`/manager/products/${product.id}?cif=${activeCif}`)" title="Ingredientes"
                  class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-info-soft hover:text-info hover:border-[rgba(37,99,235,0.15)]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg>
                </button>
                <button @click="openModal(product)" title="Editar"
                  class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-warning-soft hover:text-warning hover:border-[rgba(196,138,26,0.15)]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                </button>
                <button @click="openDeleteModal(product)" title="Eliminar"
                  class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-danger-soft hover:text-danger hover:border-[rgba(185,60,60,0.15)]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                </button>
              </div>
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
        <p class="text-sm text-text-muted mb-6">
          {{ productsStore.products.length ? 'Ningún producto coincide con esta categoría.' : 'Añade tu primer producto con el botón de arriba.' }}
        </p>
      </div>
    </template>

    <!-- Modal crear/editar -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 bg-ink/50 backdrop-blur-[4px] flex items-center justify-center z-50 p-4" @click.self="closeModal">
          <div class="bg-white rounded-[28px] shadow-[0_40px_100px_rgba(26,92,46,0.12)] w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div class="px-7 pt-7 pb-2 flex items-start justify-between">
              <div>
                <h3 class="font-display text-lg font-bold text-ink tracking-tight">{{ editingProduct ? 'Editar producto' : 'Nuevo producto' }}</h3>
                <p class="text-[13px] text-text-muted mt-1">{{ editingProduct ? 'Actualiza los datos del producto.' : 'Añade un nuevo producto.' }}</p>
              </div>
              <button @click="closeModal" class="bg-transparent border-none text-text-ghost cursor-pointer p-2 -mr-2 rounded-[10px] flex hover:bg-green-soft hover:text-text-sec transition-all">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <div class="px-7 py-5 space-y-5">
              <FormField :error="formErrors.errors.name">
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Nombre</label>
                <input v-model="form.name" placeholder="Ej: Hamburguesa clásica" class="input-mm" />
              </FormField>

              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Descripción</label>
                <textarea v-model="form.description" placeholder="Descripción del producto..." rows="3" class="input-mm !h-auto py-3 resize-none"></textarea>
              </div>

              <FormField :error="formErrors.errors.price">
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Precio</label>
                <input v-model="form.price" type="number" step="0.01" placeholder="0.00" class="input-mm font-display" />
              </FormField>

              <FormField :error="formErrors.errors.category_id">
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Categoría</label>
                <select v-model="form.category_id" class="input-mm cursor-pointer">
                  <option disabled :value="null">Selecciona una categoría</option>
                  <option v-for="cat in productsStore.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </FormField>

              <div>
                <label class="block text-[13px] font-semibold text-text-main mb-1.5">Imagen <span class="text-text-muted font-normal">(opcional)</span></label>
                <input type="file" accept="image/*" @change="onImageChange"
                  class="w-full text-sm text-text-sec file:mr-3 file:py-2.5 file:px-4 file:rounded-full file:border-0 file:bg-green-soft file:text-green-forest file:font-semibold file:text-[12px] file:cursor-pointer hover:file:bg-[rgba(26,92,46,0.12)] file:transition-colors" />
                <img v-if="imagePreview" :src="imagePreview" class="w-full h-32 object-cover rounded-2xl border border-border-green-light mt-3" />
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
                  {{ editingProduct ? 'Guardar cambios' : 'Añadir' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <ConfirmModal :visible="showDeleteModal" title="¿Eliminar producto?"
      :message="`Se eliminará &quot;${productToDelete?.name}&quot;. No se puede deshacer.`"
      confirm-text="Eliminar" :submitting="deleteSubmitting" @confirm="handleDelete" @cancel="closeDeleteModal" />
    <ConfirmModal :visible="showDeleteCategoryModal" title="¿Eliminar categoría?"
      message="Los productos asociados perderán su categoría." confirm-text="Eliminar"
      @confirm="handleDeleteCategory" @cancel="closeDeleteCategoryModal" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useProductsStore } from '../stores/products.store'
import { useToast } from '@/composables/useToast'
import { useFormErrors } from '@/composables/useFormErrors'
import type { Product } from '../interfaces/product.interface'
import { makeMenuApi } from '@/api/makeMenu'
import FormField from '@/components/FormField.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const productsStore = useProductsStore()
const toast = useToast()
const formErrors = useFormErrors()

const myEstablishments = ref<any[]>([])
const activeCif = ref('')
const isLoadingEstablishments = ref(true)

const fetchMyEstablishments = async () => {
  isLoadingEstablishments.value = true
  try {
    const { data } = await makeMenuApi.get('/establishments/')
    myEstablishments.value = data
    if (data.length > 0) {
      activeCif.value = data[0].cif
      await productsStore.fetchProducts(activeCif.value)
      await productsStore.fetchCategories(activeCif.value)
    }
  } catch { toast.error('Error cargando establecimientos.') }
  finally { isLoadingEstablishments.value = false }
}

const onEstablishmentChange = async () => {
  await productsStore.fetchProducts(activeCif.value)
  await productsStore.fetchCategories(activeCif.value)
  selectedCategoryId.value = null
}

const selectedCategoryId = ref<number | null>(null)

const toggleCategoryFilter = (id: number) => {
  if (selectedCategoryId.value === id) {
    selectedCategoryId.value = null
  } else {
    selectedCategoryId.value = id
  }
}

const filteredProducts = computed(() => {
  if (!selectedCategoryId.value) return productsStore.products
  return productsStore.products.filter(p => p.category.id === selectedCategoryId.value)
})

onMounted(() => { fetchMyEstablishments() })

const newCategory = ref('')
const handleAddCategory = async () => {
  if (!newCategory.value.trim()) { toast.warning('Escribe un nombre para la categoría.'); return }
  try { await productsStore.addCategory(activeCif.value, newCategory.value.trim()); toast.success('Categoría creada.'); newCategory.value = '' }
  catch { toast.error('Error al crear la categoría.') }
}

const showDeleteCategoryModal = ref(false)
const categoryToDelete = ref<number | null>(null)
const openDeleteCategoryModal = (id: number) => { categoryToDelete.value = id; showDeleteCategoryModal.value = true }
const closeDeleteCategoryModal = () => { showDeleteCategoryModal.value = false; categoryToDelete.value = null }
const handleDeleteCategory = async () => {
  if (!categoryToDelete.value) return
  try { await productsStore.deleteCategory(activeCif.value, categoryToDelete.value); toast.success('Categoría eliminada.'); closeDeleteCategoryModal() }
  catch { toast.error('No se pudo eliminar. Puede tener productos asociados.') }
}

const showModal = ref(false)
const editingProduct = ref<Product | null>(null)
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)
const formSubmitting = ref(false)

const form = ref({ name: '', description: '', price: 0, available: true, category_id: null as number | null })

const onImageChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  imageFile.value = file; imagePreview.value = URL.createObjectURL(file)
}

const openModal = (product?: Product) => {
  editingProduct.value = product || null; imageFile.value = null; imagePreview.value = product?.product_image || null; formErrors.clear()
  form.value = product
    ? { name: product.name, description: product.description, price: product.price, available: product.available, category_id: product.category.id }
    : { name: '', description: '', price: 0, available: true, category_id: null }
  showModal.value = true
}
const closeModal = () => { showModal.value = false; editingProduct.value = null; imageFile.value = null; imagePreview.value = null; formErrors.clear() }

const handleSave = async () => {
  const valid = formErrors.validate({
    name: [{ value: form.value.name.trim(), message: 'El nombre es obligatorio.' }],
    price: [{ value: form.value.price, message: 'El precio debe ser mayor a 0.' }],
    category_id: [{ value: form.value.category_id, message: 'Selecciona una categoría.' }],
  })
  if (!valid) return
  formSubmitting.value = true
  const payload = { name: form.value.name, description: form.value.description, price: form.value.price, available: form.value.available, category: form.value.category_id }
  try {
    let productId: number
    if (editingProduct.value) { await productsStore.editProduct(activeCif.value, editingProduct.value.id, payload); productId = editingProduct.value.id; toast.success('Producto actualizado.') }
    else { productId = await productsStore.addProduct(activeCif.value, payload); toast.success('Producto creado.') }
    if (imageFile.value) { await productsStore.uploadProductImage(activeCif.value, productId, imageFile.value) }
    closeModal()
  } catch (err: any) {
    if (err.response?.data?.errors) { formErrors.setFromBackend(err.response.data.errors) }
    else { toast.error(err.response?.data?.error || 'Error al guardar el producto.') }
  } finally { formSubmitting.value = false }
}

const showDeleteModal = ref(false)
const productToDelete = ref<Product | null>(null)
const deleteSubmitting = ref(false)
const openDeleteModal = (product: Product) => { productToDelete.value = product; showDeleteModal.value = true }
const closeDeleteModal = () => { showDeleteModal.value = false; productToDelete.value = null }
const handleDelete = async () => {
  if (!productToDelete.value) return
  deleteSubmitting.value = true
  try { await productsStore.deleteProduct(activeCif.value, productToDelete.value.id); toast.success('Producto eliminado.'); closeDeleteModal() }
  catch { toast.error('Error al eliminar el producto.') }
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