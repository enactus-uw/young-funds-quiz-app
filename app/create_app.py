import os
import json
from flask import Flask, request, jsonify

from app.models import db, Quiz, Question, Choice


# Contains all routes used by app
class Routes:
    CREATE_QUIZ = "/admin/create/quiz"
    CREATE_QUESTION = "/admin/create/question"
    CREATE_CHOICE = "/admin/create/choice"

# Gets fields out of request for create and editing 
def request_vals(*keys):
    data = request.get_json()
    return {k: data[k] for k in keys}

def create_api(model_cls, *keys):
    model = model_cls()
    for attr, val in request_vals(*keys).items():
        setattr(model, attr, val)

    db.session.add(model)
    db.session.commit()
    return str(model.id)


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)

    @app.route("/")
    def hello():
        return "Hello world"

    @app.route(Routes.CREATE_QUIZ, methods=['POST'])
    def create_quiz():
        # TODO admin auth
        return create_api(Quiz, 'title')

    @app.route(Routes.CREATE_QUESTION, methods=['POST'])
    def create_question():
        # TODO admin auth
        return create_api(Question, 'text', 'position', 'quiz_id')

    @app.route(Routes.CREATE_CHOICE, methods=['POST'])
    def create_choice():
        # TODO admin auth
        return create_api(Choice, 'text', 'correct', 'question_id')

    return app
