"""vendors data

Revision ID: 0033b33c6e97
Revises: f412a33aa4da
Create Date: 2024-02-28 11:35:14.974048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0033b33c6e97'
down_revision: Union[str, None] = 'f412a33aa4da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'vendors_transaction_table',
        sa.Column(
            'data',
            sa.JSON()
        )
    )



def downgrade() -> None:
    pass
