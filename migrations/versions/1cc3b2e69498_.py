"""Initial migration

Revision ID: 1cc3b2e69498
Revises: 
Create Date: 2019-03-26 18:51:51.741939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cc3b2e69498'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('quizzes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
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
    op.drop_table('quizzes')
