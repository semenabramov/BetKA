from app.core.database import db
from datetime import datetime

class OddsSource(db.Model):
    __tablename__ = 'odds_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    premier_league_url = db.Column(db.String(255))
    championship_url = db.Column(db.String(255))
    league_one_url = db.Column(db.String(255))
    league_two_url = db.Column(db.String(255))
    bundesliga_one_url = db.Column(db.String(255))
    bundesliga_two_url = db.Column(db.String(255))
    liga_url = db.Column(db.String(255))
    la_liga_url = db.Column(db.String(255))
    serie_a_url = db.Column(db.String(255))
    ligue_one_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    odds = db.relationship('OddsFromSource', backref='source', lazy=True)
    
    def __init__(self, name, url, **kwargs):
        self.name = name
        self.url = url
        self.premier_league_url = kwargs.get('premier_league_url')
        self.championship_url = kwargs.get('championship_url')
        self.league_one_url = kwargs.get('league_one_url')
        self.league_two_url = kwargs.get('league_two_url')
        self.bundesliga_one_url = kwargs.get('bundesliga_one_url')
        self.bundesliga_two_url = kwargs.get('bundesliga_two_url')
        self.liga_url = kwargs.get('liga_url')
        self.la_liga_url = kwargs.get('la_liga_url')
        self.serie_a_url = kwargs.get('serie_a_url')
        self.ligue_one_url = kwargs.get('ligue_one_url')
        self.is_active = kwargs.get('is_active', True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'premier_league_url': self.premier_league_url,
            'championship_url': self.championship_url,
            'league_one_url': self.league_one_url,
            'league_two_url': self.league_two_url,
            'bundesliga_one_url': self.bundesliga_one_url,
            'bundesliga_two_url': self.bundesliga_two_url,
            'liga_url': self.liga_url,
            'la_liga_url': self.la_liga_url,
            'serie_a_url': self.serie_a_url,
            'ligue_one_url': self.ligue_one_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<OddsSource {self.name}>' 