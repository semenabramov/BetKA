from app.core.database import db
from app.models.odds_source import OddsSource
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class OddsSourceService:
    @staticmethod
    def get_all_sources() -> List[OddsSource]:
        return OddsSource.query.all()
    
    @staticmethod
    def get_source_by_id(source_id: int) -> Optional[OddsSource]:
        return OddsSource.query.get(source_id)
    
    @staticmethod
    def create_source(data: dict) -> OddsSource:
        try:
            logger.info(f"Attempting to create source with data: {data}")
            source = OddsSource(**data)
            db.session.add(source)
            db.session.commit()
            logger.info(f"Successfully created source: {source}")
            return source
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating source: {str(e)}")
            raise
    
    @staticmethod
    def update_source(source_id: int, data: dict) -> Optional[OddsSource]:
        try:
            logger.info(f"Attempting to update source {source_id} with data: {data}")
            source = OddsSource.query.get(source_id)
            if not source:
                logger.warning(f"Source {source_id} not found")
                return None
                
            for key, value in data.items():
                if hasattr(source, key):
                    setattr(source, key, value)
                    
            db.session.commit()
            logger.info(f"Successfully updated source: {source}")
            return source
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating source {source_id}: {str(e)}")
            raise
    
    @staticmethod
    def delete_source(source_id: int) -> bool:
        try:
            logger.info(f"Attempting to delete source {source_id}")
            source = OddsSource.query.get(source_id)
            if not source:
                logger.warning(f"Source {source_id} not found")
                return False
                
            db.session.delete(source)
            db.session.commit()
            logger.info(f"Successfully deleted source {source_id}")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting source {source_id}: {str(e)}")
            raise 