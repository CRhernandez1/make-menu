<template>
  <div class="px-8 py-8 lg:px-12 lg:py-10">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm mb-6">
      <router-link to="/"
        class="text-gray-400 no-underline font-medium hover:text-emerald-600 transition-colors">Establishments</router-link>
      <svg class="text-gray-300" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round">
        <polyline points="9 18 15 12 9 6" />
      </svg>
      <span class="text-[#1a1a2e] font-semibold">Tables</span>
    </nav>

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-8 gap-4">
      <div>
        <h1 class="text-2xl font-extrabold text-[#1a1a2e] tracking-tight">Table Management</h1>
        <p class="text-[15px] text-gray-400 mt-1">{{ tables.length }} tables configured for this establishment.</p>
      </div>
      <button @click="openCreateModal"
        class="self-start inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold bg-emerald-500 text-white border-none cursor-pointer transition-all duration-200 hover:bg-emerald-600 hover:shadow-[0_4px_20px_rgba(16,185,129,0.3)] active:scale-[0.98] shrink-0">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
          stroke-linecap="round">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        Add Table
      </button>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
      <!-- Tabs -->
      <div class="inline-flex bg-white border border-gray-100 rounded-xl p-1 gap-1 shadow-sm">
        <button v-for="tab in tabs" :key="tab.value" @click="filter = tab.value"
          class="flex items-center gap-2 py-2 px-4 rounded-lg border-none text-sm font-medium cursor-pointer transition-all duration-150"
          :class="filter === tab.value
            ? 'bg-[#1a1a2e] text-white shadow-sm'
            : 'bg-transparent text-gray-400 hover:text-gray-600'">
          {{ tab.label }}
          <span class="text-[11px] font-bold min-w-[20px] text-center py-0.5 px-1.5 rounded-md"
            :class="filter === tab.value ? 'bg-white/15 text-white/80' : 'bg-gray-100 text-gray-400'">{{ tab.count
            }}</span>
        </button>
      </div>

      <!-- Search + Sort -->
      <div class="flex items-center gap-3">
        <div
          class="flex items-center gap-2 bg-white border border-gray-100 rounded-xl px-4 h-10 shadow-sm focus-within:border-emerald-300 focus-within:ring-2 focus-within:ring-emerald-500/10 transition-all">
          <svg class="text-gray-300 shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input v-model="searchQuery" type="text" placeholder="Search tables..."
            class="border-none outline-none bg-transparent text-sm text-[#1a1a2e] w-40 placeholder:text-gray-300" />
        </div>
        <select v-model="sortBy"
          class="h-10 px-4 rounded-xl border border-gray-100 bg-white text-sm font-medium text-gray-600 cursor-pointer shadow-sm">
          <option value="number">Sort by Number</option>
          <option value="guests">Sort by Guests</option>
          <option value="status">Sort by Status</option>
        </select>
      </div>
    </div>

    <!-- Error -->
    <div v-if="tableStore.error"
      class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 bg-red-50 text-red-600 border border-red-100">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="15" y1="9" x2="9" y2="15" />
        <line x1="9" y1="9" x2="15" y2="15" />
      </svg>
      <span class="flex-1">{{ tableStore.error }}</span>
      <button @click="tableStore.clearError"
        class="text-red-300 hover:text-red-500 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast" class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 border"
        :class="toast.type === 'success' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-red-50 text-red-600 border-red-100'">
        <svg v-if="toast.type === 'success'" width="18" height="18" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
          <polyline points="22 4 12 14.01 9 11.01" />
        </svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
        <span class="flex-1">{{ toast.message }}</span>
        <button @click="toast = null"
          class="text-current opacity-40 hover:opacity-80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
      </div>
    </Transition>

    <!-- Loading -->
    <div v-if="tableStore.loading"
      class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 animate-pulse space-y-6">
      <div v-for="n in 5" :key="n" class="flex items-center gap-8">
        <div class="w-10 h-10 rounded-xl bg-gray-100 shrink-0"></div>
        <div class="h-4 w-28 rounded-lg bg-gray-100"></div>
        <div class="h-4 w-20 rounded-lg bg-gray-100"></div>
        <div class="h-6 w-16 rounded-full bg-gray-100"></div>
        <div class="h-4 w-24 rounded-lg bg-gray-100 ml-auto"></div>
      </div>
    </div>

    <!-- Table card -->
    <div v-else-if="paginatedTables.length > 0"
      class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[700px]">
          <thead>
            <tr class="border-b border-gray-100">
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[35%]">
                Table</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[20%]">
                Capacity</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[20%]">
                Status</th>
              <th
                class="text-right py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[25%]">
                Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="table in paginatedTables" :key="table.id"
              class="border-b border-gray-50 last:border-b-0 hover:bg-[#f8f9fb] transition-colors">
              <!-- Table info -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-4">
                  <div
                    class="w-10 h-10 rounded-xl bg-[#f5f6f8] border border-gray-100 flex items-center justify-center text-gray-400 shrink-0">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
                      stroke-linecap="round">
                      <rect x="3" y="3" width="18" height="18" rx="2" />
                      <line x1="3" y1="9" x2="21" y2="9" />
                      <line x1="9" y1="21" x2="9" y2="9" />
                    </svg>
                  </div>
                  <div>
                    <span class="block text-sm font-semibold text-[#1a1a2e]">Table {{ String(table.number).padStart(2,
                      '0') }}</span>
                    <span class="block text-xs text-gray-400 mt-0.5 tabular-nums font-mono">#TB-{{
                      String(table.id).padStart(3, '0') }}</span>
                  </div>
                </div>
              </td>

              <!-- Guests -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-2 text-sm text-gray-500">
                  <svg class="text-gray-300" width="16" height="16" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                    <circle cx="9" cy="7" r="4" />
                    <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                  </svg>
                  <span class="font-medium">{{ table.max_guests }}</span> guests
                </div>
              </td>

              <!-- Status -->
              <td class="py-4 px-6">
                <span class="inline-flex items-center gap-2 text-xs font-semibold py-1.5 px-3 rounded-full" :class="table.active
                  ? 'bg-emerald-50 text-emerald-600'
                  : 'bg-gray-50 text-gray-400'">
                  <span class="w-2 h-2 rounded-full" :class="table.active
                    ? 'bg-emerald-500 shadow-[0_0_0_2px_rgba(16,185,129,0.2)]'
                    : 'bg-gray-300'"></span>
                  {{ table.active ? 'Active' : 'Inactive' }}
                </span>
              </td>

              <!-- Actions -->
              <td class="py-4 px-6">
                <div class="flex gap-1.5 justify-end">
                  <button :title="table.active ? 'Deactivate' : 'Activate'" @click="handleToggle(table.number)"
                    class="w-9 h-9 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-blue-50 hover:text-blue-500 hover:border-blue-100">
                    <svg v-if="table.active" width="15" height="15" viewBox="0 0 24 24" fill="none"
                      stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                      <rect x="6" y="4" width="4" height="16" />
                      <rect x="14" y="4" width="4" height="16" />
                    </svg>
                    <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
                      <polygon points="5,3 19,12 5,21" />
                    </svg>
                  </button>
                  <button title="Edit" @click="openEditModal(table)"
                    class="w-9 h-9 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-amber-50 hover:text-amber-500 hover:border-amber-100">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                    </svg>
                  </button>
                  <button title="Delete" @click="openDeleteModal(table)"
                    class="w-9 h-9 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-red-50 hover:text-red-500 hover:border-red-100">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6" />
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex items-center justify-between py-4 px-6 border-t border-gray-100">
        <span class="text-sm text-gray-400">
          Showing <span class="font-semibold text-gray-600">{{ paginationStart }}–{{ paginationEnd }}</span> of <span
            class="font-semibold text-gray-600">{{ sortedTables.length }}</span>
        </span>
        <div class="flex gap-1.5">
          <button :disabled="currentPage === 1" @click="currentPage--"
            class="w-9 h-9 rounded-lg border border-gray-200 bg-white text-gray-500 flex items-center justify-center cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed hover:border-emerald-300 hover:text-emerald-600 transition-all">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>
          <button v-for="page in totalPages" :key="page" @click="currentPage = page"
            class="w-9 h-9 rounded-lg border text-sm font-semibold flex items-center justify-center cursor-pointer transition-all"
            :class="currentPage === page
              ? 'bg-[#1a1a2e] border-[#1a1a2e] text-white'
              : 'border-gray-200 bg-white text-gray-500 hover:border-emerald-300 hover:text-emerald-600'">{{ page
              }}</button>
          <button :disabled="currentPage === totalPages" @click="currentPage++"
            class="w-9 h-9 rounded-lg border border-gray-200 bg-white text-gray-500 flex items-center justify-center cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed hover:border-emerald-300 hover:text-emerald-600 transition-all">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border border-dashed border-gray-200 rounded-2xl">
      <div class="w-16 h-16 rounded-2xl bg-gray-50 flex items-center justify-center mx-auto mb-5">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#c4c9d4" stroke-width="1.5"
          stroke-linecap="round">
          <rect x="3" y="3" width="18" height="18" rx="2" />
          <line x1="3" y1="9" x2="21" y2="9" />
          <line x1="9" y1="21" x2="9" y2="9" />
        </svg>
      </div>
      <h3 class="text-base font-bold text-[#1a1a2e] mb-1">No tables found</h3>
      <p v-if="filter === 'all' && !searchQuery" class="text-sm text-gray-400 mb-5">Add your first table to get started.
      </p>
      <p v-else class="text-sm text-gray-400 mb-5">Try changing your filters or search query.</p>
      <button v-if="filter === 'all' && !searchQuery" @click="openCreateModal"
        class="inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold bg-emerald-500 text-white border-none cursor-pointer hover:bg-emerald-600 transition-colors">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        Add Table
      </button>
    </div>

    <!-- Modals -->
    <TableModal :visible="showTableModal" :table="selectedTable" :error="formError" :submitting="formSubmitting"
      @close="closeTableModal" @submit="handleSubmitTable" @clear-error="formError = null" />
    <ConfirmModal :visible="showDeleteModal" title="Delete table"
      :message="`This will permanently remove Table ${String(tableToDelete?.number).padStart(2, '0')}. This action cannot be undone.`"
      confirm-text="Delete" :error="deleteError" :submitting="deleteSubmitting" @confirm="handleDelete"
      @cancel="closeDeleteModal" />
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
  { label: 'All', value: 'all' as const, count: tables.value.length },
  { label: 'Active', value: 'active' as const, count: activeTables.value },
  { label: 'Inactive', value: 'inactive' as const, count: inactiveTables.value }
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
  if (result.ok) { closeTableModal(); showToast('success', result.message ?? 'Done.') }
  else { formError.value = result.error ?? 'An error occurred.' }
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
  if (result.ok) { closeDeleteModal(); showToast('success', result.message ?? 'Deleted.') }
  else { deleteError.value = result.error ?? 'An error occurred.' }
}

const handleToggle = async (num: number) => {
  const result = await tableStore.toggleTable(cif.value, num)
  showToast(result.ok ? 'success' : 'error', (result.ok ? result.message : result.error) ?? 'Done.')
}

onMounted(() => { tableStore.fetchTables(cif.value) })
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.25s ease;
}

.toast-leave-active {
  transition: all 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>