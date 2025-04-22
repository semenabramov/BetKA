from app.core.database import db

class Split(db.Model):
    __tablename__ = 'Splits'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    Kelly_value = db.Column(db.Float)
    Bank = db.Column(db.Float)
    min_bet = db.Column(db.Float)
    status = db.Column(db.Enum('active', 'completed', 'archived'))
    
    # Связи
    matches = db.relationship('Match', backref='split_info', lazy=True)
    split_matches = db.relationship('SplitMatch', backref='split', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,
            'Kelly_value': self.Kelly_value,
            'Bank': self.Bank,
            'min_bet': self.min_bet,
            'status': self.status
        } 