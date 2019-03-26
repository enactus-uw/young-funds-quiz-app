from app.models import Quiz

def test_create_quiz(db):
    quiz = Quiz('sample', False)
    db.session.add(quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == 'sample'
    assert quiz.enabled == False
