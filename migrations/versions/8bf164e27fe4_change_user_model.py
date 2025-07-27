"""change User model

Revision ID: 8bf164e27fe4
Revises: 4e2304cf27d1
Create Date: 2025-07-27 16:47:02.907125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bf164e27fe4'
down_revision: Union[str, Sequence[str], None] = '4e2304cf27d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
