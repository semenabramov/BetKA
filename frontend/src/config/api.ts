// Конфигурация API
export const API_CONFIG = {
  // Базовый URL для API
  BASE_URL: 'https://betka.onrender.com',
  
  // Для локальной разработки используйте:
  // BASE_URL: 'http://localhost:5000',
  
  // Таймаут для запросов (в миллисекундах)
  TIMEOUT: 100000,
  
  // Эндпоинты API
  ENDPOINTS: {
    BOOKMAKERS: '/api/bookmakers',
    TEAMS: '/api/teams',
    MATCHES: '/api/matches',
    SPLITS: '/api/splits',
    ALIASES: '/api/teams/aliases',
    ODDS_SOURCES: '/api/odds-sources',
    UPDATE_MATCHES: '/api/matches/update',
    UPDATE_ALL: '/api/matches/update-all',
    UPDATE_SCORES: '/api/matches/update-all-scores',
    HEALTH: '/api/health',
  } as const,
} as const;

// Функция для получения полного URL
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Функция для получения относительного URL (для прокси в разработке)
export const getRelativeUrl = (endpoint: string): string => {
  return endpoint;
}; 