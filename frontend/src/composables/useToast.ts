import { ref } from 'vue'

interface Toast {
  type: 'success' | 'error' | 'warning'
  message: string
  id: number
}

const toasts = ref<Toast[]>([])
let nextId = 0

export function useToast() {
  const show = (type: Toast['type'], message: string, duration = 4000) => {
    const id = nextId++
    toasts.value.push({ type, message, id })
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }

  const success = (message: string) => show('success', message)
  const error = (message: string) => show('error', message)
  const warning = (message: string) => show('warning', message)
  const dismiss = (id: number) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return { toasts, success, error, warning, dismiss }
}