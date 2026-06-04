"""rename raid_meta to meta

Revision ID: ec26d94541a4
Revises: 5e09f72907e9
Create Date: 2026-05-23 08:48:35.395846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec26d94541a4'
down_revision: Union[str, Sequence[str], None] = '5e09f72907e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("raid_meta", "meta")

def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table("meta", "raid_meta")
