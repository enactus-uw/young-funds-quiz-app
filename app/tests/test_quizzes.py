import pytest
from app.models import Quiz

@pytest.mark.parametrize('title', ['sample', 'asdfghfds,ghjg'])
@pytest.mark.parametrize('enabled', [True, False])
def test_create_quiz(db, title, enabled):
    quiz = Quiz(title, enabled)
    db.session.add(quiz)
    db.session.commit()

    quiz = Quiz.query.get(quiz.id)
    assert quiz.title == title
    assert quiz.enabled == enabled
