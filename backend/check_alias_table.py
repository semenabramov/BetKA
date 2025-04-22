import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.core.database import db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    # Проверяем, существует ли таблица alias_team
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("Существующие таблицы:")
    for table in tables:
        print(f"- {table}")
    
    if 'alias_team' in tables:
        print("\nСтруктура таблицы alias_team:")
        columns = inspector.get_columns('alias_team')
        for column in columns:
            print(f"- {column['name']}: {column['type']}")
        
        # Проверяем внешние ключи
        foreign_keys = inspector.get_foreign_keys('alias_team')
        print("\nВнешние ключи таблицы alias_team:")
        for fk in foreign_keys:
            print(f"- {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    else:
        print("\nТаблица alias_team не существует!")
        
        # Проверяем, существует ли таблица Teams
        if 'Teams' in tables:
            print("\nСтруктура таблицы Teams:")
            columns = inspector.get_columns('Teams')
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        else:
            print("\nТаблица Teams не существует!")
            
        # Проверяем, существует ли таблица teams
        if 'teams' in tables:
            print("\nСтруктура таблицы teams:")
            columns = inspector.get_columns('teams')
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        else:
            print("\nТаблица teams не существует!")
            
    # Проверяем, существует ли таблица Alias_team
    if 'Alias_team' in tables:
        print("\nСтруктура таблицы Alias_team:")
        columns = inspector.get_columns('Alias_team')
        for column in columns:
            print(f"- {column['name']}: {column['type']}")
        
        # Проверяем внешние ключи
        foreign_keys = inspector.get_foreign_keys('Alias_team')
        print("\nВнешние ключи таблицы Alias_team:")
        for fk in foreign_keys:
            print(f"- {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    else:
        print("\nТаблица Alias_team не существует!") 