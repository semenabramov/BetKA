import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Typography,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

interface AliasTeam {
  id: number;
  team_id: number;
  team_name: string;
  alias: string;
  language: string;
}

const AliasTeamList: React.FC = () => {
  const [aliases, setAliases] = useState<AliasTeam[]>([]);

  const fetchAliases = async () => {
    try {
      const response = await axios.get('/api/teams/aliases');
      setAliases(response.data);
    } catch (error) {
      console.error('Error fetching aliases:', error);
    }
  };

  useEffect(() => {
    fetchAliases();
  }, []);

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот алиас?')) {
      try {
        await axios.delete(`/api/teams/aliases/${id}`);
        fetchAliases();
      } catch (error) {
        console.error('Error deleting alias:', error);
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
          {aliases.map((alias) => (
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
          ))}
          {aliases.length === 0 && (
            <TableRow>
              <TableCell colSpan={4} align="center">
                <Typography variant="body2" color="textSecondary">
                  Нет доступных алиасов
                </Typography>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default AliasTeamList; 