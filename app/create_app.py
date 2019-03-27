import os
from flask import Flask, request, jsonify

from app.models import db, Quiz

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)

    @app.route("/")
    def hello():
        return "Hello world"

    @app.route("/admin/create/quiz", methods=['POST'])
    def insert_quiz():
        # TODO admin auth
        title = request.values.get('title')

        quiz = Quiz(title)
        db.session.add(quiz)
        db.session.commit()
        return str(quiz.id)

    @app.route("/admin/create/question", methods=['POST'])
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
