import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
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
  Link
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import apiClient from '../config/axios';
import { API_CONFIG } from '../config/api';
import BookmakerModal from './BookmakerModal';

interface Bookmaker {
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
}

const BookmakersList: React.FC = () => {
  const [bookmakers, setBookmakers] = useState<Bookmaker[]>([]);
  const [selectedBookmaker, setSelectedBookmaker] = useState<Bookmaker | undefined>();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const fetchBookmakers = async () => {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.BOOKMAKERS);
      setBookmakers(response.data.data);
    } catch (error) {
      setMessage({ type: 'error', text: 'Ошибка при загрузке списка букмекеров' });
    }
  };

  useEffect(() => {
    fetchBookmakers();
  }, []);

  const handleOpenModal = (bookmaker?: Bookmaker) => {
    setSelectedBookmaker(bookmaker);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedBookmaker(undefined);
    setIsModalOpen(false);
    fetchBookmakers();
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этого букмекера?')) {
      try {
        await apiClient.delete(`${API_CONFIG.ENDPOINTS.BOOKMAKERS}/${id}`);
        setMessage({ type: 'success', text: 'Букмекер успешно удален' });
        fetchBookmakers();
      } catch (error) {
        setMessage({ type: 'error', text: 'Ошибка при удалении букмекера' });
      }
    }
  };

  const renderLeagueLink = (url: string | undefined) => {
    if (!url) return '-';
    return (
      <Link 
        href={url} 
        target="_blank" 
        rel="noopener noreferrer"
        sx={{ 
          textDecoration: 'none',
          '&:hover': {
            textDecoration: 'underline'
          }
        }}
      >
        Перейти
      </Link>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">Букмекеры</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenModal()}
        >
          Добавить букмекера
        </Button>
      </Box>

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
              <TableCell>Premier League</TableCell>
              <TableCell>Championship</TableCell>
              <TableCell>League One</TableCell>
              <TableCell>League Two</TableCell>
              <TableCell>Bundesliga 1</TableCell>
              <TableCell>Bundesliga 2</TableCell>
              <TableCell>Liga</TableCell>
              <TableCell>La Liga</TableCell>
              <TableCell>Serie A</TableCell>
              <TableCell>Ligue 1</TableCell>
              <TableCell>Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bookmakers.map((bookmaker) => (
              <TableRow key={bookmaker.id}>
                <TableCell>{bookmaker.name}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.premier_league_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.championship_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.league_one_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.league_two_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.bundesliga_one_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.bundesliga_two_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.liga_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.la_liga_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.serie_a_url)}</TableCell>
                <TableCell>{renderLeagueLink(bookmaker.ligue_one_url)}</TableCell>
                <TableCell>
                  <IconButton
                    color="primary"
                    onClick={() => handleOpenModal(bookmaker)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    color="error"
                    onClick={() => handleDelete(bookmaker.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <BookmakerModal
        open={isModalOpen}
        onClose={handleCloseModal}
        bookmaker={selectedBookmaker}
      />
    </Box>
  );
};

export default BookmakersList; 