"""Add ordering constraints

Revision ID: 69c152f1ad78
Revises: f34ad53d80fe
Create Date: 2019-03-24 18:04:29.630276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69c152f1ad78'
down_revision = 'f34ad53d80fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('choices', sa.Column('position', sa.Integer(), nullable=False))
    op.add_column('questions', sa.Column('position', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'position')
    op.drop_column('choices', 'position')
    # ### end Alembic commands ###