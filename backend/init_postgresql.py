#!/usr/bin/env python3
"""
Скрипт для инициализации PostgreSQL базы данных
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

def create_database():
    """Создание базы данных PostgreSQL"""
    
    # Параметры подключения к PostgreSQL
    postgres_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'PostgreSQLasdfgzx333221qwe'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }
    
    database_name = os.getenv('POSTGRES_DATABASE', 'betka')
    
    try:
        # Подключаемся к PostgreSQL без указания базы данных
        conn = psycopg2.connect(**postgres_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Проверяем, существует ли база данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        exists = cursor.fetchone()
        
        if not exists:
            # Создаем базу данных
            cursor.execute(f'CREATE DATABASE "{database_name}"')
            print(f"✅ База данных '{database_name}' создана успешно")
        else:
            print(f"✅ База данных '{database_name}' уже существует")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания базы данных: {e}")
        return False

def create_tables():
    """Создание таблиц в PostgreSQL"""
    
    # Используем правильную строку подключения с паролем из конфигурации
    postgres_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'PostgreSQLasdfgzx333221qwe'),
        'database': os.getenv('POSTGRES_DATABASE', 'betka'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }
    
    try:
        # Подключаемся к созданной базе данных
        conn = psycopg2.connect(**postgres_config)
        cursor = conn.cursor()
        
        # SQL для создания таблиц
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS teams (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                league VARCHAR(255) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS alias_team (
                id SERIAL PRIMARY KEY,
                id_team INTEGER NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
                alias_name VARCHAR(255) NOT NULL,
                language VARCHAR(2) DEFAULT 'ru' CHECK (language IN ('ru', 'en'))
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS "Matches" (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP NOT NULL,
                team_home INTEGER REFERENCES teams(id),
                team_away INTEGER REFERENCES teams(id),
                split INTEGER,
                match_score VARCHAR(10)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS odds_sources (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                url VARCHAR(255) NOT NULL,
                premier_league_url VARCHAR(255),
                championship_url VARCHAR(255),
                league_one_url VARCHAR(255),
                league_two_url VARCHAR(255),
                bundesliga_one_url VARCHAR(255),
                bundesliga_two_url VARCHAR(255),
                liga_url VARCHAR(255),
                la_liga_url VARCHAR(255),
                serie_a_url VARCHAR(255),
                ligue_one_url VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bookmakers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                premier_league_url VARCHAR(255),
                championship_url VARCHAR(255),
                league_one_url VARCHAR(255),
                league_two_url VARCHAR(255),
                bundesliga_one_url VARCHAR(255),
                bundesliga_two_url VARCHAR(255),
                liga_url VARCHAR(255),
                la_liga_url VARCHAR(255),
                serie_a_url VARCHAR(255),
                ligue_one_url VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS odds_from_sources (
                id SERIAL PRIMARY KEY,
                match_id INTEGER NOT NULL REFERENCES "Matches"(id),
                sources_id INTEGER REFERENCES odds_sources(id),
                odds_home FLOAT,
                odds_away FLOAT,
                odds_draw FLOAT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS "Bookmakers_odds" (
                id SERIAL PRIMARY KEY,
                match_id INTEGER NOT NULL REFERENCES "Matches"(id),
                bookmaker_id INTEGER NOT NULL REFERENCES bookmakers(id),
                odds_home FLOAT,
                odds_away FLOAT,
                odds_draw FLOAT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS "Splits" (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                date TIMESTAMP NOT NULL,
                "Kelly_value" FLOAT,
                "Bank" FLOAT,
                min_bet FLOAT,
                status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived'))
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS split_matches (
                id SERIAL PRIMARY KEY,
                split_id INTEGER NOT NULL REFERENCES "Splits"(id),
                match_id INTEGER NOT NULL REFERENCES "Matches"(id),
                bookmaker_id INTEGER NOT NULL REFERENCES bookmakers(id),
                selected_outcome VARCHAR(10) CHECK (selected_outcome IN ('home', 'draw', 'away')),
                odds_value FLOAT,
                is_success BOOLEAN,
                notes TEXT
            );
            """
        ]
        
        # Создаем таблицы
        for i, sql in enumerate(tables_sql, 1):
            try:
                cursor.execute(sql)
                print(f"✅ Таблица {i} создана успешно")
            except Exception as e:
                print(f"❌ Ошибка создания таблицы {i}: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Все таблицы созданы успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания таблиц: {e}")
        return False

def create_indexes():
    """Создание индексов для оптимизации"""
    
    # Используем правильную строку подключения с паролем из конфигурации
    postgres_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'PostgreSQLasdfgzx333221qwe'),
        'database': os.getenv('POSTGRES_DATABASE', 'betka'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }
    
    try:
        conn = psycopg2.connect(**postgres_config)
        cursor = conn.cursor()
        
        # SQL для создания индексов
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_matches_date ON \"Matches\"(date);",
            "CREATE INDEX IF NOT EXISTS idx_matches_teams ON \"Matches\"(team_home, team_away);",
            "CREATE INDEX IF NOT EXISTS idx_alias_team_id_team ON alias_team(id_team);",
            "CREATE INDEX IF NOT EXISTS idx_alias_team_alias ON alias_team(alias_name);",
            "CREATE INDEX IF NOT EXISTS idx_odds_from_sources_match ON odds_from_sources(match_id);",
            "CREATE INDEX IF NOT EXISTS idx_bookmakers_odds_match ON \"Bookmakers_odds\"(match_id);",
            "CREATE INDEX IF NOT EXISTS idx_splits_date ON \"Splits\"(date);",
            "CREATE INDEX IF NOT EXISTS idx_split_matches_split ON split_matches(split_id);"
        ]
        
        for i, sql in enumerate(indexes_sql, 1):
            try:
                cursor.execute(sql)
                print(f"✅ Индекс {i} создан успешно")
            except Exception as e:
                print(f"❌ Ошибка создания индекса {i}: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Все индексы созданы успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания индексов: {e}")
        return False

def main():
    """Основная функция инициализации"""
    print("🚀 Инициализация PostgreSQL базы данных...")
    
    # Создаем базу данных
    if not create_database():
        print("❌ Не удалось создать базу данных")
        return
    
    # Создаем таблицы
    if not create_tables():
        print("❌ Не удалось создать таблицы")
        return
    
    # Создаем индексы
    if not create_indexes():
        print("❌ Не удалось создать индексы")
        return
    
    print("✅ Инициализация PostgreSQL завершена успешно!")

if __name__ == "__main__":
    main() 