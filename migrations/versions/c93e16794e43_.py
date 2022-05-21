"""empty message

Revision ID: c93e16794e43
Revises: ebea5c8b60c7
Create Date: 2022-05-21 22:46:19.553325

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision = 'c93e16794e43'
down_revision = 'ebea5c8b60c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('featured', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_show_featured'), 'show', ['featured'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_show_featured'), table_name='show')
    op.drop_column('show', 'featured')
    # ### end Alembic commands ###
