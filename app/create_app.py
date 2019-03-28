import os
from flask import Flask, request, jsonify

from app.models import db, Quiz, Question, Choice


# Contains all routes used by app
class Routes:
    CREATE_QUIZ = "/admin/create/quiz"
    CREATE_QUESTION = "/admin/create/question"
    CREATE_CHOICE = "/admin/create/choice"

# Gets fields out of request for create and editing 
def request_vals(request, *keys):
    return tuple(request.values.get(k) for k in keys)

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)

    @app.route("/")
    def hello():
        return "Hello world"

    @app.route(Routes.CREATE_QUIZ, methods=['POST'])
    def insert_quiz():
        # TODO admin auth
        title = request_vals(request, 'title')

        quiz = Quiz(title)
        db.session.add(quiz)
        db.session.commit()
        return str(quiz.id)

    @app.route(Routes.CREATE_QUESTION, methods=['POST'])
    def insert_question():
        # TODO admin auth
        text, position, quiz_id = request_vals(request, 'text', 'position', 'quiz_id')

        question = Question(quiz_id, text, position)
        db.session.add(question)
        db.session.commit()
        return str(question.id)

    @app.route(Routes.CREATE_CHOICE, methods=['POST'])
    def insert_choice():
        # TODO admin auth
        text, correct, question_id =\
                request_vals(request, 'text', 'correct', 'question_id')

        choice = Choice(question_id, text, correct == 'True') 
        db.session.add(choice)
        db.session.commit()
        return str(choice.id)

    return app
