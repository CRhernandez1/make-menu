// Interfaces compartidas usadas por manager, waiter y kitchen

export interface OrderSummary {
  id: number
  status: number
  status_display: string
  table_number: number | null
  establishment_name?: string
  placed_at: string
  paid: boolean
  total: string
  closed_at: string | null
}

export interface OrderDetailItem {
  id: number
  product_name: string
  price: string
  quantity: number
  notes: string
}

export interface EstablishmentOption {
  id: number
  name: string
  cif: string
}

export interface TimeFilter {
  label: string
  value: string
}
