"""change User model

Revision ID: f8a412237cce
Revises: 8bf164e27fe4
Create Date: 2025-07-27 18:23:48.056577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8a412237cce'
down_revision: Union[str, Sequence[str], None] = '8bf164e27fe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
