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
def request_vals(request, *keys):
    data = request.get_json()
    return {k: data[k] for k in keys}

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
        quiz = Quiz()
        for attr, val in request_vals(request, 'title').items():
            setattr(quiz, attr, val)

        db.session.add(quiz)
        db.session.commit()
        return str(quiz.id)

    @app.route(Routes.CREATE_QUESTION, methods=['POST'])
    def create_question():
        # TODO admin auth
        question = Question()
        for attr, val in request_vals(request, 'text', 'position', 'quiz_id').items():
            setattr(question, attr, val)

        db.session.add(question)
        db.session.commit()
        return str(question.id)

    @app.route(Routes.CREATE_CHOICE, methods=['POST'])
    def create_choice():
        # TODO admin auth
        choice = Choice() 
        for attr, val in request_vals(request, 'text', 'correct', 'question_id').items():
            setattr(choice, attr, val)

        db.session.add(choice)
        db.session.commit()
        return str(choice.id)

    return app
