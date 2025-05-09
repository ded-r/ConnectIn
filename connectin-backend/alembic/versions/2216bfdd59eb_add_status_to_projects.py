"""add_status_to_projects

Revision ID: 2216bfdd59eb
Revises: 7f7fb27e026a
Create Date: 2025-05-06 16:45:41.231593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = '2216bfdd59eb'
down_revision: Union[str, None] = '7f7fb27e026a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_statuses')
    op.drop_column('conversations', 'name')
    op.alter_column('messages', 'content',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('messages', 'conversation_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('messages', 'edited_at')
    op.drop_column('messages', 'is_read')
    op.drop_column('messages', 'is_edited')
    
    # Add status column as nullable first
    op.add_column('projects', sa.Column('status', sa.String(), nullable=True))
    
    # Update existing records
    conn = op.get_bind()
    conn.execute(text("UPDATE projects SET status = 'development' WHERE status IS NULL"))
    
    # Now make it non-nullable with a default
    op.alter_column('projects', 'status', nullable=False, server_default='development')
    
    # Remove the teams.leader_id alteration since it's not related to the project status change
    # op.alter_column('teams', 'leader_id',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('teams', 'leader_id',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    op.drop_column('projects', 'status')
    op.add_column('messages', sa.Column('is_edited', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('messages', sa.Column('is_read', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('messages', sa.Column('edited_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.alter_column('messages', 'conversation_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('messages', 'content',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.add_column('conversations', sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.create_table('user_statuses',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('conversation_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_online', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_typing', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('last_seen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name='user_statuses_conversation_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_statuses_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'conversation_id', name='user_statuses_pkey')
    )
    # ### end Alembic commands ###
