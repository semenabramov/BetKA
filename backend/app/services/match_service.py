from typing import Dict, Optional, List
from datetime import datetime
from app.models.match import Match
from app.models.team import Team
from app.models.odds import OddsFromSource, BookmakerOdds
from app.core.database import db
from app.models.bookmaker import Bookmaker
from app.models.odds_source import OddsSource
from app.models.alias_team import AliasTeam

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
    def get_all_teams() -> List[dict]:
        """Получает все команды с их альтернативными названиями"""
        teams = Team.query.order_by(Team.name).all()
        result = []
        
        for team in teams:
            team_dict = team.to_dict()
            # Получаем альтернативные названия для команды
            aliases = AliasTeam.query.filter_by(id_team=team.id).all()
            team_dict['aliases'] = [alias.to_dict() for alias in aliases]
            result.append(team_dict)
            
        return result

    @staticmethod
    def create_match(data: dict) -> Match:
        match = Match(
            date=data['date'],
            team_home=data['team_home'],
            team_away=data['team_away'],
            split=data.get('split')
        )
        db.session.add(match)
        db.session.commit()
        return match
    
    @staticmethod
    def get_match_by_id(match_id: int) -> Optional[Match]:
        return Match.query.get(match_id)
    
    @staticmethod
    def get_all_matches() -> List[Match]:
        """Получает все матчи с коэффициентами"""
        matches = Match.query.order_by(Match.date.desc()).all()
        return [MatchService.get_match_with_odds(match.id) for match in matches]
    
    @staticmethod
    def update_match(match_id: int, data: dict) -> Optional[Match]:
        match = Match.query.get(match_id)
        if not match:
            return None
            
        for key, value in data.items():
            if hasattr(match, key):
                setattr(match, key, value)
                
        db.session.commit()
        return match
    
    @staticmethod
    def delete_match(match_id: int) -> bool:
        match = Match.query.get(match_id)
        if not match:
            return False
            
        # Удаляем связанные коэффициенты
        OddsFromSource.query.filter_by(match_id=match_id).delete()
        BookmakerOdds.query.filter_by(match_id=match_id).delete()
        
        db.session.delete(match)
        db.session.commit()
        return True
    
    @staticmethod
    def get_match_with_odds(match_id: int) -> Optional[dict]:
        match = Match.query.get(match_id)
        if not match:
            return None
            
        result = match.to_dict()
        
        # Добавляем коэффициенты от букмекеров с их названиями
        result['bookmaker_odds'] = []
        for odd in match.bookmaker_odds:
            bookmaker = Bookmaker.query.get(odd.bookmaker_id)
            odd_dict = odd.to_dict()
            if bookmaker:
                odd_dict['bookmaker_name'] = bookmaker.name
            result['bookmaker_odds'].append(odd_dict)
            
        # Добавляем коэффициенты от источников с их названиями
        result['source_odds'] = []
        for odd in match.source_odds:
            source = OddsSource.query.get(odd.sources_id)
            odd_dict = odd.to_dict()
            if source:
                odd_dict['source_name'] = source.name
            result['source_odds'].append(odd_dict)
            
        return result
    
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
            'source_odds': {
                'home': 2.1,
                'draw': 3.4,
                'away': 3.2
            }
        }
        print(match_data)
        
        return MatchService.create_match(match_data) 