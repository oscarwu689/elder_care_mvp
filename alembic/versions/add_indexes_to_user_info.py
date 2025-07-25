"""add indexes to user_info table

Revision ID: add_indexes_to_user_info
Revises: ecf444f17e34
Create Date: 2025-07-25 16:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_indexes_to_user_info'
down_revision: Union[str, Sequence[str], None] = 'ecf444f17e34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add indexes for better performance
    op.create_index('idx_user_info_timestamp', 'user_info', ['timestamp'])
    op.create_index('idx_user_info_user_id', 'user_info', ['user_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove indexes
    op.drop_index('idx_user_info_timestamp', 'user_info')
    op.drop_index('idx_user_info_user_id', 'user_info') 