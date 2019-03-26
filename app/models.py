from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
    
db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    questions = db.relationship(
            'Question',
            backref='quiz',
            order_by='Question.position',
            collection_class=ordering_list('position'))

    def __init__(self, title, enabled):
        self.title = title
        self.enabled = enabled

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'enabled': self.enabled,
        }

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.String(), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    choices = db.relationship(
            'Choice',
            backref='question',
            order_by='Choice.position',
            collection_class=ordering_list('position'))

    def __init__(self, text):
        self.text = text

    def serialize(self):
        return { 'text': self.text }

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    correct = db.Column(db.Boolean, default=False, nullable=False)
    position = db.Column(db.Integer, nullable=False)

    def __init__(self, text):
        self.text = text
