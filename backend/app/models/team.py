from app.core.database import db

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    league = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, league):
        self.name = name
        self.league = league
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'league': self.league
        }
    
    def __repr__(self):
        return f'<Team {self.name}>'
    
    # Связи
    home_matches = db.relationship('Match', foreign_keys='Match.team_home', backref='home_team', lazy=True)
    away_matches = db.relationship('Match', foreign_keys='Match.team_away', backref='away_team', lazy=True) 