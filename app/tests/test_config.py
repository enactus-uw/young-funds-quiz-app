import os

def test_dev_config(app):
    app.config.from_object('app.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']

def test_prod_config(app):
    app.config.from_object('app.config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']

def test_testing_config(app):
    assert app.config['DEBUG']
    assert app.config['TESTING']
