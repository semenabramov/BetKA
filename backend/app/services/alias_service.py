from typing import List, Optional
import logging
from app.models.alias_team import AliasTeam
from app.models.team import Team
from app.core.database import db

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AliasService:
    @staticmethod
    def get_aliases_by_team_id(team_id: int) -> List[AliasTeam]:
        """Получает все альтернативные названия для команды по её ID"""
        return AliasTeam.query.filter_by(id_team=team_id).all()
    
    @staticmethod
    def add_alias(team_id: int, alias: str, language: str = 'ru') -> Optional[AliasTeam]:
        """Добавляет новое альтернативное название для команды"""
        try:
            logger.debug(f"Attempting to add alias '{alias}' for team_id {team_id} with language {language}")
            
            # Проверяем, существует ли команда
            team = Team.query.get(team_id)
            if not team:
                logger.error(f"Team with id {team_id} not found")
                return None
            
            logger.debug(f"Found team: {team.name} (id: {team.id})")
            
            # Проверяем, не существует ли уже такое альтернативное название
            existing_alias = AliasTeam.query.filter_by(id_team=team_id, alias_name=alias).first()
            if existing_alias:
                logger.info(f"Alias '{alias}' already exists for team {team.name}")
                return existing_alias
            
            # Создаем новое альтернативное название
            logger.debug(f"Creating new alias: team_id={team_id}, alias='{alias}', language='{language}'")
            new_alias = AliasTeam(team_id=team_id, alias=alias, language=language)
            
            try:
                db.session.add(new_alias)
                logger.debug("Added new alias to session")
                db.session.commit()
                logger.info(f"Successfully added alias '{alias}' for team {team.name}")
                return new_alias
            except Exception as db_error:
                logger.error(f"Database error when adding alias: {str(db_error)}")
                db.session.rollback()
                return None
            
        except Exception as e:
            logger.error(f"Error adding alias: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def delete_alias(alias_id: int) -> bool:
        """Удаляет альтернативное название по его ID"""
        try:
            alias = AliasTeam.query.get(alias_id)
            if not alias:
                return False
            
            db.session.delete(alias)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting alias: {str(e)}")
            return False 