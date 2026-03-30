import { makeMenuApi } from '@/api/makeMenu'

interface RegisterPayload {
  username: string
  password: string
  email: string
  first_name: string
  last_name: string
  phone?: string
  invite_token: string
}

export const registerUser = async (payload: RegisterPayload) => {
  try {
    const response = await makeMenuApi.post('/auth/register/', payload)
    return { ok: true, message: response.data.message }
  } catch (error: any) {
    // Si Django devuelve 409 Conflict (ej: "Username already exists") o 400
    const errorMessage = error.response?.data?.error || 'Error al conectar con el servidor'
    return { ok: false, error: errorMessage }
  }
}
