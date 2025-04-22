from typing import Dict, Optional, List
from datetime import datetime
from app.models.match import Match
from app.models.team import Team
from app.models.odds import OddsFromKickform
from app.core.database import db

class MatchService:
    @staticmethod
    def create_team(name: str, league: str) -> Optional[Team]:
        """Создает новую команду в базе данных"""
        try:
            # Проверяем, существует ли уже команда с таким названием
            existing_team = Team.query.filter_by(name=name).first()
            if existing_team:
                return existing_team
            
            # Создаем новую команду
            team = Team(
                name=name,
                league=league
            )
            
            db.session.add(team)
            db.session.commit()
            return team
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating team: {str(e)}")
            return None

    @staticmethod
    def get_all_teams() -> List[Team]:
        """Получает все команды"""
        return Team.query.order_by(Team.name).all()

    @staticmethod
    def create_match(match_data: Dict) -> Optional[Match]:
        """Создает новый матч в базе данных"""
        try:
            # Проверяем существование команд
            home_team = Team.query.get(match_data['team_home'])
            away_team = Team.query.get(match_data['team_away'])
            
            if not home_team or not away_team:
                return None
            
            # Создаем матч
            match = Match(
                date=datetime.fromisoformat(match_data['date']),
                team_home=match_data['team_home'],
                team_away=match_data['team_away'],
                split=match_data.get('split')
            )
            
            db.session.add(match)
            db.session.flush()  # Получаем id матча
            
            # Если есть коэффициенты от Kickform, добавляем их
            if 'kickform_odds' in match_data:
                odds = OddsFromKickform(
                    match_id=match.id,
                    odds_home=match_data['kickform_odds']['home'],
                    odds_draw=match_data['kickform_odds']['draw'],
                    odds_away=match_data['kickform_odds']['away']
                )
                db.session.add(odds)
            
            db.session.commit()
            return match
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating match: {str(e)}")
            return None
    
    @staticmethod
    def get_match(match_id: int) -> Optional[Match]:
        """Получает матч по id"""
        return Match.query.get(match_id)
    
    @staticmethod
    def get_all_matches() -> list:
        """Получает все матчи"""
        return Match.query.order_by(Match.date.desc()).all()
    
    @staticmethod
    def create_mock_match() -> Optional[Match]:
        """Создает тестовый матч с моковыми данными"""
        # Создаем тестовые команды, если их нет
        home_team = Team.query.filter_by(name='Manchester United').first()
        if not home_team:
            home_team = Team(name='Manchester United', league='Premier League')
            db.session.add(home_team)
            db.session.flush()
        
        away_team = Team.query.filter_by(name='Liverpool').first()
        if not away_team:
            away_team = Team(name='Liverpool', league='Premier League')
            db.session.add(away_team)
            db.session.flush()
        
        # Создаем матч
        match_data = {
            'date': datetime.now().isoformat(),
            'team_home': home_team.id,
            'team_away': away_team.id,
            'kickform_odds': {
                'home': 2.1,
                'draw': 3.4,
                'away': 3.2
            }
        }
        print(match_data)
        
        return MatchService.create_match(match_data) 