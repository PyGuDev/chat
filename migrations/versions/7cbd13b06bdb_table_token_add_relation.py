"""table token add relation

Revision ID: 7cbd13b06bdb
Revises: 4d7acf27072a
Create Date: 2021-12-19 21:28:59.714276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cbd13b06bdb'
down_revision = '4d7acf27072a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('user_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'token', 'user', ['user_id'], ['uid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'token', type_='foreignkey')
    op.drop_column('token', 'user_id')
    # ### end Alembic commands ###
