import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'

export default function SendingsView({ sendings }) {
  return (
    <Box>
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
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}
