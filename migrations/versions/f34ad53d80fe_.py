"""Add Choices and Questions

Revision ID: f34ad53d80fe
Revises: 10f841afae38
Create Date: 2019-03-24 17:40:19.790573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f34ad53d80fe'
down_revision = '10f841afae38'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('choices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=100), nullable=False),
    sa.Column('correct', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('choices')
    op.drop_table('questions')
