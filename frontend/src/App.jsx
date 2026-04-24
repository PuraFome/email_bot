import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { createTheme, ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'
import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import TextField from '@mui/material/TextField'
import MenuItem from '@mui/material/MenuItem'
import Switch from '@mui/material/Switch'
import FormControlLabel from '@mui/material/FormControlLabel'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Snackbar from '@mui/material/Snackbar'
import Alert from '@mui/material/Alert'
import CircularProgress from '@mui/material/CircularProgress'
import DeleteIcon from '@mui/icons-material/Delete'
import LightModeIcon from '@mui/icons-material/LightMode'
import DarkModeIcon from '@mui/icons-material/DarkMode'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000'
})

const initialEnterpriseState = {
  name: '',
  fantasy_name: '',
  email: '',
  situation: 'ativa',
  coontact_valid: true,
  whatsapp: '',
  ddd: '',
  main_activity_code: '',
  main_activity_description: '',
  cnpj: '',
  country: '',
  region: '',
  share_capital: '',
  state: ''
}

const initialModelState = {
  html: ''
}

export default function App() {
  const [tab, setTab] = useState(0)
  const [mode, setMode] = useState('light')
  const [loading, setLoading] = useState(false)
  const [statusMessage, setStatusMessage] = useState('Pronto')
  const [snackbar, setSnackbar] = useState({ open: false, severity: 'success', message: '' })

  const [enterprises, setEnterprises] = useState([])
  const [enterpriseForm, setEnterpriseForm] = useState(initialEnterpriseState)

  const [models, setModels] = useState([])
  const [modelForm, setModelForm] = useState(initialModelState)
  const [selectedModelId, setSelectedModelId] = useState('')

  const [sendings, setSendings] = useState([])
  const [emailReturns, setEmailReturns] = useState([])

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: '#1a73e8'
          },
          background: {
            default: mode === 'dark' ? '#121212' : '#f4f6fb',
            paper: mode === 'dark' ? '#1e1e1e' : '#ffffff'
          }
        }
      }),
    [mode]
  )

  useEffect(() => {
    loadHomeData()
  }, [])

  const loadHomeData = async () => {
    fetchEnterprises()
    fetchModels()
    fetchSendings()
    fetchEmailReturns()
  }

  const handleTabChange = (_event, value) => {
    setTab(value)
    if (value === 1) fetchEnterprises()
    if (value === 2) fetchModels()
    if (value === 3) fetchSendings()
    if (value === 4) fetchEmailReturns()
  }

  const openSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, severity, message })
  }

  const closeSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }))
  }

  const handleApiError = (error, fallbackMessage) => {
    const message =
      error?.response?.data?.details || error?.response?.data?.error || error?.message || fallbackMessage
    openSnackbar(message, 'error')
    return message
  }

  const fetchEnterprises = async () => {
    try {
      const response = await api.get('/api/enterprise_meling')
      setEnterprises(response.data)
    } catch (error) {
      handleApiError(error, 'Falha ao carregar enterprises')
    }
  }

  const fetchModels = async () => {
    try {
      const response = await api.get('/api/models')
      setModels(response.data)
    } catch (error) {
      handleApiError(error, 'Falha ao carregar models')
    }
  }

  const fetchSendings = async () => {
    try {
      const response = await api.get('/api/sendings')
      setSendings(response.data)
    } catch (error) {
      handleApiError(error, 'Falha ao carregar sendings')
    }
  }

  const fetchEmailReturns = async () => {
    try {
      const response = await api.get('/api/email_returns')
      setEmailReturns(response.data)
    } catch (error) {
      handleApiError(error, 'Falha ao carregar aberturas')
    }
  }

  const handleAction = async (endpoint, modelId = null) => {
    setLoading(true)
    setStatusMessage('Aguardando resposta...')

    try {
      const payload = modelId ? { html_template_id: modelId } : {}
      const response = await api.post(endpoint, payload, {
        headers: { 'Content-Type': 'application/json' }
      })
      setStatusMessage(response.data.message || 'Ação concluída com sucesso.')
      openSnackbar(response.data.message || 'Operação concluída com sucesso.', 'success')
    } catch (error) {
      const errorMessage = handleApiError(error, 'Falha na requisição')
      setStatusMessage(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const createEnterprise = async () => {
    setLoading(true)
    try {
      await api.post('/api/enterprise_meling', enterpriseForm)
      setEnterpriseForm(initialEnterpriseState)
      openSnackbar('Enterprise criado com sucesso.')
      fetchEnterprises()
    } catch (error) {
      handleApiError(error, 'Erro ao criar enterprise')
    } finally {
      setLoading(false)
    }
  }

  const createModel = async () => {
    setLoading(true)
    try {
      await api.post('/api/models', modelForm)
      setModelForm(initialModelState)
      openSnackbar('Model criado com sucesso.')
      fetchModels()
    } catch (error) {
      handleApiError(error, 'Erro ao criar model')
    } finally {
      setLoading(false)
    }
  }

  const deleteEnterprise = async (id) => {
    setLoading(true)
    try {
      await api.delete(`/api/enterprise_meling/${id}`)
      openSnackbar('Enterprise excluído com sucesso.')
      fetchEnterprises()
    } catch (error) {
      handleApiError(error, 'Erro ao excluir enterprise')
    } finally {
      setLoading(false)
    }
  }

  const deleteModel = async (id) => {
    setLoading(true)
    try {
      await api.delete(`/api/models/${id}`)
      openSnackbar('Model excluído com sucesso.')
      fetchModels()
    } catch (error) {
      handleApiError(error, 'Erro ao excluir model')
    } finally {
      setLoading(false)
    }
  }

  const deleteSending = async (id) => {
    setLoading(true)
    try {
      await api.delete(`/api/sendings/${id}`)
      openSnackbar('Sending excluído com sucesso.')
      fetchSendings()
    } catch (error) {
      handleApiError(error, 'Erro ao excluir sending')
    } finally {
      setLoading(false)
    }
  }

  const renderHome = () => (
    <Box sx={{ p: 3 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Início
        </Typography>
        <Typography sx={{ mb: 2 }}>
          Use os botões abaixo para iniciar ou parar o serviço de envio. As abas permitem gerenciar empresas, modelos e visualizar envios e aberturas.
        </Typography>
        <Grid container spacing={2} alignItems="flex-end">
          <Grid item xs={12} sm={6} md={4}>
            <TextField
              select
              label="Selecione um modelo"
              value={selectedModelId}
              onChange={(e) => setSelectedModelId(e.target.value)}
              fullWidth
              variant="outlined"
              disabled={loading}
            >
              <MenuItem value="">
                <em>Nenhum modelo</em>
              </MenuItem>
              {models.map((model) => (
                <MenuItem key={model.model_id} value={model.model_id}>
                  {model.html?.slice(0, 50)}... ({model.model_id.slice(0, 8)})
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={3} md={2}>
            <Button variant="contained" color="primary" onClick={() => handleAction('/start_email_service', selectedModelId)} fullWidth disabled={loading}>
              Iniciar envio
            </Button>
          </Grid>
          <Grid item xs={12} sm={3} md={2}>
            <Button variant="outlined" color="primary" onClick={() => handleAction('/stop_email_service')} fullWidth disabled={loading}>
              Parar envio
            </Button>
          </Grid>
          <Grid item>{loading && <CircularProgress size={24} />}</Grid>
        </Grid>
      </Paper>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1">Enterprises</Typography>
            <Typography variant="h6">{enterprises.length}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1">Models</Typography>
            <Typography variant="h6">{models.length}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1">Envios</Typography>
            <Typography variant="h6">{sendings.length}</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )

  const renderEnterpriseTab = () => (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Gerenciar Enterprise_Meling
      </Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField
              label="Nome"
              value={enterpriseForm.name}
              fullWidth
              onChange={(e) => setEnterpriseForm({ ...enterpriseForm, name: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Fantasy name"
              value={enterpriseForm.fantasy_name}
              fullWidth
              onChange={(e) => setEnterpriseForm({ ...enterpriseForm, fantasy_name: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Email"
              type="email"
              value={enterpriseForm.email}
              fullWidth
              onChange={(e) => setEnterpriseForm({ ...enterpriseForm, email: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Situação"
              value={enterpriseForm.situation}
              fullWidth
              onChange={(e) => setEnterpriseForm({ ...enterpriseForm, situation: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="País"
              value={enterpriseForm.country}
              fullWidth
              onChange={(e) => setEnterpriseForm({ ...enterpriseForm, country: e.target.value })}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControlLabel
              control={
                <Switch
                  checked={enterpriseForm.coontact_valid}
                  onChange={(e) => setEnterpriseForm({ ...enterpriseForm, coontact_valid: e.target.checked })}
                />
              }
              label="Contato válido"
            />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" onClick={createEnterprise} disabled={loading}>
              Criar enterprise
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Fantasy name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Situação</TableCell>
              <TableCell>Contato válido</TableCell>
              <TableCell align="right">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {enterprises.map((item) => (
              <TableRow key={item.enterprise_meling_id}>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.fantasy_name}</TableCell>
                <TableCell>{item.email}</TableCell>
                <TableCell>{item.situation}</TableCell>
                <TableCell>{item.coontact_valid ? 'Sim' : 'Não'}</TableCell>
                <TableCell align="right">
                  <IconButton color="error" onClick={() => deleteEnterprise(item.enterprise_meling_id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )

  const renderModelsTab = () => (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Gerenciar Models
      </Typography>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              label="HTML do modelo"
              value={modelForm.html}
              fullWidth
              multiline
              minRows={4}
              onChange={(e) => setModelForm({ ...modelForm, html: e.target.value })}
            />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" onClick={createModel} disabled={loading}>
              Criar model
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>HTML</TableCell>
              <TableCell align="right">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {models.map((item) => (
              <TableRow key={item.model_id}>
                <TableCell>{item.model_id}</TableCell>
                <TableCell>{item.html?.slice(0, 80)}...</TableCell>
                <TableCell align="right">
                  <IconButton color="error" onClick={() => deleteModel(item.model_id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )

  const renderSendingsTab = () => (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Envios recentes
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Sending ID</TableCell>
              <TableCell>Enterprise</TableCell>
              <TableCell>Runner</TableCell>
              <TableCell>Enviado</TableCell>
              <TableCell>Data</TableCell>
              <TableCell align="right">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sendings.map((item) => (
              <TableRow key={item.sending_id}>
                <TableCell>{item.sending_id}</TableCell>
                <TableCell>{item.enterprise_meling_id}</TableCell>
                <TableCell>{item.runner_id}</TableCell>
                <TableCell>{item.sended_email ? 'Sim' : 'Não'}</TableCell>
                <TableCell>{item.sended_email_date}</TableCell>
                <TableCell align="right">
                  <IconButton color="error" onClick={() => deleteSending(item.sending_id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )

  const renderEmailReturnsTab = () => (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Aberturas de email
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Sending ID</TableCell>
              <TableCell>Aberto</TableCell>
              <TableCell>Data</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {emailReturns.map((item) => (
              <TableRow key={item.email_return_information_id}>
                <TableCell>{item.email_return_information_id}</TableCell>
                <TableCell>{item.sending_id}</TableCell>
                <TableCell>{item.email_opned ? 'Sim' : 'Não'}</TableCell>
                <TableCell>{item.email_opned_date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', color: 'text.primary' }}>
        <AppBar position="static" color="primary" elevation={1}>
          <Toolbar sx={{ justifyContent: 'space-between' }}>
            <Box>
              <Typography variant="h6" component="div">
                Email Bot Monorepo
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                Interface de gerenciamento com Material UI
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <FormControlLabel
                control={<Switch checked={mode === 'dark'} onChange={() => setMode((prev) => (prev === 'dark' ? 'light' : 'dark'))} />}
                label={mode === 'dark' ? <DarkModeIcon /> : <LightModeIcon />}
              />
            </Box>
          </Toolbar>
          <Tabs value={tab} onChange={handleTabChange} textColor="inherit" indicatorColor="secondary" variant="scrollable" scrollButtons="auto">
            <Tab label="Home" />
            <Tab label="Enterprises" />
            <Tab label="Models" />
            <Tab label="Sendings" />
            <Tab label="Aberturas" />
          </Tabs>
        </AppBar>

        {tab === 0 && renderHome()}
        {tab === 1 && renderEnterpriseTab()}
        {tab === 2 && renderModelsTab()}
        {tab === 3 && renderSendingsTab()}
        {tab === 4 && renderEmailReturnsTab()}

        <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={closeSnackbar} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
          <Alert onClose={closeSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  )
}
