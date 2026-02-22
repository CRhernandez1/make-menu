import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const router = useRouter()

  const isLoggedIn = computed(() => !!token.value)

  const login = async (username: string, password: string) => {
    const res = await fetch('http://127.0.0.1:8000/api/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    const data = await res.json()

    if (res.ok) {
      token.value = data.token
      localStorage.setItem('token', data.token)
      router.push('/')
    } else {
      throw new Error('Credenciales incorrectas')
    }
  }

  const register = async (
  username: string,
  password: string,
  firstName: string,
  lastName: string,
  email: string,
  phone: string
) => {
  const res = await fetch('http://127.0.0.1:8000/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      password,
      first_name: firstName,
      last_name: lastName,
      email,
      phone
    })
  })

  if (res.ok) {
    await login(username, password)
  } else {
    throw new Error('Error al registrar')
  }
}

  const logout = () => {
    token.value = ''
    localStorage.removeItem('token')
    router.push('/')
  }

  return { token, isLoggedIn, login, logout, register }
})