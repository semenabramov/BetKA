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
  IconButton,
  Tooltip,
  Alert
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

interface Alias {
  id: number;
  team_id: number;
  alias: string;
  language: string;
}

interface Team {
  id: number;
  name: string;
  league: string;
  aliases: Alias[];
}

const TeamsList: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const response = await axios.get('/api/teams');
        setTeams(response.data.data);
        setLoading(false);
      } catch (err) {
        setError('Ошибка при загрузке команд');
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  const handleDeleteTeam = async (teamId: number) => {
    if (window.confirm('Вы уверены, что хотите удалить эту команду?')) {
      try {
        await axios.delete(`/api/teams/${teamId}`);
        setTeams(teams.filter(team => team.id !== teamId));
        setMessage({ type: 'success', text: 'Команда успешно удалена' });
      } catch (err) {
        setMessage({ type: 'error', text: 'Ошибка при удалении команды' });
      }
    }
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
      {message && (
        <Alert severity={message.type} sx={{ mb: 2 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Название</TableCell>
              <TableCell>Лига</TableCell>
              <TableCell>Альтернативные названия</TableCell>
              <TableCell align="center">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teams.map((team) => (
              <TableRow key={team.id}>
                <TableCell>{team.name}</TableCell>
                <TableCell>{team.league}</TableCell>
                <TableCell>
                  {team.aliases && team.aliases.length > 0 ? (
                    <Box>
                      {team.aliases.map((alias) => (
                        <Box key={alias.id} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Typography 
                            variant="body2" 
                            sx={{ 
                              backgroundColor: alias.language === 'ru' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(46, 125, 50, 0.1)',
                              padding: '2px 8px',
                              borderRadius: '4px',
                              display: 'inline-block'
                            }}
                          >
                            {alias.alias}
                          </Typography>
                        </Box>
                      ))}
                    </Box>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      Нет альтернативных названий
                    </Typography>
                  )}
                </TableCell>
                <TableCell align="center">
                  <Tooltip title="Удалить команду">
                    <IconButton onClick={() => handleDeleteTeam(team.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {teams.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  <Typography variant="body1" sx={{ py: 2 }}>
                    Нет доступных команд
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default TeamsList; 