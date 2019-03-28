import json
import pytest
from app.models import Quiz, Question, Choice
from app.create_app import Routes
from app.tests.util import make_quiz, make_question


def post_json(client, route, data):
    resp = client.post(route, data=json.dumps(data), content_type='application/json')
    assert resp.status_code == 200
    return resp


def test_homepage(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # TODO elaborate

@pytest.mark.parametrize('path', [Routes.CREATE_QUIZ, Routes.CREATE_QUESTION])
def test_wrong_method(client, path):
    resp = client.get(path)
    assert resp.status_code == 405

def test_create_quiz_api(dbclient):
    resp = post_json(dbclient, Routes.CREATE_QUIZ, {'title': 'sample'})
    quiz = Quiz.query.filter_by(title='sample').one()
    assert int(resp.get_data()) == quiz.id

@pytest.mark.parametrize('pos', [0, 1, 2, 3, 400])
def test_create_question_api(dbclient, session, pos):
    quiz = make_quiz(session)
    resp = post_json(dbclient, Routes.CREATE_QUESTION,
            {'position': pos, 'text': ';dfg,', 'quiz_id': quiz.id})
    
    question = Question.query.filter_by(position=pos).one()
    assert question.position == pos
    assert question.text == ';dfg,'
    assert question.quiz == quiz
    assert question.id == int(resp.get_data())

@pytest.mark.parametrize('correct', [True, False])
def test_create_choice(dbclient, session, correct):
    question = make_question(session)
    resp = post_json(dbclient, Routes.CREATE_CHOICE,
            {'text': 'abc ooome  dfg', 'correct': correct, 'question_id': question.id})

    choice = Choice.query.filter_by(correct=correct).one()
    assert choice.text ==  'abc ooome  dfg'
    assert choice.correct == correct
    assert choice.question == question
    assert choice.id == int(resp.get_data())

def test_edit_quiz(dbclient, session):
    make_quiz(session, 'quiz1') 
    quiz = make_quiz(session, 'quiz12') 

    post_json(dbclient, Routes.EDIT_QUIZ, {'id': quiz.id, 'title': 'quiz22'})
    # Make sure empty edits don't do anything and don't crash
    post_json(dbclient, Routes.EDIT_QUIZ, {'id': quiz.id})
    assert Quiz.query.count() == 2
    assert Quiz.query.filter_by(title='quiz1').count() == 1
    assert Quiz.query.get(quiz.id).title == 'quiz22'
