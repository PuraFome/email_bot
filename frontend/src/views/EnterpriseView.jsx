import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import TextField from '@mui/material/TextField'
import FormControlLabel from '@mui/material/FormControlLabel'
import Switch from '@mui/material/Switch'
import Button from '@mui/material/Button'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import IconButton from '@mui/material/IconButton'
import DeleteIcon from '@mui/icons-material/Delete'

export default function EnterpriseView({ enterpriseForm, setEnterpriseForm, enterprises, loading, onCreate, onDelete }) {
  return (
    <Box>
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
            <Button variant="contained" color="primary" onClick={onCreate} disabled={loading}>
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
                  <IconButton color="error" onClick={() => onDelete(item.enterprise_meling_id)}>
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
}
