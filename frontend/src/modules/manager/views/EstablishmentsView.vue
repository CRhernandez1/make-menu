<template>
  <div class="px-8 py-8 lg:px-12 lg:py-10">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-8 gap-4">
      <div>
        <h1 class="text-2xl font-extrabold text-[#1a1a2e] tracking-tight">Establishments</h1>
        <p class="text-[15px] text-gray-400 mt-1">{{ store.establishments.length }} locations registered in your account.</p>
      </div>
      <button
        @click="openCreateModal"
        class="self-start inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold bg-emerald-500 text-white border-none cursor-pointer transition-all duration-200 hover:bg-emerald-600 hover:shadow-[0_4px_20px_rgba(16,185,129,0.3)] active:scale-[0.98] shrink-0"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add Establishment
      </button>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
      <!-- Tabs -->
      <div class="inline-flex bg-white border border-gray-100 rounded-xl p-1 gap-1 shadow-sm">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="filter = tab.value"
          class="flex items-center gap-2 py-2 px-4 rounded-lg border-none text-sm font-medium cursor-pointer transition-all duration-150"
          :class="filter === tab.value
            ? 'bg-[#1a1a2e] text-white shadow-sm'
            : 'bg-transparent text-gray-400 hover:text-gray-600'"
        >
          {{ tab.label }}
          <span
            class="text-[11px] font-bold min-w-[20px] text-center py-0.5 px-1.5 rounded-md"
            :class="filter === tab.value ? 'bg-white/15 text-white/80' : 'bg-gray-100 text-gray-400'"
          >{{ tab.count }}</span>
        </button>
      </div>

      <!-- Search -->
      <div class="flex items-center gap-2 bg-white border border-gray-100 rounded-xl px-4 h-10 shadow-sm focus-within:border-emerald-300 focus-within:ring-2 focus-within:ring-emerald-500/10 transition-all">
        <svg class="text-gray-300 shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="searchQuery" type="text" placeholder="Search by name, city, CIF..." class="border-none outline-none bg-transparent text-sm text-[#1a1a2e] w-52 placeholder:text-gray-300" />
      </div>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 bg-red-50 text-red-600 border border-red-100">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError" class="text-red-300 hover:text-red-500 cursor-pointer text-xl leading-none bg-transparent border-none">&times;</button>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div
        v-if="toast"
        class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 border"
        :class="toast.type === 'success' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-red-50 text-red-600 border-red-100'"
      >
        <svg v-if="toast.type === 'success'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        <span class="flex-1">{{ toast.message }}</span>
        <button @click="toast = null" class="text-current opacity-40 hover:opacity-80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
      </div>
    </Transition>

    <!-- Loading -->
    <div v-if="store.loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div v-for="n in 6" :key="n" class="bg-white rounded-2xl border border-gray-100 p-6 animate-pulse">
        <div class="flex items-center gap-4 mb-5">
          <div class="w-12 h-12 rounded-xl bg-gray-100"></div>
          <div class="flex-1 space-y-2">
            <div class="h-4 w-2/3 rounded bg-gray-100"></div>
            <div class="h-3 w-1/2 rounded bg-gray-100"></div>
          </div>
        </div>
        <div class="space-y-2">
          <div class="h-3 w-full rounded bg-gray-100"></div>
          <div class="h-3 w-3/4 rounded bg-gray-100"></div>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div v-else-if="filteredEstablishments.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div
        v-for="est in filteredEstablishments"
        :key="est.id"
        class="group bg-white rounded-2xl border border-gray-100 p-6 transition-all duration-200 hover:border-emerald-200 hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)]"
      >
        <!-- Top row -->
        <div class="flex items-start justify-between mb-5">
          <div class="w-12 h-12 rounded-xl bg-[#1a1a2e] text-white text-lg font-bold flex items-center justify-center">
            {{ est.name.charAt(0) }}
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="handleToggle(est)"
              :title="est.opened ? 'Close establishment' : 'Open establishment'"
              class="cursor-pointer bg-transparent border-none p-0"
            >
              <span
                class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full transition-all hover:ring-2"
                :class="est.opened
                  ? 'bg-emerald-50 text-emerald-600 hover:ring-emerald-200'
                  : 'bg-gray-50 text-gray-400 hover:ring-gray-200'"
              >
                <span
                  class="w-1.5 h-1.5 rounded-full"
                  :class="est.opened ? 'bg-emerald-500' : 'bg-gray-300'"
                ></span>
                {{ est.opened ? 'Open' : 'Closed' }}
              </span>
            </button>
          </div>
        </div>

        <!-- Name -->
        <h3 class="text-[16px] font-bold text-[#1a1a2e] mb-0.5 truncate">{{ est.name }}</h3>
        <p class="text-[13px] text-gray-400 mb-4 truncate">{{ est.legal_name }}</p>

        <!-- Details -->
        <div class="space-y-2.5 mb-5">
          <div class="flex items-start gap-2.5 text-[13px] text-gray-500 leading-snug">
            <svg class="text-gray-300 shrink-0 mt-0.5" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>{{ est.address }}, {{ est.city }}</span>
          </div>
          <div class="flex items-center gap-2.5 text-[13px] text-gray-500">
            <svg class="text-gray-300 shrink-0" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.6.7 2.33a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.52.57 2.33.7A2 2 0 0 1 22 16.92z"/></svg>
            <span>{{ est.phone || '—' }}</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <span class="text-[11px] font-semibold text-gray-300 tracking-wider font-mono">{{ est.cif }}</span>
          <div class="flex items-center gap-1">
            <router-link
  :to="{ name: 'staff', params: { cif: est.cif } }"
  title="Manage staff"
  class="w-8 h-8 rounded-lg bg-transparent border border-transparent text-gray-400 no-underline cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-purple-50 hover:text-purple-500 hover:border-purple-100"
>
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
</router-link>
            <router-link
              :to="{ name: 'tables', params: { cif: est.cif } }"
              title="Manage tables"
              class="w-8 h-8 rounded-lg bg-transparent border border-transparent text-gray-400 no-underline cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-emerald-50 hover:text-emerald-500 hover:border-emerald-100"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            </router-link>
            <button
              title="Edit"
              @click="openEditModal(est)"
              class="w-8 h-8 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-amber-50 hover:text-amber-500 hover:border-amber-100"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button
              title="Delete"
              @click="openDeleteModal(est)"
              class="w-8 h-8 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-red-50 hover:text-red-500 hover:border-red-100"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border border-dashed border-gray-200 rounded-2xl">
      <div class="w-16 h-16 rounded-2xl bg-gray-50 flex items-center justify-center mx-auto mb-5">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#c4c9d4" stroke-width="1.5" stroke-linecap="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <h3 class="text-base font-bold text-[#1a1a2e] mb-1">
        {{ filter === 'all' && !searchQuery ? 'No establishments yet' : 'No results found' }}
      </h3>
      <p v-if="filter === 'all' && !searchQuery" class="text-sm text-gray-400 mb-5">Create your first establishment to get started.</p>
      <p v-else class="text-sm text-gray-400 mb-5">Try changing your filters or search query.</p>
      <button
        v-if="filter === 'all' && !searchQuery"
        @click="openCreateModal"
        class="inline-flex items-center gap-2 py-2.5 px-5 rounded-xl text-sm font-semibold bg-emerald-500 text-white border-none cursor-pointer hover:bg-emerald-600 transition-colors"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add Establishment
      </button>
    </div>

    <!-- Modals -->
    <EstablishmentModal
      :visible="showModal"
      :establishment="selectedEstablishment"
      :error="formError"
      :submitting="formSubmitting"
      @close="closeModal"
      @submit="handleSubmit"
      @clear-error="formError = null"
    />
    <ConfirmModal
      :visible="showDeleteModal"
      title="Delete establishment"
      :message="`This will permanently remove &quot;${estToDelete?.name}&quot; and all its tables. This action cannot be undone.`"
      confirm-text="Delete"
      :error="deleteError"
      :submitting="deleteSubmitting"
      @confirm="handleDelete"
      @cancel="closeDeleteModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useEstablishmentStore } from '../stores/establishment.store'
import type { Establishment } from '../interfaces'
import EstablishmentModal from '../components/EstablishmentModal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const store = useEstablishmentStore()

// --- Filter & Search ---
const filter = ref<'all' | 'open' | 'closed'>('all')
const searchQuery = ref('')

const openCount = computed(() => store.establishments.filter(e => e.opened).length)
const closedCount = computed(() => store.establishments.filter(e => !e.opened).length)

const tabs = computed(() => [
  { label: 'All', value: 'all' as const, count: store.establishments.length },
  { label: 'Open', value: 'open' as const, count: openCount.value },
  { label: 'Closed', value: 'closed' as const, count: closedCount.value }
])

const filteredEstablishments = computed(() => {
  let result = store.establishments
  if (filter.value === 'open') result = result.filter(e => e.opened)
  if (filter.value === 'closed') result = result.filter(e => !e.opened)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(e =>
      e.name.toLowerCase().includes(q) ||
      e.city.toLowerCase().includes(q) ||
      e.cif.toLowerCase().includes(q) ||
      e.legal_name.toLowerCase().includes(q)
    )
  }
  return result
})

// --- Toast ---
interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 4000)
}

// --- Create / Edit Modal ---
const showModal = ref(false)
const selectedEstablishment = ref<Establishment | null>(null)
const formError = ref<string | null>(null)
const formSubmitting = ref(false)

const openCreateModal = () => { selectedEstablishment.value = null; formError.value = null; showModal.value = true }
const openEditModal = (est: Establishment) => { selectedEstablishment.value = est; formError.value = null; showModal.value = true }
const closeModal = () => { showModal.value = false; selectedEstablishment.value = null; formError.value = null }

const handleSubmit = async (form: { cif: string; name: string; legal_name: string; description: string; zip_code: string; city: string; address: string; phone: string }) => {
  formSubmitting.value = true
  formError.value = null

  const result = selectedEstablishment.value
    ? await store.updateEstablishment(selectedEstablishment.value.cif, {
        name: form.name,
        legal_name: form.legal_name,
        description: form.description,
        zip_code: form.zip_code,
        city: form.city,
        address: form.address,
        phone: form.phone
      })
    : await store.createEstablishment(form)

  formSubmitting.value = false

  if (result.ok) {
    closeModal()
    showToast('success', result.message ?? 'Done.')
  } else {
    formError.value = result.error ?? 'An error occurred.'
  }
}

// --- Delete Modal ---
const showDeleteModal = ref(false)
const estToDelete = ref<Establishment | null>(null)
const deleteError = ref<string | null>(null)
const deleteSubmitting = ref(false)

const openDeleteModal = (est: Establishment) => { estToDelete.value = est; deleteError.value = null; showDeleteModal.value = true }
const closeDeleteModal = () => { showDeleteModal.value = false; estToDelete.value = null; deleteError.value = null }
const handleDelete = async () => {
  if (!estToDelete.value) return
  deleteSubmitting.value = true
  deleteError.value = null
  const result = await store.deleteEstablishment(estToDelete.value.cif)
  deleteSubmitting.value = false
  if (result.ok) { closeDeleteModal(); showToast('success', result.message ?? 'Deleted.') }
  else { deleteError.value = result.error ?? 'An error occurred.' }
}

// --- Toggle ---
const handleToggle = async (est: Establishment) => {
  const result = await store.toggleEstablishment(est.cif)
  showToast(result.ok ? 'success' : 'error', (result.ok ? result.message : result.error) ?? 'Done.')
}

// --- Init ---
onMounted(() => { store.fetchEstablishments() })
</script>

<style scoped>
.toast-enter-active { transition: all 0.25s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-8px); }
</style>