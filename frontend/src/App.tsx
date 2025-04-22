import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {
  Box,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Container
} from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import GroupsIcon from '@mui/icons-material/Groups';
import CasinoIcon from '@mui/icons-material/Casino';

import Home from './pages/Home';
import Matches from './pages/Matches';
import Teams from './pages/Teams';
import BookmakersList from './components/BookmakersList';

const App: React.FC = () => {
  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
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
            width: 240,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>
            <List>
              <ListItem button component={Link} to="/">
                <ListItemIcon>
                  <HomeIcon />
                </ListItemIcon>
                <ListItemText primary="Главная" />
              </ListItem>
              <ListItem button component={Link} to="/matches">
                <ListItemIcon>
                  <SportsSoccerIcon />
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
            </List>
          </Box>
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Container>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/matches" element={<Matches />} />
              <Route path="/teams" element={<Teams />} />
              <Route path="/bookmakers" element={<BookmakersList />} />
            </Routes>
          </Container>
        </Box>
      </Box>
    </Router>
  );
};

export default App; 