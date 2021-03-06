"""add saving and fine

Revision ID: 0d55e5e43ac8
Revises: 74f1fe19f3a1
Create Date: 2022-05-18 09:18:34.975113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d55e5e43ac8'
down_revision = '74f1fe19f3a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fine_id'), 'fine', ['id'], unique=False)
    op.create_table('saving',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('date_submitted', sa.Date(), nullable=False),
    sa.Column('is_late', sa.Boolean(), nullable=True),
    sa.Column('fine_id', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['fine_id'], ['fine.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('month', 'year', name='month_year_unique')
    )
    op.create_index(op.f('ix_saving_id'), 'saving', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_saving_id'), table_name='saving')
    op.drop_table('saving')
    op.drop_index(op.f('ix_fine_id'), table_name='fine')
    op.drop_table('fine')
    # ### end Alembic commands ###
