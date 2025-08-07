import React, { useState } from 'react';
import { Typography, Box, Button } from '@mui/material';
import CreateTeam from '../components/CreateTeam';
import TeamAliases from '../components/TeamAliases';
import TeamsList from '../components/TeamsList';

const Teams: React.FC = () => {
  const [isCreateTeamOpen, setIsCreateTeamOpen] = useState(false);
  const [isTeamAliasesOpen, setIsTeamAliasesOpen] = useState(false);

  const handleOpenCreateTeam = () => setIsCreateTeamOpen(true);
  const handleCloseCreateTeam = () => setIsCreateTeamOpen(false);
  const handleOpenTeamAliases = () => setIsTeamAliasesOpen(true);
  const handleCloseTeamAliases = () => setIsTeamAliasesOpen(false);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2, gap: 2 }}>
        <Button 
          variant="outlined" 
          color="primary" 
          onClick={handleOpenTeamAliases}
        >
          Альтернативные названия
        </Button>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleOpenCreateTeam}
        >
          Создать команду
        </Button>
      </Box>

      <Typography variant="h4" gutterBottom>
        Команды
      </Typography>
      
      <TeamsList />

      <CreateTeam 
        open={isCreateTeamOpen} 
        onClose={handleCloseCreateTeam} 
      />

      <TeamAliases
        open={isTeamAliasesOpen}
        onClose={handleCloseTeamAliases}
      />
    </Box>
  );
};

export default Teams; 