import { makeMenuApi } from '@/api/makeMenu'

// 👇 Modificamos la interfaz para que coincida con Django y tu vista
interface RegisterPayload {
  username: string
  password: string
  email: string
  first_name: string
  last_name: string
  phone?: string
  invitation_id: string // 👈 CAMBIO AQUÍ (antes era invite_token)
}

export const registerUser = async (payload: RegisterPayload) => {
  try {
    // Axios enviará el payload exacto, incluyendo el invitation_id
    const response = await makeMenuApi.post('/auth/register/', payload)
    return { ok: true, message: response.data.message }
  } catch (error: any) {
    // Si Django devuelve 409 Conflict (ej: "Username already exists") o 400
    const errorMessage = error.response?.data?.error || 'Error al conectar con el servidor'
    return { ok: false, error: errorMessage }
  }
}
