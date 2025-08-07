import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Константа для переключения между локальной БД и Supabase
    USE_SUPABASE = os.getenv('USE_SUPABASE', 'True').lower() == 'true'
    
    # Настройки локальной базы данных PostgreSQL
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'PostgreSQLasdfgzx333221qwe')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'betka')
    
    # Настройки Supabase (PostgreSQL connection)
    SUPABASE_USER = os.getenv('SUPABASE_USER', 'postgres')
    SUPABASE_PASSWORD = os.getenv('SUPABASE_PASSWORD', '5yqbCzz9W2KKsNNF')
    SUPABASE_HOST = os.getenv('SUPABASE_HOST', 'db.tihxefzgynuvqaocfdui.supabase.co')
    SUPABASE_PORT = os.getenv('SUPABASE_PORT', '5432')
    SUPABASE_DB = os.getenv('SUPABASE_DB', 'postgres')
     
    # Формируем строку подключения для SQLAlchemy
    if USE_SUPABASE:
        # Подключение к Supabase через PostgreSQL
        SQLALCHEMY_DATABASE_URI = 'postgresql://semen:58b5WOGgBk88efEcjJhfuH11yxlHpmnd@dpg-d2ade47diees738tsl80-a.oregon-postgres.render.com/betka'
    else:
        # Подключение к локальной PostgreSQL
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки сервера
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true' 