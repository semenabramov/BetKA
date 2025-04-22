import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Grid,
  IconButton,
  Typography,
  Box,
  Alert
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';

interface BookmakerModalProps {
  open: boolean;
  onClose: () => void;
  bookmaker?: {
    id: number;
    name: string;
    url: string;
    premier_league_url?: string;
    championship_url?: string;
    league_one_url?: string;
    league_two_url?: string;
    bundesliga_one_url?: string;
    bundesliga_two_url?: string;
    liga_url?: string;
    la_liga_url?: string;
    serie_a_url?: string;
    ligue_one_url?: string;
  };
}

const BookmakerModal: React.FC<BookmakerModalProps> = ({ open, onClose, bookmaker }) => {
  const [formData, setFormData] = useState({
    name: '',
    premier_league_url: '',
    championship_url: '',
    league_one_url: '',
    league_two_url: '',
    bundesliga_one_url: '',
    bundesliga_two_url: '',
    liga_url: '',
    la_liga_url: '',
    serie_a_url: '',
    ligue_one_url: ''
  });
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    if (bookmaker) {
      setFormData({
        name: bookmaker.name,
        premier_league_url: bookmaker.premier_league_url || '',
        championship_url: bookmaker.championship_url || '',
        league_one_url: bookmaker.league_one_url || '',
        league_two_url: bookmaker.league_two_url || '',
        bundesliga_one_url: bookmaker.bundesliga_one_url || '',
        bundesliga_two_url: bookmaker.bundesliga_two_url || '',
        liga_url: bookmaker.liga_url || '',
        la_liga_url: bookmaker.la_liga_url || '',
        serie_a_url: bookmaker.serie_a_url || '',
        ligue_one_url: bookmaker.ligue_one_url || ''
      });
    }
  }, [bookmaker]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    try {
      if (bookmaker) {
        await axios.put(`http://localhost:5000/api/bookmakers/${bookmaker.id}`, formData);
      } else {
        await axios.post('http://localhost:5000/api/bookmakers', formData);
      }
      setMessage({ type: 'success', text: bookmaker ? 'Букмекер обновлен' : 'Букмекер добавлен' });
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      setMessage({ type: 'error', text: 'Произошла ошибка при сохранении' });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {bookmaker ? 'Редактировать букмекера' : 'Добавить букмекера'}
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{ position: 'absolute', right: 8, top: 8 }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Название"
                name="name"
                value={formData.name}
                onChange={handleChange}
                margin="normal"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>Ссылки на лиги:</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Premier League"
                name="premier_league_url"
                value={formData.premier_league_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Championship"
                name="championship_url"
                value={formData.championship_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="League One"
                name="league_one_url"
                value={formData.league_one_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="League Two"
                name="league_two_url"
                value={formData.league_two_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Bundesliga 1"
                name="bundesliga_one_url"
                value={formData.bundesliga_one_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Bundesliga 2"
                name="bundesliga_two_url"
                value={formData.bundesliga_two_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Liga"
                name="liga_url"
                value={formData.liga_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="La Liga"
                name="la_liga_url"
                value={formData.la_liga_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Serie A"
                name="serie_a_url"
                value={formData.serie_a_url}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Ligue 1"
                name="ligue_one_url"
                value={formData.ligue_one_url}
                onChange={handleChange}
              />
            </Grid>
          </Grid>
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
          {bookmaker ? 'Сохранить' : 'Добавить'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default BookmakerModal; 