import { makeMenuApi } from '@/api/makeMenu'
import type { UserProfile } from '../interfaces/auth.response'

interface CheckAuthSuccess {
  ok: true
  user: UserProfile
}

interface CheckAuthFailure {
  ok: false
}

export const checkAuthAction = async (): Promise<CheckAuthSuccess | CheckAuthFailure> => {
  try {
    const { data } = await makeMenuApi.get<UserProfile>('/auth/profile/')
    return { ok: true, user: data }
  } catch {
    // Cookie ausente, expirada o inválida → el backend devuelve 401
    return { ok: false }
  }
}

