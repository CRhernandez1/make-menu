import { makeMenuApi } from '@/api/makeMenu'

export const logoutAction = async () => {
  try {
    await makeMenuApi.post('/auth/logout/')
    return true
  } catch (error) {
    console.error('Error al cerrar sesión', error)
    return true
  }
}
