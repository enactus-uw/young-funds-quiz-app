import pytest
from app.create_app import create_app
from app.config import TestingConfig
from app.models import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)

    with app.app_context() as ctx:
        yield app

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def db(app):
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()

@pytest.fixture(scope='function')
def dbclient(db, client):
    return client
