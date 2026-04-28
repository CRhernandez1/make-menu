<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-8 gap-4">
      <div>
        <h1 class="font-display text-2xl font-bold text-green-forest tracking-tight">Establecimientos</h1>
        <p class="text-sm text-text-muted mt-1">{{ store.establishments.length }} locales registrados en tu cuenta.</p>
      </div>
      <button
        @click="openCreateModal"
        class="btn-mm btn-primary self-start text-[13px] px-5 py-2.5"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Nuevo establecimiento
      </button>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <!-- Tabs -->
      <div class="inline-flex bg-white border border-border-green rounded-[14px] p-1 gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="filter = tab.value"
          class="flex items-center gap-2 py-2 px-4 rounded-[10px] border-none text-[13px] font-semibold cursor-pointer transition-all duration-200"
          :class="filter === tab.value
            ? 'bg-green-forest text-cream shadow-[0_2px_10px_rgba(26,92,46,0.15)]'
            : 'bg-transparent text-text-muted hover:text-green-forest hover:bg-green-soft'"
        >
          {{ tab.label }}
          <span
            class="text-[11px] font-bold min-w-[20px] text-center py-0.5 px-1.5 rounded-md"
            :class="filter === tab.value ? 'bg-white/15 text-cream/80' : 'bg-green-soft text-text-muted'"
          >{{ tab.count }}</span>
        </button>
      </div>

      <!-- Search -->
      <div class="flex items-center gap-2.5 bg-white border border-border-green rounded-[var(--radius-input)] px-4 h-11 focus-within:border-green-medium focus-within:shadow-[0_0_0_4px_rgba(26,92,46,0.06)] transition-all">
        <svg class="text-text-ghost shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nombre, ciudad, CIF..."
          class="border-none outline-none bg-transparent text-sm text-ink w-52 placeholder:text-text-ghost font-sans"
        />
      </div>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="alert-mm bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] text-danger mb-5">
      <svg class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <span class="flex-1">{{ store.error }}</span>
      <button @click="store.clearError" class="text-danger/40 hover:text-danger/80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div
        v-if="toast"
        class="alert-mm mb-5 border-[1.5px]"
        :class="toast.type === 'success'
          ? 'bg-green-soft border-border-green text-green-forest'
          : 'bg-danger-soft border-[rgba(185,60,60,0.15)] text-danger'"
      >
        <svg v-if="toast.type === 'success'" class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <svg v-else class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        <span class="flex-1">{{ toast.message }}</span>
        <button @click="toast = null" class="text-current opacity-40 hover:opacity-80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
      </div>
    </Transition>

    <!-- Loading skeletons -->
    <div v-if="store.loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div v-for="n in 6" :key="n" class="bg-white rounded-[var(--radius-card)] border border-border-green-light p-7">
        <div class="flex items-center gap-4 mb-5">
          <div class="w-12 h-12 rounded-2xl skeleton-mm"></div>
          <div class="flex-1 space-y-2.5">
            <div class="h-4 w-2/3 rounded-xl skeleton-mm"></div>
            <div class="h-3 w-1/2 rounded-lg skeleton-mm"></div>
          </div>
        </div>
        <div class="space-y-2.5">
          <div class="h-3 w-full rounded-lg skeleton-mm"></div>
          <div class="h-3 w-3/4 rounded-lg skeleton-mm"></div>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div v-else-if="filteredEstablishments.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div
        v-for="est in filteredEstablishments"
        :key="est.id"
        class="card-mm p-7 group"
      >
        <!-- Top row -->
        <div class="flex items-start justify-between mb-5">
          <div class="w-12 h-12 rounded-2xl bg-green-forest text-cream text-lg font-bold flex items-center justify-center font-display">
            {{ est.name.charAt(0) }}
          </div>
          <button
            @click="handleToggle(est)"
            :title="est.opened ? 'Cerrar establecimiento' : 'Abrir establecimiento'"
            class="cursor-pointer bg-transparent border-none p-0"
          >
            <span
              class="badge-mm transition-all hover:ring-2"
              :class="est.opened
                ? 'bg-green-soft text-green-forest hover:ring-[rgba(26,92,46,0.15)]'
                : 'bg-danger-soft text-danger hover:ring-[rgba(185,60,60,0.15)]'"
            >
              <span
                class="w-1.5 h-1.5 rounded-full"
                :class="est.opened ? 'bg-green-bright' : 'bg-danger'"
              ></span>
              {{ est.opened ? 'Abierto' : 'Cerrado' }}
            </span>
          </button>
        </div>

        <!-- Name -->
        <h3 class="text-[16px] font-bold text-ink mb-0.5 truncate">{{ est.name }}</h3>
        <p class="text-[13px] text-text-muted mb-4 truncate">{{ est.legal_name }}</p>

        <!-- Details -->
        <div class="space-y-2.5 mb-5">
          <div class="flex items-start gap-2.5 text-[13px] text-text-sec leading-snug">
            <svg class="text-text-ghost shrink-0 mt-0.5" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>{{ est.address }}, {{ est.city }}</span>
          </div>
          <div class="flex items-center gap-2.5 text-[13px] text-text-sec">
            <svg class="text-text-ghost shrink-0" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.6.7 2.33a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.52.57 2.33.7A2 2 0 0 1 22 16.92z"/></svg>
            <span>{{ est.phone || '—' }}</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between pt-5 border-t border-border-green-light">
          <span class="text-[11px] font-semibold text-text-ghost tracking-wider font-display">{{ est.cif }}</span>
          <div class="flex items-center gap-1">
            <router-link
              :to="{ name: 'staff', params: { cif: est.cif } }"
              title="Staff"
              class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted no-underline cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-green-soft hover:text-green-forest hover:border-border-green"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </router-link>
            <router-link
              :to="{ name: 'tables', params: { cif: est.cif } }"
              title="Mesas"
              class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted no-underline cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-green-soft hover:text-green-forest hover:border-border-green"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            </router-link>
            <button
              title="Editar"
              @click="openEditModal(est)"
              class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-warning-soft hover:text-warning hover:border-[rgba(196,138,26,0.15)]"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button
              title="Eliminar"
              @click="openDeleteModal(est)"
              class="w-8 h-8 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-danger-soft hover:text-danger hover:border-[rgba(185,60,60,0.15)]"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
      <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-ink mb-2">
        {{ filter === 'all' && !searchQuery ? 'Aún sin locales' : 'Sin resultados' }}
      </h3>
      <p v-if="filter === 'all' && !searchQuery" class="text-sm text-text-muted mb-6 max-w-xs mx-auto">Crea tu primer establecimiento para empezar a gestionar tu negocio.</p>
      <p v-else class="text-sm text-text-muted mb-6">Prueba cambiando los filtros o el término de búsqueda.</p>
      <button
        v-if="filter === 'all' && !searchQuery"
        @click="openCreateModal"
        class="btn-mm btn-primary text-[13px]"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Crear establecimiento
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
      title="¿Eliminar establecimiento?"
      :message="`Esta acción eliminará &quot;${estToDelete?.name}&quot; y todas sus mesas. No se puede deshacer.`"
      confirm-text="Eliminar"
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
  { label: 'Todos', value: 'all' as const, count: store.establishments.length },
  { label: 'Abiertos', value: 'open' as const, count: openCount.value },
  { label: 'Cerrados', value: 'closed' as const, count: closedCount.value }
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
    showToast('success', result.message ?? 'Hecho.')
  } else {
    formError.value = result.error ?? 'Ha ocurrido un error.'
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
  if (result.ok) { closeDeleteModal(); showToast('success', result.message ?? 'Eliminado.') }
  else { deleteError.value = result.error ?? 'Ha ocurrido un error.' }
}

// --- Toggle ---
const handleToggle = async (est: Establishment) => {
  const result = await store.toggleEstablishment(est.cif)
  showToast(result.ok ? 'success' : 'error', (result.ok ? result.message : result.error) ?? 'Hecho.')
}

// --- Init ---
onMounted(() => { store.fetchEstablishments() })
</script>

<style scoped>
.toast-enter-active { transition: all 0.25s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-8px); }
</style>