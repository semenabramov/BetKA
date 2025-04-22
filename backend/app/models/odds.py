from app.core.database import db

class OddsFromKickform(db.Model):
    __tablename__ = 'Odds_from_kickform'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, db.ForeignKey('Matches.id'), nullable=False)
    odds_home = db.Column(db.Float)
    odds_away = db.Column(db.Float)
    odds_draw = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'odds_home': self.odds_home,
            'odds_away': self.odds_away,
            'odds_draw': self.odds_draw
        }

class BookmakerOdds(db.Model):
    __tablename__ = 'Bookmakers_odds'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, db.ForeignKey('Matches.id'), nullable=False)
    bookmaker_id = db.Column(db.Integer, db.ForeignKey('Bookmakers.id'), nullable=False)
    odds_home = db.Column(db.Float)
    odds_away = db.Column(db.Float)
    odds_draw = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'bookmaker_id': self.bookmaker_id,
            'odds_home': self.odds_home,
            'odds_away': self.odds_away,
            'odds_draw': self.odds_draw
        } 