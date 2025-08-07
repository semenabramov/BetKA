from app.core.database import db
from app.models.odds import OddsFromSource, BookmakerOdds
from typing import List, Optional

class OddsService:
    @staticmethod
    def get_odds_by_match_id(match_id: int) -> List[OddsFromSource]:
        return OddsFromSource.query.filter_by(match_id=match_id).all()
    
    @staticmethod
    def get_bookmaker_odds_by_match_id(match_id: int) -> List[BookmakerOdds]:
        return BookmakerOdds.query.filter_by(match_id=match_id).all()
    
    @staticmethod
    def create_source_odds(match_id: int, source_id: int, data: dict) -> OddsFromSource:
        odds = OddsFromSource(
            match_id=match_id,
            sources_id=source_id,
            odds_home=data.get('odds_home'),
            odds_away=data.get('odds_away'),
            odds_draw=data.get('odds_draw')
        )
        db.session.add(odds)
        db.session.commit()
        return odds
    
    @staticmethod
    def update_source_odds(odds_id: int, data: dict) -> Optional[OddsFromSource]:
        odds = OddsFromSource.query.get(odds_id)
        if not odds:
            return None
            
        for key, value in data.items():
            if hasattr(odds, key):
                setattr(odds, key, value)
                
        db.session.commit()
        return odds
    
    @staticmethod
    def delete_source_odds(odds_id: int) -> bool:
        odds = OddsFromSource.query.get(odds_id)
        if not odds:
            return False
            
        db.session.delete(odds)
        db.session.commit()
        return True 