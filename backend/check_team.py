import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.team import Team
from app.models.alias_team import AliasTeam

app = create_app()

with app.app_context():
    # Проверяем, существует ли команда с ID 5
    team = Team.query.get(5)
    
    if team:
        print(f"Команда с ID 5 существует: {team.name} (лига: {team.league})")
        
        # Проверяем альтернативные названия для этой команды
        aliases = AliasTeam.query.filter_by(team_id=5).all()
        print(f"Количество альтернативных названий: {len(aliases)}")
        
        for alias in aliases:
            print(f"- {alias.alias}")
    else:
        print("Команда с ID 5 не существует!")
        
        # Выводим список всех команд
        teams = Team.query.all()
        print("\nСписок всех команд:")
        for t in teams:
            print(f"- ID: {t.id}, Название: {t.name}, Лига: {t.league}")
            
        # Проверяем структуру таблицы alias_team
        try:
            aliases = AliasTeam.query.all()
            print(f"\nВсего альтернативных названий: {len(aliases)}")
        except Exception as e:
            print(f"\nОшибка при запросе к таблице alias_team: {str(e)}") 