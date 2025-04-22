from app.core.database import db

class SplitMatch(db.Model):
    __tablename__ = 'split_matches'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    split_id = db.Column(db.Integer, db.ForeignKey('Splits.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('Matches.id'), nullable=False)
    bookmaker_id = db.Column(db.Integer, db.ForeignKey('bookmakers.id'), nullable=False)
    selected_outcome = db.Column(db.Enum('home', 'draw', 'away'))
    odds_value = db.Column(db.Float)
    is_success = db.Column(db.Boolean)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'split_id': self.split_id,
            'match_id': self.match_id,
            'bookmaker_id': self.bookmaker_id,
            'selected_outcome': self.selected_outcome,
            'odds_value': self.odds_value,
            'is_success': self.is_success,
            'notes': self.notes
        } 