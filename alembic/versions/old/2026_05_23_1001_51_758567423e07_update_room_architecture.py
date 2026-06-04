"""update room architecture

Revision ID: 758567423e07
Revises: ec26d94541a4
Create Date: 2026-05-23 10:01:51.464823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '758567423e07'
down_revision: Union[str, Sequence[str], None] = 'ec26d94541a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text_pointer', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('texts', sa.JSON(), nullable=False))
        batch_op.add_column(sa.Column('stoppers', sa.JSON(), nullable=False))
        batch_op.add_column(sa.Column('next_state', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('updated_states', sa.JSON(), nullable=False))
        batch_op.drop_column('local_state')
        batch_op.drop_column('state_texts')

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state_texts', sqlite.JSON(), nullable=False))
        batch_op.add_column(sa.Column('local_state', sa.INTEGER(), nullable=False))
        batch_op.drop_column('updated_states')
        batch_op.drop_column('next_state')
        batch_op.drop_column('stoppers')
        batch_op.drop_column('texts')
        batch_op.drop_column('text_pointer')
