"""change User model

Revision ID: b3bf14e9abe9
Revises: 9fc3dcd89e08
Create Date: 2025-07-27 16:40:37.824009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3bf14e9abe9'
down_revision: Union[str, Sequence[str], None] = '9fc3dcd89e08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
