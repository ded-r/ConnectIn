"""Add comments, likes, saves, and votes tables

Revision ID: 4326d1ca41ae
Revises: 18d3616ade58
Create Date: 2025-02-26 14:03:41.265651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4326d1ca41ae'
down_revision: Union[str, None] = '18d3616ade58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_recommendations_id'), 'recommendations', ['id'], unique=False)
    op.drop_constraint('recommendations_project_id_fkey', 'recommendations', type_='foreignkey')
    op.drop_column('recommendations', 'score')
    op.drop_column('recommendations', 'created_at')
    op.drop_column('recommendations', 'project_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommendations', sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('recommendations', sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.add_column('recommendations', sa.Column('score', sa.NUMERIC(precision=3, scale=2), autoincrement=False, nullable=True))
    op.create_foreign_key('recommendations_project_id_fkey', 'recommendations', 'projects', ['project_id'], ['id'])
    op.drop_index(op.f('ix_recommendations_id'), table_name='recommendations')
    # ### end Alembic commands ###
