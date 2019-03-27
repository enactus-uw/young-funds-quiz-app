"""Fix questions unique constraint to include quiz_id

Revision ID: 6c2cab4ba69b
Revises: 1f79b7fdd00f
Create Date: 2019-03-26 21:31:38.868109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c2cab4ba69b'
down_revision = '1f79b7fdd00f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('questions_position_key', 'questions', type_='unique')
    op.create_unique_constraint(None, 'questions', ['position', 'quiz_id'])


def downgrade():
    op.drop_constraint(None, 'questions', type_='unique')
    op.create_unique_constraint('questions_position_key', 'questions', ['position'])
