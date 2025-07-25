"""add_default_timestamp_to_user_info

Revision ID: ecf444f17e34
Revises: 09eb325dbb12
Create Date: 2025-07-25 16:33:58.746698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecf444f17e34'
down_revision: Union[str, Sequence[str], None] = '09eb325dbb12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add default value for timestamp column
    op.execute("ALTER TABLE user_info ALTER COLUMN timestamp DROP NOT NULL")
    op.execute("ALTER TABLE user_info ALTER COLUMN timestamp SET DEFAULT EXTRACT(EPOCH FROM NOW()) * 1000")
    op.execute("ALTER TABLE user_info ALTER COLUMN timestamp SET NOT NULL")


def downgrade() -> None:
    """Downgrade schema."""
    # Remove default value from timestamp column
    op.execute("ALTER TABLE user_info ALTER COLUMN timestamp DROP DEFAULT")
