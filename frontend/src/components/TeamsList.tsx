import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Typography,
  Alert,
  Chip,
  Tooltip
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import InfoIcon from '@mui/icons-material/Info';

interface Team {
  id: number;
  name: string;
  league: string;
}

interface Alias {
  id: number;
  team_id: number;
  alias: string;
  language: string;
}

const TeamsList: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [aliases, setAliases] = useState<Record<number, Alias[]>>({});
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/teams');
      setTeams(response.data.data || []);
      
      // Загружаем альтернативные названия для каждой команды
      const aliasesData: Record<number, Alias[]> = {};
      for (const team of response.data.data) {
        try {
          const aliasResponse = await axios.get(`http://localhost:5000/api/teams/${team.id}/aliases`);
          aliasesData[team.id] = aliasResponse.data.data || [];
        } catch (error) {
          console.error(`Error fetching aliases for team ${team.id}:`, error);
          aliasesData[team.id] = [];
        }
      }
      setAliases(aliasesData);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Ошибка при загрузке списка команд' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTeam = async (teamId: number) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту команду? Это действие нельзя отменить.')) {
      return;
    }
    
    try {
      setLoading(true);
      await axios.delete(`http://localhost:5000/api/teams/${teamId}`);
      setMessage({ type: 'success', text: 'Команда успешно удалена' });
      fetchTeams(); // Обновляем список команд
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Ошибка при удалении команды' 
      });
    } finally {
      setLoading(false);
    }
  };

  const renderAliases = (teamId: number) => {
    const teamAliases = aliases[teamId] || [];
    if (teamAliases.length === 0) {
      return '-';
    }
    
    return (
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
        {teamAliases.map((alias) => (
          <Chip 
            key={alias.id} 
            label={alias.alias} 
            size="small" 
            color={alias.language === 'ru' ? 'primary' : 'secondary'}
            variant="outlined"
          />
        ))}
      </Box>
    );
  };

  return (
    <Box>
      {message && (
        <Alert severity={message.type} sx={{ mb: 2 }}>
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
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teams.map((team) => (
              <TableRow key={team.id}>
                <TableCell>{team.name}</TableCell>
                <TableCell>{team.league}</TableCell>
                <TableCell>{renderAliases(team.id)}</TableCell>
                <TableCell>
                  <Tooltip title="Удалить команду">
                    <IconButton 
                      color="error" 
                      onClick={() => handleDeleteTeam(team.id)}
                      disabled={loading}
                    >
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