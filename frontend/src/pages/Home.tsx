import React from 'react';
import { Typography, Box } from '@mui/material';

const Home: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Добро пожаловать в BetKA
      </Typography>
      <Typography variant="body1">
        Это приложение для управления матчами, командами и букмекерами.
      </Typography>
    </Box>
  );
};

export default Home; 