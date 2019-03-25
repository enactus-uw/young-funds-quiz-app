import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Quiz

@app.route("/")
def hello():
    return "Hello world"

@app.route("/admin/insert/quiz", methods=['POST'])
def insert_quiz():
    # TODO admin auth
    title = request.args.get('title')
    enabled = request.args.get('enabled')
    quiz = Quiz(title=title, enabled=enabled)
    db.session.add(quiz)
    db.session.commit()
    return str(quiz.id)

@app.route("/admin/insert/<quiz_id>/question", methods=['POST'])
def insert_question(quiz_id):
    # TODO admin auth
    text = request.args.get('text')
    quiz = Quizzes.query.filter_by(id=quiz_id).first()
    question = Question(text=text)
    quiz.questions.append(question)
    db.session.add(question)
    db.session.commit()
    return str(question.id)
