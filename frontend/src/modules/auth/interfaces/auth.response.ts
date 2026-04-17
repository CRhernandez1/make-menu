export interface UserProfile {
  id: number
  user: {
    id: number
    username: string
    email: string
    first_name: string
    last_name: string
  }
  phone: string
  avatar: string | null
  role: string | null
  establishment_id: number | null
  establishment_cif: string | null
}
