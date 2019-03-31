import json
import pytest
from app.models import Quiz, Question, Choice
from app.create_app import Routes
from app.tests.util import make_quiz, make_question, make_choice


def post_json(client, route, data, status=200):
    resp = client.post(route, data=json.dumps(data), content_type='application/json')
    assert resp.status_code == status
    return resp


def test_homepage(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # TODO elaborate

@pytest.mark.parametrize('path', Routes.POST_ENDPOINTS)
def test_wrong_method(client, path):
    resp = client.get(path)
    assert resp.status_code == 405

@pytest.mark.parametrize('path', Routes.POST_ENDPOINTS)
def test_empty_request(client, path):
    post_json(client, path, {}, status=422)

def test_create_quiz_api(dbclient):
    resp = post_json(dbclient, Routes.CREATE_QUIZ, {'title': 'sample'})
    quiz = Quiz.query.filter_by(title='sample').one()
    assert int(resp.get_data()) == quiz.id

@pytest.mark.parametrize('pos', [0, 1, 2, 3, 400])
def test_create_question_api(dbclient, db, pos):
    quiz = make_quiz(db.session)
    resp = post_json(dbclient, Routes.CREATE_QUESTION,
            {'position': pos, 'text': 'a', 'quiz_id': quiz.id})

    question = Question.query.filter_by(text='a').one()
    assert question.position == pos
    assert question.text == 'a'
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

    post_json(dbclient, Routes.EDIT_QUIZ,
            {'id': quiz.id + 3, 'title': 'q23'}, status=404)

def test_edit_question(dbclient, session):
    question = make_question(session, 'q23', 0)

    post_json(dbclient, Routes.EDIT_QUESTION, {'id': question.id, 'text': 'q23'})
    assert Question.query.filter_by(text='q23').one().id == question.id
    post_json(dbclient, Routes.EDIT_QUESTION, {'id': question.id, 'text': '{}}'})
    assert Question.query.filter_by(text='{}}').one().id == question.id

    post_json(dbclient, Routes.EDIT_QUESTION,
            {'id': question.id + 3, 'text': 'q23'}, status=404)
    # Editing position not allowed
    post_json(dbclient, Routes.EDIT_QUESTION,
            {'id': question.id, 'text': 'q23', 'position': 5}, status=422)

def test_swap_question(dbclient, session):
    quiz = make_quiz(session)
    q1 = make_question(session, position=0, quiz=quiz)
    q2 = make_question(session, position=5, quiz=quiz)

    # Swap with own position. No changes expected
    post_json(dbclient, Routes.SWAP_QUESTION,
            {'id': q1.id, 'position': q1.position})
    assert q1.position == 0
    assert q2.position == 5

    post_json(dbclient, Routes.SWAP_QUESTION,
            {'id': q1.id, 'position': q2.position})
    assert q1.position == 5
    assert q2.position == 0

def test_bad_swap(dbclient, session):
    q = make_question(session, position=2)
    # Invalid ID
    post_json(dbclient, Routes.SWAP_QUESTION,
        {'id': q.id + 1, 'position': q.position}, status=404)
    # Invalid position
    post_json(dbclient, Routes.SWAP_QUESTION,
        {'id': q.id, 'position': q.position + 1}, status=404)

def test_edit_choice(dbclient, session):
    choice = make_choice(session, 'choice', False)

    post_json(dbclient, Routes.EDIT_CHOICE,
            {'id': choice.id, 'text': 'ZZek', 'correct': True})
    assert Choice.query.count() == 1
    assert Choice.query.get(choice.id).text == 'ZZek'
    assert Choice.query.get(choice.id).correct == True

    # Nonexistent ID
    post_json(dbclient, Routes.EDIT_CHOICE,
            {'id': choice.id + 3, 'text': 'ZZek', 'correct': True}, status=404)

@pytest.mark.parametrize('mk_model,url',
        [(make_quiz, Routes.EDIT_QUIZ),
         (make_question, Routes.EDIT_QUESTION),
         (make_choice, Routes.EDIT_CHOICE)])
def test_bad_edits(dbclient, session, mk_model, url):
    model = mk_model(session)

    post_json(dbclient, url, {'id': model.id}, status=422)
