import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const getErrorMessage = (error, fallbackMessage = 'Erro desconhecido') => {
  return (
    error?.response?.data?.details ||
    error?.response?.data?.error ||
    error?.message ||
    fallbackMessage
  )
}

export default api
