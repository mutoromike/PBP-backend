"""relate transactions with users and business

Revision ID: 66cdf659fd3f
Revises: 709d41f0316e
Create Date: 2020-07-13 18:27:40.836792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66cdf659fd3f'
down_revision = '709d41f0316e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transations', sa.Column('business_id', sa.String(), nullable=False))
    op.add_column('transations', sa.Column('created_by_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'transations', 'businesses', ['business_id'], ['uuid'])
    op.create_foreign_key(None, 'transations', 'users', ['created_by_id'], ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transations', type_='foreignkey')
    op.drop_constraint(None, 'transations', type_='foreignkey')
    op.drop_column('transations', 'created_by_id')
    op.drop_column('transations', 'business_id')
    # ### end Alembic commands ###
