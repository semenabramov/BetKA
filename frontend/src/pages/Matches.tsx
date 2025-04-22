import React from 'react';
import { Typography, Box } from '@mui/material';

const Matches: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Матчи
      </Typography>
      <Typography variant="body1">
        Здесь будет список матчей
      </Typography>
    </Box>
  );
};

export default Matches; 