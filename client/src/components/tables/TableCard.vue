<template>
  <div class="table-card" :class="cardClass">
    <!-- Estado visual -->
    <div class="card-status">
      <span class="status-dot"></span>
      <span class="status-text">{{ statusText }}</span>
    </div>

    <!-- Número de mesa -->
    <div class="card-number">{{ table.number }}</div>
    <div class="card-label">Mesa</div>

    <!-- Capacidad -->
    <div class="card-capacity">
      <span class="capacity-icon">👤</span>
      <span class="capacity-text">{{ table.max_guests }}</span>
    </div>

    <!-- Acciones -->
    <div class="card-actions">
      <button class="action-btn toggle-btn" :title="table.active ? 'Desactivar mesa' : 'Activar mesa'"
        @click="$emit('toggle', table.number)">
        {{ table.active ? '⏸' : '▶' }}
      </button>
      <button class="action-btn edit-btn" title="Editar mesa" @click="$emit('edit', table)">
        ✏️
      </button>
      <button class="action-btn delete-btn" title="Eliminar mesa" @click="$emit('delete', table)">
        🗑️
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Table } from '@/types/table';

const props = defineProps<{
  table: Table;
}>();

defineEmits<{
  toggle: [id: number];
  edit: [table: Table];
  delete: [table: Table];
}>();

const cardClass = computed(() => ({
  'card--active': props.table.active,
  'card--inactive': !props.table.active,
}));

const statusText = computed(() => (props.table.active ? 'Activa' : 'Inactiva'));
</script>

<style scoped>
.table-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  position: relative;
  transition: all 0.25s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.table-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* ===== Estados ===== */
.card--active {
  border-color: #d1fae5;
  background: linear-gradient(180deg, #fff 60%, #f0fdf4);
}

.card--active .status-dot {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.card--inactive {
  border-color: #f3f4f6;
  background: linear-gradient(180deg, #fff 60%, #f9fafb);
  opacity: 0.7;
}

.card--inactive .status-dot {
  background: #9ca3af;
}

.card--inactive .card-number {
  color: #9ca3af;
}

/* ===== Status badge ===== */
.card-status {
  display: flex;
  align-items: center;
  gap: 6px;
  align-self: flex-start;
  margin-bottom: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.card--inactive .status-dot {
  animation: none;
}

.status-text {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

/* ===== Número de mesa ===== */
.card-number {
  font-family: 'Sora', sans-serif;
  font-size: 42px;
  font-weight: 800;
  color: #1a1a2e;
  line-height: 1;
  margin: 4px 0;
}

.card-label {
  font-size: 12px;
  font-weight: 500;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* ===== Capacidad ===== */
.card-capacity {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  background: #f3f4f6;
  padding: 4px 12px;
  border-radius: 20px;
}

.capacity-icon {
  font-size: 12px;
}

.capacity-text {
  font-size: 13px;
  font-weight: 700;
  color: #374151;
}

/* ===== Acciones ===== */
.card-actions {
  display: flex;
  gap: 6px;
  margin-top: 12px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.table-card:hover .card-actions {
  opacity: 1;
}

.action-btn {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  background: #f3f4f6;
}

.toggle-btn:hover {
  background: #dbeafe;
}

.edit-btn:hover {
  background: #fef3c7;
}

.delete-btn:hover {
  background: #fee2e2;
}

@keyframes pulse {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }
}
</style>
