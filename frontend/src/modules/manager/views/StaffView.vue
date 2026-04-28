<template>
  <div>
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm mb-6">
      <router-link :to="{ name: 'manager' }" class="text-text-muted no-underline font-medium hover:text-green-forest transition-colors">Establecimientos</router-link>
      <svg class="text-text-ghost" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
      <span class="text-ink font-semibold">Equipo</span>
    </nav>

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-8 gap-4">
      <div>
        <h1 class="font-display text-2xl font-bold text-green-forest tracking-tight">Gestión de equipo</h1>
        <p class="text-sm text-text-muted mt-1">{{ staff.length }} miembros en este establecimiento.</p>
      </div>
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
      <div class="flex items-center gap-2.5 bg-white border border-border-green rounded-[var(--radius-input)] px-4 h-11 focus-within:border-green-medium focus-within:shadow-[0_0_0_4px_rgba(26,92,46,0.06)] transition-all">
        <svg class="text-text-ghost shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="searchQuery" type="text" placeholder="Buscar por nombre, usuario..." class="border-none outline-none bg-transparent text-sm text-ink w-52 placeholder:text-text-ghost font-sans" />
      </div>
    </div>

    <!-- Error -->
    <div v-if="staffStore.error" class="alert-mm bg-danger-soft border-[1.5px] border-[rgba(185,60,60,0.15)] text-danger mb-5">
      <svg class="w-5 h-5 shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <span class="flex-1">{{ staffStore.error }}</span>
      <button @click="staffStore.clearError" class="text-danger/40 hover:text-danger/80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
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
    <div v-if="staffStore.loading" class="bg-white rounded-[var(--radius-card)] border border-border-green-light p-8 space-y-6">
      <div v-for="n in 4" :key="n" class="flex items-center gap-8">
        <div class="w-10 h-10 rounded-full skeleton-mm shrink-0"></div>
        <div class="h-4 w-32 rounded-xl skeleton-mm"></div>
        <div class="h-4 w-20 rounded-xl skeleton-mm"></div>
        <div class="h-6 w-16 rounded-full skeleton-mm"></div>
        <div class="h-4 w-24 rounded-xl skeleton-mm ml-auto"></div>
      </div>
    </div>

    <!-- Table -->
    <div v-else-if="filteredStaff.length > 0" class="bg-white rounded-[var(--radius-card)] border border-border-green-light shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[700px]">
          <thead>
            <tr class="border-b border-border-green-light">
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[35%]">Miembro</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[20%]">Rol</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[20%]">Fecha</th>
              <th class="text-right py-3.5 px-6 text-[11px] font-bold text-text-muted uppercase tracking-[0.1em] w-[25%]">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredStaff" :key="s.id" class="border-b border-border-green-light last:border-b-0 hover:bg-green-soft-2 transition-colors">
              <td class="py-4 px-6">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full bg-green-forest text-cream text-sm font-bold flex items-center justify-center shrink-0 font-display">
                    {{ s.member.first_name.charAt(0) }}{{ s.member.last_name.charAt(0) }}
                  </div>
                  <div>
                    <span class="block text-sm font-bold text-ink">{{ s.member.first_name }} {{ s.member.last_name }}</span>
                    <span class="block text-xs text-text-muted mt-0.5">@{{ s.member.username }}</span>
                  </div>
                </div>
              </td>
              <td class="py-4 px-6">
                <span class="badge-mm" :class="roleClass(s.role)">{{ roleLabel(s.role) }}</span>
              </td>
              <td class="py-4 px-6">
                <span class="text-sm text-text-sec">{{ formatDate(s.joined_at) }}</span>
              </td>
              <td class="py-4 px-6">
                <div class="flex gap-1.5 justify-end">
                  <button title="Cambiar rol" @click="openRoleModal(s)"
                    class="w-9 h-9 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-warning-soft hover:text-warning hover:border-[rgba(196,138,26,0.15)]">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  </button>
                  <button title="Eliminar" @click="openRemoveModal(s)"
                    class="w-9 h-9 rounded-[10px] bg-transparent border border-transparent text-text-muted cursor-pointer flex items-center justify-center transition-all duration-200 hover:bg-danger-soft hover:text-danger hover:border-[rgba(185,60,60,0.15)]">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border-2 border-dashed border-border-green rounded-[var(--radius-card)]">
      <div class="w-20 h-20 rounded-full bg-green-soft flex items-center justify-center mx-auto mb-5" style="animation:float 6s ease-in-out infinite">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c2e" stroke-width="1.5" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <h3 class="font-display text-lg font-bold text-ink mb-2">
        {{ filter === 'all' && !searchQuery ? 'Sin miembros' : 'Sin resultados' }}
      </h3>
      <p class="text-sm text-text-muted mb-5 max-w-xs mx-auto">
        {{ filter === 'all' && !searchQuery ? 'Invita a tu equipo usando el código QR.' : 'Prueba cambiando los filtros o el término de búsqueda.' }}
      </p>
    </div>

    <!-- Modals -->
    <RoleModal :visible="showRoleModal"
      :member-name="staffToEdit?.member.first_name + ' ' + staffToEdit?.member.last_name"
      :current-role="staffToEdit?.role ?? 'waiter'" :error="roleError" :submitting="roleSubmitting"
      @close="closeRoleModal" @submit="handleRoleChange" />
    <ConfirmModal :visible="showRemoveModal" title="¿Eliminar miembro?"
      :message="`Se eliminará a &quot;${staffToRemove?.member.first_name} ${staffToRemove?.member.last_name}&quot; de este establecimiento. Perderá todo acceso.`"
      confirm-text="Eliminar" :error="removeError" :submitting="removeSubmitting"
      @confirm="handleRemove" @cancel="closeRemoveModal" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStaffStore } from '../stores/staff.store'
import type { Staff } from '../interfaces'
import RoleModal from '../components/RoleModal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'

const route = useRoute()
const cif = computed(() => route.params.cif as string)
const staffStore = useStaffStore()
const staff = computed(() => staffStore.staff)

const filter = ref<'all' | 'manager' | 'waiter' | 'kitchen'>('all')
const searchQuery = ref('')

const tabs = computed(() => [
  { label: 'Todos', value: 'all' as const, count: staff.value.length },
  { label: 'Managers', value: 'manager' as const, count: staff.value.filter(s => s.role === 'manager').length },
  { label: 'Camareros', value: 'waiter' as const, count: staff.value.filter(s => s.role === 'waiter').length },
  { label: 'Cocina', value: 'kitchen' as const, count: staff.value.filter(s => s.role === 'kitchen').length }
])

const filteredStaff = computed(() => {
  let result = staff.value
  if (filter.value !== 'all') result = result.filter(s => s.role === filter.value)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(s =>
      s.member.first_name.toLowerCase().includes(q) ||
      s.member.last_name.toLowerCase().includes(q) ||
      s.member.username.toLowerCase().includes(q)
    )
  }
  return result
})

const roleLabel = (role: string) => {
  switch (role) {
    case 'manager': return 'Manager'
    case 'waiter': return 'Camarero'
    case 'kitchen': return 'Cocina'
    default: return role
  }
}

const roleClass = (role: string) => {
  switch (role) {
    case 'manager': return 'bg-green-soft text-green-forest'
    case 'waiter': return 'bg-info-soft text-info'
    case 'kitchen': return 'bg-warning-soft text-warning'
    default: return 'bg-cream-dark text-text-muted'
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' })
}

interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 4000)
}

const showRoleModal = ref(false)
const staffToEdit = ref<Staff | null>(null)
const roleError = ref<string | null>(null)
const roleSubmitting = ref(false)

const openRoleModal = (s: Staff) => { staffToEdit.value = s; roleError.value = null; showRoleModal.value = true }
const closeRoleModal = () => { showRoleModal.value = false; staffToEdit.value = null; roleError.value = null }

const handleRoleChange = async (role: string) => {
  if (!staffToEdit.value) return
  roleSubmitting.value = true; roleError.value = null
  const result = await staffStore.updateRole(cif.value, staffToEdit.value.member.id, role)
  roleSubmitting.value = false
  if (result.ok) { closeRoleModal(); showToast('success', result.message ?? 'Hecho.') }
  else { roleError.value = result.error ?? 'Ha ocurrido un error.' }
}

const showRemoveModal = ref(false)
const staffToRemove = ref<Staff | null>(null)
const removeError = ref<string | null>(null)
const removeSubmitting = ref(false)

const openRemoveModal = (s: Staff) => { staffToRemove.value = s; removeError.value = null; showRemoveModal.value = true }
const closeRemoveModal = () => { showRemoveModal.value = false; staffToRemove.value = null; removeError.value = null }

const handleRemove = async () => {
  if (!staffToRemove.value) return
  removeSubmitting.value = true; removeError.value = null
  const result = await staffStore.removeMember(cif.value, staffToRemove.value.member.id)
  removeSubmitting.value = false
  if (result.ok) { closeRemoveModal(); showToast('success', result.message ?? 'Eliminado.') }
  else { removeError.value = result.error ?? 'Ha ocurrido un error.' }
}

onMounted(() => { staffStore.fetchStaff(cif.value) })
</script>

<style scoped>
.toast-enter-active { transition: all 0.25s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-8px); }
</style>