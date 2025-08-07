# Развертывание BetKA Backend на Render

## Структура проекта

```
BetKA/
├── backend/           # Основной код бэкенда
│   ├── app/          # Flask приложение
│   ├── run.py        # Точка входа для gunicorn
│   ├── requirements.txt
│   └── runtime.txt
├── frontend/         # React приложение
├── render.yaml       # Конфигурация Render
└── Procfile         # Конфигурация процесса
```

## Конфигурация Render

### render.yaml
- `rootDir: backend` - указывает, что код находится в папке backend
- `startCommand: gunicorn run:app` - запускает приложение через gunicorn
- Настроены переменные окружения для подключения к PostgreSQL

### Procfile
```
web: gunicorn --bind 0.0.0.0:$PORT run:app
```

## Переменные окружения

- `USE_SUPABASE: True` - использовать Supabase
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` - настройки PostgreSQL
- `HOST: 0.0.0.0` - слушать все интерфейсы
- `PORT: 5000` - порт приложения
- `DEBUG: False` - отключить режим отладки

## Исправленные проблемы

1. **Ошибка "module 'app' has no attribute 'app'"**
   - Создан файл `run.py` для явного экспорта переменной `app`
   - Обновлен `Procfile` для использования `run:app`

2. **Неправильная структура проекта**
   - Перемещен `render.yaml` в корень проекта
   - Указан `rootDir: backend` для правильного поиска файлов

3. **Конфигурация gunicorn**
   - Добавлен `--bind 0.0.0.0:$PORT` для правильного связывания
   - Используется переменная окружения `$PORT` от Render

## Проверка развертывания

После развертывания проверьте:
1. Логи в Render Dashboard
2. Доступность эндпоинта: `https://your-app.onrender.com/api/health`
3. Подключение к базе данных

## Локальная разработка

```bash
cd backend
python run.py
```

Приложение будет доступно на `http://localhost:5000` 