import pytest
from app.models import Quiz, Question, Choice
from app.create_app import Routes
from app.tests.util import make_quiz, make_question

def test_homepage(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # TODO elaborate

@pytest.mark.parametrize('path', [Routes.CREATE_QUIZ, Routes.CREATE_QUESTION])
def test_wrong_method(client, path):
    resp = client.get(path)
    assert resp.status_code == 405

def call_api(client, route, data):
    resp = client.post(route, data=data)
    assert resp.status_code == 200
    return resp

def test_create_quiz_api(dbclient):
    resp = call_api(dbclient, Routes.CREATE_QUIZ, {'title': 'sample'})
    quiz = Quiz.query.filter_by(title='sample').one()
    assert int(resp.get_data()) == quiz.id

@pytest.mark.parametrize('pos', [0, 1, 2, 3, 400])
def test_create_question_api(dbclient, session, pos):
    quiz = make_quiz(session)
    session.commit()
    resp = call_api(dbclient, Routes.CREATE_QUESTION,
            {'position': pos, 'text': ';dfg,', 'quiz_id': quiz.id})
    
    question = Question.query.filter_by(position=pos).one()
    assert question.position == pos
    assert question.text == ';dfg,'
    assert question.quiz == quiz
    assert question.id == int(resp.get_data())
