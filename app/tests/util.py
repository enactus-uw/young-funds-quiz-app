from app.models import Quiz, Question, Choice

def make_quiz(db, title='sample_quiz'):
    quiz = Quiz(title)
    db.session.add(quiz)
    return quiz

def make_question(db, text='sample_question', position=0, quiz=None):
    if quiz is None:
        quiz = make_quiz(db)

    question = Question(quiz, text, position)
    db.session.add(question)
    return question

def make_choice(db, text='sample_choice', question=None):
    if question is None:
        question = make_question(db)

    choice = Choice(question, text)
    db.session.add(choice)
    return choice
