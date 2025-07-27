"""change User model

Revision ID: 9fc3dcd89e08
Revises: fcca1be52de1
Create Date: 2025-07-27 16:39:20.046207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fc3dcd89e08'
down_revision: Union[str, Sequence[str], None] = 'fcca1be52de1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
