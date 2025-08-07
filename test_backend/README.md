# BetKA Test Backend

Простое тестовое Flask приложение для проверки деплоя на Render.

## Эндпоинты

- `GET /` - Основная страница с сообщением о запуске сервера
- `GET /health` - Проверка состояния сервера

## Локальный запуск

```bash
pip install -r requirements.txt
python app.py
```

## Деплой на Render

1. Создайте новый Web Service на Render
2. Укажите корневую папку как `test_backend`
3. Используйте команду запуска: `gunicorn app:app`

## Структура файлов

- `app.py` - Основное Flask приложение
- `requirements.txt` - Зависимости Python
- `runtime.txt` - Версия Python
- `Procfile` - Команда запуска для Render
- `render.yaml` - Конфигурация деплоя 