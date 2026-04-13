export interface Establishment {
  id: number
  name: string
  legal_name: string
  cif: string
  description: string
  zip_code: string
  city: string
  address: string
  phone: string
  opened: boolean
}

export interface EstablishmentCreate {
  cif: string
  name: string
  legal_name: string
  description: string
  zip_code: string
  city: string
  address: string
  phone: string
}

export interface EstablishmentUpdate {
  name: string
  legal_name: string
  description: string
  zip_code: string
  city: string
  address: string
  phone: string
}

export interface Table {
  id: number
  establishment: Establishment
  number: number
  max_guests: number
  active: boolean
}

export interface TableCreate {
  number: number
  max_guests: number
}

export interface TableUpdate {
  max_guests: number
}

export interface Staff {
  id: number
  member: {
    id: number
    username: string
    first_name: string
    last_name: string
    email: string
  }
  role: 'manager' | 'waiter' | 'kitchen'
  joined_at: string
  end_date: string | null
}

export interface ActionResult {
  ok: boolean
  error?: string
  message?: string
}