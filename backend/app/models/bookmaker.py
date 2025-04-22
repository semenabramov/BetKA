from app.core.database import db

class Bookmaker(db.Model):
    __tablename__ = 'Bookmakers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Связи
    odds = db.relationship('BookmakerOdds', backref='bookmaker', lazy=True)
    split_matches = db.relationship('SplitMatch', backref='bookmaker', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        } 