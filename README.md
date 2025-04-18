# BetKA - Система анализа футбольных матчей

Веб-приложение для анализа футбольных матчей с использованием данных из различных источников.

## Функциональность

- Парсинг данных о матчах из thepunterspage.com
- Парсинг коэффициентов с Winline
- Прогнозирование результатов матчей
- Поддержка различных лиг (Англия, Испания, Германия, Италия, Франция)
- Удобный интерфейс для просмотра данных

## Технологии

### Backend
- Python 3.8+
- Flask
- BeautifulSoup4
- Requests
- Pandas
- Scikit-learn

### Frontend
- React
- TypeScript
- Material-UI
- Vite

## Установка и запуск

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Структура проекта

```
.
├── backend/
│   ├── app.py              # Основной файл Flask приложения
│   ├── parser.py           # Парсер данных с thepunterspage
│   ├── winline_parser.py   # Парсер данных с Winline
│   ├── utils.py            # Вспомогательные функции
│   └── team_translations.py # Переводы названий команд
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # Основной компонент React
│   │   └── main.tsx       # Точка входа
│   └── package.json
└── README.md
```

## Лицензия

MIT 