"""Add unique constraint to question.position

Revision ID: 1f79b7fdd00f
Revises: 1cc3b2e69498
Create Date: 2019-03-26 20:25:13.384802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f79b7fdd00f'
down_revision = '1cc3b2e69498'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'questions', ['position'])


def downgrade():
    op.drop_constraint(None, 'questions', type_='unique')
