import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
  IconButton
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import apiClient from '../config/axios';
import { API_CONFIG } from '../config/api';

interface AliasTeam {
  id: number;
  team_id: number;
  team_name: string;
  alias: string;
  language: string;
}

const AliasTeamList: React.FC = () => {
  const [aliases, setAliases] = useState<AliasTeam[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info' as 'success' | 'error' | 'info' | 'warning'
  });

  const fetchAliases = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.ALIASES);
      setAliases(response.data);
      setError(null);
    } catch (err) {
      setError('Ошибка при загрузке алиасов команд');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAliases();
  }, []);

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот алиас?')) {
      try {
        await apiClient.delete(`${API_CONFIG.ENDPOINTS.ALIASES}/${id}`);
        setSnackbar({
          open: true,
          message: 'Алиас успешно удален',
          severity: 'success'
        });
        fetchAliases();
      } catch (error) {
        setSnackbar({
          open: true,
          message: 'Ошибка при удалении алиаса',
          severity: 'error'
        });
      }
    }
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Команда</TableCell>
            <TableCell>Алиас</TableCell>
            <TableCell>Язык</TableCell>
            <TableCell>Действия</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {loading ? (
            <TableRow>
              <TableCell colSpan={4} align="center">
                <CircularProgress />
              </TableCell>
            </TableRow>
          ) : error ? (
            <TableRow>
              <TableCell colSpan={4} align="center">
                <Alert severity="error">{error}</Alert>
              </TableCell>
            </TableRow>
          ) : aliases.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} align="center">
                <Typography variant="body2" color="textSecondary">
                  Нет доступных алиасов
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            aliases.map((alias) => (
              <TableRow key={alias.id}>
                <TableCell>{alias.team_name}</TableCell>
                <TableCell>{alias.alias}</TableCell>
                <TableCell>{alias.language}</TableCell>
                <TableCell>
                  <IconButton
                    onClick={() => handleDelete(alias.id)}
                    color="error"
                    size="small"
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      {snackbar.open && (
        <Alert
          severity={snackbar.severity}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          sx={{ mt: 2 }}
        >
          {snackbar.message}
        </Alert>
      )}
    </TableContainer>
  );
};

export default AliasTeamList; 