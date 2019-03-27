import pytest
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
    question = Question(quiz, 'question')
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
    question1 = Question(quiz, 'question1')
    question2 = Question(quiz, 'question2')
    db.session.add_all([quiz, question1, question2])
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.questions[0].text == 'question1'
    assert quiz.questions[1].text == 'question2'
