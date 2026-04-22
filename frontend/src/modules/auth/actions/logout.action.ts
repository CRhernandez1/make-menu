import { makeMenuApi } from '@/api/makeMenu'

export const logoutAction = async (): Promise<boolean> => {
  try {
    await makeMenuApi.post('/auth/logout/')
    return true
  } catch {
    // Si el backend falla (ej: cookie ya expirada), el estado local
    // se limpia igualmente en el store — el usuario siempre queda desautenticado
    return false
  }
}
