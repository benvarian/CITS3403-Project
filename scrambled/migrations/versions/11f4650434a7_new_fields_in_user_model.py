"""new fields in user model

Revision ID: 11f4650434a7
Revises: a2b32218c36f
Create Date: 2022-04-22 20:30:51.857789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f4650434a7'
down_revision = 'a2b32218c36f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
