from app.models import Quiz, Question, Choice

def make_quiz(session, title='sample_quiz'):
    quiz = Quiz()
    quiz.title = title
    session.add(quiz)
    session.commit()
    return quiz

def make_question(session, text='sample_question', position=0, quiz=None):
    if quiz is None:
        quiz = make_quiz(session)

    question = Question()
    question.quiz_id = quiz.id
    question.text = text
    question.position = position
    session.add(question)
    session.commit()
    return question

def make_choice(session, text='sample_choice', correct=False, question=None):
    if question is None:
        question = make_question(session)

    choice = Choice()
    choice.question_id = question.id
    choice.text = text
    choice.correct = correct
    session.add(choice)
    session.commit()
    return choice
