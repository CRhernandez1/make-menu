import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'
import type { AuthResponse } from '../interfaces'

interface LoginError {
  ok: false
  message: string
}

interface LoginSuccess {
  ok: true
  token: string
}

export const loginAction = async (
  username: string,
  password: string,
): Promise<LoginError | LoginSuccess> => {
  try {
    const { data } = await makeMenuApi.post<AuthResponse>('/auth/login/', {
      username,
      password,
    })

    return {
      ok: true,
      token: data.token,
    }
  } catch (error) {
    if (isAxiosError(error) && error.response?.status === 401) {
      return {
        ok: false,
        message: 'Usuario o contraseña incorrectos',
      }
    }
    // Si el servidor explota (Error 500) o no hay internet
    console.error(error)
    throw new Error('No se pudo realizar la petición. Inténtalo más tarde.')
  }
}
