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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Divider,
  Chip
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import apiClient from '../config/axios';
import { API_CONFIG } from '../config/api';

interface Split {
  id: number;
  name: string;
  date: string;
  Kelly_value: number;
  Bank: number;
  min_bet: number;
  status: 'active' | 'completed' | 'archived';
}

const SplitsList: React.FC = () => {
  const [splits, setSplits] = useState<Split[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedSplit, setExpandedSplit] = useState<number | false>(false);

  const fetchSplits = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.SPLITS);
      console.log('Splits API Response:', response.data);
      // Проверяем структуру ответа
      const splitsData = response.data.data || response.data;
      console.log('Splits Data:', splitsData);
      setSplits(Array.isArray(splitsData) ? splitsData : []);
      setError(null);
    } catch (err) {
      setError('Ошибка при загрузке сплитов');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSplits();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'completed':
        return 'info';
      case 'archived':
        return 'default';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active':
        return 'Активный';
      case 'completed':
        return 'Завершен';
      case 'archived':
        return 'В архиве';
      default:
        return status;
    }
  };

  const handleAccordionChange = (splitId: number) => (event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedSplit(isExpanded ? splitId : false);
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Загрузка сплитов...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" component="h2" sx={{ mb: 3 }}>
        Сплиты
      </Typography>

      {!Array.isArray(splits) || splits.length === 0 ? (
        <Typography variant="body1" align="center" sx={{ py: 4 }}>
          Нет доступных сплитов
        </Typography>
      ) : (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {splits.map((split) => (
            <Accordion
              key={split.id}
              expanded={expandedSplit === split.id}
              onChange={handleAccordionChange(split.id)}
              sx={{
                '&:before': {
                  display: 'none',
                },
                boxShadow: 1,
                '&:hover': {
                  boxShadow: 3,
                },
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                sx={{
                  backgroundColor: expandedSplit === split.id ? 'rgba(0, 0, 0, 0.03)' : 'inherit',
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    {split.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(split.date).toLocaleDateString()}
                  </Typography>
                  <Chip
                    label={getStatusLabel(split.status)}
                    color={getStatusColor(split.status) as any}
                    size="small"
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Divider sx={{ mb: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Значение Келли
                    </Typography>
                    <Typography variant="body1">
                      {split.Kelly_value}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Размер банка
                    </Typography>
                    <Typography variant="body1">
                      {split.Bank}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Минимальная ставка
                    </Typography>
                    <Typography variant="body1">
                      {split.min_bet}
                    </Typography>
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      )}
    </Box>
  );
};

export default SplitsList; 