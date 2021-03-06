"""rename date_submitted to date_sent

Revision ID: 658aae61827e
Revises: 0d55e5e43ac8
Create Date: 2022-05-18 14:13:54.092191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '658aae61827e'
down_revision = '0d55e5e43ac8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('saving', sa.Column('date_sent', sa.Date(), nullable=False))
    op.drop_column('saving', 'date_submitted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('saving', sa.Column('date_submitted', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('saving', 'date_sent')
    # ### end Alembic commands ###
