import pytest
from app.models import Quiz

@pytest.mark.parametrize('title', ['sample', 'asdfghfds,ghjg'])
def test_create_quiz(db, title):
    quiz = Quiz(title)
    db.session.add(quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == title
