"""empty message

Revision ID: d3a1f51b2832
Revises: ae7f29e49b03, b0ef835c5e4c
Create Date: 2025-10-21 07:17:18.978976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3a1f51b2832'
down_revision: Union[str, Sequence[str], None] = ('ae7f29e49b03', 'b0ef835c5e4c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
