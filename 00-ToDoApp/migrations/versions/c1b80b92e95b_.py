"""empty message

Revision ID: c1b80b92e95b
Revises: 07f13b41fddd
Create Date: 2020-03-05 14:45:09.630966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1b80b92e95b'
down_revision = '07f13b41fddd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('completed', sa.Boolean(), nullable=True))
    op.execute('UPDATE todolists SET completed = False WHERE completed IS NULL')
    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolists', 'completed')
    # ### end Alembic commands ###
