import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Alert,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  Divider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';

interface TeamAliasesProps {
  open: boolean;
  onClose: () => void;
}

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

const TeamAliases: React.FC<TeamAliasesProps> = ({ open, onClose }) => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<number | ''>('');
  const [newAlias, setNewAlias] = useState<string>('');
  const [language, setLanguage] = useState<string>('ru');
  const [aliases, setAliases] = useState<Alias[]>([]);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (open) {
      fetchTeams();
    }
  }, [open]);

  useEffect(() => {
    if (selectedTeam) {
      fetchAliases(selectedTeam);
    } else {
      setAliases([]);
    }
  }, [selectedTeam]);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/teams');
      setTeams(response.data.data || []);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Ошибка при загрузке списка команд' 
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchAliases = async (teamId: number) => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/teams/${teamId}/aliases`);
      setAliases(response.data.data || []);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Ошибка при загрузке альтернативных названий' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddAlias = async () => {
    if (!selectedTeam || !newAlias.trim()) return;
    
    try {
      setLoading(true);
      await axios.post(`http://localhost:5000/api/teams/${selectedTeam}/aliases`, {
        alias: newAlias.trim(),
        language: language
      });
      
      setNewAlias('');
      fetchAliases(selectedTeam);
      setMessage({ type: 'success', text: 'Альтернативное название добавлено' });
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Ошибка при добавлении альтернативного названия' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAlias = async (aliasId: number) => {
    try {
      setLoading(true);
      await axios.delete(`http://localhost:5000/api/teams/aliases/${aliasId}`);
      if (typeof selectedTeam === 'number') {
        fetchAliases(selectedTeam);
      }
      setMessage({ type: 'success', text: 'Альтернативное название удалено' });
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Ошибка при удалении альтернативного названия' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setSelectedTeam('');
    setNewAlias('');
    setLanguage('ru');
    setAliases([]);
    setMessage(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Управление альтернативными названиями команд</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Выберите команду</InputLabel>
            <Select
              value={selectedTeam}
              onChange={(e) => setSelectedTeam(e.target.value as number)}
              label="Выберите команду"
            >
              {teams.map((team) => (
                <MenuItem key={team.id} value={team.id}>
                  {team.name} ({team.league})
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {selectedTeam && (
            <>
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={8}>
                  <TextField
                    fullWidth
                    label="Новое альтернативное название"
                    value={newAlias}
                    onChange={(e) => setNewAlias(e.target.value)}
                    margin="normal"
                    size="small"
                  />
                </Grid>
                <Grid item xs={3}>
                  <FormControl fullWidth margin="normal">
                    <InputLabel>Язык</InputLabel>
                    <Select
                      value={language}
                      onChange={(e) => setLanguage(e.target.value as string)}
                      label="Язык"
                      size="small"
                    >
                      <MenuItem value="ru">Русский</MenuItem>
                      <MenuItem value="en">English</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={1} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <IconButton 
                    color="primary" 
                    onClick={handleAddAlias}
                    disabled={!newAlias.trim() || loading}
                  >
                    <AddIcon />
                  </IconButton>
                </Grid>
              </Grid>

              <Typography variant="subtitle1" sx={{ mb: 1 }}>
                Существующие альтернативные названия:
              </Typography>

              <List>
                {aliases.map((alias) => (
                  <React.Fragment key={alias.id}>
                    <ListItem>
                      <ListItemText 
                        primary={alias.alias} 
                        secondary={`Язык: ${alias.language === 'ru' ? 'Русский' : 'English'}`}
                      />
                      <ListItemSecondaryAction>
                        <IconButton 
                          edge="end" 
                          onClick={() => handleDeleteAlias(alias.id)}
                          disabled={loading}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
                {aliases.length === 0 && (
                  <ListItem>
                    <ListItemText primary="Нет альтернативных названий" />
                  </ListItem>
                )}
              </List>
            </>
          )}

          {message && (
            <Alert severity={message.type} sx={{ mt: 2 }}>
              {message.text}
            </Alert>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Закрыть</Button>
      </DialogActions>
    </Dialog>
  );
};

export default TeamAliases; 