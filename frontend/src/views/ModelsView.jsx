import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import IconButton from '@mui/material/IconButton'
import DeleteIcon from '@mui/icons-material/Delete'

export default function ModelsView({ modelForm, setModelForm, models, loading, onCreate, onDelete }) {
  return (
    <Box>
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
            <Button variant="contained" color="primary" onClick={onCreate} disabled={loading}>
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
                  <IconButton color="error" onClick={() => onDelete(item.model_id)}>
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
