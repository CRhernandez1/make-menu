import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'
import type { UserProfile } from '../interfaces/auth.response'

interface LoginError {
  ok: false
  message: string
}

interface LoginSuccess {
  ok: true
  user: UserProfile
}

export const loginAction = async (
  username: string,
  password: string,
  rememberMe: boolean,
): Promise<LoginError | LoginSuccess> => {
  try {
    const { data } = await makeMenuApi.post<UserProfile>('/auth/login/', {
      username,
      password,
      remember_me: rememberMe,
    })

    return {
      ok: true,
      user: data,
    }
  } catch (error) {
    if (isAxiosError(error) && error.response?.status === 401) {
      return {
        ok: false,
        message: 'Usuario o contraseña incorrectos',
      }
    }
    if (isAxiosError(error) && error.response?.data?.error) {
      return {
        ok: false,
        message: error.response.data.error,
      }
    }
    return {
      ok: false,
      message: 'No se pudo conectar con el servidor. Inténtalo más tarde.',
    }
  }
}

