import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { 
  Container, 
  Typography, 
  Button, 
  Box, 
  Paper,
  CircularProgress,
  Tooltip,
  Tabs,
  Tab,
  Divider,
  Chip,
  Alert,
  Snackbar,
  TextField,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent
} from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import RefreshIcon from '@mui/icons-material/Refresh'
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer'
import AccessTimeIcon from '@mui/icons-material/AccessTime'
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents'
import CompareArrowsIcon from '@mui/icons-material/CompareArrows'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import DownloadIcon from '@mui/icons-material/Download'

interface MatchData {
  id: number;
  date: string;
  time: string;
  home: string;
  away: string;
  home_percent: number;
  draw_percent: number;
  away_percent: number;
  recommended_score: string;
  home_odds: string | null;
  draw_odds: string | null;
  away_odds: string | null;
  source: string;
}

interface PredictionData {
  id: number;
  home: string;
  away: string;
  outcome: string;
  odds: number;
  confidence: number;
  value_bet: number;
  bet_amount: number;
  bankroll_after_bet: number;
  possible_profit: number;
}

// Список доступных стран
const COUNTRIES = [
  { code: 'all', name: 'Все страны' },
  { code: 'england', name: 'Англия' },
  { code: 'spain', name: 'Испания' },
  { code: 'germany', name: 'Германия' },
  { code: 'italy', name: 'Италия' },
  { code: 'france', name: 'Франция' }
];

// Функция для определения цвета на основе процента
const getPercentColor = (percent: number) => {
  if (percent >= 70) return '#4caf50'; // Зеленый
  if (percent >= 50) return '#ff9800'; // Оранжевый
  return '#f44336'; // Красный
}

// Колонки для данных с thepunterspage
const punterspageColumns: GridColDef[] = [
  { 
    field: 'date', 
    headerName: 'Дата', 
    flex: 1,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <AccessTimeIcon sx={{ mr: 1, fontSize: '1rem' }} />
        {params.value}
      </Box>
    )
  },
  { 
    field: 'time', 
    headerName: 'Время', 
    flex: 1 
  },
  { 
    field: 'home', 
    headerName: 'Домашняя команда', 
    flex: 1.5,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'away', 
    headerName: 'Гостевая команда', 
    flex: 1.5,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'home_percent', 
    headerName: 'Вероятность победы хозяев', 
    flex: 1,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="body2" fontWeight="bold">
          {params.value}%
        </Typography>
        {params.row.home_odds && (
          <Typography variant="caption" color="text.secondary">
            Winline: {params.row.home_odds}
          </Typography>
        )}
      </Box>
    )
  },
  { 
    field: 'draw_percent', 
    headerName: 'Вероятность ничьей', 
    flex: 1,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="body2" fontWeight="bold">
          {params.value}%
        </Typography>
        {params.row.draw_odds && (
          <Typography variant="caption" color="text.secondary">
            Winline: {params.row.draw_odds}
          </Typography>
        )}
      </Box>
    )
  },
  { 
    field: 'away_percent', 
    headerName: 'Вероятность победы гостей', 
    flex: 1,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="body2" fontWeight="bold">
          {params.value}%
        </Typography>
        {params.row.away_odds && (
          <Typography variant="caption" color="text.secondary">
            Winline: {params.row.away_odds}
          </Typography>
        )}
      </Box>
    )
  },
  { 
    field: 'recommended_score', 
    headerName: 'Прогноз счета', 
    flex: 1,
    renderCell: (params) => (
      <Tooltip title="Рекомендуемый счет">
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <EmojiEventsIcon color="primary" />
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      </Tooltip>
    )
  }
]

// Колонки для данных с Winline
const winlineColumns: GridColDef[] = [
  { 
    field: 'date', 
    headerName: 'Дата', 
    flex: 1,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <AccessTimeIcon sx={{ mr: 1, fontSize: '1rem' }} />
        {params.value}
      </Box>
    )
  },
  { 
    field: 'time', 
    headerName: 'Время', 
    flex: 1 
  },
  { 
    field: 'home', 
    headerName: 'Домашняя команда', 
    flex: 1.5,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'away', 
    headerName: 'Гостевая команда', 
    flex: 1.5,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'home_odds', 
    headerName: 'Коэф. победы хозяев', 
    flex: 1,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'draw_odds', 
    headerName: 'Коэф. ничьей', 
    flex: 1,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'away_odds', 
    headerName: 'Коэф. победы гостей', 
    flex: 1,
    renderCell: (params) => (
      <Typography variant="body2" fontWeight="bold">
        {params.value}
      </Typography>
    )
  },
  { 
    field: 'home_percent', 
    headerName: 'Вероятность победы хозяев', 
    flex: 1,
    renderCell: (params) => (
      <Typography 
        variant="body2" 
        sx={{ 
          color: getPercentColor(params.value),
          fontWeight: 'bold'
        }}
      >
        {params.value}%
      </Typography>
    )
  },
  { 
    field: 'draw_percent', 
    headerName: 'Вероятность ничьей', 
    flex: 1,
    renderCell: (params) => (
      <Typography 
        variant="body2" 
        sx={{ 
          color: getPercentColor(params.value),
          fontWeight: 'bold'
        }}
      >
        {params.value}%
      </Typography>
    )
  },
  { 
    field: 'away_percent', 
    headerName: 'Вероятность победы гостей', 
    flex: 1,
    renderCell: (params) => (
      <Typography 
        variant="body2" 
        sx={{ 
          color: getPercentColor(params.value),
          fontWeight: 'bold'
        }}
      >
        {params.value}%
      </Typography>
    )
  }
]

function App() {
  const [matches, setMatches] = useState<MatchData[]>([])
  const [predictions, setPredictions] = useState<PredictionData[]>([])
  const [loading, setLoading] = useState(false)
  const [tabValue, setTabValue] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error'}>({
    open: false,
    message: '',
    severity: 'success'
  })
  const [selectedCountry, setSelectedCountry] = useState('all')

  // Параметры для расчета ставок
  const [initialBankroll, setInitialBankroll] = useState<number>(10000)
  const [fraction, setFraction] = useState<number>(2)
  const [minBankroll, setMinBankroll] = useState<number>(100)

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get('http://localhost:5000/api/matches', {
        params: {
          initial_bankroll: initialBankroll,
          fraction: fraction,
          min_bankroll: minBankroll,
          country: selectedCountry
        }
      })
      const data = await response.data
      
      // Добавляем id для каждой записи
      const matchesWithIds = data.matches.map((match: MatchData, index: number) => ({
        ...match,
        id: index + 1,
      }))
      
      const predictionsWithIds = data.predictions.map((prediction: PredictionData, index: number) => ({
        ...prediction,
        id: index + 1,
      }))
      
      setMatches(matchesWithIds)
      setPredictions(predictionsWithIds)
    } catch (err) {
      setError('Ошибка при загрузке данных')
      console.error('Error fetching data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue)
  }

  const handleUpdateWinline = async () => {
    setLoading(true)
    try {
      const response = await axios.post('http://localhost:5000/api/update-winline', { country: selectedCountry })
      const data = await response.data
      
      if (data.status === 'success') {
        setSnackbar({
          open: true,
          message: 'Данные Winline успешно обновлены',
          severity: 'success'
        })
        // Обновляем данные после успешного обновления Winline
        await fetchData()
      } else {
        throw new Error(data.message)
      }
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Ошибка при обновлении данных Winline',
        severity: 'error'
      })
      console.error('Error updating Winline data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false })
  }

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    const numValue = parseFloat(value)
    
    if (!isNaN(numValue)) {
      switch (name) {
        case 'initialBankroll':
          setInitialBankroll(numValue)
          break
        case 'fraction':
          setFraction(numValue)
          break
        case 'minBankroll':
          setMinBankroll(numValue)
          break
      }
    }
  }

  const handleCountryChange = (event: SelectChangeEvent) => {
    setSelectedCountry(event.target.value)
  }

  const handleExportExcel = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/export-excel?country=${selectedCountry}`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `matches_${selectedCountry}_${new Date().toISOString().slice(0,19).replace(/[:-]/g, '')}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting to Excel:', error)
    }
  }

  const handleExportPredictionsExcel = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/export-predictions-excel?country=${selectedCountry}`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `predictions_${selectedCountry}_${new Date().toISOString().slice(0,19).replace(/[:-]/g, '')}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exporting predictions to Excel:', error)
    }
  }

  const matchColumns: GridColDef[] = [
    { field: 'date', headerName: 'Дата', width: 100 },
    { field: 'time', headerName: 'Время', width: 100 },
    {
      field: 'match',
      headerName: 'Матч',
      width: 300,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="body2">{params.row.home}</Typography>
          <Typography variant="body2" color="text.secondary">vs</Typography>
          <Typography variant="body2">{params.row.away}</Typography>
        </Box>
      ),
    },
    {
      field: 'home_percent',
      headerName: 'Победа хозяев',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography variant="body2" fontWeight="bold">
            {params.row.home_percent}%
          </Typography>
          {params.row.home_odds && (
            <Typography variant="caption" color="text.secondary">
              Winline: {params.row.home_odds}
            </Typography>
          )}
        </Box>
      ),
    },
    {
      field: 'draw_percent',
      headerName: 'Ничья',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography variant="body2" fontWeight="bold">
            {params.row.draw_percent}%
          </Typography>
          {params.row.draw_odds && (
            <Typography variant="caption" color="text.secondary">
              Winline: {params.row.draw_odds}
            </Typography>
          )}
        </Box>
      ),
    },
    {
      field: 'away_percent',
      headerName: 'Победа гостей',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography variant="body2" fontWeight="bold">
            {params.row.away_percent}%
          </Typography>
          {params.row.away_odds && (
            <Typography variant="caption" color="text.secondary">
              Winline: {params.row.away_odds}
            </Typography>
          )}
        </Box>
      ),
    },
    {
      field: 'recommended_score',
      headerName: 'Рекомендуемый счет',
      width: 150,
      renderCell: (params) => (
        <Tooltip title="Рекомендуемый счет">
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <EmojiEventsIcon color="primary" />
            <Typography variant="body2">{params.row.recommended_score}</Typography>
          </Box>
        </Tooltip>
      ),
    },
  ]

  const predictionColumns: GridColDef[] = [
    {
      field: 'match',
      headerName: 'Матч',
      width: 300,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="body2">{params.row.home}</Typography>
          <Typography variant="body2" color="text.secondary">vs</Typography>
          <Typography variant="body2">{params.row.away}</Typography>
        </Box>
      ),
    },
    {
      field: 'outcome',
      headerName: 'Исход',
      width: 150,
      renderCell: (params) => {
        let outcomeText = ''
        let color = ''
        
        switch (params.value) {
          case 'home':
            outcomeText = 'Победа хозяев'
            color = '#4caf50'
            break
          case 'draw':
            outcomeText = 'Ничья'
            color = '#ff9800'
            break
          case 'away':
            outcomeText = 'Победа гостей'
            color = '#f44336'
            break
          default:
            outcomeText = params.value
        }
        
        return (
          <Chip 
            label={outcomeText} 
            sx={{ 
              backgroundColor: color, 
              color: 'white',
              fontWeight: 'bold'
            }} 
          />
        )
      },
    },
    { 
      field: 'odds', 
      headerName: 'Коэффициент', 
      width: 120,
      renderCell: (params) => (
        <Typography variant="body2" fontWeight="bold">
          {params.value.toFixed(2)}
        </Typography>
      ),
    },
    { 
      field: 'confidence', 
      headerName: 'Уверенность', 
      width: 120,
      renderCell: (params) => (
        <Typography variant="body2" fontWeight="bold">
          {(params.value * 100).toFixed(0)}%
        </Typography>
      ),
    },
    { 
      field: 'value_bet', 
      headerName: 'Value Bet', 
      width: 120,
      renderCell: (params) => (
        <Typography variant="body2" fontWeight="bold">
          {params.value.toFixed(2)}
        </Typography>
      ),
    },
    { 
      field: 'bet_amount', 
      headerName: 'Сумма ставки', 
      width: 150,
      renderCell: (params) => (
        <Typography variant="body2" fontWeight="bold">
          {params.value.toFixed(2)} ₽
        </Typography>
      ),
    },
    { 
      field: 'possible_profit', 
      headerName: 'Возможный выигрыш', 
      width: 180,
      renderCell: (params) => (
        <Typography variant="body2" fontWeight="bold" color="success.main">
          {params.value.toFixed(2)} ₽
        </Typography>
      ),
    },
  ]

  useEffect(() => {
    fetchData()
  }, [selectedCountry])

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Прогнозы матчей Премьер-лиги
        </Typography>

        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={8}>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <TextField
                label="Начальный банк"
                type="number"
                name="initialBankroll"
                value={initialBankroll}
                onChange={handleInputChange}
                size="small"
                sx={{ width: 150 }}
              />
              <TextField
                label="Коэффициент Келли"
                type="number"
                name="fraction"
                value={fraction}
                onChange={handleInputChange}
                size="small"
                sx={{ width: 150 }}
              />
              <TextField
                label="Минимальный банк"
                type="number"
                name="minBankroll"
                value={minBankroll}
                onChange={handleInputChange}
                size="small"
                sx={{ width: 150 }}
              />
              <FormControl sx={{ minWidth: 200 }}>
                <InputLabel id="country-select-label">Страна</InputLabel>
                <Select
                  labelId="country-select-label"
                  value={selectedCountry}
                  label="Страна"
                  size="small"
                  onChange={handleCountryChange}
                >
                  {COUNTRIES.map((country) => (
                    <MenuItem key={country.code} value={country.code}>
                      {country.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <Button
                variant="contained"
                onClick={fetchData}
                disabled={loading}
              >
                Загрузить данные
              </Button>
            </Box>
          </Grid>
          <Grid item xs={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              color="secondary"
              onClick={handleUpdateWinline}
              disabled={loading}
              startIcon={<RefreshIcon />}
            >
              Обновить данные Winline
            </Button>
          </Grid>
        </Grid>
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        <Box sx={{ mb: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="таблицы данных">
            <Tab icon={<SportsSoccerIcon />} label="Матчи" />
            <Tab icon={<TrendingUpIcon />} label="Предсказания" />
          </Tabs>
          <Divider sx={{ my: 1 }} />
        </Box>
        
        {tabValue === 0 && (
          <Paper elevation={3} sx={{ width: '100%' }}>
            <DataGrid
              rows={matches}
              columns={matchColumns}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 25 },
                },
              }}
              pageSizeOptions={[25, 50, 100]}
              disableRowSelectionOnClick
              loading={loading}
              components={{
                LoadingOverlay: () => (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <CircularProgress />
                  </Box>
                ),
              }}
              paginationMode="client"
              pagination
              autoHeight
            />
          </Paper>
        )}
        
        {tabValue === 1 && (
          <Paper elevation={3} sx={{ width: '100%' }}>
            <DataGrid
              rows={predictions}
              columns={predictionColumns}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 25 },
                },
              }}
              pageSizeOptions={[25, 50, 100]}
              disableRowSelectionOnClick
              loading={loading}
              sx={{
                '& .MuiDataGrid-cell': {
                  borderColor: 'divider',
                },
                '& .MuiDataGrid-columnHeaders': {
                  backgroundColor: 'background.paper',
                }
              }}
              paginationMode="client"
              pagination
              autoHeight
            />
          </Paper>
        )}

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
        >
          <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
            {snackbar.message}
          </Alert>
        </Snackbar>

        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="outlined"
            onClick={handleExportExcel}
            startIcon={<DownloadIcon />}
          >
            Выгрузить матчи в Excel
          </Button>
          <Button
            variant="outlined"
            onClick={handleExportPredictionsExcel}
            startIcon={<DownloadIcon />}
          >
            Выгрузить предсказания в Excel
          </Button>
        </Box>
      </Box>
    </Container>
  )
}

export default App 