"""empty message

Revision ID: b7f6513bf3eb
Revises: 84629679b94b
Create Date: 2020-03-25 10:12:25.551823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f6513bf3eb'
down_revision = '84629679b94b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('People')
    op.drop_constraint('Objective_user_id_fkey', 'Objective', type_='foreignkey')
    op.drop_table('User')
    op.add_column('Objective', sa.Column('athlete_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Objective', 'Athlete', ['athlete_id'], ['id'])
    op.drop_column('Objective', 'frequency')
    op.drop_column('Objective', 'user_id')
    op.drop_column('Objective', 'history')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Objective', sa.Column('history', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Objective', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Objective', sa.Column('frequency', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Objective', type_='foreignkey')
    op.create_foreign_key('Objective_user_id_fkey', 'Objective', 'User', ['user_id'], ['id'])
    op.drop_column('Objective', 'athlete_id')
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"User_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='User_pkey')
    )
    op.create_table('People',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"People_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('catchphrase', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='People_pkey')
    )
    # ### end Alembic commands ###
