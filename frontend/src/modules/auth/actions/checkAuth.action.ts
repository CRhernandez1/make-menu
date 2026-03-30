import { makeMenuApi } from '@/api/makeMenu'

export const checkAuthAction = async () => {
  try {
    // Aquí llamamos a un endpoint de tu Django que te devuelva los datos del perfil
    // Nota: Necesitarás tener este endpoint creado en Django.
    // Si no lo tienes aún, puedes usar uno de prueba o crearlo luego.
    const { data } = await makeMenuApi.get('/auth/profile/')
    return { ok: true, user: data }
  } catch (error) {
    // Si Django devuelve 401 (token expirado o inválido)
    return { ok: false }
  }
}
