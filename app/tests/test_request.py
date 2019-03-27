import pytest

def test_homepage(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # TODO elaborate

@pytest.mark.parametrize('path', ['/admin/create/quiz', 'admin/create/question'])
def test_wrong_method(client, path):
    resp = client.get(path)
    assert resp.status_code == 405

def test_create_quiz_api(dbclient):
    resp = dbclient.post('admin/create/quiz', data={'title': 'sample'})
    assert resp.status_code == 200

