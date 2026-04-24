import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'

export default function EmailReturnsView({ emailReturns }) {
  return (
    <Box>
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
}
