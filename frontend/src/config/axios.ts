import axios from 'axios';
import { API_CONFIG } from './api';

// Создаем экземпляр axios с базовой конфигурацией
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Интерцептор для добавления заголовков
apiClient.interceptors.request.use(
  (config) => {
    // Можно добавить токены авторизации здесь
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient; 