import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import TextField from '@mui/material/TextField'
import MenuItem from '@mui/material/MenuItem'

export default function HomeView({ onAction, loading, counts, models, selectedModelId, onModelChange }) {
  return (
    <Box>
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
              onChange={(e) => onModelChange(e.target.value)}
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
            <Button variant="contained" color="primary" onClick={() => onAction('/start_email_service', selectedModelId)} fullWidth disabled={loading}>
              Iniciar envio
            </Button>
          </Grid>
          <Grid item xs={12} sm={3} md={2}>
            <Button variant="outlined" color="primary" onClick={() => onAction('/stop_email_service')} fullWidth disabled={loading}>
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
            <Typography variant="h6">{counts.enterprises}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1">Models</Typography>
            <Typography variant="h6">{counts.models}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle1">Envios</Typography>
            <Typography variant="h6">{counts.sendings}</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
