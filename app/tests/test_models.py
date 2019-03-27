import pytest
from sqlalchemy import exc
from app.models import Quiz, Question
from .util import make_quiz, make_choice, make_question

@pytest.mark.parametrize('title', ['sample', 'asdfghfds,ghjg'])
def test_create_quiz(db, title):
    quiz = make_quiz(db, title)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == title
    assert quiz.enabled == False

def test_create_questions(db):
    quiz = make_quiz(db)
    question = make_question(db, 'question', quiz=quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    question = quiz.questions[0]
    assert question.text == 'question'
    assert question.quiz.id == quiz.id

    question2 = Question.query.filter_by(quiz=quiz).one()
    assert question == question2

def test_question_ordering(db):
    quiz = make_quiz(db)
    make_question(db, 'question3', 5, quiz=quiz)
    make_question(db, 'question1', 0, quiz=quiz)
    make_question(db, 'question2', 3, quiz=quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.questions[0].text == 'question1'
    assert quiz.questions[0].position == 0
    assert quiz.questions[1].text == 'question2'
    assert quiz.questions[1].position == 3
    assert quiz.questions[2].text == 'question3'
    assert quiz.questions[2].position == 5

def test_question_repeat_position(db):
    quiz = make_quiz(db)
    make_question(db, position=0, quiz=quiz)
    make_question(db, position=0, quiz=quiz)
    # No repeated positions
    with pytest.raises(exc.IntegrityError):
        db.session.commit()

    #make_question(db, position=0)
