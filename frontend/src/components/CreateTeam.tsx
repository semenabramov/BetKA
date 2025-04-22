import React, { useState } from 'react';
import axios from 'axios';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Alert,
  Box
} from '@mui/material';

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/teams', teamData);
      setMessage({ type: 'success', text: 'Команда успешно создана!' });
      setTeamData({ name: '', league: 'Premier League' });
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error instanceof Error ? error.message : 'Произошла ошибка при создании команды' 
      });
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