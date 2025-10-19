"""Initial version

Revision ID: 4dc11366aefc
Revises:
Create Date: 2025-10-19 09:10:27.842701

"""

from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4dc11366aefc"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "portals",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        ),
        sa.Column("name", sa.String(), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("portal_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["portal_id"], ["portals.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    op.drop_table("portals")
