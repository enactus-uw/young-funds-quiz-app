import pytest
from app.create_app import create_app
from app.config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
