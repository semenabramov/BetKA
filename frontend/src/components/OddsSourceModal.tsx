import React, { useState, useEffect } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    Grid,
    FormControlLabel,
    Switch
} from '@mui/material';
import { OddsSource } from '../types/oddsSource';

interface OddsSourceModalProps {
    open: boolean;
    onClose: () => void;
    onSave: (source: OddsSource) => void;
    source?: OddsSource | null;
}

const OddsSourceModal: React.FC<OddsSourceModalProps> = ({ open, onClose, onSave, source }) => {
    const [formData, setFormData] = useState<OddsSource>({
        name: '',
        url: '',
        premier_league_url: '',
        championship_url: '',
        league_one_url: '',
        league_two_url: '',
        bundesliga_one_url: '',
        bundesliga_two_url: '',
        liga_url: '',
        la_liga_url: '',
        serie_a_url: '',
        ligue_one_url: '',
        is_active: true
    });

    useEffect(() => {
        if (source) {
            setFormData(source);
        } else {
            setFormData({
                name: '',
                url: '',
                premier_league_url: '',
                championship_url: '',
                league_one_url: '',
                league_two_url: '',
                bundesliga_one_url: '',
                bundesliga_two_url: '',
                liga_url: '',
                la_liga_url: '',
                serie_a_url: '',
                ligue_one_url: '',
                is_active: true
            });
        }
    }, [source]);

    const handleChange = (field: keyof OddsSource) => (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({
            ...prev,
            [field]: event.target.value
        }));
    };

    const handleSwitchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({
            ...prev,
            is_active: event.target.checked
        }));
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        onSave(formData);
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <form onSubmit={handleSubmit}>
                <DialogTitle>
                    {source ? 'Редактировать источник' : 'Добавить источник'}
                </DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Название"
                                value={formData.name}
                                onChange={handleChange('name')}
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="URL"
                                value={formData.url}
                                onChange={handleChange('url')}
                                required
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Премьер-лиги"
                                value={formData.premier_league_url}
                                onChange={handleChange('premier_league_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Чемпионшипа"
                                value={formData.championship_url}
                                onChange={handleChange('championship_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Лиги 1"
                                value={formData.league_one_url}
                                onChange={handleChange('league_one_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Лиги 2"
                                value={formData.league_two_url}
                                onChange={handleChange('league_two_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Бундеслиги 1"
                                value={formData.bundesliga_one_url}
                                onChange={handleChange('bundesliga_one_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Бундеслиги 2"
                                value={formData.bundesliga_two_url}
                                onChange={handleChange('bundesliga_two_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Лиги"
                                value={formData.liga_url}
                                onChange={handleChange('liga_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Ла Лиги"
                                value={formData.la_liga_url}
                                onChange={handleChange('la_liga_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Серии А"
                                value={formData.serie_a_url}
                                onChange={handleChange('serie_a_url')}
                            />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField
                                fullWidth
                                label="URL Лиги 1"
                                value={formData.ligue_one_url}
                                onChange={handleChange('ligue_one_url')}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={formData.is_active}
                                        onChange={handleSwitchChange}
                                        color="primary"
                                    />
                                }
                                label="Активен"
                            />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onClose}>Отмена</Button>
                    <Button type="submit" variant="contained" color="primary">
                        {source ? 'Сохранить' : 'Добавить'}
                    </Button>
                </DialogActions>
            </form>
        </Dialog>
    );
};

export default OddsSourceModal; 