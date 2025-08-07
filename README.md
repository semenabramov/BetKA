# BetKA - Система анализа футбольных матчей

Веб-приложение для анализа футбольных матчей с использованием данных из различных источников.

## Функциональность

-   Парсинг данных о матчах из thepunterspage.com
-   Парсинг коэффициентов с Winline
-   Прогнозирование результатов матчей
-   Поддержка различных лиг (Англия, Испания, Германия, Италия, Франция)
-   Удобный интерфейс для просмотра данных

## Технологии

### Backend

-   Python 3.8+
-   Flask
-   PostgreSQL
-   BeautifulSoup4
-   Requests
-   Pandas
-   Scikit-learn

### Frontend

-   React
-   TypeScript
-   Material-UI
-   Vite

## Установка и запуск

### 1. Установка PostgreSQL

#### Windows:

```bash
# Скачайте и установите PostgreSQL с официального сайта
# https://www.postgresql.org/download/windows/
```

#### Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS:

```bash
brew install postgresql
brew services start postgresql
```

### 2. Настройка базы данных

Создайте файл `.env` в папке `backend/`:

```env
# Настройки базы данных PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/betka

# Настройки сервера
HOST=0.0.0.0
PORT=5000
DEBUG=True

# Настройки для миграции (если нужно)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=mysql
MYSQL_DATABASE=betka

POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DATABASE=betka
POSTGRES_PORT=5432
```

### 3. Инициализация PostgreSQL

```bash
cd backend
python init_postgresql.py
```

### 4. Миграция данных (если есть данные в MySQL)

```bash
cd backend
python migrate_to_postgresql.py
```

### 5. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
python run.py
```

### 6. Frontend

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
│   ├── init_postgresql.py  # Инициализация PostgreSQL
│   ├── migrate_to_postgresql.py # Миграция данных
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

## Миграция с MySQL на PostgreSQL

### Пошаговая инструкция:

1. **Установите PostgreSQL** (см. выше)

2. **Создайте файл .env** с настройками подключения

3. **Инициализируйте PostgreSQL**:

    ```bash
    cd backend
    python init_postgresql.py
    ```

4. **Если у вас есть данные в MySQL, выполните миграцию**:

    ```bash
    cd backend
    python migrate_to_postgresql.py
    ```

5. **Обновите зависимости**:

    ```bash
    pip install -r requirements.txt
    ```

6. **Запустите приложение**:
    ```bash
    python run.py
    ```

### Преимущества PostgreSQL:

-   **ACID-совместимость** - полная поддержка транзакций
-   **Расширенные типы данных** - JSON, массивы, геометрические типы
-   **Мощные индексы** - B-tree, Hash, GiST, SP-GiST, GIN, BRIN
-   **Параллельные запросы** - лучшая производительность
-   **Расширения** - PostGIS, pg_trgm, и другие
-   **Более строгая проверка типов** - лучшая целостность данных

## Лицензия

MIT
