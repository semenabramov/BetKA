from flask_sqlalchemy import SQLAlchemy
from app.core.config import Config

db = SQLAlchemy()

def init_db(app):
    """Инициализация подключения к базе данных"""
    db.init_app(app)
    
    # Выводим информацию о подключении
    if Config.USE_SUPABASE:
        print("✅ Connected to Supabase via SQLAlchemy")
    else:
        print("✅ Connected to local PostgreSQL via SQLAlchemy") 