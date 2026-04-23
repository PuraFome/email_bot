import { useState } from 'react'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000'
})

export default function App() {
  const [status, setStatus] = useState('Pronto')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAction = async (endpoint) => {
    setLoading(true)
    setStatus('Aguardando resposta...')
    setMessage('')

    try {
        const response = await api.post(endpoint, {}, {
            headers: { 'Content-Type': 'application/json' }
        })
      setStatus('Concluído')
      setMessage(response.data.message || 'Ação concluída com sucesso.')
    } catch (error) {
      setStatus('Erro')
      setMessage(error.response?.data?.error || error.message || 'Falha na requisição.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1>Email Bot</h1>
      <p>Backend: <strong>{import.meta.env.VITE_API_URL || 'http://localhost:5000'}</strong></p>
      <div className="button-row">
        <button onClick={() => handleAction('/start_email_service')} disabled={loading}>
          Iniciar envio
        </button>
        <button onClick={() => handleAction('/stop_email_service')} disabled={loading}>
          Parar envio
        </button>
      </div>

      <div className="status-card">
        <p><strong>Status:</strong> {status}</p>
        {message && <p><strong>Resposta:</strong> {message}</p>}
      </div>
    </div>
  )
}
