import { makeMenuApi } from '@/api/makeMenu'
import { isAxiosError } from 'axios'
import { useToast } from './useToast'

interface ApiResult<T = any> {
  ok: boolean
  data?: T
  errors?: Record<string, string[]>
  message?: string
}

export function useApi() {
  const toast = useToast()

  const call = async <T = any>(
    method: 'get' | 'post',
    url: string,
    payload?: any,
    options?: { silent?: boolean }
  ): Promise<ApiResult<T>> => {
    try {
      const response = method === 'get'
        ? await makeMenuApi.get<T>(url)
        : await makeMenuApi.post<T>(url, payload)

      return { ok: true, data: response.data }
    } catch (err) {
      if (isAxiosError(err) && err.response) {
        const data = err.response.data
        const status = err.response.status

        // Errores de validación por campo
        if (data.errors) {
          return { ok: false, errors: data.errors }
        }

        // Error simple
        const message = data.error || data.message || getDefaultMessage(status)
        if (!options?.silent) toast.error(message)
        return { ok: false, message }
      }

      const message = 'No se pudo conectar con el servidor.'
      if (!options?.silent) toast.error(message)
      return { ok: false, message }
    }
  }

  const get = <T = any>(url: string) => call<T>('get', url)
  const post = <T = any>(url: string, payload?: any, options?: { silent?: boolean }) =>
    call<T>('post', url, payload, options)

  return { get, post }
}

function getDefaultMessage(status: number): string {
  switch (status) {
    case 400: return 'Datos inválidos. Revisa los campos.'
    case 403: return 'No tienes permiso para esta acción.'
    case 404: return 'Recurso no encontrado.'
    case 409: return 'Ya existe un registro con estos datos.'
    case 500: return 'Error en el servidor. Inténtalo más tarde.'
    default: return 'Ocurrió un error inesperado.'
  }
}