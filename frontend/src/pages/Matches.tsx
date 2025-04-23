import React from 'react';
import { Typography, Box } from '@mui/material';
import MatchesList from '../components/MatchesList';

const Matches: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Матчи
      </Typography>
      <MatchesList />
    </Box>
  );
};

export default Matches; 