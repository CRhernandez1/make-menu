/**
 * Mapeo de status numérico a clases de Tailwind.
 * Extraído de ManagerOrders y WaiterOrders (eran idénticas).
 */

const STATUS_CLASS_MAP: Record<number, string> = {
  [-1]: 'bg-danger-soft text-danger',
  1: 'bg-warning-soft text-warning',
  2: 'bg-info-soft text-info',
  3: 'bg-green-soft text-green-forest',
}

const STATUS_DOT_MAP: Record<number, string> = {
  [-1]: 'bg-danger',
  1: 'bg-warning',
  2: 'bg-info',
  3: 'bg-green-bright',
}

const DEFAULT_CLASS = 'bg-cream-dark text-text-muted'
const DEFAULT_DOT = 'bg-text-ghost'

export function useOrderStatus() {
  const getStatusClass = (status: number): string => STATUS_CLASS_MAP[status] ?? DEFAULT_CLASS
  const getStatusDot = (status: number): string => STATUS_DOT_MAP[status] ?? DEFAULT_DOT

  return { getStatusClass, getStatusDot }
}
