import axios from 'axios'

const makeMenuApi = axios.create({
  baseURL: import.meta.env.VITE_MAKE_MENU_API_URL,
})

makeMenuApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export { makeMenuApi }
