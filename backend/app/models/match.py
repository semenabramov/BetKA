from app.core.database import db

class Match(db.Model):
    __tablename__ = 'Matches'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    team_home = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_away = db.Column(db.Integer, db.ForeignKey('teams.id'))
    split = db.Column(db.Integer, db.ForeignKey('Splits.id'))
    
    # Связи
    kickform_odds = db.relationship('OddsFromKickform', backref='match', lazy=True, uselist=False)
    bookmaker_odds = db.relationship('BookmakerOdds', backref='match', lazy=True)
    split_matches = db.relationship('SplitMatch', backref='match', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'team_home': self.team_home,
            'team_away': self.team_away,
            'split': self.split,
            'home_team_name': self.home_team.name if self.home_team else None,
            'away_team_name': self.away_team.name if self.away_team else None
        } 