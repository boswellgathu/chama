"""add loan and instalment

Revision ID: ba9d6e71a5b5
Revises: 658aae61827e
Create Date: 2022-05-22 14:54:16.571375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba9d6e71a5b5'
down_revision = '658aae61827e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_acquired', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('interest_rate', sa.Integer(), nullable=True),
    sa.Column('amount_paid', sa.Float(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('period', sa.Integer(), nullable=True),
    sa.Column('remaining_period', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_loan_id'), 'loan', ['id'], unique=False)
    op.create_table('instalment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_paid', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('principal', sa.Float(), nullable=True),
    sa.Column('interest', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('loan_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['loan_id'], ['loan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instalment_id'), 'instalment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_instalment_id'), table_name='instalment')
    op.drop_table('instalment')
    op.drop_index(op.f('ix_loan_id'), table_name='loan')
    op.drop_table('loan')
    # ### end Alembic commands ###
