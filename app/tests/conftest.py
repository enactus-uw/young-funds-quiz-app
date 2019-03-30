import pytest
from app.create_app import create_app
from app.config import TestingConfig
from app.models import db as _db
import sqlalchemy as sa

@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)

    with app.app_context() as ctx:
        yield app

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='session')
def db(app):
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    yield db.session
    db.session.rollback()
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

@pytest.fixture(scope='function')
def dbclient(session, client):
    return client
