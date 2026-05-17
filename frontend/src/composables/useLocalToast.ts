import { ref, onUnmounted } from 'vue'

export interface LocalToast {
  type: 'success' | 'error'
  message: string
}

export function useLocalToast(duration = 4000) {
  const toast = ref<LocalToast | null>(null)
  let timer: ReturnType<typeof setTimeout> | null = null

  const show = (type: 'success' | 'error', message: string) => {
    if (timer) clearTimeout(timer)
    toast.value = { type, message }
    timer = setTimeout(() => { toast.value = null }, duration)
  }

  const success = (message: string) => show('success', message)
  const error = (message: string) => show('error', message)

  onUnmounted(() => { if (timer) clearTimeout(timer) })

  return { toast, show, success, error }
}
