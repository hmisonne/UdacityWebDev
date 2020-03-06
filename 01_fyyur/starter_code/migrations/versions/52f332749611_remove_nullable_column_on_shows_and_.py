"""Remove nullable column on Shows and remove upcoming_show param

Revision ID: 52f332749611
Revises: 2e46681db56b
Create Date: 2020-03-06 15:05:42.441986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52f332749611'
down_revision = '2e46681db56b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('Show', 'upcoming_show')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('upcoming_show', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('Show', 'name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###
