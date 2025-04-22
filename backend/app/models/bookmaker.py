from app.core.database import db

class Bookmaker(db.Model):
    __tablename__ = 'bookmakers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Ссылки на сайты для разных лиг
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
    
    # Связи
    odds = db.relationship('BookmakerOdds', 
                         backref=db.backref('bookmaker', lazy=True),
                         lazy=True,
                         foreign_keys='BookmakerOdds.bookmaker_id')
                         
    split_matches = db.relationship('SplitMatch',
                                  backref=db.backref('bookmaker', lazy=True),
                                  lazy=True,
                                  foreign_keys='SplitMatch.bookmaker_id')
    
    def __init__(self, name, **kwargs):
        self.name = name
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'premier_league_url': self.premier_league_url,
            'championship_url': self.championship_url,
            'league_one_url': self.league_one_url,
            'league_two_url': self.league_two_url,
            'bundesliga_one_url': self.bundesliga_one_url,
            'bundesliga_two_url': self.bundesliga_two_url,
            'liga_url': self.liga_url,
            'la_liga_url': self.la_liga_url,
            'serie_a_url': self.serie_a_url,
            'ligue_one_url': self.ligue_one_url
        }
    
    def __repr__(self):
        return f'<Bookmaker {self.name}>' 