import React, { useState } from 'react'
import { Button, Container, Box } from '@mui/material'
import CreateTeam from './components/CreateTeam'
import TeamAliases from './components/TeamAliases'

const App: React.FC = () => {
  const [isCreateTeamOpen, setIsCreateTeamOpen] = useState<boolean>(false)
  const [isTeamAliasesOpen, setIsTeamAliasesOpen] = useState<boolean>(false)

  const handleOpenCreateTeam = () => {
    setIsCreateTeamOpen(true)
  }

  const handleCloseCreateTeam = () => {
    setIsCreateTeamOpen(false)
  }

  const handleOpenTeamAliases = () => {
    setIsTeamAliasesOpen(true)
  }

  const handleCloseTeamAliases = () => {
    setIsTeamAliasesOpen(false)
  }

  return (
    <Container>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2, mb: 2, gap: 2 }}>
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
      
      <CreateTeam 
        open={isCreateTeamOpen} 
        onClose={handleCloseCreateTeam} 
      />
      
      <TeamAliases
        open={isTeamAliasesOpen}
        onClose={handleCloseTeamAliases}
      />
    </Container>
  )
}

export default App 