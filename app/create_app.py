import os
from flask import Flask, request, jsonify

from app.models import db, Quiz, Question, Choice


# Contains all routes used by app
class Routes:
    CREATE_QUIZ = "/admin/create/quiz"
    CREATE_QUESTION = "/admin/create/question"
    CREATE_CHOICE = "/admin/create/choice"

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
        title = request.values.get('title')

        quiz = Quiz(title)
        db.session.add(quiz)
        db.session.commit()
        return str(quiz.id)

    @app.route(Routes.CREATE_QUESTION, methods=['POST'])
    def insert_question():
        # TODO admin auth
        text = request.values.get('text')
        position = request.values.get('position')
        quiz_id = request.values.get('quiz_id')

        quiz = Quiz.query.get(quiz_id)
        question = Question(quiz, text, position)
        db.session.add(question)
        db.session.commit()
        return str(question.id)

    return app
