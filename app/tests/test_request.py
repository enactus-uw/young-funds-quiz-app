import json
import pytest
from app.models import Quiz, Question, Choice
from app.create_app import Routes
from app.tests.util import make_quiz, make_question, make_choice


def post_json(client, route, data):
    resp = client.post(route, data=json.dumps(data), content_type='application/json')
    assert resp.status_code == 200
    return resp


def test_homepage(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # TODO elaborate

@pytest.mark.parametrize('path',
        [Routes.CREATE_QUIZ, Routes.CREATE_QUESTION, Routes.CREATE_CHOICE,
         Routes.EDIT_QUIZ, Routes.EDIT_QUESTION, Routes.EDIT_CHOICE,])
def test_wrong_method(client, path):
    resp = client.get(path)
    assert resp.status_code == 405

def test_create_quiz_api(dbclient):
    resp = post_json(dbclient, Routes.CREATE_QUIZ, {'title': 'sample', 'dummy': 2})
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
    assert Quiz.query.count() == 2
    assert Quiz.query.filter_by(title='quiz1').count() == 1
    assert Quiz.query.get(quiz.id).title == 'quiz22'

    with pytest.raises(BaseException):
        post_json(dbclient, Routes.EDIT_QUIZ,
                {'id': quiz.id + 3, 'title': 'q23'})

def test_edit_question(dbclient, session):
    question = make_question(session, 'q23', 0)

    post_json(dbclient, Routes.EDIT_QUESTION, {'id': question.id, 'text': 'q23'})
    assert Question.query.filter_by(text='q23').one().id == question.id
    post_json(dbclient, Routes.EDIT_QUESTION, {'id': question.id, 'text': '{}}'})
    assert Question.query.filter_by(text='{}}').one().id == question.id

    with pytest.raises(BaseException):
        post_json(dbclient, Routes.EDIT_QUESTION,
                {'id': question.id + 3, 'text': 'q23'})

def test_edit_choice(dbclient, session):
    choice = make_choice(session, 'choice', False)

    post_json(dbclient, Routes.EDIT_CHOICE,
            {'id': choice.id, 'text': 'ZZek', 'correct': True})
    assert Choice.query.count() == 1
    assert Choice.query.get(choice.id).text == 'ZZek'
    assert Choice.query.get(choice.id).correct == True

    with pytest.raises(BaseException):
        # Nonexistent ID
        post_json(dbclient, Routes.EDIT_CHOICE,
                {'id': choice.id + 3, 'text': 'ZZek', 'correct': True})

@pytest.mark.parametrize('mk_model,url',
        [(make_quiz, Routes.EDIT_QUIZ),
         (make_question, Routes.EDIT_QUESTION),
         (make_choice, Routes.EDIT_CHOICE)])
def test_bad_edits(dbclient, session, mk_model, url):
    model = mk_model(session)

    with pytest.raises(KeyError):
        post_json(dbclient, url, {'id': model.id})
