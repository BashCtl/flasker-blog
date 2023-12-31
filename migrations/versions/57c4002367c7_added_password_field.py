"""added password field

Revision ID: 57c4002367c7
Revises: b90d811baefa
Create Date: 2023-09-19 21:22:34.090328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57c4002367c7'
down_revision = 'b90d811baefa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
