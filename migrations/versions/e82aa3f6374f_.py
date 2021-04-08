"""empty message

Revision ID: e82aa3f6374f
Revises: 762402052503
Create Date: 2021-04-08 02:22:02.143768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e82aa3f6374f'
down_revision = '762402052503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=120), nullable=False),
    sa.Column('is_done', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    # ### end Alembic commands ###
