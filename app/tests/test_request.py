def test_homepage(client):
    resp = client.get('/')
    assert resp.status_code == 200
    # TODO elaborate
