import { createTheme } from '@mui/material/styles'

export const createAppTheme = (mode) =>
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
  })
