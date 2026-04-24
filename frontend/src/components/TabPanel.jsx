import Box from '@mui/material/Box'

export default function TabPanel({ children, value, index }) {
  return value === index ? <Box sx={{ p: 3 }}>{children}</Box> : null
}
