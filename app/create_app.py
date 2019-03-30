import os
import json
from flask import Flask, request, jsonify, abort

from app.models import db, Quiz, Question, Choice


# Contains all routes used by app
class Routes:
    CREATE_QUIZ = "/admin/create/quiz"
    CREATE_QUESTION = "/admin/create/question"
    CREATE_CHOICE = "/admin/create/choice"

    EDIT_QUIZ = "/admin/edit/quiz"
    EDIT_QUESTION = "/admin/edit/question"
    EDIT_CHOICE = "/admin/edit/choice"

    POST_ENDPOINTS = [CREATE_QUIZ, CREATE_QUESTION, CREATE_CHOICE, EDIT_QUIZ,
            EDIT_QUESTION, EDIT_CHOICE]

# Gets fields out of request for create and editing
def request_vals(*keys):
    data = request.get_json()
    out = {}
    for k in keys:
        # Handle missing keys in request JSON with 422 error
        if k not in data:
            abort(422)
        out[k] = data.pop(k)

    # Extra fields will be ignored, which is confusing and therefore disallowed
    if len(data) > 0:
        abort(422)
    return out

def create_api(model_cls, *keys):
    model = model_cls()
    for attr, val in request_vals(*keys).items():
        setattr(model, attr, val)

    db.session.add(model)
    db.session.commit()
    return str(model.id)

def edit_api(model_cls, *keys):
    # Request JSON must contain ID of the model to edit
    fields = request_vals(*keys, 'id')
    # Handle nonexistent model ID with 404 not found
    model = model_cls.query.get_or_404(fields.pop('id'))
    for attr, val in fields.items():
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

    @app.route(Routes.EDIT_QUIZ, methods=['POST'])
    def edit_quiz():
        # TODO admin auth
        return edit_api(Quiz, 'title')

    @app.route(Routes.EDIT_QUESTION, methods=['POST'])
    def edit_question():
        # TODO admin auth
        # Disallow editing of foreign key and position
        return edit_api(Question, 'text')

    @app.route(Routes.EDIT_CHOICE, methods=['POST'])
    def edit_choice():
        # TODO admin auth
        # Disallow editting of foreign key
        return edit_api(Choice, 'text', 'correct')

    return app
