<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="flex items-center gap-4">
      <button
        @click="$router.back()"
        class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-colors"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>
      <div>
        <h2 class="text-xl font-bold text-gray-700">{{ product?.name ?? 'Cargando...' }}</h2>
        <p class="text-sm text-gray-400">Gestión de ingredientes y componentes</p>
      </div>
    </div>

    <!-- Info del producto -->
    <div v-if="product" class="bg-white border border-gray-200 rounded-2xl p-5 flex gap-5 items-center">
      <img
        v-if="product.product_image"
        :src="product.product_image"
        :alt="product.name"
        class="w-20 h-20 object-cover rounded-xl border border-gray-100"
      />
      <div v-else class="w-20 h-20 bg-gray-100 rounded-xl flex items-center justify-center text-gray-300">
        <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d='M3 2v7c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2V2'/>
          <path d='M7 2v20'/>
          <path d='M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h1'/>
          <path d='M21 22v-7'/>
        </svg>
      </div>
      <div class="flex-1 space-y-1">
        <h3 class="font-semibold text-gray-800">{{ product.name }}</h3>
        <span class="text-xs text-emerald-600 font-medium bg-emerald-50 px-2 py-0.5 rounded-full">
          {{ product.category.name }}
        </span>
        <p class="text-sm text-gray-500">{{ product.description }}</p>
      </div>
      <span class="text-emerald-600 font-bold text-xl">{{ product.price }}€</span>
    </div>

    <!-- Componentes -->
    <div class="bg-white border border-gray-200 rounded-2xl overflow-hidden">
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
        <h3 class="font-semibold text-gray-700">Ingredientes del producto</h3>
        <button
          @click="openModal()"
          class="flex items-center gap-2 px-4 py-2 bg-emerald-400 text-white text-sm font-semibold rounded-xl hover:bg-emerald-500 transition-colors"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Añadir ingrediente
        </button>
      </div>

      <div v-if="isLoading" class="p-12 text-center text-gray-400">
        Cargando componentes...
      </div>

      <div v-else-if="components.length">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wide">Ingrediente</th>
              <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wide">Cantidad</th>
              <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wide">Unidad</th>
              <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wide">Removible</th>
              <th class="px-6 py-3"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="component in components" :key="component.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 font-medium text-gray-800">{{ component.ingredient_name }}</td>
              <td class="px-6 py-4 text-gray-600">{{ component.quantity }}</td>
              <td class="px-6 py-4 text-gray-600">{{ unityLabel(component.unity) }}</td>
              <td class="px-6 py-4">
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full"
                  :class="component.removable ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-500'"
                >
                  {{ component.removable ? 'Sí' : 'No' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button
                  @click="handleDeleteComponent(component.id)"
                  class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                    <path d="M10 11v6M14 11v6"/>
                    <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="p-12 text-center text-gray-400">
        <p class="font-medium">Sin ingredientes asignados</p>
        <p class="text-sm mt-1">Añade los ingredientes que componen este producto</p>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 space-y-4">
          <h3 class="text-lg font-bold text-gray-700">Añadir ingrediente</h3>

          <div class="space-y-3">
            <select
              v-model="form.ingredient"
              class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
            >
              <option disabled :value="null">Selecciona un ingrediente</option>
              <option v-for="ing in availableIngredients" :key="ing.id" :value="ing.id">
                {{ ing.name }}
              </option>
            </select>

            <div class="flex gap-3">
              <input
                v-model="form.quantity"
                type="number"
                step="0.01"
                placeholder="Cantidad"
                class="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              />
              <select
                v-model="form.unity"
                class="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
              >
                <option disabled value="">Unidad</option>
                <option v-for="u in unities" :key="u.value" :value="u.value">{{ u.label }}</option>
              </select>
            </div>

            <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
              <input v-model="form.removable" type="checkbox" class="accent-emerald-500" />
              El cliente puede pedir que se quite
            </label>
          </div>

          <div class="flex gap-3 pt-2">
            <button
              @click="closeModal"
              class="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-600 hover:bg-gray-50"
            >
              Cancelar
            </button>
            <div
              @click="handleAddComponent"
              class="flex-1 px-4 py-2.5 rounded-xl bg-emerald-400 text-white text-sm font-semibold hover:bg-emerald-500 cursor-pointer text-center"
            >
              Añadir
            </div>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { makeMenuApi } from '@/api/makeMenu'
import { useProductsStore } from '../stores/products.store'
import type { Product } from '../interfaces/product.interface'

const route = useRoute()
const productsStore = useProductsStore()

const productId = Number(route.params.productId)
const activeCif = ref(route.query.cif as string)
const product = ref<Product | null>(null)
const components = ref<any[]>([])
const isLoading = ref(true)

const unities = [
  { value: 'ea', label: 'Unidad' },
  { value: 'gr', label: 'Gramos' },
  { value: 'kg', label: 'Kilogramos' },
  { value: 'l', label: 'Litros' },
  { value: 'ml', label: 'Mililitros' },
]

const unityLabel = (value: string) => unities.find(u => u.value === value)?.label ?? value

const availableIngredients = computed(() =>
  productsStore.ingredients.filter(
    ing => !components.value.some(c => c.ingredient === ing.id)
  )
)

const fetchData = async () => {
  isLoading.value = true
  try {
    if (!activeCif.value) return

    const { data: prod } = await makeMenuApi.get(
      `/establishments/${activeCif.value}/products/${productId}/`
    )
    product.value = prod

    const { data: comps } = await makeMenuApi.get(
      `/establishments/${activeCif.value}/products/${productId}/components/`
    )
    components.value = comps

    await productsStore.fetchIngredients(activeCif.value)
  } catch (error) {
    console.error('Error cargando datos:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchData)

const showModal = ref(false)

const form = ref({
  ingredient: null as number | null,
  quantity: 1,
  unity: '',
  removable: false,
})

const openModal = () => {
  form.value = { ingredient: null, quantity: 1, unity: '', removable: false }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const handleAddComponent = async () => {
  if (!form.value.ingredient || !form.value.unity) return
  console.log('ingredient:', form.value.ingredient)
  console.log('unity:', form.value.unity)
  await makeMenuApi.post(
    `/establishments/${activeCif.value}/products/${productId}/components/add/`,
    {
      ingredient: form.value.ingredient,
      quantity: form.value.quantity,
      unity: form.value.unity,
      removable: form.value.removable,
    }
  )

  const { data } = await makeMenuApi.get(
    `/establishments/${activeCif.value}/products/${productId}/components/`
  )
  components.value = data
  closeModal()
}

const handleDeleteComponent = async (componentId: number) => {
  if (!confirm('¿Eliminar este ingrediente del producto?')) return
  await makeMenuApi.post(
    `/establishments/${activeCif.value}/products/${productId}/components/${componentId}/delete/`
  )
  components.value = components.value.filter(c => c.id !== componentId)
}
</script>