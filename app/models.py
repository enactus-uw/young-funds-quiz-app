from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    questions = db.relationship(
            'Question',
            backref='quiz',
            order_by='Question.position',
            collection_class=ordering_list('position'))

    def __init__(self, title):
        self.title = title
        # Not to be set manually
        self.enabled = False

    class EnableException(Exception):
        pass

    @validates('enabled')
    def validates_enabled(self, key, val):
        if val:
            # Cannot enable quizzes with no questions or if any question has no choice
            if len(self.questions) == 0 or\
                    any([len(q.choices) == 0 for q in self.questions]):
                raise Quiz.EnableException()
        return val

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
    # Used to order questions. Not necessarily equal to question number
    position = db.Column(db.Integer, nullable=False)
    choices = db.relationship('Choice', backref='question')

    __table_args__ = (
        # No duplicate position values for a given quiz
        UniqueConstraint('position', 'quiz_id'),
    )

    def __init__(self, quiz, text, position):
        self.quiz = quiz
        self.text = text
        self.position = position

    def serialize(self):
        return { 'text': self.text }

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.String(), nullable=False)
    correct = db.Column(db.Boolean, default=False, nullable=False)
    # Choices don't need to be ordered, so no position column

    def __init__(self, question, text, correct):
        self.question = question
        self.text = text
        self.correct = correct
