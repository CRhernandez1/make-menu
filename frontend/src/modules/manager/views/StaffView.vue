<template>
  <div class="px-8 py-8 lg:px-12 lg:py-10">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm mb-6">
      <router-link to="/" class="text-gray-400 no-underline font-medium hover:text-emerald-600 transition-colors">Establishments</router-link>
      <svg class="text-gray-300" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>
      <span class="text-[#1a1a2e] font-semibold">Staff</span>
    </nav>

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-8 gap-4">
      <div>
        <h1 class="text-2xl font-extrabold text-[#1a1a2e] tracking-tight">Staff Management</h1>
        <p class="text-[15px] text-gray-400 mt-1">{{ staff.length }} members in this establishment.</p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
      <div class="inline-flex bg-white border border-gray-100 rounded-xl p-1 gap-1 shadow-sm">
        <button
          v-for="tab in tabs" :key="tab.value"
          @click="filter = tab.value"
          class="flex items-center gap-2 py-2 px-4 rounded-lg border-none text-sm font-medium cursor-pointer transition-all duration-150"
          :class="filter === tab.value ? 'bg-[#1a1a2e] text-white shadow-sm' : 'bg-transparent text-gray-400 hover:text-gray-600'"
        >
          {{ tab.label }}
          <span class="text-[11px] font-bold min-w-[20px] text-center py-0.5 px-1.5 rounded-md"
            :class="filter === tab.value ? 'bg-white/15 text-white/80' : 'bg-gray-100 text-gray-400'">{{ tab.count }}</span>
        </button>
      </div>

      <div class="flex items-center gap-2 bg-white border border-gray-100 rounded-xl px-4 h-10 shadow-sm focus-within:border-emerald-300 focus-within:ring-2 focus-within:ring-emerald-500/10 transition-all">
        <svg class="text-gray-300 shrink-0" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="searchQuery" type="text" placeholder="Search by name, username..."
          class="border-none outline-none bg-transparent text-sm text-[#1a1a2e] w-52 placeholder:text-gray-300" />
      </div>
    </div>

    <!-- Error -->
    <div v-if="staffStore.error" class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 bg-red-50 text-red-600 border border-red-100">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <span class="flex-1">{{ staffStore.error }}</span>
      <button @click="staffStore.clearError" class="text-red-300 hover:text-red-500 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
    </div>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast" class="flex items-center gap-3 p-4 rounded-xl text-sm mb-5 border"
        :class="toast.type === 'success' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-red-50 text-red-600 border-red-100'">
        <svg v-if="toast.type === 'success'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        <span class="flex-1">{{ toast.message }}</span>
        <button @click="toast = null" class="text-current opacity-40 hover:opacity-80 text-xl leading-none bg-transparent border-none cursor-pointer">&times;</button>
      </div>
    </Transition>

    <!-- Loading -->
    <div v-if="staffStore.loading" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 animate-pulse space-y-6">
      <div v-for="n in 4" :key="n" class="flex items-center gap-8">
        <div class="w-10 h-10 rounded-full bg-gray-100 shrink-0"></div>
        <div class="h-4 w-32 rounded-lg bg-gray-100"></div>
        <div class="h-4 w-20 rounded-lg bg-gray-100"></div>
        <div class="h-6 w-16 rounded-full bg-gray-100"></div>
        <div class="h-4 w-24 rounded-lg bg-gray-100 ml-auto"></div>
      </div>
    </div>

    <!-- Table -->
    <div v-else-if="filteredStaff.length > 0" class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[700px]">
          <thead>
            <tr class="border-b border-gray-100">
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[35%]">Member</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[20%]">Role</th>
              <th class="text-left py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[20%]">Joined</th>
              <th class="text-right py-3.5 px-6 text-[11px] font-bold text-gray-400 uppercase tracking-[0.08em] w-[25%]">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredStaff" :key="s.id" class="border-b border-gray-50 last:border-b-0 hover:bg-[#f8f9fb] transition-colors">
              <!-- Member -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full bg-[#1a1a2e] text-white text-sm font-bold flex items-center justify-center shrink-0">
                    {{ s.member.first_name.charAt(0) }}{{ s.member.last_name.charAt(0) }}
                  </div>
                  <div>
                    <span class="block text-sm font-semibold text-[#1a1a2e]">{{ s.member.first_name }} {{ s.member.last_name }}</span>
                    <span class="block text-xs text-gray-400 mt-0.5">@{{ s.member.username }}</span>
                  </div>
                </div>
              </td>

              <!-- Role -->
              <td class="py-4 px-6">
                <span class="inline-flex items-center gap-1.5 text-xs font-semibold py-1.5 px-3 rounded-full"
                  :class="roleClass(s.role)">
                  {{ roleLabel(s.role) }}
                </span>
              </td>

              <!-- Joined -->
              <td class="py-4 px-6">
                <span class="text-sm text-gray-500">{{ formatDate(s.joined_at) }}</span>
              </td>

              <!-- Actions -->
              <td class="py-4 px-6">
                <div class="flex gap-1.5 justify-end">
                  <button title="Change role" @click="openRoleModal(s)"
                    class="w-9 h-9 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-amber-50 hover:text-amber-500 hover:border-amber-100">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  </button>
                  <button title="Remove" @click="openRemoveModal(s)"
                    class="w-9 h-9 rounded-lg bg-transparent border border-transparent text-gray-400 cursor-pointer flex items-center justify-center transition-all duration-150 hover:bg-red-50 hover:text-red-500 hover:border-red-100">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-24 bg-white border border-dashed border-gray-200 rounded-2xl">
      <div class="w-16 h-16 rounded-2xl bg-gray-50 flex items-center justify-center mx-auto mb-5">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#c4c9d4" stroke-width="1.5" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <h3 class="text-base font-bold text-[#1a1a2e] mb-1">
        {{ filter === 'all' && !searchQuery ? 'No staff members' : 'No results found' }}
      </h3>
      <p class="text-sm text-gray-400 mb-5">
        {{ filter === 'all' && !searchQuery ? 'Invite members using a QR code.' : 'Try changing your filters or search query.' }}
      </p>
    </div>

    <!-- Modals -->
    <RoleModal
      :visible="showRoleModal"
      :member-name="staffToEdit?.member.first_name + ' ' + staffToEdit?.member.last_name"
      :current-role="staffToEdit?.role ?? 'waiter'"
      :error="roleError"
      :submitting="roleSubmitting"
      @close="closeRoleModal"
      @submit="handleRoleChange"
    />
    <ConfirmModal
      :visible="showRemoveModal"
      title="Remove member"
      :message="`This will remove &quot;${staffToRemove?.member.first_name} ${staffToRemove?.member.last_name}&quot; from this establishment. They will lose all access.`"
      confirm-text="Remove"
      :error="removeError"
      :submitting="removeSubmitting"
      @confirm="handleRemove"
      @cancel="closeRemoveModal"
    />
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
  { label: 'All', value: 'all' as const, count: staff.value.length },
  { label: 'Managers', value: 'manager' as const, count: staff.value.filter(s => s.role === 'manager').length },
  { label: 'Waiters', value: 'waiter' as const, count: staff.value.filter(s => s.role === 'waiter').length },
  { label: 'Kitchen', value: 'kitchen' as const, count: staff.value.filter(s => s.role === 'kitchen').length }
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
    case 'waiter': return 'Waiter'
    case 'kitchen': return 'Kitchen'
    default: return role
  }
}

const roleClass = (role: string) => {
  switch (role) {
    case 'manager': return 'bg-purple-50 text-purple-600'
    case 'waiter': return 'bg-emerald-50 text-emerald-600'
    case 'kitchen': return 'bg-amber-50 text-amber-600'
    default: return 'bg-gray-50 text-gray-400'
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

// Toast
interface Toast { type: 'success' | 'error'; message: string }
const toast = ref<Toast | null>(null)
let toastTimer: ReturnType<typeof setTimeout> | null = null
const showToast = (type: 'success' | 'error', message: string) => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => { toast.value = null }, 4000)
}

// Role modal
const showRoleModal = ref(false)
const staffToEdit = ref<Staff | null>(null)
const roleError = ref<string | null>(null)
const roleSubmitting = ref(false)

const openRoleModal = (s: Staff) => { staffToEdit.value = s; roleError.value = null; showRoleModal.value = true }
const closeRoleModal = () => { showRoleModal.value = false; staffToEdit.value = null; roleError.value = null }

const handleRoleChange = async (role: string) => {
  if (!staffToEdit.value) return
  roleSubmitting.value = true
  roleError.value = null
  const result = await staffStore.updateRole(cif.value, staffToEdit.value.member.id, role)
  roleSubmitting.value = false
  if (result.ok) { closeRoleModal(); showToast('success', result.message ?? 'Done.') }
  else { roleError.value = result.error ?? 'An error occurred.' }
}

// Remove modal
const showRemoveModal = ref(false)
const staffToRemove = ref<Staff | null>(null)
const removeError = ref<string | null>(null)
const removeSubmitting = ref(false)

const openRemoveModal = (s: Staff) => { staffToRemove.value = s; removeError.value = null; showRemoveModal.value = true }
const closeRemoveModal = () => { showRemoveModal.value = false; staffToRemove.value = null; removeError.value = null }

const handleRemove = async () => {
  if (!staffToRemove.value) return
  removeSubmitting.value = true
  removeError.value = null
  const result = await staffStore.removeMember(cif.value, staffToRemove.value.member.id)
  removeSubmitting.value = false
  if (result.ok) { closeRemoveModal(); showToast('success', result.message ?? 'Removed.') }
  else { removeError.value = result.error ?? 'An error occurred.' }
}

onMounted(() => { staffStore.fetchStaff(cif.value) })
</script>

<style scoped>
.toast-enter-active { transition: all 0.25s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-8px); }
</style>