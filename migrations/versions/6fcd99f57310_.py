"""empty message

Revision ID: 6fcd99f57310
Revises: 
Create Date: 2019-05-31 18:33:20.198305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fcd99f57310'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('hash', sa.String(length=256), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('phoneNumber', sa.String(length=255), nullable=False),
    sa.Column('comment', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phoneNumber')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
