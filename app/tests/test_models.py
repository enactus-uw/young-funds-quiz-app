import pytest
from sqlalchemy import exc
from app.models import Quiz, Question
from .util import make_quiz, make_choice, make_question

def test_create_quiz(session):
    title = 'asdfghfds'
    quiz = make_quiz(session, title)

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == title
    assert quiz.enabled == False
    assert len(quiz.questions) == 0

def test_create_questions(session):
    quiz = make_quiz(session)
    question = make_question(session, 'question', quiz=quiz)

    quiz = Quiz.query.get(quiz.id)
    question = quiz.questions[0]
    assert question.text == 'question'
    assert question.quiz.id == quiz.id
    assert len(question.choices) == 0

    question2 = Question.query.filter_by(quiz=quiz).one()
    assert question == question2

def test_question_ordering(session):
    quiz = make_quiz(session)
    make_question(session, 'question3', 5, quiz=quiz)
    make_question(session, 'question1', 0, quiz=quiz)
    make_question(session, 'question2', 3, quiz=quiz)

    quiz = Quiz.query.get(quiz.id)
    assert quiz.questions[0].text == 'question1'
    assert quiz.questions[0].position == 0
    assert quiz.questions[1].text == 'question2'
    assert quiz.questions[1].position == 3
    assert quiz.questions[2].text == 'question3'
    assert quiz.questions[2].position == 5

def test_question_repeat_position(session):
    quiz = make_quiz(session)
    make_question(session, position=0, quiz=quiz)
    # No repeated positions
    with pytest.raises(exc.IntegrityError):
        make_question(session, position=0, quiz=quiz)

def test_question_repeat_position_diff_quiz(session):
    # Allow repeated positions across different quizzes
    make_question(session, position=0)
    make_question(session, position=0)
    assert Question.query.filter_by(position=0).count() == 2

# Test that the unique constriant on question.position is really deferrable
def test_reorder_questions(session):
    quiz = make_quiz(session)
    q1 = make_question(session, position=0, quiz=quiz)
    q2 = make_question(session, position=1, quiz=quiz)
    q1.position = 1
    q2.position = 0
    session.add(q1, q2)
    session.commit()

    assert q1.position == 1
    assert q2.position == 0

def test_create_choice(session):
    question = make_question(session)
    choice1 = make_choice(session, 'choice1', False, question=question)
    choice2 = make_choice(session, 'choice2', True, question=question)

    assert question.choices[0] == choice1
    assert question.choices[1] == choice2
    assert question.choices[0].question == question
    assert question.choices[1].question == question

def test_quiz_enable(session):
    quiz = make_quiz(session)
    with pytest.raises(Quiz.EnableException):
        quiz.enabled = True
    assert quiz.enabled == False

    question = make_question(session, quiz=quiz)
    make_choice(session, question=question)
    quiz.enabled = False
    assert quiz.enabled == False

    make_question(session, quiz=quiz, position=2)
    with pytest.raises(Quiz.EnableException):
        quiz.enabled = True
    assert quiz.enabled == False

def test_big_strings(session):
    make_quiz(session, ";;#@$^&&*()"*100)
    make_choice(session, ";;#@$^&&*()"*100)
    make_question(session, ";;#@$^&&*()"*100)
