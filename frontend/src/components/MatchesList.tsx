import React, { useState, useEffect } from "react";
import {
    Box,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
    CircularProgress,
    Button,
    Alert,
    Snackbar,
    IconButton,
    Tooltip,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogContentText,
    DialogActions,
    Divider,
    ButtonGroup,
    Checkbox,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import DeleteIcon from "@mui/icons-material/Delete";
import DownloadIcon from "@mui/icons-material/Download";
import CompareIcon from "@mui/icons-material/Compare";
import ScoreIcon from "@mui/icons-material/SportsSoccer";
import {
    Add as AddIcon,
    ShowChart as ShowChartIcon,
} from "@mui/icons-material";
import apiClient from "../config/axios";
import { API_CONFIG } from "../config/api";
import CreateSplitDialog from "./CreateSplitDialog";

interface Match {
    id: number;
    date: string;
    team_home: number;
    team_away: number;
    home_team_name: string;
    away_team_name: string;
    bookmaker_odds: Array<{
        bookmaker_id: number;
        bookmaker_name?: string;
        odds_home: number;
        odds_away: number;
        odds_draw: number;
    }>;
    source_odds: Array<{
        sources_id: number;
        source_name?: string;
        odds_home: number;
        odds_away: number;
        odds_draw: number;
    }>;
    match_score?: string; // Added for score display
}

const MatchesList: React.FC = () => {
    const [matches, setMatches] = useState<Match[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [updateLoading, setUpdateLoading] = useState(false);
    const [parseLoading, setParseLoading] = useState(false);
    const [updateScoresLoading, setUpdateScoresLoading] = useState(false);
    const [selectedMatches, setSelectedMatches] = useState<number[]>([]);
    const [snackbar, setSnackbar] = useState<{
        open: boolean;
        message: string;
        severity: "success" | "error" | "info" | "warning";
    }>({
        open: false,
        message: "",
        severity: "info",
    });
    const [deleteDialog, setDeleteDialog] = useState<{
        open: boolean;
        matchId: number | null;
        matchInfo: string;
    }>({
        open: false,
        matchId: null,
        matchInfo: "",
    });
    const [createSplitDialogOpen, setCreateSplitDialogOpen] = useState(false);

    const isMatchPast = (dateString: string) => {
        const matchDate = new Date(dateString);
        const now = new Date();
        return matchDate < now;
    };

    const fetchMatches = async () => {
        try {
            setLoading(true);
            const response = await apiClient.get(API_CONFIG.ENDPOINTS.MATCHES);
            setMatches(response.data);
            setError(null);
        } catch (err) {
            setError("Ошибка при загрузке матчей");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMatches();
    }, []);

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleString("ru-RU", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    const handleUpdateMatches = async () => {
        try {
            setUpdateLoading(true);
            const response = await apiClient.post(
                API_CONFIG.ENDPOINTS.UPDATE_MATCHES
            );

            setSnackbar({
                open: true,
                message: "Матчи успешно обновлены",
                severity: "success",
            });

            fetchMatches();
        } catch (error) {
            setSnackbar({
                open: true,
                message: "Ошибка при обновлении матчей",
                severity: "error",
            });
        } finally {
            setUpdateLoading(false);
        }
    };

    const handleParseAllMatches = async () => {
        try {
            setParseLoading(true);
            const response = await apiClient.post(
                API_CONFIG.ENDPOINTS.UPDATE_ALL
            );

            setSnackbar({
                open: true,
                message: "Все матчи успешно обновлены",
                severity: "success",
            });

            fetchMatches();
        } catch (error) {
            setSnackbar({
                open: true,
                message: "Ошибка при обновлении всех матчей",
                severity: "error",
            });
        } finally {
            setParseLoading(false);
        }
    };

    const handleUpdateAllScores = async () => {
        try {
            setUpdateScoresLoading(true);
            const response = await apiClient.post(
                API_CONFIG.ENDPOINTS.UPDATE_SCORES
            );

            setSnackbar({
                open: true,
                message: "Счета матчей успешно обновлены",
                severity: "success",
            });

            fetchMatches();
        } catch (error) {
            setSnackbar({
                open: true,
                message: "Ошибка при обновлении счетов матчей",
                severity: "error",
            });
        } finally {
            setUpdateScoresLoading(false);
        }
    };

    const handleCloseSnackbar = () => {
        setSnackbar((prev) => ({ ...prev, open: false }));
    };

    const handleDeleteClick = (
        matchId: number,
        homeTeam: string,
        awayTeam: string,
        matchDate: string
    ) => {
        setDeleteDialog({
            open: true,
            matchId,
            matchInfo: `${homeTeam} - ${awayTeam} (${formatDate(matchDate)})`,
        });
    };

    const handleDeleteConfirm = async () => {
        if (deleteDialog.matchId) {
            try {
                await apiClient.delete(
                    `${API_CONFIG.ENDPOINTS.MATCHES}/${deleteDialog.matchId}`
                );

                setSnackbar({
                    open: true,
                    message: "Матч успешно удален",
                    severity: "success",
                });

                fetchMatches();
            } catch (error) {
                setSnackbar({
                    open: true,
                    message: "Ошибка при удалении матча",
                    severity: "error",
                });
            }
        }
        setDeleteDialog({ open: false, matchId: null, matchInfo: "" });
    };

    const handleDeleteCancel = () => {
        setDeleteDialog({ open: false, matchId: null, matchInfo: "" });
    };

    const handleDownloadCSV = () => {
        // Создаем заголовки CSV
        const headers = [
            "ID",
            "Дата",
            "Домашняя команда",
            "Гостевая команда",
            "Счет",
            "Коэффициенты источников (П1)",
            "Коэффициенты источников (X)",
            "Коэффициенты источников (П2)",
            "Коэффициенты букмекеров (П1)",
            "Коэффициенты букмекеров (X)",
            "Коэффициенты букмекеров (П2)",
        ];

        // Создаем строки данных
        const csvRows = [headers.join(",")];

        matches.forEach((match) => {
            const sourceOddsHome =
                match.source_odds
                    ?.map(
                        (odd) =>
                            `${
                                odd.source_name || `Источник ${odd.sources_id}`
                            }: ${odd.odds_home.toFixed(2)}`
                    )
                    .join("; ") || "Нет данных";
            const sourceOddsDraw =
                match.source_odds
                    ?.map(
                        (odd) =>
                            `${
                                odd.source_name || `Источник ${odd.sources_id}`
                            }: ${odd.odds_draw.toFixed(2)}`
                    )
                    .join("; ") || "Нет данных";
            const sourceOddsAway =
                match.source_odds
                    ?.map(
                        (odd) =>
                            `${
                                odd.source_name || `Источник ${odd.sources_id}`
                            }: ${odd.odds_away.toFixed(2)}`
                    )
                    .join("; ") || "Нет данных";

            const bookmakerOddsHome =
                match.bookmaker_odds
                    ?.map(
                        (odd) =>
                            `${
                                odd.bookmaker_name ||
                                `Букмекер ${odd.bookmaker_id}`
                            }: ${odd.odds_home.toFixed(2)}`
                    )
                    .join("; ") || "Нет данных";
            const bookmakerOddsDraw =
                match.bookmaker_odds
                    ?.map(
                        (odd) =>
                            `${
                                odd.bookmaker_name ||
                                `Букмекер ${odd.bookmaker_id}`
                            }: ${odd.odds_draw.toFixed(2)}`
                    )
                    .join("; ") || "Нет данных";
            const bookmakerOddsAway =
                match.bookmaker_odds
                    ?.map(
                        (odd) =>
                            `${
                                odd.bookmaker_name ||
                                `Букмекер ${odd.bookmaker_id}`
                            }: ${odd.odds_away.toFixed(2)}`
                    )
                    .join("; ") || "Нет данных";

            const row = [
                match.id,
                formatDate(match.date),
                `"${match.home_team_name}"`,
                `"${match.away_team_name}"`,
                `"${match.match_score || "-"}"`,
                `"${sourceOddsHome}"`,
                `"${sourceOddsDraw}"`,
                `"${sourceOddsAway}"`,
                `"${bookmakerOddsHome}"`,
                `"${bookmakerOddsDraw}"`,
                `"${bookmakerOddsAway}"`,
            ];

            csvRows.push(row.join(","));
        });

        // Создаем CSV контент
        const csvContent = csvRows.join("\n");

        // Создаем Blob и скачиваем файл
        const blob = new Blob(["\ufeff" + csvContent], {
            type: "text/csv;charset=utf-8;",
        });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute(
            "download",
            `matches_${new Date().toISOString().split("T")[0]}.csv`
        );
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Показываем уведомление об успешном скачивании
        setSnackbar({
            open: true,
            message: "Таблица матчей успешно скачана в формате CSV",
            severity: "success",
        });
    };

    const handleSelectAll = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.checked) {
            // Выбираем только будущие матчи
            setSelectedMatches(
                matches
                    .filter((match) => !isMatchPast(match.date))
                    .map((match) => match.id)
            );
        } else {
            setSelectedMatches([]);
        }
    };

    const handleSelectMatch = (matchId: number) => {
        setSelectedMatches((prev) => {
            if (prev.includes(matchId)) {
                return prev.filter((id) => id !== matchId);
            } else {
                return [...prev, matchId];
            }
        });
    };

    const isAllSelected =
        matches.length > 0 &&
        matches.filter((match) => !isMatchPast(match.date)).length > 0 &&
        selectedMatches.length ===
            matches.filter((match) => !isMatchPast(match.date)).length;

    const isSomeSelected =
        selectedMatches.length > 0 &&
        selectedMatches.length <
            matches.filter((match) => !isMatchPast(match.date)).length;

    const renderOddsCell = (match: Match, type: "home" | "draw" | "away") => {
        const bookmakerOdds = match.bookmaker_odds || [];
        const sourceOdds = match.source_odds || [];

        const getOddsValue = (odds: any, type: "home" | "draw" | "away") => {
            if (type === "home") return odds.odds_home;
            if (type === "draw") return odds.odds_draw;
            return odds.odds_away;
        };

        return (
            <Box>
                {sourceOdds.map((odd, index) => (
                    <Box key={`source-${index}`} sx={{ mb: 1 }}>
                        <Typography variant="caption" color="text.secondary">
                            {odd.source_name || `Источник ${odd.sources_id}`}:
                        </Typography>
                        <Typography component="span" sx={{ ml: 1 }}>
                            {getOddsValue(odd, type).toFixed(2)}
                        </Typography>
                    </Box>
                ))}

                {bookmakerOdds.map((odd, index) => (
                    <Box key={`bookmaker-${index}`} sx={{ mb: 1 }}>
                        <Typography variant="caption" color="text.secondary">
                            {odd.bookmaker_name ||
                                `Букмекер ${odd.bookmaker_id}`}
                            :
                        </Typography>
                        <Typography component="span" sx={{ ml: 1 }}>
                            {getOddsValue(odd, type).toFixed(2)}
                        </Typography>
                    </Box>
                ))}

                {bookmakerOdds.length === 0 && sourceOdds.length === 0 && (
                    <Typography variant="body2" color="text.secondary">
                        Нет данных
                    </Typography>
                )}
            </Box>
        );
    };

    const getScoreDisplay = (match: Match) => {
        if (!match.match_score) {
            return (
                <Typography variant="body2" color="text.secondary">
                    -
                </Typography>
            );
        }

        return (
            <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                {match.match_score}
            </Typography>
        );
    };

    if (loading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="200px"
            >
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box p={2}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    return (
        <Box sx={{ p: 3 }}>
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 3,
                }}
            >
                <Typography variant="h5" component="h2">
                    Матчи
                </Typography>
                <Box sx={{ display: "flex", gap: 2 }}>
                    <Tooltip title="Создать сплит">
                        <IconButton
                            color="primary"
                            onClick={() => setCreateSplitDialogOpen(true)}
                            size="large"
                        >
                            <ShowChartIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Обновить данные">
                        <IconButton
                            color="primary"
                            onClick={handleParseAllMatches}
                            disabled={updateLoading}
                            size="large"
                        >
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Обновить счет">
                        <IconButton
                            color="primary"
                            onClick={handleUpdateAllScores}
                            disabled={updateScoresLoading}
                            size="large"
                        >
                            <ScoreIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Скачать CSV">
                        <IconButton
                            color="primary"
                            onClick={handleDownloadCSV}
                            size="large"
                        >
                            <DownloadIcon />
                        </IconButton>
                    </Tooltip>
                </Box>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell padding="checkbox">
                                <Checkbox
                                    indeterminate={isSomeSelected}
                                    checked={isAllSelected}
                                    onChange={handleSelectAll}
                                />
                            </TableCell>
                            <TableCell align="center">№</TableCell>
                            <TableCell>Дата</TableCell>
                            <TableCell>Команды</TableCell>
                            <TableCell align="center">П1</TableCell>
                            <TableCell align="center">X</TableCell>
                            <TableCell align="center">П2</TableCell>
                            <TableCell align="center">Счет</TableCell>
                            <TableCell align="center">Действия</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {matches.map((match, index) => (
                            <TableRow
                                key={match.id}
                                sx={{
                                    backgroundColor: isMatchPast(match.date)
                                        ? "rgba(0, 0, 0, 0.04)"
                                        : "inherit",
                                    "&:hover": {
                                        backgroundColor: isMatchPast(match.date)
                                            ? "rgba(0, 0, 0, 0.08)"
                                            : "rgba(0, 0, 0, 0.04)",
                                    },
                                }}
                            >
                                <TableCell padding="checkbox">
                                    {!isMatchPast(match.date) && (
                                        <Checkbox
                                            checked={selectedMatches.includes(
                                                match.id
                                            )}
                                            onChange={() =>
                                                handleSelectMatch(match.id)
                                            }
                                        />
                                    )}
                                </TableCell>
                                <TableCell align="center">
                                    {index + 1}
                                </TableCell>
                                <TableCell>{formatDate(match.date)}</TableCell>
                                <TableCell>
                                    {match.home_team_name} -{" "}
                                    {match.away_team_name}
                                </TableCell>
                                <TableCell>
                                    {renderOddsCell(match, "home")}
                                </TableCell>
                                <TableCell>
                                    {renderOddsCell(match, "draw")}
                                </TableCell>
                                <TableCell>
                                    {renderOddsCell(match, "away")}
                                </TableCell>
                                <TableCell align="center">
                                    {getScoreDisplay(match)}
                                </TableCell>
                                <TableCell align="center">
                                    <Tooltip title="Удалить матч">
                                        <IconButton
                                            color="error"
                                            size="small"
                                            onClick={() =>
                                                handleDeleteClick(
                                                    match.id,
                                                    match.home_team_name,
                                                    match.away_team_name,
                                                    match.date
                                                )
                                            }
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                        {matches.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={9} align="center">
                                    <Typography variant="body1" sx={{ py: 2 }}>
                                        Нет доступных матчей
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            <Snackbar
                open={snackbar.open}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            >
                <Alert
                    onClose={handleCloseSnackbar}
                    severity={snackbar.severity}
                >
                    {snackbar.message}
                </Alert>
            </Snackbar>

            <Dialog open={deleteDialog.open} onClose={handleDeleteCancel}>
                <DialogTitle>Подтверждение удаления</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Вы уверены, что хотите удалить матч "
                        {deleteDialog.matchInfo}"? Это действие нельзя отменить.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleDeleteCancel} color="primary">
                        Отмена
                    </Button>
                    <Button
                        onClick={handleDeleteConfirm}
                        color="error"
                        autoFocus
                    >
                        Удалить
                    </Button>
                </DialogActions>
            </Dialog>

            <CreateSplitDialog
                open={createSplitDialogOpen}
                onClose={() => setCreateSplitDialogOpen(false)}
                onSuccess={() => {
                    fetchMatches();
                    setSelectedMatches([]);
                }}
                selectedMatches={selectedMatches}
            />
        </Box>
    );
};

export default MatchesList;
