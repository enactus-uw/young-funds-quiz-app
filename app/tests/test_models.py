import pytest
from sqlalchemy import exc
from app.models import Quiz, Question

@pytest.mark.parametrize('title', ['sample', 'asdfghfds,ghjg'])
def test_create_quiz(db, title):
    quiz = Quiz(title)
    db.session.add(quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == title
    assert quiz.enabled == False

def test_create_questions(db):
    quiz = Quiz('sample')
    question = Question(quiz, 'question', 0)
    db.session.add(quiz)
    db.session.add(question)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    question = quiz.questions[0]
    assert question.text == 'question'
    assert question.quiz.id == quiz.id

    question2 = Question.query.filter_by(quiz=quiz).one()
    assert question == question2

def test_question_ordering(db):
    quiz = Quiz('sample')
    question3 = Question(quiz, 'question3', 5)
    question1 = Question(quiz, 'question1', 0)
    question2 = Question(quiz, 'question2', 3)
    db.session.add_all([quiz, question1, question2, question3])
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.questions[0].text == 'question1'
    assert quiz.questions[0].position == 0
    assert quiz.questions[1].text == 'question2'
    assert quiz.questions[1].position == 3
    assert quiz.questions[2].text == 'question3'
    assert quiz.questions[2].position == 5

def test_question_repeat_position(db):
    quiz = Quiz('sample')
    question1 = Question(quiz, 'question1', 0)
    question2 = Question(quiz, 'question1', 0)
    db.session.add_all([quiz, question1, question2])
    # No repeated positions
    with pytest.raises(exc.IntegrityError):
        db.session.commit()
