#!/usr/bin/env python3
"""
Скрипт для миграции данных из MySQL в PostgreSQL
"""

import os
import sys
from dotenv import load_dotenv
import pymysql
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

load_dotenv()

class MySQLToPostgreSQLMigrator:
    def __init__(self):
        # MySQL подключение
        self.mysql_config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', 'mysql'),
            'database': os.getenv('MYSQL_DATABASE', 'betka'),
            'charset': 'utf8mb4'
        }
        
        # PostgreSQL подключение
        self.postgres_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'password'),
            'database': os.getenv('POSTGRES_DATABASE', 'betka'),
            'port': os.getenv('POSTGRES_PORT', '5432')
        }
    
    def connect_mysql(self):
        """Подключение к MySQL"""
        try:
            connection = pymysql.connect(**self.mysql_config)
            print("✅ Подключение к MySQL успешно")
            return connection
        except Exception as e:
            print(f"❌ Ошибка подключения к MySQL: {e}")
            return None
    
    def connect_postgresql(self):
        """Подключение к PostgreSQL"""
        try:
            connection = psycopg2.connect(**self.postgres_config)
            print("✅ Подключение к PostgreSQL успешно")
            return connection
        except Exception as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            return None
    
    def create_postgresql_tables(self, pg_conn):
        """Создание таблиц в PostgreSQL"""
        cursor = pg_conn.cursor()
        
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
        
        try:
            for sql in tables_sql:
                cursor.execute(sql)
            pg_conn.commit()
            print("✅ Таблицы в PostgreSQL созданы успешно")
        except Exception as e:
            print(f"❌ Ошибка создания таблиц: {e}")
            pg_conn.rollback()
    
    def migrate_data(self):
        """Миграция данных из MySQL в PostgreSQL"""
        mysql_conn = self.connect_mysql()
        pg_conn = self.connect_postgresql()
        
        if not mysql_conn or not pg_conn:
            return
        
        try:
            # Создаем таблицы в PostgreSQL
            self.create_postgresql_tables(pg_conn)
            
            # Мигрируем данные
            self.migrate_teams(mysql_conn, pg_conn)
            self.migrate_alias_teams(mysql_conn, pg_conn)
            self.migrate_odds_sources(mysql_conn, pg_conn)
            self.migrate_bookmakers(mysql_conn, pg_conn)
            self.migrate_matches(mysql_conn, pg_conn)
            self.migrate_odds_from_sources(mysql_conn, pg_conn)
            self.migrate_bookmakers_odds(mysql_conn, pg_conn)
            self.migrate_splits(mysql_conn, pg_conn)
            self.migrate_split_matches(mysql_conn, pg_conn)
            
            print("✅ Миграция данных завершена успешно!")
            
        except Exception as e:
            print(f"❌ Ошибка миграции: {e}")
        finally:
            mysql_conn.close()
            pg_conn.close()
    
    def migrate_teams(self, mysql_conn, pg_conn):
        """Миграция команд"""
        print("🔄 Миграция команд...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, name, league FROM teams")
        teams = mysql_cursor.fetchall()
        
        for team in teams:
            pg_cursor.execute(
                "INSERT INTO teams (id, name, league) VALUES (%s, %s, %s)",
                team
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(teams)} команд")
    
    def migrate_alias_teams(self, mysql_conn, pg_conn):
        """Миграция альтернативных названий команд"""
        print("🔄 Миграция альтернативных названий команд...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, id_team, alias_name, language FROM alias_team")
        aliases = mysql_cursor.fetchall()
        
        for alias in aliases:
            pg_cursor.execute(
                "INSERT INTO alias_team (id, id_team, alias_name, language) VALUES (%s, %s, %s, %s)",
                alias
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(aliases)} альтернативных названий")
    
    def migrate_odds_sources(self, mysql_conn, pg_conn):
        """Миграция источников коэффициентов"""
        print("🔄 Миграция источников коэффициентов...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT * FROM odds_sources")
        sources = mysql_cursor.fetchall()
        
        for source in sources:
            pg_cursor.execute("""
                INSERT INTO odds_sources (
                    id, name, url, premier_league_url, championship_url, 
                    league_one_url, league_two_url, bundesliga_one_url, 
                    bundesliga_two_url, liga_url, la_liga_url, serie_a_url, 
                    ligue_one_url, is_active, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, source)
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(sources)} источников")
    
    def migrate_bookmakers(self, mysql_conn, pg_conn):
        """Миграция букмекеров"""
        print("🔄 Миграция букмекеров...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT * FROM bookmakers")
        bookmakers = mysql_cursor.fetchall()
        
        for bookmaker in bookmakers:
            pg_cursor.execute("""
                INSERT INTO bookmakers (
                    id, name, premier_league_url, championship_url, 
                    league_one_url, league_two_url, bundesliga_one_url, 
                    bundesliga_two_url, liga_url, la_liga_url, serie_a_url, ligue_one_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, bookmaker)
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(bookmakers)} букмекеров")
    
    def migrate_matches(self, mysql_conn, pg_conn):
        """Миграция матчей"""
        print("🔄 Миграция матчей...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, date, team_home, team_away, split, match_score FROM Matches")
        matches = mysql_cursor.fetchall()
        
        for match in matches:
            pg_cursor.execute(
                "INSERT INTO \"Matches\" (id, date, team_home, team_away, split, match_score) VALUES (%s, %s, %s, %s, %s, %s)",
                match
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(matches)} матчей")
    
    def migrate_odds_from_sources(self, mysql_conn, pg_conn):
        """Миграция коэффициентов из источников"""
        print("🔄 Миграция коэффициентов из источников...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, match_id, sources_id, odds_home, odds_away, odds_draw FROM odds_from_sources")
        odds = mysql_cursor.fetchall()
        
        for odd in odds:
            pg_cursor.execute(
                "INSERT INTO odds_from_sources (id, match_id, sources_id, odds_home, odds_away, odds_draw) VALUES (%s, %s, %s, %s, %s, %s)",
                odd
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(odds)} коэффициентов из источников")
    
    def migrate_bookmakers_odds(self, mysql_conn, pg_conn):
        """Миграция коэффициентов букмекеров"""
        print("🔄 Миграция коэффициентов букмекеров...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, match_id, bookmaker_id, odds_home, odds_away, odds_draw FROM Bookmakers_odds")
        odds = mysql_cursor.fetchall()
        
        for odd in odds:
            pg_cursor.execute(
                "INSERT INTO \"Bookmakers_odds\" (id, match_id, bookmaker_id, odds_home, odds_away, odds_draw) VALUES (%s, %s, %s, %s, %s, %s)",
                odd
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(odds)} коэффициентов букмекеров")
    
    def migrate_splits(self, mysql_conn, pg_conn):
        """Миграция сплитов"""
        print("🔄 Миграция сплитов...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, name, date, Kelly_value, Bank, min_bet, status FROM Splits")
        splits = mysql_cursor.fetchall()
        
        for split in splits:
            pg_cursor.execute(
                "INSERT INTO \"Splits\" (id, name, date, \"Kelly_value\", \"Bank\", min_bet, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                split
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(splits)} сплитов")
    
    def migrate_split_matches(self, mysql_conn, pg_conn):
        """Миграция связей сплитов с матчами"""
        print("🔄 Миграция связей сплитов с матчами...")
        
        mysql_cursor = mysql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        mysql_cursor.execute("SELECT id, split_id, match_id, bookmaker_id, selected_outcome, odds_value, is_success, notes FROM split_matches")
        split_matches = mysql_cursor.fetchall()
        
        for split_match in split_matches:
            pg_cursor.execute(
                "INSERT INTO split_matches (id, split_id, match_id, bookmaker_id, selected_outcome, odds_value, is_success, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                split_match
            )
        
        pg_conn.commit()
        print(f"✅ Мигрировано {len(split_matches)} связей сплитов")

def main():
    print("🚀 Начинаем миграцию с MySQL на PostgreSQL...")
    
    migrator = MySQLToPostgreSQLMigrator()
    migrator.migrate_data()
    
    print("✅ Миграция завершена!")

if __name__ == "__main__":
    main() 