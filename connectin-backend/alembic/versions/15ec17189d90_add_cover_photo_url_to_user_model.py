"""add cover_photo_url to user model

Revision ID: 15ec17189d90
Revises: 66591bf07d4d
Create Date: 2025-05-02 16:16:45.688757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '15ec17189d90'
down_revision: Union[str, None] = '66591bf07d4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Only add the cover_photo_url column
    op.add_column('users', sa.Column('cover_photo_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Only drop the cover_photo_url column
    op.drop_column('users', 'cover_photo_url')
    # ### end Alembic commands ###
