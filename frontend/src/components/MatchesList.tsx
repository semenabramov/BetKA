import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  CircularProgress,
  Button,
  Alert,
  Snackbar,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Divider,
  ButtonGroup
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import axios from 'axios';

interface Match {
  id: number;
  date: string;
  team_home: number;
  team_away: number;
  home_team_name: string;
  away_team_name: string;
  bookmaker_odds: Array<{
    bookmaker_id: number;
    bookmaker_name?: string;
    odds_home: number;
    odds_away: number;
    odds_draw: number;
  }>;
  source_odds: Array<{
    sources_id: number;
    source_name?: string;
    odds_home: number;
    odds_away: number;
    odds_draw: number;
  }>;
}

const MatchesList: React.FC = () => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updateLoading, setUpdateLoading] = useState(false);
  const [parseLoading, setParseLoading] = useState(false);
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error';
  }>({
    open: false,
    message: '',
    severity: 'success'
  });
  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean;
    matchId: number | null;
    matchInfo: string;
  }>({
    open: false,
    matchId: null,
    matchInfo: ''
  });

  const fetchMatches = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/matches');
      setMatches(response.data);
      setError(null);
    } catch (err) {
      setError('Ошибка при загрузке матчей');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatches();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleUpdateMatches = async () => {
    try {
      setUpdateLoading(true);
      const response = await axios.post('/api/matches/update');
      
      setSnackbar({
        open: true,
        message: response.data.message,
        severity: response.data.status === 'success' ? 'success' : 'error'
      });
      
      if (response.data.status === 'success') {
        fetchMatches();
      }
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Ошибка при обновлении матчей',
        severity: 'error'
      });
      console.error(err);
    } finally {
      setUpdateLoading(false);
    }
  };

  const handleParseAllMatches = async () => {
    try {
      setParseLoading(true);
      const response = await axios.post('/api/matches/update-all');
      setSnackbar({
        open: true,
        message: response.data.message || 'Матчи успешно спарсены и объединены',
        severity: 'success'
      });
      await fetchMatches();
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Ошибка при парсинге и объединении матчей',
        severity: 'error'
      });
      console.error('Error parsing and merging matches:', err);
    } finally {
      setParseLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  const handleDeleteClick = (matchId: number, homeTeam: string, awayTeam: string, matchDate: string) => {
    setDeleteDialog({
      open: true,
      matchId,
      matchInfo: `${homeTeam} - ${awayTeam} (${formatDate(matchDate)})`
    });
  };

  const handleDeleteConfirm = async () => {
    if (!deleteDialog.matchId) return;
    
    try {
      const response = await axios.delete(`/api/matches/${deleteDialog.matchId}`);
      
      setSnackbar({
        open: true,
        message: response.data.message,
        severity: response.data.status === 'success' ? 'success' : 'error'
      });
      
      // Обновляем список матчей после успешного удаления
      if (response.data.status === 'success') {
        fetchMatches();
      }
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Ошибка при удалении матча',
        severity: 'error'
      });
      console.error(err);
    } finally {
      setDeleteDialog({ open: false, matchId: null, matchInfo: '' });
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialog({ open: false, matchId: null, matchInfo: '' });
  };

  const renderOddsCell = (match: Match, type: 'home' | 'draw' | 'away') => {
    const bookmakerOdds = match.bookmaker_odds || [];
    const sourceOdds = match.source_odds || [];
    
    const getOddsValue = (odds: any, type: 'home' | 'draw' | 'away') => {
      if (type === 'home') return odds.odds_home;
      if (type === 'draw') return odds.odds_draw;
      return odds.odds_away;
    };
    
    return (
      <Box>
        {sourceOdds.map((odd, index) => (
          <Box key={`source-${index}`} sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              {odd.source_name || `Источник ${odd.sources_id}`}:
            </Typography>
            <Typography component="span" sx={{ ml: 1 }}>
              {getOddsValue(odd, type).toFixed(2)}
            </Typography>
          </Box>
        ))}
        
        {bookmakerOdds.map((odd, index) => (
          <Box key={`bookmaker-${index}`} sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              {odd.bookmaker_name || `Букмекер ${odd.bookmaker_id}`}:
            </Typography>
            <Typography component="span" sx={{ ml: 1 }}>
              {getOddsValue(odd, type).toFixed(2)}
            </Typography>
          </Box>
        ))}
        
        {bookmakerOdds.length === 0 && sourceOdds.length === 0 && (
          <Typography variant="body2" color="text.secondary">
            Нет данных
          </Typography>
        )}
      </Box>
    );
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Матчи</Typography>
        <ButtonGroup variant="contained" color="primary">
          <Button
            startIcon={<DownloadIcon />}
            onClick={handleParseAllMatches}
            disabled={parseLoading}
          >
            {parseLoading ? 'Парсинг...' : 'Парсить матчи'}
          </Button>
          <Button
            startIcon={<RefreshIcon />}
            onClick={handleUpdateMatches}
            disabled={updateLoading}
          >
            {updateLoading ? 'Обновление...' : 'Обновить данные'}
          </Button>
        </ButtonGroup>
      </Box>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Дата</TableCell>
              <TableCell>Команды</TableCell>
              <TableCell align="center">П1</TableCell>
              <TableCell align="center">X</TableCell>
              <TableCell align="center">П2</TableCell>
              <TableCell align="center">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {matches.map((match) => (
              <TableRow key={match.id}>
                <TableCell>{formatDate(match.date)}</TableCell>
                <TableCell>{match.home_team_name} - {match.away_team_name}</TableCell>
                <TableCell>{renderOddsCell(match, 'home')}</TableCell>
                <TableCell>{renderOddsCell(match, 'draw')}</TableCell>
                <TableCell>{renderOddsCell(match, 'away')}</TableCell>
                <TableCell align="center">
                  <Tooltip title="Удалить матч">
                    <IconButton
                      color="error"
                      size="small"
                      onClick={() => handleDeleteClick(match.id, match.home_team_name, match.away_team_name, match.date)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {matches.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography variant="body1" sx={{ py: 2 }}>
                    Нет доступных матчей
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
      
      <Dialog
        open={deleteDialog.open}
        onClose={handleDeleteCancel}
      >
        <DialogTitle>Подтверждение удаления</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Вы уверены, что хотите удалить матч "{deleteDialog.matchInfo}"?
            Это действие нельзя отменить.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} color="primary">
            Отмена
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" autoFocus>
            Удалить
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MatchesList; 