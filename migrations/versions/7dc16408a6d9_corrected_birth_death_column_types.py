"""corrected birth/death column types

Revision ID: 7dc16408a6d9
Revises: 93583aedfb8e
Create Date: 2018-08-10 21:46:53.750459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dc16408a6d9'
down_revision = '93583aedfb8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('person', 'birth_year',
               existing_type=sa.DATE(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('person', 'death_year',
               existing_type=sa.DATE(),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('person', 'death_year',
               existing_type=sa.Integer(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('person', 'birth_year',
               existing_type=sa.Integer(),
               type_=sa.DATE(),
               existing_nullable=True)
    # ### end Alembic commands ###
