<template>
  <div>
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm mb-6">
      <router-link :to="{ name: 'manager' }" class="text-text-muted no-underline font-medium hover:text-green-forest transition-colors">Establecimientos</router-link>
      <svg class="text-text-ghost" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
      <span class="text-ink font-semibold">Mesas</span>
    </nav>

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-8 gap-4">
      <div>
        <h1 class="font-display text-2xl font-bold text-green-forest tracking-tight">Gestión de mesas</h1>
        <p class="text-sm text-text-muted mt-1">{{ tables.length }} mesas configuradas en este establecimiento.</p>
      </div>
      <button @click="openCreateModal" class="btn-mm btn-primary self-start text-[13px] px-5 py-2.5">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Nueva mesa
      </button>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div class="inline-flex bg-white border border-border-green rounded-[14px] p-1 gap-1">
        <button v-for="tab in tabs" :key="tab.value" @click="filter = tab.value"
          class="flex items-center gap-2 py-2 px-4 rounded-[10px] border-none text-[13px] font-semibold cursor-pointer transition-all duration-200"
          :class="filter === tab.value
            ? 'bg-green-forest text-cream shadow-[0_2px_10px_rgba(26,92,46,0.15)]'
            : 'bg-transparent text-text-muted hover:text-green-forest hover:bg-green-soft'">
          {{ tab.label }}
          <span class="text-[11px] font-bold min-w-[20px] text-center py-0.5 px-1.5 rounded-md"
            :class="filter === tab.value ? 'bg-white/15 text-cream/80' : 'bg-green-soft text-text-muted'">{{ tab.count }}</span>
        </button>
      </div>
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2.5 bg-white border border-border-green rounded-[var(--radius-input)] px-4 h-11 focus-within:border-green-medium focus-within:shadow-[0_0_0_4px_rgba(26,92,46,0.06)] transition-all">
          <svg class="text-text-ghost shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input v-model="searchQuery" type="text" placeholder="Buscar mesas..." class="border-none outline-none bg-transparent text-sm text-ink w-40 placeholder:text-text-ghost font-sans" />
        </div>
        <select v-model="sortBy" class="h-11 px-4 rounded-[var(--radius-input)] border border-border-green bg-white text-sm font-medium text-text-sec cursor-pointer focus:border-green-medium focus:shadow-[0_0_0_4px_rgba(26,92,46,0.06)] outline-none transition-all font-sans">
          <option value="number">Por número</option>
          <option value="guests">Por capacidad</option>
          <option value="status">Por estado</option>
        </select>
      </div>
    </div>

    <!-- Error -->
    <div v-if="tableStore.error" class="alert-mm bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] text-danger mb-5">
      <svg class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <span class="flex-1">{{ tableStore.error }}</span>
      <button @click="tableStore.clearError" class="text-danger/40 hover:text-danger/80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast" class="alert-mm mb-5 border-[1.5px]"
        :class="toast.type === 'success' ? 'bg-green-soft border-border-green text-green-forest' : 'bg-danger-soft border-[rgba(185,60,60,0.15)] text-danger'">
        <svg v-if="toast.type === 'success'" class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <svg v-else class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        <span class="flex-1">{{ toast.message }}</span>
        <button @click="toast = null" class="text-current opacity-40 hover:opacity-80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
      </div>
    </Transition>

    <!-- Loading -->
    <div v-if="tableStore.loading" class="bg-white rounded-[var(--radius-card)] border border-border-green-light p-8 space-y-6">
      <div v-for="n in 5" :key="n" class="flex items-center gap-8">
        <div class="w-10 h-10 rounded-2xl skeleton-mm shrink-0"></div>
        <div class="h-4 w-28 rounded-xl skeleton-mm"></div>
        <div class="h-4 w-20 rounded-xl skeleton-mm"></div>
        <div class="h-6 w-16 rounded-full skeleton-mm"></div>
        <div class="h-4 w-24 rounded-xl skeleton-mm ml-auto"></div>
      </div>
    </div>

    <!-- Table -->
    <div v-else-if="paginatedTables.length > 0" class="bg-white rounded-[var(--radius-card)] border border-border-green-light shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[700px]">
          <thead>
            <tr class="border-b border-border-green-light">
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[35%]">Mesa</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[20%]">Capacidad</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[20%]">Estado</th>
              <th class="text-right py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[25%]">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="table in paginatedTables" :key="table.id" class="border-b border-border-green-light last:border-b-0 hover:bg-green-soft-2 transition-colors">
              <td class="py-4 px-6">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-2xl bg-cream border border-border-green flex items-center justify-center text-text-muted shrink-0">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
                  </div>
                  <div>
                    <span class="block text-sm font-bold text-ink">Mesa {{ String(table.number).padStart(2, '0') }}</span>
                    <span class="block text-xs text-text-muted mt-0.5 font-display">#TB-{{ String(table.id).padStart(3, '0') }}</span>
                  </div>
                </div>
              </td>
              <td class="py-4 px-6">
                <div class="flex items-center gap-2 text-sm text-text-sec">
                  <svg class="text-text-ghost" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                  <span class="font-medium font-display">{{ table.max_guests }}</span> personas
                </div>
              </td>
              <td class="py-4 px-6">
                <span class="badge-mm" :class="table.active ? 'bg-green-soft text-green-forest' : 'bg-cream-dark text-text-muted'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="table.active ? 'bg-green-bright' : 'bg-text-ghost'"></span>
                  {{ table.active ? 'Activa' : 'Inactiva' }}
                </span>
              </td>
              <td class="py-4 px-6">
                <div class="flex gap-1.5 justify-end">
                  <button :title="table.active ? 'Desactivar' : 'Activar'" @click="handleToggle(table.number)"
                    class="w-9 h-9 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-info-soft hover:text-info hover:border-[rgba(37,99,235,0.15)]">
                    <svg v-if="table.active" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>
                    <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg>
                  </button>
                  <button title="Editar" @click="openEditModal(table)"
                    class="w-9 h-9 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-warning-soft hover:text-warning hover:border-[rgba(196,138,26,0.15)]">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  </button>
                  <button title="Eliminar" @click="openDeleteModal(table)"
                    class="w-9 h-9 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-danger-soft hover:text-danger hover:border-[rgba(185,60,60,0.15)]">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex items-center justify-between py-4 px-6 border-t border-border-green-light">
        <span class="text-sm text-text-muted">
          Mostrando <span class="font-semibold text-text-sec">{{ paginationStart }}–{{ paginationEnd }}</span> de <span class="font-semibold text-text-sec">{{ sortedTables.length }}</span>
        </span>
        <div class="flex gap-1.5">
          <button :disabled="currentPage === 1" @click="currentPage--"
            class="w-9 h-9 rounded-[10px] border border-border-green bg-white text-text-muted flex items-center justify-center cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed hover:border-green-medium hover:text-green-forest transition-all">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <button v-for="page in totalPages" :key="page" @click="currentPage = page"
            class="w-9 h-9 rounded-[10px] border text-sm font-bold flex items-center justify-center cursor-pointer transition-all font-display"
            :class="currentPage === page
              ? 'bg-green-forest border-green-forest text-cream'
              : 'border-border-green bg-white text-text-muted hover:border-green-medium hover:text-green-forest'">{{ page }}</button>
          <button :disabled="currentPage === totalPages" @click="currentPage++"
            class="w-9 h-9 rounded-[10px] border border-border-green bg-white text-text-muted flex items-center justify-center cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed hover:border-green-medium hover:text-green-forest transition-all">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
      <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-ink mb-2">
        {{ filter === 'all' && !searchQuery ? 'Aún sin mesas' : 'Sin resultados' }}
      </h3>
      <p v-if="filter === 'all' && !searchQuery" class="text-sm text-text-muted mb-6 max-w-xs mx-auto">Añade la primera mesa para empezar a gestionar tu local.</p>
      <p v-else class="text-sm text-text-muted mb-6">Prueba cambiando los filtros o el término de búsqueda.</p>
      <button v-if="filter === 'all' && !searchQuery" @click="openCreateModal" class="btn-mm btn-primary text-[13px]">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Añadir mesa
      </button>
    </div>

    <!-- Modals -->
    <TableModal :visible="showTableModal" :table="selectedTable" :error="formError" :submitting="formSubmitting" @close="closeTableModal" @submit="handleSubmitTable" @clear-error="formError = null" />
    <ConfirmModal :visible="showDeleteModal" title="¿Eliminar mesa?"
      :message="`Se eliminará permanentemente la Mesa ${String(tableToDelete?.number).padStart(2, '0')}. No se puede deshacer.`"
      confirm-text="Eliminar" :error="deleteError" :submitting="deleteSubmitting" @confirm="handleDelete" @cancel="closeDeleteModal" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTableStore } from '../stores/table.store'
import type { Table } from '../interfaces'
import TableModal from '../components/TableModal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const route = useRoute()
const cif = computed(() => route.params.cif as string)
const tableStore = useTableStore()
const tables = computed(() => tableStore.tables)

const filter = ref<'all' | 'active' | 'inactive'>('all')
const sortBy = ref<'number' | 'guests' | 'status'>('number')
const searchQuery = ref('')
const currentPage = ref(1)
const perPage = 8

const activeTables = computed(() => tables.value.filter(t => t.active).length)
const inactiveTables = computed(() => tables.value.filter(t => !t.active).length)

const tabs = computed(() => [
  { label: 'Todas', value: 'all' as const, count: tables.value.length },
  { label: 'Activas', value: 'active' as const, count: activeTables.value },
  { label: 'Inactivas', value: 'inactive' as const, count: inactiveTables.value }
])

const filteredTables = computed(() => {
  let result = tables.value
  if (filter.value === 'active') result = result.filter(t => t.active)
  if (filter.value === 'inactive') result = result.filter(t => !t.active)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(t => String(t.number).includes(q) || String(t.max_guests).includes(q))
  }
  return result
})

const sortedTables = computed(() => {
  const arr = [...filteredTables.value]
  switch (sortBy.value) {
    case 'number': return arr.sort((a, b) => a.number - b.number)
    case 'guests': return arr.sort((a, b) => b.max_guests - a.max_guests)
    case 'status': return arr.sort((a, b) => Number(b.active) - Number(a.active))
    default: return arr
  }
})

const totalPages = computed(() => Math.ceil(sortedTables.value.length / perPage))
const paginationStart = computed(() => (currentPage.value - 1) * perPage + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * perPage, sortedTables.value.length))
const paginatedTables = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return sortedTables.value.slice(start, start + perPage)
})

watch([filter, sortBy, searchQuery], () => { currentPage.value = 1 })

const showTableModal = ref(false)
const selectedTable = ref<Table | null>(null)
const formError = ref<string | null>(null)
const formSubmitting = ref(false)

interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 4000)
}

const openCreateModal = () => { selectedTable.value = null; formError.value = null; showTableModal.value = true }
const openEditModal = (t: Table) => { selectedTable.value = t; formError.value = null; showTableModal.value = true }
const closeTableModal = () => { showTableModal.value = false; selectedTable.value = null; formError.value = null }

const handleSubmitTable = async (number: number, maxGuests: number) => {
  formSubmitting.value = true; formError.value = null
  const result = selectedTable.value
    ? await tableStore.updateTable(cif.value, selectedTable.value.number, { max_guests: maxGuests })
    : await tableStore.createTable(cif.value, { number, max_guests: maxGuests })
  formSubmitting.value = false
  if (result.ok) { closeTableModal(); showToast('success', result.message ?? 'Hecho.') }
  else { formError.value = result.error ?? 'Ha ocurrido un error.' }
}

const showDeleteModal = ref(false)
const tableToDelete = ref<Table | null>(null)
const deleteError = ref<string | null>(null)
const deleteSubmitting = ref(false)

const openDeleteModal = (t: Table) => { tableToDelete.value = t; deleteError.value = null; showDeleteModal.value = true }
const closeDeleteModal = () => { showDeleteModal.value = false; tableToDelete.value = null; deleteError.value = null }
const handleDelete = async () => {
  if (!tableToDelete.value) return
  deleteSubmitting.value = true; deleteError.value = null
  const result = await tableStore.deleteTable(cif.value, tableToDelete.value.number)
  deleteSubmitting.value = false
  if (result.ok) { closeDeleteModal(); showToast('success', result.message ?? 'Eliminada.') }
  else { deleteError.value = result.error ?? 'Ha ocurrido un error.' }
}

const handleToggle = async (num: number) => {
  const result = await tableStore.toggleTable(cif.value, num)
  showToast(result.ok ? 'success' : 'error', (result.ok ? result.message : result.error) ?? 'Hecho.')
}

onMounted(() => { tableStore.fetchTables(cif.value) })
</script>

<style scoped>
.toast-enter-active { transition: all 0.25s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-8px); }
</style>