"""Recreate education and experience tables

Revision ID: 15b8f7ed4175
Revises: 8e7e567795a5
Create Date: 2025-02-12 20:41:56.278080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15b8f7ed4175'
down_revision: Union[str, None] = '8e7e567795a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('education',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('institution', sa.String(length=255), nullable=False),
    sa.Column('degree', sa.String(length=255), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('end_year', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_education_id'), 'education', ['id'], unique=False)
    op.create_table('experience',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('end_year', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_experience_id'), 'experience', ['id'], unique=False)
    op.drop_constraint('users_google_id_key', 'users', type_='unique')
    op.drop_column('users', 'google_id')
    op.drop_column('users', 'google_refresh_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('google_refresh_token', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('google_id', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.create_unique_constraint('users_google_id_key', 'users', ['google_id'])
    op.drop_index(op.f('ix_experience_id'), table_name='experience')
    op.drop_table('experience')
    op.drop_index(op.f('ix_education_id'), table_name='education')
    op.drop_table('education')
    # ### end Alembic commands ###
