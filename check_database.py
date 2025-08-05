#!/usr/bin/env python3
"""
Скрипт для проверки структуры базы данных
"""

from app import create_app
from app.core.database import db
from sqlalchemy import text

def check_database():
    """Проверяет структуру базы данных"""
    
    app = create_app()
    with app.app_context():
        
        print("🔍 Проверка структуры базы данных...")
        
        # Проверяем подключение
        try:
            result = db.session.execute(text('SELECT 1'))
            print("✅ Подключение к базе данных успешно")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return
        
        # Получаем список таблиц
        try:
            result = db.session.execute(text('SHOW TABLES'))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Найденные таблицы: {tables}")
            
            # Ищем таблицу с матчами
            match_tables = [t for t in tables if 'match' in t.lower()]
            if match_tables:
                print(f"🎯 Таблицы с матчами: {match_tables}")
            else:
                print("⚠️ Таблица с матчами не найдена")
                
        except Exception as e:
            print(f"❌ Ошибка при получении списка таблиц: {e}")
        
        # Проверяем структуру таблицы Matches
        try:
            result = db.session.execute(text('DESCRIBE Matches'))
            columns = result.fetchall()
            print(f"📊 Структура таблицы Matches:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        except Exception as e:
            print(f"❌ Ошибка при проверке таблицы Matches: {e}")
            
            # Пробуем другие варианты названия
            for table_name in ['matches', '`Matches`', '`matches`']:
                try:
                    result = db.session.execute(text(f'DESCRIBE {table_name}'))
                    columns = result.fetchall()
                    print(f"📊 Структура таблицы {table_name}:")
                    for col in columns:
                        print(f"  - {col[0]}: {col[1]}")
                    break
                except Exception as e:
                    print(f"❌ Таблица {table_name} не найдена")

if __name__ == "__main__":
    check_database() 