import axios from 'axios'

const makeMenuApi = axios.create({
  baseURL: import.meta.env.VITE_MAKE_MENU_API_URL,
  withCredentials: true,
})

export { makeMenuApi }