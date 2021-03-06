from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    enabled = db.Column(db.Boolean, default=False, nullable=False)
    questions = db.relationship(
            'Question',
            backref='quiz',
            order_by='Question.position',
            collection_class=ordering_list('position'),
            cascade='delete-orphan,delete')

    def __init__(self):
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

    def serialize(self, recursive=False):
        data = {
            'id': self.id,
            'title': self.title,
            'enabled': self.enabled
        }
        if recursive:
            data['questions'] = [q.serialize(True) for q in self.questions]
        return data

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.String(), nullable=False)
    # Used to order questions. Not necessarily equal to question number
    position = db.Column(db.Integer, nullable=False)
    choices = db.relationship('Choice', backref='question', cascade='delete-orphan,delete')

    __table_args__ = (
        # No duplicate position values for a given quiz
        UniqueConstraint('position', 'quiz_id', deferrable=True, initially='DEFERRED'),
    )

    def serialize(self, recursive=False):
        data = {
            'id': self.id,
            'text': self.text,
            'position': self.position,
            'quiz_id': self.quiz_id
        }
        if recursive:
            data['choices'] = [c.serialize(True) for c in self.choices]
        return data

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.String(), nullable=False)
    correct = db.Column(db.Boolean, default=False, nullable=False)
    # Choices don't need to be ordered, so no position column

    def serialize(self, recursive=True):
        return {
            'id': self.id,
            'text': self.text,
            'correct': self.correct,
            'question_id': self.question_id
        }
