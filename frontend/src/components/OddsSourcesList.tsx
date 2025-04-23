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
    Link,
    Typography,
    Button
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { OddsSource } from '../types/oddsSource';
import OddsSourceModal from './OddsSourceModal';

interface OddsSourcesListProps {
    onEdit?: (source: OddsSource) => void;
    onDelete?: (id: number) => void;
}

const OddsSourcesList: React.FC<OddsSourcesListProps> = ({ onEdit, onDelete }) => {
    const [sources, setSources] = useState<OddsSource[]>([]);
    const [selectedSource, setSelectedSource] = useState<OddsSource | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchSources();
    }, []);

    const fetchSources = async () => {
        try {
            const response = await fetch('/api/odds-sources');
            if (!response.ok) {
                throw new Error('Failed to fetch sources');
            }
            const data = await response.json();
            setSources(data);
        } catch (error) {
            console.error('Error fetching sources:', error);
        }
    };

    const handleEdit = (source: OddsSource) => {
        setSelectedSource(source);
        setIsModalOpen(true);
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Вы уверены, что хотите удалить этот источник?')) {
            try {
                const response = await fetch(`/api/odds-sources/${id}`, {
                    method: 'DELETE',
                });
                if (!response.ok) {
                    throw new Error('Failed to delete source');
                }
                fetchSources();
                if (onDelete) {
                    onDelete(id);
                }
            } catch (error) {
                console.error('Error deleting source:', error);
            }
        }
    };

    const handleSave = async (source: OddsSource) => {
        try {
            const url = source.id ? `/api/odds-sources/${source.id}` : '/api/odds-sources';
            const method = source.id ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(source),
            });

            if (!response.ok) {
                throw new Error('Failed to save source');
            }

            fetchSources();
            setIsModalOpen(false);
            setSelectedSource(null);
        } catch (error) {
            console.error('Error saving source:', error);
        }
    };

    const handleAddNew = () => {
        setSelectedSource(null);
        setIsModalOpen(true);
    };

    const renderUrlLink = (url: string | undefined) => {
        if (!url) return null;
        return (
            <Link href={url} target="_blank" rel="noopener noreferrer">
                Открыть
            </Link>
        );
    };

    return (
        <>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <Typography variant="h5">Источники коэффициентов</Typography>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddIcon />}
                    onClick={handleAddNew}
                >
                    Добавить источник
                </Button>
            </div>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Действия</TableCell>
                            <TableCell>Название</TableCell>
                            <TableCell>URL</TableCell>
                            <TableCell>Премьер-лига</TableCell>
                            <TableCell>Чемпионшип</TableCell>
                            <TableCell>Лига 1</TableCell>
                            <TableCell>Лига 2</TableCell>
                            <TableCell>Бундеслига 1</TableCell>
                            <TableCell>Бундеслига 2</TableCell>
                            <TableCell>Лига</TableCell>
                            <TableCell>Ла Лига</TableCell>
                            <TableCell>Серия А</TableCell>
                            <TableCell>Лига 1</TableCell>
                            <TableCell>Активен</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sources.map((source) => (
                            <TableRow key={source.id}>
                                <TableCell>
                                    <IconButton onClick={() => handleEdit(source)}>
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton onClick={() => source.id && handleDelete(source.id)}>
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                                <TableCell>{source.name}</TableCell>
                                <TableCell>{renderUrlLink(source.url)}</TableCell>
                                <TableCell>{renderUrlLink(source.premier_league_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.championship_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.league_one_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.league_two_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.bundesliga_one_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.bundesliga_two_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.liga_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.la_liga_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.serie_a_url)}</TableCell>
                                <TableCell>{renderUrlLink(source.ligue_one_url)}</TableCell>
                                <TableCell>{source.is_active ? 'Да' : 'Нет'}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <OddsSourceModal
                open={isModalOpen}
                onClose={() => {
                    setIsModalOpen(false);
                    setSelectedSource(null);
                }}
                onSave={handleSave}
                source={selectedSource}
            />
        </>
    );
};

export default OddsSourcesList; 