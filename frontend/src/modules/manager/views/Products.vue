<template>
  <div class="space-y-6">

    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-700">Productos</h2>
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
          Añadir producto
        </button>
      </div>
    </div>

    <div v-if="!myEstablishments.length && !isLoadingEstablishments" class="text-center py-16 text-gray-400">
      <p class="text-lg font-medium">No gestionas ningún establecimiento</p>
    </div>

    <template v-else-if="activeCif">

      <div class="bg-white border border-gray-200 rounded-2xl p-4">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-semibold text-gray-700">Categorías</h3>
          <div class="flex items-center gap-2">
            <input
              v-model="newCategory"
              placeholder="Nueva categoría..."
              class="px-3 py-1.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              @keyup.enter="handleAddCategory"
            />
            <button
              @click="handleAddCategory"
              class="px-3 py-1.5 bg-emerald-400 text-white text-sm font-semibold rounded-xl hover:bg-emerald-500 transition-colors"
            >
              Añadir
            </button>
          </div>
        </div>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="cat in productsStore.categories"
            :key="cat.id"
            class="flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-full"
          >
            {{ cat.name }}
            <button
              @click="openDeleteCategoryModal(cat.id)"
              class="text-emerald-400 hover:text-red-500 transition-colors font-bold leading-none"
            >×</button>
          </span>
          <span v-if="!productsStore.categories.length" class="text-xs text-gray-400">
            No hay categorías aún
          </span>
        </div>
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
                  @click="$router.push(`/manager/products/${product.id}?cif=${activeCif}`)"
                  class="p-2 text-gray-400 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors"
                  title="Ver ingredientes"
                >
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/>
                    <rect x="9" y="3" width="6" height="4" rx="1"/>
                    <path d="M9 12h6M9 16h4"/>
                  </svg>
                </button>
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
                  @click="openDeleteModal(product)"
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

    </template>

    <!-- Modal crear/editar -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4 max-h-[90vh] overflow-y-auto">
          <h3 class="text-lg font-bold text-gray-700">
            {{ editingProduct ? 'Editar producto' : 'Nuevo producto' }}
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
              placeholder="Descripción"
              rows="3"
              class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300 resize-none"
            />

            <FormField :error="formErrors.errors.price">
              <input
                v-model="form.price"
                type="number"
                step="0.01"
                placeholder="Precio"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              />
            </FormField>

            <FormField :error="formErrors.errors.category_id">
              <select
                v-model="form.category_id"
                class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              >
                <option disabled :value="null">Selecciona una categoría</option>
                <option v-for="cat in productsStore.categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </FormField>

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
              :disabled="formSubmitting"
              class="flex-1 px-4 py-2.5 rounded-xl bg-emerald-400 text-white text-sm font-semibold hover:bg-emerald-500 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {{ editingProduct ? 'Guardar cambios' : 'Añadir' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modal eliminar producto -->
    <ConfirmModal
      :visible="showDeleteModal"
      title="Eliminar producto"
      :message="`¿Eliminar &quot;${productToDelete?.name}&quot;? Esta acción no se puede deshacer.`"
      confirm-text="Eliminar"
      :submitting="deleteSubmitting"
      @confirm="handleDelete"
      @cancel="closeDeleteModal"
    />

    <!-- Modal eliminar categoría -->
    <ConfirmModal
      :visible="showDeleteCategoryModal"
      title="Eliminar categoría"
      message="¿Eliminar esta categoría? Los productos asociados perderán su categoría."
      confirm-text="Eliminar"
      @confirm="handleDeleteCategory"
      @cancel="closeDeleteCategoryModal"
    />

  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
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
  } catch {
    toast.error('Error cargando establecimientos.')
  } finally {
    isLoadingEstablishments.value = false
  }
}

const onEstablishmentChange = async () => {
  await productsStore.fetchProducts(activeCif.value)
  await productsStore.fetchCategories(activeCif.value)
}

onMounted(() => { fetchMyEstablishments() })

// Categorías
const newCategory = ref('')

const handleAddCategory = async () => {
  if (!newCategory.value.trim()) {
    toast.warning('Escribe un nombre para la categoría.')
    return
  }
  try {
    await productsStore.addCategory(activeCif.value, newCategory.value.trim())
    toast.success('Categoría creada.')
    newCategory.value = ''
  } catch {
    toast.error('Error al crear la categoría.')
  }
}

// Modal eliminar categoría
const showDeleteCategoryModal = ref(false)
const categoryToDelete = ref<number | null>(null)

const openDeleteCategoryModal = (id: number) => {
  categoryToDelete.value = id
  showDeleteCategoryModal.value = true
}
const closeDeleteCategoryModal = () => {
  showDeleteCategoryModal.value = false
  categoryToDelete.value = null
}
const handleDeleteCategory = async () => {
  if (!categoryToDelete.value) return
  try {
    await productsStore.deleteCategory(activeCif.value, categoryToDelete.value)
    toast.success('Categoría eliminada.')
    closeDeleteCategoryModal()
  } catch {
    toast.error('No se pudo eliminar. Puede tener productos asociados.')
  }
}

// Modal crear/editar producto
const showModal = ref(false)
const editingProduct = ref<Product | null>(null)
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)
const formSubmitting = ref(false)

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
  formErrors.clear()
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
  formErrors.clear()
}

const handleSave = async () => {
  const valid = formErrors.validate({
    name: [{ value: form.value.name.trim(), message: 'El nombre es obligatorio.' }],
    price: [{ value: form.value.price, message: 'El precio debe ser mayor a 0.' }],
    category_id: [{ value: form.value.category_id, message: 'Selecciona una categoría.' }],
  })
  if (!valid) return

  formSubmitting.value = true

  const payload = {
    name: form.value.name,
    description: form.value.description,
    price: form.value.price,
    available: form.value.available,
    category: form.value.category_id,
  }

  try {
    let productId: number

    if (editingProduct.value) {
      await productsStore.editProduct(activeCif.value, editingProduct.value.id, payload)
      productId = editingProduct.value.id
      toast.success('Producto actualizado.')
    } else {
      productId = await productsStore.addProduct(activeCif.value, payload)
      toast.success('Producto creado.')
    }

    if (imageFile.value) {
      await productsStore.uploadProductImage(activeCif.value, productId, imageFile.value)
    }

    closeModal()
  } catch (err: any) {
    if (err.response?.data?.errors) {
      formErrors.setFromBackend(err.response.data.errors)
    } else {
      toast.error(err.response?.data?.error || 'Error al guardar el producto.')
    }
  } finally {
    formSubmitting.value = false
  }
}

// Modal eliminar producto
const showDeleteModal = ref(false)
const productToDelete = ref<Product | null>(null)
const deleteSubmitting = ref(false)

const openDeleteModal = (product: Product) => {
  productToDelete.value = product
  showDeleteModal.value = true
}
const closeDeleteModal = () => {
  showDeleteModal.value = false
  productToDelete.value = null
}
const handleDelete = async () => {
  if (!productToDelete.value) return
  deleteSubmitting.value = true
  try {
    await productsStore.deleteProduct(activeCif.value, productToDelete.value.id)
    toast.success('Producto eliminado.')
    closeDeleteModal()
  } catch {
    toast.error('Error al eliminar el producto.')
  } finally {
    deleteSubmitting.value = false
  }
}
</script>