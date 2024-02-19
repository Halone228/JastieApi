"""match url add

Revision ID: f412a33aa4da
Revises: b472b360fa68
Create Date: 2024-02-16 23:16:20.588250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f412a33aa4da'
down_revision: Union[str, None] = 'b472b360fa68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'matches_table',
        sa.Column(
            'url',
            sa.String(),
            server_default='https://example.com'
        )
    )


def downgrade() -> None:
    op.drop_column(
        'matches_table',
        'url'
    )
