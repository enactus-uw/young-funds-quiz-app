from app.models import Quiz, Question, Choice

def make_quiz(session, title='sample_quiz'):
    quiz = Quiz(title)
    session.add(quiz)
    return quiz

def make_question(session, text='sample_question', position=0, quiz=None):
    if quiz is None:
        quiz = make_quiz(session)

    question = Question(quiz, text, position)
    session.add(question)
    return question

def make_choice(session, text='sample_choice', correct=False, question=None):
    if question is None:
        question = make_question(session)

    choice = Choice(question, text, correct)
    session.add(choice)
    return choice
