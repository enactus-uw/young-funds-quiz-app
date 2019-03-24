from app import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, title):
        self.title = title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'enabled': self.enabled,
        }
