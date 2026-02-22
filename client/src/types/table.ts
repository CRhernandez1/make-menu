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