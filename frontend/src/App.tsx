import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {
    AppBar,
    Toolbar,
    Typography,
    Button,
    Container,
    Box,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Drawer
} from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import GroupsIcon from '@mui/icons-material/Groups';
import CasinoIcon from '@mui/icons-material/Casino';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import Matches from './pages/Matches';
import Teams from './pages/Teams';
import Bookmakers from './pages/Bookmakers';
import Sources from './pages/Sources';
import SplitsList from './components/SplitsList';

const App: React.FC = () => {
    const drawerWidth = 240;

    return (
        <Router>
            <Box sx={{ display: 'flex' }}>
                <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
                    <Toolbar>
                        <Typography variant="h6" noWrap component="div">
                            BetKA
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Drawer
                    variant="permanent"
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        '& .MuiDrawer-paper': {
                            width: drawerWidth,
                            boxSizing: 'border-box',
                        },
                    }}
                >
                    <Toolbar />
                    <Box sx={{ overflow: 'auto' }}>
                        <List>
                            <ListItem button component={Link} to="/">
                                <ListItemIcon>
                                    <HomeIcon />
                                </ListItemIcon>
                                <ListItemText primary="Матчи" />
                            </ListItem>
                            <ListItem button component={Link} to="/teams">
                                <ListItemIcon>
                                    <GroupsIcon />
                                </ListItemIcon>
                                <ListItemText primary="Команды" />
                            </ListItem>
                            <ListItem button component={Link} to="/bookmakers">
                                <ListItemIcon>
                                    <CasinoIcon />
                                </ListItemIcon>
                                <ListItemText primary="Букмекеры" />
                            </ListItem>
                            <ListItem button component={Link} to="/sources">
                                <ListItemIcon>
                                    <AnalyticsIcon />
                                </ListItemIcon>
                                <ListItemText primary="Ресурсы" />
                            </ListItem>
                            <ListItem button component={Link} to="/splits">
                                <ListItemIcon>
                                    <AnalyticsIcon />
                                </ListItemIcon>
                                <ListItemText primary="Сплиты" />
                            </ListItem>
                        </List>
                    </Box>
                </Drawer>
                <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                    <Toolbar />
                    <Container>
                        <Routes>
                            <Route path="/" element={<Matches />} />
                            <Route path="/teams" element={<Teams />} />
                            <Route path="/bookmakers" element={<Bookmakers />} />
                            <Route path="/sources" element={<Sources />} />
                            <Route path="/splits" element={<SplitsList />} />
                        </Routes>
                    </Container>
                </Box>
            </Box>
        </Router>
    );
};

export default App; 