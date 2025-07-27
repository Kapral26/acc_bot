"""change User model

Revision ID: 4e2304cf27d1
Revises: b3bf14e9abe9
Create Date: 2025-07-27 16:41:48.678025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e2304cf27d1'
down_revision: Union[str, Sequence[str], None] = 'b3bf14e9abe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
