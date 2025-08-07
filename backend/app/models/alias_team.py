from app.core.database import db

class AliasTeam(db.Model):
    __tablename__ = 'alias_team'
    
    id = db.Column(db.Integer, primary_key=True)
    id_team = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    alias_name = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(2), default='ru', check_constraint="language IN ('ru', 'en')")
    
    # Связь с моделью Team
    team = db.relationship('Team', backref=db.backref('aliases', lazy=True, cascade='all, delete-orphan'))
    
    def __init__(self, team_id, alias, language='ru'):
        self.id_team = team_id
        self.alias_name = alias
        self.language = language
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.id_team,
            'alias': self.alias_name,
            'language': self.language
        }
    
    def __repr__(self):
        return f'<AliasTeam {self.alias_name} for team {self.id_team}>' 