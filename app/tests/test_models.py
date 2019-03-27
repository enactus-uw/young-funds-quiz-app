import pytest
from sqlalchemy import exc
from app.models import Quiz, Question
from .util import make_quiz, make_choice, make_question

def test_create_quiz(db):
    title = 'asdfghfds'
    quiz = make_quiz(db, title)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == title
    assert quiz.enabled == False
    assert len(quiz.questions) == 0

def test_create_questions(db):
    quiz = make_quiz(db)
    question = make_question(db, 'question', quiz=quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    question = quiz.questions[0]
    assert question.text == 'question'
    assert question.quiz.id == quiz.id
    assert len(question.choices) == 0

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

def test_question_repeat_position_diff_quiz(db):
    # Allow repeated positions across different quizzes
    make_question(db, position=0)
    make_question(db, position=0)
    db.session.commit()
    assert Question.query.filter_by(position=0).count() == 2

def test_create_choice(db):
    question = make_question(db)
    choice1 = make_choice(db, 'choice1', False, question=question)
    choice2 = make_choice(db, 'choice2', True, question=question)
    db.session.commit()

    assert question.choices[0] == choice1
    assert question.choices[1] == choice2
    assert question.choices[0].question == question
    assert question.choices[1].question == question

def test_quiz_enable(db):
    quiz = make_quiz(db)
    with pytest.raises(Quiz.EnableException):
        quiz.enabled = True
    assert quiz.enabled == False

    question = make_question(db, quiz=quiz)
    make_choice(db, question=question)
    quiz.enabled = False
    assert quiz.enabled == False

    make_question(db, quiz=quiz)
    with pytest.raises(Quiz.EnableException):
        quiz.enabled = True
    assert quiz.enabled == False
