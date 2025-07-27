"""
seed base roles

Revision ID: 8b55ae7d64b3
Revises: f8a412237cce
Create Date: 2025-07-27 18:48:11.722233

"""
from typing import Union
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b55ae7d64b3"
down_revision: str | Sequence[str] | None = "f8a412237cce"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uq_roles_name", "roles", ["name"])
    conn = op.get_bind()
    # Убедитесь, что поле name уникально в таблице roles!
    conn.execute(
        sa.text("""
                         INSERT INTO roles (name, updated_at)
                         VALUES
                             ('admin', current_timestamp),
                             ('user', current_timestamp)
                         ON CONFLICT (name) DO NOTHING;
                         """)
    )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute(
        sa.text("""
                         DELETE FROM roles WHERE name IN ('admin', 'user');
                         """)
    )
