import { reactive } from 'vue'

export function useFormErrors() {
  const errors = reactive<Record<string, string>>({})

  const clear = () => {
    Object.keys(errors).forEach(key => delete errors[key])
  }

  const setFromBackend = (data: Record<string, string[]>) => {
    clear()
    for (const [field, msgs] of Object.entries(data)) {
      errors[field] = Array.isArray(msgs) ? msgs.join('. ') : String(msgs)
    }
  }

  const set = (field: string, message: string) => {
    errors[field] = message
  }

  const validate = (rules: Record<string, { value: any; message: string }[]>): boolean => {
    clear()
    let valid = true
    for (const [field, checks] of Object.entries(rules)) {
      for (const check of checks) {
        const v = check.value
        if (v === null || v === undefined || v === '' || (typeof v === 'number' && v <= 0)) {
          errors[field] = check.message
          valid = false
          break
        }
      }
    }
    return valid
  }

  return { errors, clear, set, setFromBackend, validate }
}