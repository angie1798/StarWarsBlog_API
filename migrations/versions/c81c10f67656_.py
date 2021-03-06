"""empty message

Revision ID: c81c10f67656
Revises: 45014bd7a6ff
Create Date: 2021-04-05 21:43:42.615104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c81c10f67656'
down_revision = '45014bd7a6ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('name', sa.String(length=250), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('people', 'name')
    # ### end Alembic commands ###
