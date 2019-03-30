"""Change position constraint to deferrable

Revision ID: 1364df5736da
Revises: 79d0e79611d0
Create Date: 2019-03-29 23:01:45.400455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1364df5736da'
down_revision = '79d0e79611d0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('questions_position_quiz_id_key', 'questions', type_='unique')
    op.create_unique_constraint(None, 'questions', ['position', 'quiz_id'],
            deferrable=True, initially='DEFERRED')


def downgrade():
    op.drop_constraint('questions_position_quiz_id_key', 'questions', type_='unique')
    op.create_unique_constraint(None, 'questions', ['position', 'quiz_id'])
