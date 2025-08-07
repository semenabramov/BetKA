import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  Alert
} from '@mui/material';
import axios from 'axios';

interface CreateSplitDialogProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  selectedMatches?: number[];
}

const CreateSplitDialog: React.FC<CreateSplitDialogProps> = ({ 
  open, 
  onClose, 
  onSuccess,
  selectedMatches = [] 
}) => {
  const [formData, setFormData] = useState({
    name: '',
    Kelly_value: '',
    Bank: '',
    min_bet: ''
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);

      // Валидация
      if (!formData.name) {
        throw new Error('Введите название сплита');
      }
      if (!formData.Kelly_value || isNaN(Number(formData.Kelly_value))) {
        throw new Error('Введите корректное значение критерия Келли');
      }
      if (!formData.Bank || isNaN(Number(formData.Bank))) {
        throw new Error('Введите корректный размер банка');
      }
      if (!formData.min_bet || isNaN(Number(formData.min_bet))) {
        throw new Error('Введите корректную минимальную ставку');
      }
      if (selectedMatches.length === 0) {
        throw new Error('Выберите хотя бы один матч');
      }

      const response = await axios.post('/api/splits', {
        ...formData,
        Kelly_value: Number(formData.Kelly_value),
        Bank: Number(formData.Bank),
        min_bet: Number(formData.min_bet),
        status: 'active',
        selected_matches: selectedMatches
      });

      if (response.data.status === 'success') {
        onSuccess();
        onClose();
        setFormData({
          name: '',
          Kelly_value: '',
          Bank: '',
          min_bet: ''
        });
      } else {
        throw new Error(response.data.message || 'Ошибка при создании сплита');
      }
    } catch (err: any) {
      setError(err.message || 'Произошла ошибка при создании сплита');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Создать новый сплит</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {selectedMatches.length === 0 && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              Выберите хотя бы один матч для создания сплита
            </Alert>
          )}
          <TextField
            name="name"
            label="Название сплита"
            value={formData.name}
            onChange={handleChange}
            fullWidth
            required
          />
          <TextField
            name="Kelly_value"
            label="Значение критерия Келли"
            type="number"
            value={formData.Kelly_value}
            onChange={handleChange}
            fullWidth
            required
            inputProps={{ step: "0.01" }}
          />
          <TextField
            name="Bank"
            label="Размер банка"
            type="number"
            value={formData.Bank}
            onChange={handleChange}
            fullWidth
            required
            inputProps={{ step: "0.01" }}
          />
          <TextField
            name="min_bet"
            label="Минимальная ставка"
            type="number"
            value={formData.min_bet}
            onChange={handleChange}
            fullWidth
            required
            inputProps={{ step: "0.01" }}
          />
          {error && (
            <Typography color="error" variant="body2">
              {error}
            </Typography>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Отмена
        </Button>
        <Button 
          onClick={handleSubmit} 
          variant="contained" 
          color="primary"
          disabled={loading || selectedMatches.length === 0}
        >
          {loading ? 'Создание...' : 'Создать'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreateSplitDialog; 