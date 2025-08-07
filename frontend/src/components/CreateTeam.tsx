import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Alert,
  Box
} from '@mui/material';
import apiClient from '../config/axios';
import { API_CONFIG } from '../config/api';

interface CreateTeamProps {
  open: boolean;
  onClose: () => void;
}

interface TeamData {
  name: string;
  league: string;
}

interface Message {
  type: 'success' | 'error';
  text: string;
}

const CreateTeam: React.FC<CreateTeamProps> = ({ open, onClose }) => {
  const [teamData, setTeamData] = useState<TeamData>({
    name: '',
    league: 'Premier League'
  });
  const [message, setMessage] = useState<Message | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTeamData({
      ...teamData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    try {
      const requestData = {
        name: teamData.name,
        league: teamData.league
      };
      
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.TEAMS, requestData);
      
      setMessage({ type: 'success', text: 'Команда успешно создана' });
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      setMessage({ type: 'error', text: 'Ошибка при создании команды' });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Создать новую команду</DialogTitle>
      <DialogContent>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          <TextField
            fullWidth
            label="Название команды"
            name="name"
            value={teamData.name}
            onChange={handleChange}
            required
            margin="normal"
          />
          <TextField
            fullWidth
            label="Лига"
            name="league"
            value={teamData.league}
            onChange={handleChange}
            required
            margin="normal"
          />
          
          {message && (
            <Alert severity={message.type} sx={{ mt: 2 }}>
              {message.text}
            </Alert>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Отмена</Button>
        <Button onClick={handleSubmit} variant="contained" color="primary">
          Создать команду
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreateTeam; 